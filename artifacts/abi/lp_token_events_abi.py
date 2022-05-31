LP_TOKEN_EVENT_ABI = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "sender", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "amount0", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "amount1", "type": "uint256"},
            {"indexed": True, "internalType": "address", "name": "to", "type": "address"}
        ],
        "name": "Burn",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "sender", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "amount0", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "amount1", "type": "uint256"}
        ],
        "name": "Mint",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "sender", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "amount0_in", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "amount1_in", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "amount0_out", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "amount1_out", "type": "uint256"},
            {"indexed": True, "internalType": "address", "name": "to", "type": "address"}
        ],
        "name": "Swap",
        "type": "event"
    }
]
