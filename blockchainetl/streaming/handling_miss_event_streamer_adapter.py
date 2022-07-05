from artifacts.abi.trava_oracle_abi import TRAVA_ORACLE_ABI

from artifacts.abi.lending.trava.lending_pool_abi import LENDING_POOL_ABI

from blockchainetl.streaming.lending_log_streamer_adapter import EthLendingLogStreamerAdapter
from blockchainetl.jobs.handle_miss_events import MissedEventHanler


class MissedEventStreamerAdapter(EthLendingLogStreamerAdapter):
    def __init__(
            self,
            oracle_address,
            provider_uri_archive_node,
            client_querier_archive_node,
            client_querier_full_node,
            contract_address,
            item_exporter,
            provider,
            batch_size=96,
            max_workers=8,
            abi=LENDING_POOL_ABI,
            oracle_abi=TRAVA_ORACLE_ABI,
            collector_id=None,
            param=None,
    ):
        super().__init__(
            oracle_address=oracle_address,
            provider_uri_archive_node=provider_uri_archive_node,
            client_querier_archive_node=client_querier_archive_node,
            client_querier_full_node=client_querier_full_node,
            contract_addresses=[contract_address],
            item_exporter=item_exporter,
            provider=provider,
            batch_size=batch_size,
            max_workers=max_workers,
            abi=abi,
            collector_id=collector_id,
            oracle_abi=oracle_abi,
        )
        self.contract_address = contract_address
        self.param = param

    def _export_token_transfers(self, start_block, end_block):
        job = MissedEventHanler(
            start_block=start_block,
            end_block=end_block,
            batch_size=self.batch_size,
            web3=self.w3,
            web3_=self.w3_archive_node,
            item_exporter=self.item_exporter,
            max_workers=self.max_workers,
            contract_address=self.contract_address,
            oracle_address=self.oracle_address,
            abi=self.abi,
            oracle_abi=self.oracle_abi,
            client_querier_archive_node=self.client_querier_archive_node,
            client_querier_full_node=self.client_querier_full_node,
            param=self.param
        )
        job.run()
