from artifacts.abi.trava_oracle_abi import TRAVA_ORACLE_ABI

from artifacts.abi.lending.trava.lending_pool_abi import LENDING_POOL_ABI
import logging
from blockchainetl.streaming.multi_lending_log_streamer_adapter import EthAllLendingEventStreamerAdapter
from blockchainetl.jobs.handle_miss_events import MissedEventHanler


class MissedEventStreamerAdapter(EthAllLendingEventStreamerAdapter):
    def __init__(
            self,
            provider_uri_archive_node,
            client_querier_archive_node,
            client_querier_full_node,
            item_exporter,
            provider,
            batch_size=96,
            max_workers=8,
            collector_id=None,
            param=None,
            pool_names=None
    ):
        super().__init__(
            provider_uri_archive_node=provider_uri_archive_node,
            client_querier_archive_node=client_querier_archive_node,
            client_querier_full_node=client_querier_full_node,
            item_exporter=item_exporter,
            provider=provider,
            batch_size=batch_size,
            max_workers=max_workers,
            collector_id=collector_id,
            pool_names=pool_names
        )
        self.param = param

    def _export_token_transfers(self, start_block, end_block):
        for pool_name in self.pool_names:
            if pool_name not in self.pool_constant:
                logging.error(f'{pool_name} is not in pool constant')
                continue
            contract_address = self.w3.toChecksumAddress(self.pool_constant[pool_name]['address'])
            oracle_address = self.w3.toChecksumAddress(self.pool_constant[pool_name]['oracle_address'])
            job = MissedEventHanler(
                start_block=start_block,
                end_block=end_block,
                batch_size=self.batch_size,
                web3=self.w3,
                web3_=self.w3_archive_node,
                item_exporter=self.item_exporter,
                max_workers=self.max_workers,
                contract_address=contract_address,
                oracle_address=oracle_address,
                abi=self.pool_constant[pool_name]['abi'],
                event_abi=self.pool_constant[pool_name]['event_abi'],
                oracle_abi=self.pool_constant[pool_name]['oracle_abi'],
                client_querier_archive_node=self.client_querier_archive_node,
                client_querier_full_node=self.client_querier_full_node,
                param=self.param
            )
            job.run()
