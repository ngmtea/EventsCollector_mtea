import logging
import time

from artifacts.abi.trava_oracle_abi import TRAVA_ORACLE_ABI
from artifacts.abi.erc20_abi import ERC20_ABI
from configs.config import MongoDBConfig
from constants.event_constants import Event
from constants.lending_pool_constants import PoolConstant
from query_state_lib.base.mappers.eth_call_mapper import EthCall
from query_state_lib.base.mappers.eth_json_rpc_mapper import EthJsonRpc
from blockchainetl.jobs.event_exporter import ExportEvent
from query_state_lib.base.utils.encoder import encode_eth_call_data
from web3 import Web3
from artifacts.abi.chainlink_abi import CHAINLINK_ABI
from artifacts.abi.lending.trava.lending_pool_abi import LENDING_POOL_ABI

_LOGGER = logging.getLogger(__name__)


def update_events_with_err(event_list):
    for event in event_list:
        event['related_wallets'] = []
    return


def eth_call_transaction_by_hash(transaction_hash, identify):
    return EthJsonRpc(id=identify, params=[transaction_hash], method="eth_getTransactionByHash")


def eth_call_block_by_block_number(block_number, identify):
    return EthJsonRpc(id=identify, params=[str(hex(block_number)), False], method="eth_getBlockByNumber")


