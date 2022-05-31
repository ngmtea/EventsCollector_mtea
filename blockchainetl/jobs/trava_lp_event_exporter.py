import logging
from artifacts.abi.lending.lp_token_events_abi import LP_TOKEN_EVENT_ABI
from blockchainetl.jobs.event_exporter import ExportEvent
from query_state_lib.base.utils.encoder import encode_eth_call_data
from query_state_lib.base.mappers.eth_call_mapper import EthCall
from query_state_lib.base.mappers.eth_json_rpc_mapper import EthJsonRpc
from constants.trava_lp_contant import TravaLPConstant
from data_storage.memory_storage import MemoryStorage
from artifacts.abi.chainlink_abi import CHAINLINK_ABI
from constants.event_constant import *

_LOGGER = logging.getLogger(__name__)


def eth_call_block_by_block_number(block_number, identify):
    return EthJsonRpc(id=identify, params=[str(hex(block_number)), False], method="eth_getBlockByNumber")


class ExportEventTravaLP(ExportEvent):
    def __init__(self,
                 start_block,
                 end_block,
                 batch_size,
                 max_workers,
                 item_exporter,
                 web3,
                 contract_addresses,
                 abi=LP_TOKEN_EVENT_ABI,
                 client_querier=None,
                 ):
        super().__init__(
            start_block=start_block,
            end_block=end_block,
            batch_size=batch_size,
            max_workers=max_workers,
            item_exporter=item_exporter,
            web3=web3,
            contract_addresses=contract_addresses,
            abi=abi,
        )
        self.client_querier = client_querier
        self.local_storage = MemoryStorage.getInstance()
        self.contract_addresses_info = {}
        for address in contract_addresses:
            self.contract_addresses_info[address.lower()] = TravaLPConstant.mapping[address.lower()]
            self.contract_addresses_info[address.lower()]["encode_chainlink_price"] = encode_eth_call_data(
                abi=CHAINLINK_ABI,
                fn_name="latestRoundData",
                args=[]
            )

    def _end(self):
        self.batch_work_executor.shutdown()
        self.enrich_events()
        self.item_exporter.export_items(self.event_data)
        self.item_exporter.close()
        _LOGGER.info(f'Crawled {len(self.event_data)} events from {self.start_block} to {self.end_block}!')

    def enrich_events(self):
        call = []
        for event in self.event_data:
            call.append(eth_call_block_by_block_number(event["block_number"], event["_id"] + "_block_timestamp"))
            if event["event_type"] == EventTypes.swap:
                call.append(EthCall(
                    to=self.web3.toChecksumAddress(self.contract_addresses_info[
                                                       event["contract_address"]]["chainlink_token1_address"]),
                    abi=CHAINLINK_ABI,
                    fn_name="latestRoundData",
                    data=self.contract_addresses_info[event["contract_address"]]["encode_chainlink_price"],
                    block_number=event["block_number"],
                    id=event["_id"] + "_token1_price"
                ))

        response = self.client_querier.sent_batch_to_provider(call)

        for event in self.event_data:
            event["block_timestamp"] = int(response[event['_id'] + '_block_timestamp'].result['timestamp'], 16)
            if event["event_type"]==EventTypes.swap:
                if float(event["amount0_in"]) != 0 and float(event["amount1_out"]) != 0:
                    event["ratio_between_token1_and_token0"] = float(event["amount1_out"]) / float(event["amount0_in"])
                    event["action"] = "BUY"

                elif float(event["amount0_out"]) != 0 and float(event["amount1_in"]) != 0:
                    event["ratio_between_token1_and_token0"] = float(event["amount1_in"]) / float(event["amount0_out"])
                    event["action"] = "SELL"

                else:
                    event["ratio_between_token0_and_token1"] = 0

                event["token1_price"] = round(response[event["_id"] + "_token1_price"].decode_result()[1]/10**8, 2)
                event["token0_price"] = event["ratio_between_token1_and_token0"] * event["token1_price"]
