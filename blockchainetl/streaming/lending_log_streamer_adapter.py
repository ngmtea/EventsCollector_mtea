import os
import pathlib

from web3 import Web3
from web3.middleware import geth_poa_middleware
from blockchainetl.jobs.export_lending_log_job import ExportLendingEvent
from blockchainetl.streaming.event_streamer_adapter import EventStreamerAdapter
from artifacts.abi.trava_oracle_abi import TRAVA_ORACLE_ABI


class EthLendingLogStreamerAdapter(EventStreamerAdapter):
    def __init__(
            self,
            oracle_address,
            provider_uri_archive_node,
            client_querier_archive_node,
            client_querier_full_node,
            oracle_abi=TRAVA_ORACLE_ABI):
        self.oracle_abi = oracle_abi
        self.oracle_address = oracle_address
        self.provider_uri_archive_node = provider_uri_archive_node
        self.w3_archive_node = Web3(provider_uri_archive_node)
        self.w3_archive_node.middleware_onion.inject(geth_poa_middleware, layer=0)
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


    def export_all(self, start_block, end_block):
        # Extract token transfers
        self._export_token_transfers(start_block, end_block)

    def _export_token_transfers(self, start_block, end_block):
        job = ExportLendingEvent(
            start_block=start_block,
            end_block=end_block,
            batch_size=self.batch_size,
            web3=self.w3,
            web3_=self.w3_archive_node,
            item_exporter=self.item_exporter,
            max_workers=self.max_workers,
            contract_addresses=self.contract_addresses,
            oracle_address=self.oracle_address,
            abi=self.abi,
            oracle_abi=self.oracle_abi,
            client_querier_archive_node=self.client_querier_archive_node,
            client_querier_full_node=self.client_querier_full_node
        )
        job.run()

    def close(self):
        self.item_exporter.close()
