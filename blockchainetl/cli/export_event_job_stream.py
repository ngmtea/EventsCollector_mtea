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
import os
import json
import click
from utils.logging_utils import logging_basic_config
from blockchainetl.providers.auto import get_provider_from_uri
from blockchainetl.utils.thread_local_proxy import ThreadLocalProxy
from blockchainetl.streaming.streaming_exporter_creator import create_steaming_exporter
from blockchainetl.streaming.event_streamer_adapter import EventStreamerAdapter
from blockchainetl.streaming.streamer import Streamer
from constants.abi_constants import ABI


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-l', '--last-synced-block-file', default='last_synced_block.txt', show_default=True, type=str, help='')
@click.option('--lag', default=0, show_default=True, type=int, help='The number of blocks to lag behind the network.')
@click.option('-p', '--provider', required=True, type=str,
              help='The URI of the web3 provider e.g. file://$HOME/Library/Ethereum/geth.ipc or http://localhost:8545/')
@click.option('-o', '--output', default='-', show_default=True, type=str,
              help='The output file. If not specified stdout is used.')
@click.option('--db-prefix', default="", show_default=True, type=str, help='prefix of db')
@click.option('-s', '--start-block', default=None, show_default=True, type=int, help='Start block')
@click.option('-e', '--end-block', default=None, type=int, help='End block')
@click.option('--period-seconds', default=1, show_default=True, type=int,
              help='How many seconds to sleep between syncs')
@click.option('-b', '--collector-batch-size', default=100, show_default=True, type=int,
              help='The number of blocks to filter at a time.')
@click.option('-B', '--streamer_batch_size', default=100, show_default=True, type=int,
              help='The number of blocks to collect at a time.')
@click.option('-w', '--max-workers', default=5, show_default=True, type=int,
              help='The maximum number of workers.')
@click.option('-ca', '--contract-addresses', default=[], show_default=True, type=str, multiple=True,
              help='The list of contract addresses to filter by.')
@click.option('-a', '--abi', default='trava_lending_abi', type=str, help='lending abi vesion')
@click.option('--log-file', default=None, show_default=True, type=str, help='Log file')
@click.option('--pid-file', default=None, show_default=True, type=str, help='pid file')
@click.option('--event-collector-id', default="events",
              show_default=True, type=str, help='event collector id')
def stream_event_collector(last_synced_block_file, lag, provider, output,
                           db_prefix="", start_block=None, end_block=None,
                           period_seconds=10, collector_batch_size=96, streamer_batch_size=960, max_workers=5,
                           contract_addresses=None, abi='trava_lending_abi',
                           log_file=None, pid_file=None, event_collector_id="events"):
    """Collect events."""
    logging_basic_config(filename=log_file)
    logger = logging.getLogger('Stream_event_collector')

    provider = pick_random_provider_uri(provider)
    logger.info(f"Start streaming from block {start_block} to block {end_block}")

    logger.info('Using full node: ' + provider)
    streamer_adapter = EventStreamerAdapter(
        abi=get_abi(abi),
        contract_addresses=list(contract_addresses),
        provider=ThreadLocalProxy(lambda: get_provider_from_uri(provider, batch=True)),
        item_exporter=create_steaming_exporter(output=output, db_prefix=db_prefix,
                                               collector_id=event_collector_id),
        batch_size=collector_batch_size,
        max_workers=max_workers
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
        db_prefix=db_prefix
    )
    start_time = int(time.time())
    streamer.stream()
    end_time = int(time.time())
    logging.info('Total time ' + str(end_time - start_time))


def get_abi(abi):
    if os.path.exists(abi):
        with open(abi, 'r') as f:
            result = f.read()
        return json.loads(result)
    elif abi in ABI.mapping.keys():
        return ABI.mapping[abi]
    else:
        raise click.BadOptionUsage('abi', 'ABI not found')


def pick_random_provider_uri(provider_uri):
    provider_uris = [uri.strip() for uri in provider_uri.split(',')]
    return random.choice(provider_uris)
