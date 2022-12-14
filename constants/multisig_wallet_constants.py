class MultiSigFactories:
    chain_id = "chain_id"
    addresses = [
        "0x1047b4694cc749c3abaab6fac300997777373a39",
        "0xfe8fe26c81d0de4be50d872bca23d6522dd0b1ef",
        "0x1047b4694cc749c3abaab6fac300997777373a39"
    ]
    mapping = {
        "0x1047b4694cc749c3abaab6fac300997777373a39":{
            chain_id:"0x4",
        },
        "0x1047b4694cc749c3abaab6fac300997777373a39":{
            chain_id:"0x61"
        }
    }
    chain_id_mapping = {
        "rinkeby":"0x4",
        "bsc_testnet":'0x61'
    }