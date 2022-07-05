from blockchainetl.jobs.event_exporter import ExportEvent
import logging
from query_state_lib.base.mappers.eth_call_mapper import EthCall
from query_state_lib.base.mappers.eth_json_rpc_mapper import EthJsonRpc
from constants.event_constant import Event

_LOGGER = logging.getLogger(__name__)


def eth_call_block_by_block_number(block_number, identify):
    return EthJsonRpc(id=identify, params=[str(hex(block_number)), False], method="eth_getBlockByNumber")


def eth_call_transaction_by_hash(transaction_hash, identify):
    return EthJsonRpc(id=identify, params=[transaction_hash], method="eth_getTransactionByHash")


class MultiSigWalletEventExporter(ExportEvent):
    def __init__(self,
                 start_block,
                 end_block,
                 batch_size,
                 max_workers,
                 item_exporter,
                 web3,
                 contract_addresses,
                 abi,
                 client_querier_full_node):
        super().__init__(
            start_block,
            end_block,
            batch_size,
            max_workers,
            item_exporter,
            web3,
            contract_addresses,
            abi
        )
        self.client_querier_full_node = client_querier_full_node
        self.eth_call_full_node = []

    def _end(self):
        self.batch_work_executor.shutdown()
        self.event_data = self._check_events()
        for eth_event_dict in self.event_data:
            self._make_eth_call(eth_event_dict)
        self.event_data = self.enrich_event()
        self.item_exporter.export_items(self.event_data)
        self.item_exporter.close()
        _LOGGER.info(f'Crawled {len(self.event_data)} events from {self.start_block} to {self.end_block}!')

    def _check_events(self):
        contract_addresses, result = [], []
        for event in self.event_data:
            if event[Event.contract_address] not in contract_addresses:
                contract_addresses.append(event[Event.contract_address])

        identities = self.item_exporter.get_items("CrossChainIdentities", "identities", {"_id":{"$in":contract_addresses}})
        identity_addresses = []
        for i in identities:
            identity_addresses.append(i["_id"])

        for event in self.event_data:
            if event[Event.contract_address] not in identity_addresses:continue
            result.append(event)

        return result

    def enrich_event(self):
        block_transaction = self.client_querier_full_node.sent_batch_to_provider(
            self.eth_call_full_node)
        result = []
        for event in self.event_data:
            event['block_timestamp'] = int(block_transaction[event['_id'] + '_block'].result['timestamp'], 16)
            event['wallet'] = str(block_transaction[event['_id'] + '_transaction'].result['from']).lower()

            result.append(event)
        return result

    def _make_eth_call(self, eth_event_dict):
        call_block = eth_call_block_by_block_number(
            eth_event_dict['block_number'], eth_event_dict['_id'] + '_block')
        if call_block not in self.eth_call_full_node: self.eth_call_full_node.append(call_block)
        call_transaction = eth_call_transaction_by_hash(
            eth_event_dict['transaction_hash'], eth_event_dict['_id'] + '_transaction')
        if call_transaction not in self.eth_call_full_node: self.eth_call_full_node.append(call_transaction)
