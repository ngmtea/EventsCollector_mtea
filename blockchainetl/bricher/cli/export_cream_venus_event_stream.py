import time
import click
import logging
from blockchainetl.bricher.configs.config import Provider
from blockchainetl.bricher.streaming.cream_venus_event_streamer_adapter import (
    CreamVenusEventStreamerAdapter,
)
from blockchainetl.bricher.streaming.cream_venus_streamer import CreamVenusStreamer
from blockchainetl.bricher.streaming.exporter.cream_venus_mongo_streaming_exporter import (
    CreamVenusMongodbStreamingExporter,
)

from blockchainetl.bricher.streaming.importer.mongo_streaming_importer import (
    MongoStreamingImporter,
)


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "-s",
    "--start-block",
    default=20045095,
    show_default=True,
    type=int,
    help="Start block",
)
@click.option("-e", "--end-block", default=20936754, type=int, help="End block")
def stream_cream_venus_event_collector(start_block: int, end_block: int):
    # events_deleter = CreamVenusMongodbStreamingExporter()
    # events_deleter.delete_events_for_testing()
    # return

    token_address_importer: MongoStreamingImporter = MongoStreamingImporter()
    token_addresses: list = token_address_importer.get_cream_venus_token_address()

    logger = logging.getLogger("Stream_cream_venus_event_collector")
    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
    logger.info(f"Start streaming from block {start_block} to block {end_block}")

    streamer_adapter: CreamVenusEventStreamerAdapter = CreamVenusEventStreamerAdapter(
        contract_addresses=token_addresses,
        provider=Provider.BSC_PUBLIC_RPC_NODE,
        item_exporter=CreamVenusMongodbStreamingExporter(),
    )

    streamer: CreamVenusStreamer = CreamVenusStreamer(
        blockchain_streamer_adapter=streamer_adapter,
        start_block=start_block,
        end_block=end_block,
    )

    start_time = int(time.time())
    streamer.stream()
    end_time = int(time.time())
    logging.info("Total time " + str(end_time - start_time))
