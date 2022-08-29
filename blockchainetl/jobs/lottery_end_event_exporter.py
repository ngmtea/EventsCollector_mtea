import logging
import time

from query_state_lib.base.mappers.eth_call_mapper import EthCall
from query_state_lib.base.utils.encoder import encode_eth_call_data
from artifacts.abi.lending.loterry import LOTTERY
from data_storage.memory_storage import MemoryStorage
from blockchainetl.jobs.base_job import BaseJob
from constants.lottery_constant import LotteryConstant

_LOGGER = logging.getLogger(__name__)


class ExportEndEventLottery(BaseJob):
    def __init__(self,
                 item_exporter,
                 web3,
                 client_querier_full_node,
                 contract_addresses,
                 lottery_abi=LOTTERY
                 ):
        self.chain_id = LotteryConstant.chain_id
        self.memory = MemoryStorage.getInstance()
        self.timestamp = time.time()
        self.item_exporter = item_exporter
        self.web3 = web3
        self.client_querier_full_node = client_querier_full_node
        self.contract_addresses = [i.lower() for i in contract_addresses]
        self.lottery_abi = lottery_abi
        self.end_event_ids = {}

    def _start(self):
        self.get_end_event_id()

    def _export(self):
        self.query_end_events()

    def get_end_event_id(self):
        chain_id = {}
        for address in self.contract_addresses:
            _id = self.chain_id[address]
            if _id not in chain_id:
                chain_id[_id] = list(self.item_exporter.get_items("lottery", "collectors", {"_id": _id}))[0]
            self.end_event_ids[address] = chain_id[_id][address]

    def query_end_events(self):
        start = time.time()
        key = "lottery_end_event"
        lottery_data = self.memory.get(key)
        if not lottery_data: lottery_data = {}
        lotteries = []
        for address in self.contract_addresses:
            if address not in lottery_data:
                lotteries.append(address)
                lottery_data[address] = 0
            elif int(self.timestamp) >= lottery_data[address]:
                lotteries.append(address)
            else:
                continue

        lottery_id_call = []
        for address in lotteries:
            data = encode_eth_call_data(abi=self.lottery_abi, fn_name="getLastEventId", args=[])
            call = EthCall(to=self.web3.toChecksumAddress(address), block_number="latest", data=data,
                           abi=self.lottery_abi, fn_name='getLastEventId', id=address)
            lottery_id_call.append(call)

        _ids_response = self.client_querier_full_node.sent_batch_to_provider(lottery_id_call)
        end_event_data_call = []
        update_ids = []
        for address in lotteries:
            update_id = {"_id": self.chain_id[address]}
            try:
                _last_id = _ids_response[address].decode_result()[0]
            except Exception as e:
                _last_id = None
            if not _last_id: continue

            update_id[address] = int(_last_id)
            update_ids.append(update_id)
            for _id in range(self.end_event_ids[address], update_id[address] + 1):
                data = encode_eth_call_data(abi=self.lottery_abi, fn_name='getLotteryEvent', args=[int(_id)])
                call = EthCall(to=self.web3.toChecksumAddress(address), block_number="latest", data=data,
                               abi=self.lottery_abi, fn_name='getLotteryEvent', id=address + str(_id))
                end_event_data_call.append(call)

        _end_event_data_response = self.client_querier_full_node.sent_batch_to_provider(end_event_data_call)
        end_event_data = []
        for address in lotteries:
            try:
                _last_id = _ids_response[address].decode_result()[0]
            except Exception as e:
                _last_id = None
            if not _last_id: continue

            for _id in range(self.end_event_ids[address], _last_id + 1):
                end_event = {"_id": self.chain_id[address.lower()] + "_" + address.lower() + "_" + str(_id),
                             "chain_id": self.chain_id[address.lower()]}
                try:
                    data = _end_event_data_response[address + str(_id)].decode_result()[0]
                    if not data[0]: continue
                    lottery_data[address] = data[1]
                    end_event["id"] = _id
                    end_event["ticket"] = address
                    end_event["start_time"] = data[0]
                    end_event["end_time"] = data[1]
                    end_event["total_deposit"] = data[2] / 10 ** LotteryConstant.decimals[address.lower()]
                    end_event["t_token_reward"] = data[3] / 10 ** LotteryConstant.decimals[address.lower()]
                    end_event["r_trava_reward"] = data[4] / 10 ** 18
                    end_event["random_num"] = str(data[5])
                    end_event["winner"] = data[6].lower()
                    end_event["claimed"] = data[7]
                    end_event_data.append(end_event)
                except Exception as e:
                    logging.error(f"Got exception {e}")
                    pass

        self.memory.set(key, lottery_data)
        self.item_exporter.export_collection_items('lottery', 'end_events', end_event_data)
        self.item_exporter.export_collection_items('lottery', 'collectors', update_ids)
        _LOGGER.info(f"Exporting {len(end_event_data)} end events takes {round(time.time() - start, 2)}s!")
