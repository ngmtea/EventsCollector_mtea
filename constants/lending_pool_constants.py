from artifacts.abi.lending.trava.lending_pool_abi import LENDING_POOL_ABI
from artifacts.abi.lending.aave.lending_pool_aave_v2_abi import LENDING_POOL_AAVE_V2_ABI
from artifacts.abi.events.lending_event_abi import *
from artifacts.abi.trava_oracle_abi import TRAVA_ORACLE_ABI


class PoolConstant:
    trava_bsc = 'trava_bsc'
    geist = 'geist'
    trava_ftm = 'trava_ftm'
    trava_eth = 'trava-eth'
    aave_v2 = 'aave-v2'
    mapping = {
        'trava-bsc': {
            'name': 'trava-bsc',
            'chain_name': 'bsc',
            'decimals': 8,
            'address': '0x75de5f7c91a89c16714017c7443eca20c7a8c295',
            'abi': LENDING_POOL_ABI,
            'event_abi': TRAVA_LENDING_EVENT_ABI,
            'oracle_abi': TRAVA_ORACLE_ABI,
            'db_prefix': '',
            'chain_id': "0x38",
            'oracle_address': '0x7cd53b71bf56cc6c9c9b43719fe98e7c360c35df',
            "enricher_id": 'enricher-default-id',
            'abi_type': 'v1',
            'last_syned_block': "trava_bsc.txt",
        },
        'geist': {
            'name': 'geist',
            'chain_name': 'ftm',
            'decimals': 18,
            'address': '0x9fad24f572045c7869117160a571b2e50b10d068',
            'abi': LENDING_POOL_AAVE_V2_ABI,
            'event_abi': AAVE_LENDING_EVENT_ABI,
            'oracle_abi': TRAVA_ORACLE_ABI,
            'db_prefix': 'ftm',
            'chain_id': "0xfa",
            'oracle_address': '0xC466e3FeE82C6bdc2E17f2eaF2c6F1E91AD10FD3',
            "enricher_id": 'enricher-event-id',
            'abi_type': 'v2',
            'last_syned_block': "geist_ftm.txt",
        },
        'trava-ftm': {
            'name': 'trava_ftm',
            'chain_name': 'ftm',
            'decimals': 8,
            'address': '0xd98bb590bdfabf18c164056c185fbb6be5ee643f',
            'abi': LENDING_POOL_ABI,
            'event_abi': TRAVA_LENDING_EVENT_ABI,
            'oracle_abi': TRAVA_ORACLE_ABI,
            'db_prefix': 'ftm',
            'chain_id': "0xfa",
            'oracle_address': '0x290346e682d51b97e2c1f186eb61eb49881c5ec7',
            "enricher_id": 'enricher-default-id',
            'abi_type': 'v1',
            'last_syned_block': "trava_ftm.txt",
        },
        'trava-eth': {
            'name': 'trava-eth',
            'chain_name': 'eth',
            'decimals': 8,
            'address': '0xd61afaaa8a69ba541bc4db9c9b40d4142b43b9a4',
            'abi': LENDING_POOL_ABI,
            'event_abi': TRAVA_LENDING_EVENT_ABI,
            'oracle_abi': TRAVA_ORACLE_ABI,
            'db_prefix': 'ethereum',
            'chain_id': "0x1",
            'oracle_address': '0x2bd81260fe864173b6ec1ec9ee41a76366922565',
            "enricher_id": 'enricher-event-id',
            'abi_type': 'v1',
            'last_syned_block': "trava_eth.txt",
        },
        'aave-v2': {
            'name': 'aave-v2',
            'chain_name': 'eth',
            'decimals': 8,
            'address': '0x7d2768de32b0b80b7a3454c06bdac94a69ddc7a9',
            'abi': LENDING_POOL_AAVE_V2_ABI,
            'event_abi': AAVE_LENDING_EVENT_ABI,
            'oracle_abi': TRAVA_ORACLE_ABI,
            'db_prefix': 'ethereum',
            'chain_id': "0x1",
            'oracle_address': '0xA50ba011c48153De246E5192C8f9258A2ba79Ca9',
            "enricher_id": "enricher-event-id",
            'abi_type': 'v2',
            'last_syned_block': "aave_v2.txt",
        },
        'valas-bsc': {
            'name': 'valas-bsc',
            'chain_name': 'bsc',
            'decimals': 18,
            'address': '0xe29a55a6aeff5c8b1beede5bcf2f0cb3af8f91f5',
            'abi': LENDING_POOL_AAVE_V2_ABI,
            'event_abi': AAVE_LENDING_EVENT_ABI,
            'oracle_abi': TRAVA_ORACLE_ABI,
            'db_prefix': '',
            'chain_id': "0x38",
            'oracle_address': '0x3436c4B4A27B793539844090e271591cbCb0303c',
            "enricher_id": "enricher-default-id",
            'abi_type': 'v2',
            'last_syned_block': "valas_bsc.txt",
        }
    }
    all_pool = [trava_eth, trava_bsc, trava_ftm, aave_v2, geist]
    ftm_pool = [trava_ftm, geist]
    bsc_pool = [trava_bsc]
    eth_pool = [trava_eth]
    token_type = ['reserve', 'debtAsset', 'collateralAsset']
    event_type = ['DEPOSIT', 'WITHDRAW']
