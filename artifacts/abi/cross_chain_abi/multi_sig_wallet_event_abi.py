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