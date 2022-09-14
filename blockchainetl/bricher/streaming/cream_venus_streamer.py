import logging
from blockchainetl.bricher.configs.config import MongoDBConfig
from blockchainetl.bricher.streaming.cream_venus_event_streamer_adapter import (
    CreamVenusEventStreamerAdapter,
)
from blockchainetl.bricher.streaming.exporter.cream_venus_mongo_streaming_exporter import (
    CreamVenusMongodbStreamingExporter,
)

_LOGGER = logging.getLogger(__name__)


class CreamVenusStreamer:
    def __init__(
        self,
        blockchain_streamer_adapter: CreamVenusEventStreamerAdapter,
        start_block: int,
        end_block: int,
    ) -> None:
        self.blockchain_streamer_adapter = blockchain_streamer_adapter
        self.start_block: int = start_block
        self.end_block: int = end_block
        self.exporter: CreamVenusMongodbStreamingExporter = (
            CreamVenusMongodbStreamingExporter()
        )
        self.target_block: int = 0
        self.last_synced_block: int = self.start_block - 1

    def stream(self):
        try:
            self.blockchain_streamer_adapter.open()
            self._do_stream()
        finally:
            self.blockchain_streamer_adapter.close()

    def _do_stream(self):
        while True and self.last_synced_block < self.end_block:
            try:
                self._sync_cycle()
            except Exception as e:
                _LOGGER.warning("An exception occurred while syncing block data")
                _LOGGER.info(f"Error: {e}")

    def _sync_cycle(self):
        self.target_block: int = self._calculate_target_block()
        _LOGGER.info(
            f"Current block: {self.last_synced_block + 1}, target block: {self.target_block}"
        )
        self.blockchain_streamer_adapter.export_all(
            self.last_synced_block + 1, self.target_block
        )
        self.last_synced_block = self.target_block

    def _calculate_target_block(self):
        next_block: int = self.last_synced_block + 1
        target_block: int = next_block + 5000

        if target_block >= self.end_block:
            return self.end_block
        return target_block