class ExportLendingEvent(ExportEvent):
    def __init__(self,
                 start_block,
                 end_block,
                 batch_size,
                 max_workers,
                 item_exporter,
                 web3,
                 web3_,
                 contract_addresses,
                 client_querier_full_node,
                 client_querier_archive_node,
                 oracle_address,
                 event_abi,
                 abi=LENDING_POOL_ABI,
                 oracle_abi=TRAVA_ORACLE_ABI):
        super().__init__(
            start_block=start_block,
            end_block=end_block,
            batch_size=batch_size,
            max_workers=max_workers,
            item_exporter=item_exporter,
            web3=web3,
            contract_addresses=contract_addresses,
            abi=event_abi
        )
        self.lending_abi = abi
        self.encode_price = None
        self.eth_price = None
        self.web3_ = web3_
        self.oracle_abi = oracle_abi
        self.oracle_address = oracle_address
        self.oracle_contract = web3.eth.contract(address=oracle_address, abi=oracle_abi)
        self.eth_call_full_node = []
        self.eth_call_archive_node = []
        self.eth_token_price_call = []
        self.listAssets = []
        self.get_token_info()
        self.client_querier_archive_node = client_querier_archive_node
        self.client_querier_full_node = client_querier_full_node

    def get_token_info(self):
        self.assets = {}
        self.tTokens = []
        self.listAssets = []
        for i in self.contract_addresses:
            self.check_aave_v2(i)
            assets, t_tokens, list_assets = self.get_t_token_assets(i)
            self.listAssets += list_assets
            self.assets.update(assets)
            self.tTokens += t_tokens

        self.listAssets = list(set(self.listAssets))
        self.tTokens = list(set(self.tTokens))
        self.tokens = self.contract_addresses + self.tTokens
        self.encode_price = self._encode_price()

    def export_batch(self, block_number_batch):
        _LOGGER.info(f'crawling event data from {block_number_batch[0]} to {block_number_batch[-1]}')
        e_list = self.export_events(block_number_batch[0], block_number_batch[-1], event_subscriber=self.event_info,
                                    topic=self.topics, pools=self.tokens)
        self.event_data += e_list

    def _end(self):
        self.batch_work_executor.shutdown()
        for eth_event_dict in self.event_data:
            self._make_eth_call(eth_event_dict)
        self.event_data = self.enrich_event()
        self.item_exporter.export_items(self.event_data)
        self.item_exporter.close()
        _LOGGER.info(f'Crawled {len(self.event_data)} events from {self.start_block} to {self.end_block}!')

    def _export(self):
        abi_transfer = self.receipt_log.build_list_info_event(ERC20_ABI)[0]
        self.event_info[abi_transfer[1]] = abi_transfer[0]
        self.topics.append(abi_transfer[1])
        self.batch_work_executor.execute(
            range(self.start_block, self.end_block + 1),
            self.export_batch
        )

    def export_events(self, start_block, end_block, event_subscriber, topic, pools=None):
        filter_params = {
            'fromBlock': start_block,
            'toBlock': end_block,
            'topics': [topic]
        }
        if pools is not None and len(pools) > 0:
            filter_params['address'] = pools

        event_filter = self.web3.eth.filter(filter_params)
        events = event_filter.get_all_entries()
        events_list = []
        for event in events:
            log = self.receipt_log.web3_dict_to_receipt_log(event)
            eth_event = self.receipt_log.extract_event_from_log(log, event_subscriber[log.topics[0]])
            if eth_event is not None:
                eth_event_dict = self.receipt_log.eth_event_to_dict(eth_event)
                if eth_event_dict.get(Event.event_type) == "TRANSFER":
                    if eth_event_dict.get("_from") == "0x0000000000000000000000000000000000000000" \
                            or eth_event_dict.get("_to") == "0x0000000000000000000000000000000000000000": continue
                transaction_hash = eth_event_dict.get(Event.transaction_hash)
                event_type = eth_event_dict.get(Event.event_type)
                block_number = eth_event_dict.get(Event.block_number)
                log_index = eth_event_dict.get(Event.log_index)
                eth_event_dict['_id'] = f"transaction_{transaction_hash}_{event_type}_{block_number}_{log_index}"
                events_list.append(eth_event_dict)

        self.web3.eth.uninstallFilter(event_filter.filter_id)

        return events_list

    def enrich_event(self):
        eth_price = {}
        block_transaction = self.client_querier_full_node.sent_batch_to_provider(
            self.eth_call_full_node)
        price = self.client_querier_archive_node.sent_batch_to_provider(
            self.eth_call_archive_node)
        if self.eth_token_price_call:
            eth_price = self.client_querier_archive_node.sent_batch_to_provider(self.eth_token_price_call)
        result = []
        for event in self.event_data:
            if event['contract_address'] in self.assets.keys():
                event['asset'] = self.assets[event['contract_address']]
            event['block_timestamp'] = int(block_transaction[event['_id'] + '_block'].result['timestamp'], 16)
            event['wallet'] = str(block_transaction[event['_id'] + '_transaction'].result['from']).lower()
            for i in PoolConstant.token_type:
                if i in event.keys():
                    event[f'decimal_of_{i.replace("Asset", "_asset")}'] = self.token_get_decimals(event[i])
                    try:
                        price_token = price[event['_id'] + '_' + i].result
                        price_token = int(price_token, 16)
                    except:
                        _LOGGER.warning(f"Can not crawl price of {event[i]}!")
                        _LOGGER.info(f"Get latest price!")
                        price_token, count = None, 0
                        while not price_token:
                            if count < 10:
                                count += 1
                            else:
                                break
                            block = self.web3.eth.blockNumber
                            try:
                                price_token = self.oracle_contract.functions.getAssetPrice(
                                self.web3.toChecksumAddress(event[i])). \
                                call(block_identifier=block - 10)
                            except Exception as e:
                                logging.info(f"Err {e} in {block}")
                                time.sleep(10)
                                pass

                        if count > 10:
                            _LOGGER.info(f"Get price in mongo!")
                            token = self.item_exporter.get_item_in_collection(MongoDBConfig.TOKENS, {"_id": "token_" + event[i]})
                            token = list(token)
                            if token and "price" in token[0]:
                                price_token = token[0]["price"]
                            else:
                                price_token = 1

                    if eth_price:
                        price_token = price_token * (
                                int(eth_price[event['_id'] + '_' + i].result[66:130], 16) / 10 ** 18)
                    event[f'price_of_{i.replace("Asset", "_asset")}'] = str(int(price_token))

            result.append(event)
        return result

    def token_get_decimals(self, address):
        key_decimals = "key_decimals"
        token_decimals = self.localstorage.get(key_decimals) or {}
        self.localstorage.set(key_decimals, token_decimals)
        decimals = 18
        if address == "0x":
            return 18
        try:
            lower_address = str(address).lower()
            if token_decimals.get(lower_address):
                return token_decimals[lower_address]
            token = self.web3.eth.contract(self.web3.toChecksumAddress(address), abi=ERC20_ABI)
            decimals = token.functions.decimals().call()
            token_decimals[lower_address] = decimals
        except Exception as e:
            _LOGGER.warning(f"get decimals of address {address} err {e}")

        return decimals

    def _make_eth_call(self, eth_event_dict):
        call_block = eth_call_block_by_block_number(
            eth_event_dict['block_number'], eth_event_dict['_id'] + '_block')
        if call_block not in self.eth_call_full_node: self.eth_call_full_node.append(call_block)
        call_transaction = eth_call_transaction_by_hash(
            eth_event_dict['transaction_hash'], eth_event_dict['_id'] + '_transaction')
        if call_transaction not in self.eth_call_full_node: self.eth_call_full_node.append(call_transaction)

        for i in PoolConstant.token_type:
            if i in eth_event_dict.keys():
                if eth_event_dict[i] not in self.listAssets:
                    self.get_token_info()
                call_token = EthCall(
                    to=self.oracle_address,
                    data=self.encode_price[eth_event_dict[i]],
                    block_number=eth_event_dict['block_number'],
                    abi=self.oracle_abi,
                    fn_name='getAssetPrice',
                    id=eth_event_dict['_id'] + '_' + i
                )
                if call_token not in self.eth_call_archive_node:
                    self.eth_call_archive_node.append(call_token)
                if self.eth_price:
                    call_eth_price = EthCall(
                        to=self.web3.toChecksumAddress('0x5f4ec3df9cbd43714fe2740f5e3616155c5b8419'),
                        data=self.eth_price,
                        block_number=eth_event_dict['block_number'],
                        abi=CHAINLINK_ABI,
                        fn_name='latestRoundData',
                        id=eth_event_dict['_id'] + '_' + i
                    )
                    if call_eth_price not in self.eth_token_price_call:
                        self.eth_token_price_call.append(call_eth_price)

    def get_t_token_assets(self, pool):
        contract = self.web3.eth.contract(address=pool, abi=self.lending_abi)
        assets_addresses = contract.functions.getReservesList().call()
        assets, t_tokens = {}, []
        for asset_address in assets_addresses:

            asset_info = contract.functions.getReserveData(asset_address).call()
            if Web3.isAddress(asset_info[6]):
                t_token = asset_info[6]
                debt_token = asset_info[7]

            else:
                t_token = asset_info[7]
                debt_token = asset_info[9]

            assets[t_token.lower()] = asset_address.lower()
            t_tokens.append(t_token)
        assets_addresses = [i.lower() for i in assets_addresses]
        return assets, t_tokens, assets_addresses

    def _encode_price(self):
        result = {}
        for token in self.listAssets:
            result[token.lower()] = encode_eth_call_data(
                abi=self.oracle_abi, fn_name='getAssetPrice', args=[self.web3.toChecksumAddress(token)])
        return result

    def check_aave_v2(self, address):
        if address.lower() == PoolConstant.mapping["aave-v2"]["address"]:
            self.eth_price = encode_eth_call_data(abi=CHAINLINK_ABI, fn_name='latestRoundData', args=[])
        return
