import logging
from web3 import Web3
from web3._utils.filters import Filter
from blockchainetl.bricher.streaming.exporter.cream_venus_mongo_streaming_exporter import (
    CreamVenusMongodbStreamingExporter,
)
from blockchainetl.jobs.base_job import BaseJob
from constants.event_constants import Event
from blockchainetl.mappers.receipt_lending_log_mapper import EthReceiptLendingLogMapper


_LOGGER = logging.getLogger(__name__)


class ExportCreamVenusEvent(BaseJob):
    def __init__(
        self,
        start_block: int,
        end_block: int,
        web3: Web3,
        contract_addresses: list,
        item_exporter: CreamVenusMongodbStreamingExporter,
        abi: list,
    ) -> None:
        self.start_block: int = start_block
        self.end_block: int = end_block
        self.web3: Web3 = web3
        self.contract_addresses: list = contract_addresses
        self.item_exporter = item_exporter
        self.abi: list = abi
        self.event_info: dict = {}
        self.topics: list = []
        self.receipt_log: EthReceiptLendingLogMapper = EthReceiptLendingLogMapper()

    def _start(self):
        self.event_data = []
        self.list_abi: list = self.receipt_log.build_list_info_event(abi=self.abi)
        for abi in self.list_abi:
            self.event_info[abi[1]] = abi[0]
            self.topics.append(abi[1])
        _LOGGER.info("Start crawling events")

    def _export(self):
        _LOGGER.info(f"Crawling events from {self.start_block} to {self.end_block}")
        event_list: list = self.export_event(
            start_block=self.start_block,
            end_block=self.end_block,
            topics=self.topics,
            addresses=self.contract_addresses,
            event_subscriber=self.event_info,
        )

        self.event_data += event_list

    def export_event(
        self,
        start_block: int,
        end_block: int,
        topics: list,
        addresses: list,
        event_subscriber: dict,
    ):
        filter_params: dict = {
            "fromBlock": start_block,
            "toBlock": end_block,
            "topics": [topics],
        }
        if addresses is not None and len(addresses) > 0:
            filter_params["address"] = addresses

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

    def _end(self):
        self.item_exporter.export_items(self.event_data)
        _LOGGER.info(f"Crawled events from {self.start_block} to {self.end_block}")
