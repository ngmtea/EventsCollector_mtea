from blockchainetl.mappers.receipt_lending_log_mapper import *

logger = logging.getLogger('EthLendingService')


class EthReceiptCrossChainLogMapper(EthReceiptLendingLogMapper):
    def extract_event_from_log(self,receipt_log, event_subscriber):
        topics = receipt_log.topics
        if topics is None or len(topics) < 1:
            logger.warning("Topics are empty in log {} of transaction {}".format(receipt_log.log_index,
                                                                                receipt_log.transaction_hash))
            return None
        if event_subscriber.topic_hash == topics[0]:
            list_params_in_order = event_subscriber.list_params_in_order
            list_params_indexed = [param for param in list_params_in_order if param.get('indexed') == True]
            list_params_unindexed = [param for param in list_params_in_order if param.get('indexed') == False]
            
            num_params_index = len(list_params_indexed)
            num_params_unindex = len(list_params_unindexed)
        
            # Handle indexed event fields
            topics = topics[1:]
            if len(topics) != (num_params_index):
                logger.warning("The number of topics parts is not equal to {} in log {} of transaction {}"
                            .format(str(num_params_index), receipt_log.log_index, receipt_log.transaction_hash))
                return None
            
            event = EthEvent()
            event.contract_address = to_normalized_address(receipt_log.address)
            event.transaction_hash = receipt_log.transaction_hash
            event.log_index = receipt_log.log_index
            event.block_number = receipt_log.block_number
            event.event_type = event_subscriber.name
            for i in range(num_params_index):
                param_i = list_params_indexed[i]
                name = param_i.get("name")
                type = param_i.get("type")
                data = topics[i]
                event.params[name] = self.decode_data_by_type(data, type)

            # Handle unindexed event fields
            event_data = split_to_words(receipt_log.data)
            # if the number of topics and fields in data part != len(list_params_unindexed), then it's a weird event
            if len(event_data) != num_params_unindex:
                element_count = 0       # Count total element in array param and param
                for i in range(num_params_unindex):
                    element_count += 1          # Param lưu offset của mảng
                    param_i = list_params_unindexed[i]
                    name = param_i.get("name")
                    type = param_i.get("type")
                    data = event_data[i]

                    # Hanlde params is array
                    if type.endswith(']'):
                        if type.endswith('[]'):
                            event.params[name] = []
                            element_type = type.split('[')[0]
                            offset = int(int(self.decode_data_by_type(data, "uint256")) / 32)
                            length = int(self.decode_data_by_type(event_data[offset], "uint256"))
                            for index in range(offset+1, offset+length+1):
                                if type == "bytes[]":
                                    offset_byte = int(int(self.decode_data_by_type(event_data[index], "uint256")) / 32)
                                    offset_byte = offset + offset_byte + 1

                                    length_byte = int(self.decode_data_by_type(event_data[offset_byte], "uint256"))
                                    length_params = int(length_byte / 32) + 1

                                    data_byte = ""
                                    for index_byte in range(offset_byte+1, offset_byte+length_params+1):
                                        data_temp = self.decode_data_by_type(event_data[index_byte], element_type)
                                        data_byte = data_byte + data_temp[2:]
                                        element_count += 1      # Param lưu giá trị phần tử byte

                                    data_byte = "0x" + data_byte[:(length_byte*2)]
                                    event.params[name].append(data_byte)

                                    element_count += 1      # Param lưu offset của phần tử mảng byte
                                else:
                                    event.params[name].append(self.decode_data_by_type(event_data[index], element_type))

                                element_count += 1     # Param lưu giá trị phần tử mảng
                            element_count += 1    # Param lưu số phần tử mảng
                    else:
                        event.params[name] = self.decode_data_by_type(data, type)

                if len(event_data) != element_count:
                    logger.warning("The number of data parts is not equal to {} in log {} of transaction {}"
                                .format(str(num_params_unindex), receipt_log.log_index, receipt_log.transaction_hash))
                    return None
            else:
                for i in range(num_params_unindex):
                    param_i = list_params_unindexed[i]
                    name = param_i.get("name")
                    type = param_i.get("type")
                    data = event_data[i]
                    event.params[name] = self.decode_data_by_type(data, type)
                    
            return event

        return None