import os
import pathlib

from web3 import Web3
from web3.middleware import geth_poa_middleware
from blockchainetl.jobs.multi_sig_wallet_event_exporter import MultiSigWalletEventExporter
from artifacts.abi.lending.trava.lending_pool_abi import LENDING_POOL_ABI


class MultiSigWalletEventStreamerAdapter:
    def __init__(
            self,
            contract_addresses,
            item_exporter,
            provider,
            batch_size=96,
            max_workers=8,
            abi=LENDING_POOL_ABI,
            collector_id=None,
            client_querier_full_node=None
    ):
        self.abi = abi
        self.provider = provider
        self.w3 = Web3(provider)
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.item_exporter = item_exporter
        self.batch_size = batch_size
        self.max_workers = max_workers
        self.contract_addresses = [Web3.toChecksumAddress(i) for i in contract_addresses]
        self.collector_id = collector_id
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
        self._export_token_transfers(start_block, end_block)

    def _export_token_transfers(self, start_block, end_block):
        job = MultiSigWalletEventExporter(
            start_block=start_block,
            end_block=end_block,
            batch_size=self.batch_size,
            web3=self.w3,
            item_exporter=self.item_exporter,
            max_workers=self.max_workers,
            contract_addresses=self.contract_addresses,
            abi=self.abi,
            client_querier_full_node=self.client_querier_full_node
        )
        job.run()

    def close(self):
        self.item_exporter.close()