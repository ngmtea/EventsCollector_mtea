import logging
import os
import pathlib

from web3 import Web3
from web3.middleware import geth_poa_middleware
from blockchainetl.jobs.export_lending_log_job import ExportLendingEvent
from constants.lending_pool_constant import PoolConstant


class EthAllLendingEventStreamerAdapter:
    def __init__(
            self,
            provider_uri_archive_node=None,
            client_querier_archive_node=None,
            client_querier_full_node=None,
            item_exporter=None,
            provider=None,
            batch_size=96,
            max_workers=8,
            collector_id=None,
            pool_names=None
    ):
        self.pool_names = pool_names
        self.pool_constant = PoolConstant.mapping
        self.item_exporter = item_exporter
        self.batch_size = batch_size
        self.max_workers = max_workers
        self.collector_id = collector_id
        self.provider_uri_archive_node = provider_uri_archive_node
        self.w3_archive_node = Web3(provider_uri_archive_node)
        self.w3_archive_node.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.w3 = Web3(provider)
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.client_querier_archive_node = client_querier_archive_node
        self.client_querier_full_node = client_querier_full_node
        """
        log performance realtime for mr.dat
        """
        root_path = str(pathlib.Path(__file__).parent.resolve()) + "/../../"
        self.log_performance_file = root_path + "log_performance_file.csv"
        if not os.path.exists(self.log_performance_file):
            with open(self.log_performance_file, 'w+') as f:
                f.write("start_block,end_block,start,end\n")

    def open(self):
        self.item_exporter.open()

    def get_current_block_number(self):
        if self.collector_id:
            collector = self.item_exporter.get_collector(collector_id=self.collector_id)
            block_number = collector.get('last_updated_at_block_number')
        else:
            block_number = self.w3.eth.blockNumber
        return int(block_number)

    def export_all(self, start_block, end_block):
        # Extract token transfers
        self._export_events(start_block, end_block)

    def _export_events(self, start_block, end_block):
        for pool_name in self.pool_names:
            if pool_name not in self.pool_constant:
                logging.error(f'{pool_name} is not in pool constant')
                continue
            contract_address = self.w3.toChecksumAddress(self.pool_constant[pool_name]['address'])
            oracle_address = self.w3.toChecksumAddress(self.pool_constant[pool_name]['oracle_address'])
            job = ExportLendingEvent(
                start_block=start_block,
                end_block=end_block,
                batch_size=self.batch_size,
                web3=self.w3,
                web3_=self.w3_archive_node,
                item_exporter=self.item_exporter,
                max_workers=self.max_workers,
                contract_addresses=[contract_address],
                oracle_address=oracle_address,
                abi=self.pool_constant[pool_name]['abi'],
                event_abi = self.pool_constant[pool_name]['event_abi'],
                oracle_abi=self.pool_constant[pool_name]['oracle_abi'],
                client_querier_archive_node=self.client_querier_archive_node,
                client_querier_full_node=self.client_querier_full_node
            )
            job.run()

    def close(self):
        self.item_exporter.close()
