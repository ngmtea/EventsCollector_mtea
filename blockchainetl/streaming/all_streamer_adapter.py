import os
import pathlib

from web3 import Web3
from web3.middleware import geth_poa_middleware
from blockchainetl.jobs.export_lending_log_job import ExportLendingEvent
from blockchainetl.streaming.event_streamer_adapter import EventStreamerAdapter
from constants.event_constant import *
from artifacts.abi.trava_oracle_abi import TRAVA_ORACLE_ABI
from artifacts.abi.lending_pool_abi import LENDING_POOL_ABI
from blockchainetl.jobs.event_exporter import ExportEvent
from blockchainetl.jobs.trava_lp_event_exporter import ExportEventTravaLP


class EthAllStreamerAdapter(EventStreamerAdapter):
    def __init__(
            self,
            oracle_address=None,
            provider_uri_archive_node=None,
            client_querier_archive_node=None,
            client_querier_full_node=None,
            contract_addresses=None,
            item_exporter=None,
            provider=None,
            batch_size=96,
            max_workers=8,
            abi=LENDING_POOL_ABI,
            oracle_abi=TRAVA_ORACLE_ABI,
            collector_id=None,
            streamer_types=StreamerTypes.all
    ):
        super().__init__(
            contract_addresses=contract_addresses,
            item_exporter=item_exporter,
            provider=provider,
            batch_size=batch_size,
            max_workers=max_workers,
            abi=abi,
            collector_id=collector_id
        )
        self.streamer_types = streamer_types
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
        if StreamerTypes.lending_events in self.streamer_types:
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

        if StreamerTypes.events in self.streamer_types:
            job = ExportEvent(
                start_block=start_block,
                end_block=end_block,
                batch_size=self.batch_size,
                web3=self.w3,
                item_exporter=self.item_exporter,
                max_workers=self.max_workers,
                contract_addresses=self.contract_addresses,
                abi=self.abi,
            )
            job.run()

        if StreamerTypes.trava_lp_events in self.streamer_types:
            job = ExportEventTravaLP(
                start_block=start_block,
                end_block=end_block,
                batch_size=self.batch_size,
                max_workers=self.max_workers,
                item_exporter=self.item_exporter,
                web3=self.w3,
                contract_addresses=self.contract_addresses,
                abi=self.abi,
                client_querier=self.client_querier_archive_node,
            )
            job.run()

    def close(self):
        self.item_exporter.close()
