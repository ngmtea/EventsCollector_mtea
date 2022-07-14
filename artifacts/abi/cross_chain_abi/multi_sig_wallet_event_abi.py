from domain.lending_log_subcriber import EventSubscriber
from mappers.receipt_lending_log_mapper import get_topic_filter, get_all_address_name_field, get_list_params_in_order

MULTI_SIG_WALLET_EVENT_ABI = [
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "sender",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "transaction_id",
                "type": "uint256"
            }
        ],
        "name": "Confirmation",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "sender",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "transaction_id",
                "type": "uint256"
            }
        ],
        "name": "Revocation",
        "type": "event"
    }
]
MULTI_SIG_WALLET_FACTORY_EVENT_ABI = [
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address[]",
                "name": "addresses",
                "type": "address[]"
            },
            {
                "indexed": False,
                "internalType": "bytes[]",
                "name": "signature",
                "type": "bytes[]"
            }
        ],
        "name": "ConnectUser",
        "type": "event"
    }
]

if __name__ == "__main__":
    def init_events_subscription(abi):
        event_abi = abi
        if event_abi.get('type') == 'event':
            method_signature_hash = get_topic_filter(event_abi)
            list_params_in_order = get_list_params_in_order(event_abi)
            event_name = event_abi.get('name')
            event_subscriber = EventSubscriber(method_signature_hash, event_name, list_params_in_order)
            topic = method_signature_hash
            address_name_field = get_all_address_name_field(event_abi)
            return [event_subscriber, topic, address_name_field]
        return []

    for i in MULTI_SIG_WALLET_FACTORY_EVENT_ABI:
        print(init_events_subscription(i))