import time
import click
import random
import logging
from configs.config import Provider
from blockchainetl.streaming.cream_venus_event_streamer_adapter import (
    CreamVenusEventStreamerAdapter,
)
from blockchainetl.streaming.cream_venus_streamer import CreamVenusStreamer
from blockchainetl.streaming.exporter.cream_venus_mongo_streaming_exporter import (
    CreamVenusMongodbStreamingExporter,
)

from blockchainetl.streaming.importer.mongo_streaming_importer import (
    MongoStreamingImporter,
)

from query_state_lib.client.client_querier import ClientQuerier
from blockchainetl.utils.thread_local_proxy import ThreadLocalProxy
from blockchainetl.providers.auto import get_provider_from_uri


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
@click.option("-m", "--mongo-uri", default="", type=str, help="Mongo db")
@click.option('-p', '--provider', type=str,
              help='The URI of the web3 provider e.g. file://$HOME/Library/Ethereum/geth.ipc or http://localhost:8545/')
def stream_cream_venus_event_collector(start_block: int, end_block: int, mongo_uri, provider):
    # events_deleter = CreamVenusMongodbStreamingExporter()
    # events_deleter.delete_events_for_testing()
    # return
    if not mongo_uri:
        token_address_importer: MongoStreamingImporter = MongoStreamingImporter()
    else:
        token_address_importer: MongoStreamingImporter = MongoStreamingImporter(mongo_uri)
    token_addresses: list = token_address_importer.get_cream_venus_token_address("Cream")
    token_addresses: list = ['0x1ffe17b99b439be0afc831239ddecda2a790ff3a']

    logger = logging.getLogger("Stream_cream_venus_event_collector")
    provider = pick_random_provider_uri(provider)
    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

    logger.info(f"Start streaming from block {start_block} to block {end_block}")

    logger.info('Using full node: ' + provider)

    client_querier_full_node = ClientQuerier(provider_url=provider)

    streamer_adapter: CreamVenusEventStreamerAdapter = CreamVenusEventStreamerAdapter(
        contract_addresses=token_addresses,
        provider=provider,

        item_exporter=CreamVenusMongodbStreamingExporter(),

        client_querier_full_node=client_querier_full_node,
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


def pick_random_provider_uri(provider_uri):
    provider_uris = [uri.strip() for uri in provider_uri.split(',')]
    return random.choice(provider_uris)
