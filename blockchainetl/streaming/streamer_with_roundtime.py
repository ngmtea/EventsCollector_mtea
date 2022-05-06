from blockchainetl.streaming.streamer import Streamer, write_to_file, delete_file
from blockchainetl.streaming.streamer_adapter_stub import StreamerAdapterStub
from configs.blockchain_etl_config import BlockchainEtlConfig


class RoundTimeStreamer(Streamer):
    def __init__(
            self,
            blockchain_streamer_adapter=StreamerAdapterStub(),
            last_synced_block_file='last_synced_block.txt',
            lag=0,
            start_block=None,
            end_block=None,
            period_seconds=10,
            block_batch_size=10,
            retry_errors=True,
            pid_file=None,
            stream_id=BlockchainEtlConfig.STREAM_ID,
            output=BlockchainEtlConfig.OUTPUT,
            db_prefix="",
    ):
        super().__init__(
            blockchain_streamer_adapter=blockchain_streamer_adapter,
            last_synced_block_file=last_synced_block_file,
            lag=lag,
            start_block=start_block,
            end_block=end_block,
            period_seconds=period_seconds,
            block_batch_size=block_batch_size,
            retry_errors=retry_errors,
            pid_file=pid_file,
            stream_id=stream_id,
            output=output,
            db_prefix=db_prefix
        )

