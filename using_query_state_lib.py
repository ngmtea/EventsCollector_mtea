from query_state_lib.base.utils.encoder import encode_eth_call_data
from query_state_lib.base.mappers.eth_call_mapper import EthCall


def using_query_state_lib(lending_address, web3, client_querier, abi, fn_name, args):
    number_query = 100
    call_infos = []
    get_balances = []

    data = encode_eth_call_data(abi=abi, fn_name=fn_name, args=args)

    for i in range(number_query):
        call1 = EthCall(to=web3.toChecksumAddress(lending_address), data=data, block_number="latest", abi=abi,
                        fn_name=fn_name, id=f"{lending_address}_{i}")
        call_infos.append(call1)

    list_json_rpc = call_infos + get_balances

    data_result = client_querier.sent_batch_to_provider(list_json_rpc, batch_size=2000, max_workers=1, timeout=200)
    result_tmp = data_result.get(f"{lending_address}_{0}").decode_result()

    return result_tmp
