import logging

from query_state_lib.base.mappers.eth_json_rpc_mapper import EthJsonRpc
from artifacts.abi.events.transfer_event_abi import TRANSFER_EVENT_ABI
from blockchainetl.jobs.event_exporter import ExportEvent

_LOGGER = logging.getLogger(__name__)


def eth_call_block_by_block_number(block_number, identify):
    return EthJsonRpc(id=identify, params=[str(hex(block_number)), False], method="eth_getBlockByNumber")


def eth_call_transaction_by_hash(transaction_hash, identify):
    return EthJsonRpc(id=identify, params=[transaction_hash], method="eth_getTransactionByHash")


class ExportEventLottery(ExportEvent):
    def __init__(self,
                 start_block,
                 end_block,
                 batch_size,
                 max_workers,
                 item_exporter,
                 web3,
                 client_querier_full_node,
                 contract_addresses,
                 abi=TRANSFER_EVENT_ABI
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

        self.block_timestamp = None
        self.client_querier_full_node = client_querier_full_node

    def _export(self):
        self.batch_work_executor.execute(
            range(self.start_block, self.end_block + 1),
            self.export_batch
        )

    def _end(self):
        self.batch_work_executor.shutdown()
        self.item_exporter.export_items(self.event_data)
        _LOGGER.info(f'enrich event data from')
        self.get_block_timestamp()
        self.enrich_event()
        self.item_exporter.close()
        _LOGGER.info(f'Crawled {len(self.event_data)} events from {self.start_block} to {self.end_block}!')

    def export_batch(self, block_number_batch):
        _LOGGER.info(f'crawling event data from {block_number_batch[0]} to {block_number_batch[-1]}')
        # for abi in self.list_abi:
        e_list = self.export_events(block_number_batch[0], block_number_batch[-1], event_subscriber=self.event_info,
                                    topic=self.topics, pools=self.contract_addresses)
        self.event_data += e_list

    def enrich_event(self):
        e_list, _votes = [], []
        data = {}
        for event in self.event_data:
            if event['contract_address'] not in data:
                data[event['contract_address']] = {}

            if event['_from'] != "0x0000000000000000000000000000000000000000":
                if event['_from'] not in data[event['contract_address']]:
                    data[event['contract_address']][event['_from']] = {"add": 0, "sub": 0}

                data[event['contract_address']][event['_from']]["sub"] += float(event["_value"])

            if event['_to'] != "0x0000000000000000000000000000000000000000":
                if event['_to'] not in data[event['contract_address']]:
                    data[event['contract_address']][event['_to']] = {"add": 0, "sub": 0}

                data[event['contract_address']][event['_to']]["add"] += float(event["_value"])

        _filter = {
            "_id": {"$in": list(data.keys())}
        }
        tickets = self.item_exporter.get_items('lottery', 'tickets', filter=_filter)
        result = []
        ticket_ids = []
        for ticket in tickets:
            _id = ticket['_id']
            ticket_ids.append(_id)
            for address in data[_id]:
                if address not in ticket: ticket[address] = 0
                ticket[address] += data[_id][address]['add'] - data[_id][address]['sub']
                # if ticket[address] == 0:
                #     if len(ticket.keys()) > 2:
                #         del ticket[address]
                #     else:
                #         ticket = {"_id": ticket["_id"]}

            result.append(ticket)

        for ticket in data:
            ticket_data = {}
            if ticket not in ticket_ids:
                ticket_data["_id"] = ticket
                for address in data[ticket]:
                    ticket_data[address] = data[ticket][address]['add'] - data[ticket][address]['sub']
                result.append(ticket_data)

        self.item_exporter.export_collection_items('lottery', 'tickets', result)

    def get_block_timestamp(self):
        eth_call = []
        for event in self.event_data:
            block = event['block_number']
            call_block = eth_call_block_by_block_number(
                event['block_number'], block)
            if call_block not in eth_call:
                eth_call.append(call_block)
        eth_response_data = self.client_querier_full_node.sent_batch_to_provider(eth_call)
        for event in self.event_data:
            event["block_timestamp"] = int(eth_response_data[event['block_number']].result['timestamp'], 16)
