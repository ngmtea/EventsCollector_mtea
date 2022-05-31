from constants.lending_pool_constant import PoolConstant
from update_missed_event import run
from artifacts.abi.trava_oracle_abi import TRAVA_ORACLE_ABI
import logging
from artifacts.abi.lending.lending_pool_abi import LENDING_POOL_ABI

from blockchainetl.jobs.export_lending_log_job import ExportLendingEvent

_LOGGER = logging.getLogger(__name__)


class MissedEventHanler(ExportLendingEvent):
    def __init__(
            self,
            start_block,
            end_block,
            batch_size,
            max_workers,
            item_exporter,
            web3,
            web3_,
            contract_address,
            client_querier_full_node,
            client_querier_archive_node,
            oracle_address,
            abi=LENDING_POOL_ABI,
            oracle_abi=TRAVA_ORACLE_ABI,
            param=None,
    ):
        super().__init__(
            start_block=start_block,
            end_block=end_block,
            batch_size=batch_size,
            max_workers=max_workers,
            item_exporter=item_exporter,
            web3=web3,
            web3_=web3_,
            contract_addresses=[contract_address],
            client_querier_full_node=client_querier_full_node,
            client_querier_archive_node=client_querier_archive_node,
            oracle_address=oracle_address,
            abi=abi,
            oracle_abi=oracle_abi
        )
        self.param = param
        self.contract_address = contract_address
        self.pool_info = PoolConstant.mapping["trava-bsc"]
        for key in PoolConstant.mapping:
            if PoolConstant.mapping[key]["address"] == contract_address.lower():
                self.pool_info = PoolConstant.mapping[key]

        self.miss_events = []

    def check_missed_events(self):
        event_keys = []
        for event in self.event_data:
            event_keys.append(event["_id"])
        filter_ = {
            "_id": {"$in": event_keys}
        }

        events = self.item_exporter.get_event_items(filter_)

        for event in events:
            event_keys.remove(event["_id"])

        for event in self.event_data:
            if event["_id"] in event_keys:
                self.miss_events.append(event)

    def _end(self):
        self.batch_work_executor.shutdown()
        self.check_missed_events()

        for eth_event_dict in self.miss_events:
            self._make_eth_call(eth_event_dict)

        self.miss_events = self.enrich_event()
        self.item_exporter.export_items(self.miss_events)
        self.item_exporter.close()
        self.update_events()

        _LOGGER.info(f'Crawled {len(self.miss_events)} missed events from {self.start_block} to {self.end_block}!')

    def update_events(self):
        for event in self.miss_events:
            params = {
                "start_block": str(event["block_number"] - 1),
                "end_block": str(event["block_number"] + 1),
                "address": self.contract_address,
                'abi': self.pool_info['abi_type'],
                'last_synced_block': self.pool_info['last_syned_block'],
                "provider": self.param["link_archive_node"],
                "mongo_db": self.param["link_mongo_db"],
                "arrango_db": self.param["link_graph_db"],
                "enricher_id": self.pool_info["enricher_id"],
                "timestamp": str(event["block_timestamp"] + 3600),
                "chain_id": self.pool_info["chain_id"],
                "oracle_address": self.pool_info["oracle_address"],
                "db_prefix": self.pool_info["db_prefix"]
            }
            run(params)

    def enrich_event(self):
        eth_price = {}
        block_transaction = self.client_querier_full_node.sent_batch_to_provider(
            self.eth_call_full_node)
        price = self.client_querier_archive_node.sent_batch_to_provider(
            self.eth_call_archive_node)
        if self.eth_token_price_call:
            eth_price = self.client_querier_archive_node.sent_batch_to_provider(self.eth_token_price_call)
        result = []
        for event in self.miss_events:
            if event['contract_address'] in self.assets.keys():
                event['asset'] = self.assets[event['contract_address']]
            event['block_timestamp'] = int(block_transaction[event['_id'] + '_block'].result['timestamp'], 16)
            event['wallet'] = str(block_transaction[event['_id'] + '_transaction'].result['from']).lower()
            for i in PoolConstant.token_type:
                if i in event.keys():
                    event[f'decimal_of_{i.replace("Asset", "_asset")}'] = self.token_get_decimals(event[i])
                    price_token = int(price[event['_id'] + '_' + i].result, 16)
                    if eth_price:
                        price_token = price_token * (
                                int(eth_price[event['_id'] + '_' + i].result[66:130], 16) / 10 ** 18)
                    event[f'price_of_{i.replace("Asset", "_asset")}'] = str(int(price_token))

            result.append(event)
        return result
