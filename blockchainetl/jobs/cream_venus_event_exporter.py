import logging
from web3.auto import w3
from web3 import Web3
from web3._utils.filters import Filter
from blockchainetl.streaming.exporter.cream_venus_mongo_streaming_exporter import (
    CreamVenusMongodbStreamingExporter,
)
from blockchainetl.jobs.event_exporter import ExportEvent
from constants.event_constants import Event
from blockchainetl.mappers.receipt_lending_log_mapper import EthReceiptLendingLogMapper

from query_state_lib.base.mappers.eth_json_rpc_mapper import EthJsonRpc

from artifacts.abi.CREAM_LENS_ABI import CREAM_LENS_ABI
from artifacts.abi.COMPOUND_COMPTROLLER_ABI import COMPOUND_COMPTROLLER_ABI
from artifacts.abi.lending.trava.lending_pool_abi import LENDING_POOL_ABI

from query_state_lib.base.mappers.eth_call_mapper import EthCall
from query_state_lib.base.utils.encoder import encode_eth_call_data

from using_query_state_lib import using_query_state_lib


from pycoingecko import CoinGeckoAPI

_LOGGER = logging.getLogger(__name__)


def eth_call_transaction_by_hash(transaction_hash, identify):
    return EthJsonRpc(id=identify, params=[transaction_hash], method="eth_getTransactionByHash")


def eth_call_block_by_block_number(block_number, identify):
    return EthJsonRpc(id=identify, params=[str(hex(block_number)), False], method="eth_getBlockByNumber")


class ExportCreamVenusEvent(ExportEvent):
    def __init__(
            self,
            start_block: int,
            end_block: int,
            batch_size: int,
            max_workers: int,
            item_exporter: CreamVenusMongodbStreamingExporter,
            web3: Web3,
            contract_addresses: list,
            client_querier_full_node,
            abi: list
    ):
        super().__init__(
            start_block=start_block,
            end_block=end_block,
            batch_size=batch_size,
            max_workers=max_workers,
            item_exporter=item_exporter,
            web3=web3,
            contract_addresses=contract_addresses,
            abi=abi
        )
        self.event_info: dict = {}
        self.topics: list = []
        self.receipt_log: EthReceiptLendingLogMapper = EthReceiptLendingLogMapper()
        self.client_querier_full_node = client_querier_full_node
        self.eth_call_full_node = []

    def _start(self):
        self.event_data = []
        self.list_abi: list = self.receipt_log.build_list_info_event(abi=self.abi)
        for abi in self.list_abi:
            self.event_info[abi[1]] = abi[0]
            self.topics.append(abi[1])
        _LOGGER.info("Start crawling events")

    def _end(self):
        self.batch_work_executor.shutdown()
        for eth_event_dict in self.event_data:
            self._make_eth_call(eth_event_dict)
        self.event_data = self.enrich_event()
        self.item_exporter.export_items(self.event_data)
        _LOGGER.info(f"Crawled {len(self.event_data)} events from {self.start_block} to {self.end_block}")

    def export_events(
            self,
            start_block: int,
            end_block: int,
            topic: list,
            pools: list,
            event_subscriber: dict,
    ):
        filter_params: dict = {
            "fromBlock": start_block,
            "toBlock": end_block,
            "topics": [topic],
        }
        if pools is not None and len(pools) > 0:
            filter_params['address'] = pools

        event_filter: Filter = self.web3.eth.filter(filter_params)

        events: list = event_filter.get_all_entries()

        events_list = []
        for event in events:
            log = self.receipt_log.web3_dict_to_receipt_log(event)
            eth_event = self.receipt_log.extract_event_from_log(
                log, event_subscriber[log.topics[0]]
            )

            if eth_event is not None:
                eth_event_dict = self.receipt_log.eth_event_to_dict(eth_event)
                transaction_hash = eth_event_dict.get(Event.transaction_hash)
                event_type = eth_event_dict.get(Event.event_type)
                block_number = eth_event_dict.get(Event.block_number)
                log_index = eth_event_dict.get(Event.log_index)
                eth_event_dict[
                    "_id"
                ] = f"transaction_{transaction_hash}_{event_type}_{block_number}_{log_index}"
                events_list.append(eth_event_dict)

        self.web3.eth.uninstallFilter(event_filter.filter_id)

        return events_list

    def enrich_event(self):

        lending_address = "0x1a014ffe0cd187a298a7e79ba5ab05538686ea4a"

        result = []
        block_transaction = self.client_querier_full_node.sent_batch_to_provider(
            self.eth_call_full_node)
        for event in self.event_data:

            token = event["contract_address"]
            token = [self.web3.toChecksumAddress(token)]

            event['block_timestamp'] = int(block_transaction[event['_id'] + '_block'].result['timestamp'], 16)
            event['wallet'] = str(block_transaction[event['_id'] + '_transaction'].result['from']).lower()

            result_tmp_exchange_rate = using_query_state_lib(lending_address=lending_address,
                                               web3=self.web3,
                                               client_querier=self.client_querier_full_node,
                                               abi=CREAM_LENS_ABI,
                                               fn_name='cTokenMetadata',
                                               args=token)

            #reserves_token_info = lending_contract.functions.cTokenMetadataAll(token).call(
            #    block_identifier=event['block_number'])

            #exchange_rate = reserves_token_info[0][1]
            exchange_rate = result_tmp_exchange_rate[0][1]

            #underlying_price = lending_contract.functions.cTokenUnderlyingPriceAll(token).call(
            #    block_identifier=event['block_number'])

            result_tmp_underlying_price = using_query_state_lib(lending_address=lending_address,
                                                                web3=self.web3,
                                                                client_querier=self.client_querier_full_node,
                                                                abi=CREAM_LENS_ABI,
                                                                fn_name='cTokenUnderlyingPrice',
                                                                args=token)
            underlying_price = result_tmp_underlying_price[0][1]

            coingecko = CoinGeckoAPI()
            bnb_price: float = coingecko.get_coins_markets(vs_currency='usd', ids='binancecoin')[0]['current_price']

            tokenPrice: float = (underlying_price * bnb_price * exchange_rate)/(10**18)

            event['price_token'] = tokenPrice

            result.append(event)

        return result

    def _make_eth_call(self, eth_event_dict):
        call_block = eth_call_block_by_block_number(
            eth_event_dict['block_number'], eth_event_dict['_id'] + '_block')
        if call_block not in self.eth_call_full_node: self.eth_call_full_node.append(call_block)
        call_transaction = eth_call_transaction_by_hash(
            eth_event_dict['transaction_hash'], eth_event_dict['_id'] + '_transaction')
        if call_transaction not in self.eth_call_full_node: self.eth_call_full_node.append(call_transaction)
