from web3 import Web3
from web3.middleware import geth_poa_middleware
from artifacts.abi.events.c_token_event import CTOKEN_EVENT
from blockchainetl.bricher.jobs.cream_venus_event_exporter import ExportCreamVenusEvent
from blockchainetl.bricher.streaming.exporter.cream_venus_mongo_streaming_exporter import (
    CreamVenusMongodbStreamingExporter,
)


class CreamVenusEventStreamerAdapter:
    def __init__(
        self,
        contract_addresses: list,
        provider: str,
        item_exporter: CreamVenusMongodbStreamingExporter,
        abi=CTOKEN_EVENT,
    ) -> None:
        self.contract_addresses: list = [
            Web3.toChecksumAddress(i) for i in contract_addresses
        ]
        self.provider = provider
        self.web3: Web3 = Web3(Web3.HTTPProvider(provider))
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.item_exporter = item_exporter
        self.abi = abi

    def open(self):
        pass

    def export_all(self, start_block, end_block):
        # Extract token transfers
        self._export_token_transfers(start_block, end_block)

    def _export_token_transfers(self, start_block, end_block):
        job = ExportCreamVenusEvent(
            start_block=start_block,
            end_block=end_block,
            web3=self.web3,
            contract_addresses=self.contract_addresses,
            item_exporter=self.item_exporter,
            abi=self.abi,
        )
        job.run()

    def close(self):
        pass