# MIT License
#
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import logging
import random
import time
import click
from configs.config import MongoDBConfig
from utils.logging_utils import logging_basic_config
from blockchainetl.providers.auto import get_provider_from_uri
from blockchainetl.utils.thread_local_proxy import ThreadLocalProxy
from query_state_lib.client.client_querier import ClientQuerier
from blockchainetl.streaming.streaming_exporter_creator import create_steaming_exporter
from blockchainetl.streaming.multi_lending_log_streamer_adapter import EthAllLendingEventStreamerAdapter
from blockchainetl.streaming.streamer import Streamer


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-l', '--last-synced-block-file', default='last_synced_block.txt', show_default=True, type=str, help='')
@click.option('--lag', default=0, show_default=True, type=int, help='The number of blocks to lag behind the network.')
@click.option('-pf', '--provider-uri-full-node', type=str, default=None,
              help='The URI of the web3 provider')
@click.option('-pa', '--provider-uri-archive-node', type=str, default=None,
              help='The URI of the web3 provider')
@click.option('-o', '--output', default='-', show_default=True, type=str,
              help='The output file. If not specified stdout is used.')
@click.option('--db-prefix', default="", show_default=True, type=str, help='prefix of db')
@click.option('--database-name', default=MongoDBConfig.DATABASE,
              show_default=True, type=str, help='database name')
@click.option('-pns', '--pool-names', default=[], show_default=True, type=str, multiple=True,
              help='The list of contract name to filter by.')
@click.option('-s', '--start-block', default=None, show_default=True, type=int, help='Start block')
@click.option('-e', '--end-block', default=None, type=int, help='End block')
@click.option('--period-seconds', default=1, show_default=True, type=int,
              help='How many seconds to sleepl between syncs')
@click.option('-b', '--collector-batch-size', default=100, show_default=True, type=int,
              help='The number of blocks to filter at a time.')
@click.option('-B', '--streamer_batch_size', default=100, show_default=True, type=int,
              help='The number of blocks to collect at a time.')
@click.option('-w', '--max-workers', default=5, show_default=True, type=int,
              help='The maximum number of workers.')
@click.option('--log-file', default=None, show_default=True, type=str, help='Log file')
@click.option('--pid-file', default=None, show_default=True, type=str, help='pid file')
@click.option('--event-collector-id', default="events",
              show_default=True, type=str, help='event collector id')
@click.option('--transaction-collector-id', default=None,
              show_default=True, type=str, help='transaction collector id')
def stream_multi_lending_event_collector(last_synced_block_file, lag, provider_uri_full_node=None,
                                         provider_uri_archive_node=None, output=None,
                                         db_prefix="", database_name=MongoDBConfig.DATABASE, pool_names=None,
                                         start_block=None, end_block=None,
                                         period_seconds=10, collector_batch_size=96,
                                         streamer_batch_size=960, max_workers=5,
                                         log_file=None, pid_file=None, event_collector_id="events",
                                         transaction_collector_id=None):
    """Collect token transfer events."""
    if pool_names is None:
        pool_names = []
    logging_basic_config(filename=log_file)
    logger = logging.getLogger('Streamer')
    logger.info(f"Start streaming from block {start_block} to block {end_block}")
    logger.info('Using full node: ' + provider_uri_full_node + ' and archive node: ' + provider_uri_archive_node)

    client_querier_archive_node = ClientQuerier(provider_url=provider_uri_archive_node)
    client_querier_full_node = ClientQuerier(provider_url=provider_uri_full_node)

    streamer_adapter = EthAllLendingEventStreamerAdapter(
        provider=ThreadLocalProxy(lambda: get_provider_from_uri(provider_uri_full_node, batch=True)),
        provider_uri_archive_node=ThreadLocalProxy(lambda: get_provider_from_uri(provider_uri_archive_node,
                                                                                 batch=True)),
        client_querier_full_node=client_querier_full_node,
        client_querier_archive_node=client_querier_archive_node,
        item_exporter=create_steaming_exporter(output=output, db_prefix=db_prefix,
                                               collector_id=event_collector_id, database=database_name),
        batch_size=collector_batch_size,
        max_workers=max_workers,
        collector_id=transaction_collector_id,
        pool_names=list(pool_names),
    )
    streamer = Streamer(
        blockchain_streamer_adapter=streamer_adapter,
        last_synced_block_file=last_synced_block_file,
        lag=lag,
        start_block=start_block,
        end_block=end_block,
        period_seconds=period_seconds,
        block_batch_size=streamer_batch_size,
        pid_file=pid_file,
        stream_id=event_collector_id,
        output=output,
        db_prefix=db_prefix,
        database=database_name
    )
    start_time = int(time.time())
    streamer.stream()
    end_time = int(time.time())
    logging.info('Total time ' + str(end_time - start_time))
