from artifacts.abi.lending_pool_abi import LENDING_POOL_ABI
from artifacts.abi.lending_pool_aave_v2_abi import LENDING_POOL_AAVE_V2_ABI


class PoolConstant:
    mapping = {
        'trava-bsc': {
            'name': 'trava-bsc',
            'chain_name': 'bsc',
            'decimals': 8,
            'address': '0x75de5f7c91a89c16714017c7443eca20c7a8c295',
            'abi': LENDING_POOL_ABI,
            'db_prefix': '',
            'chain_id': "0x38",
            'oracle_address': '0x7cd53b71bf56cc6c9c9b43719fe98e7c360c35df',
            "enricher_id": 'enricher-default-id',
            'abi_type': 'v1',
        },
        'geist': {
            'name': 'geist',
            'chain_name': 'ftm',
            'decimals': 18,
            'address': '0x9fad24f572045c7869117160a571b2e50b10d068',
            'abi': LENDING_POOL_AAVE_V2_ABI,
            'db_prefix': 'ftm',
            'chain_id': "0xfa",
            'oracle_address': '0xC466e3FeE82C6bdc2E17f2eaF2c6F1E91AD10FD3',
            "enricher_id": 'enricher-geist-event-id',
            'abi_type': 'v2',
        },
        'trava-ftm': {
            'name': 'trava_ftm',
            'chain_name': 'ftm',
            'decimals': 8,
            'address': '0xd98bb590bdfabf18c164056c185fbb6be5ee643f',
            'abi': LENDING_POOL_ABI,
            'db_prefix': 'ftm',
            'chain_id': "0xfa",
            'oracle_address': '0x290346e682d51b97e2c1f186eb61eb49881c5ec7',
            "enricher_id": 'enricher-default-id',
            'abi_type': 'v1',
        },
        'trava-eth': {
            'name': 'trava-eth',
            'chain_name': 'eth',
            'decimals': 8,
            'address': '0xd61afaaa8a69ba541bc4db9c9b40d4142b43b9a4',
            'abi': LENDING_POOL_ABI,
            'db_prefix': 'ethereum',
            'chain_id': "0x1",
            'oracle_address': '0x2bd81260fe864173b6ec1ec9ee41a76366922565',
            "enricher_id": 'enricher-default-id',
            'abi_type': 'v1',
        },
        'aave-v2': {
            'name': 'aave-v2',
            'chain_name': 'eth',
            'decimals': 8,
            'address': '0x7d2768de32b0b80b7a3454c06bdac94a69ddc7a9',
            'abi': LENDING_POOL_ABI,
            'db_prefix': 'ethereum',
            'chain_id': "0x1",
            'oracle_address': '0xA50ba011c48153De246E5192C8f9258A2ba79Ca9',
            "enricher_id": "enricher-aave-v2",
            'abi_type': 'v2',
        },
    }
    token_type = ['reserve', 'debtAsset', 'collateralAsset']
    event_type = ['DEPOSIT', 'WITHDRAW']
