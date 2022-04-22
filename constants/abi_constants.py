from artifacts.abi.bep20_abi import BEP20_ABI
from artifacts.abi.lending_pool_abi import LENDING_POOL_ABI
from artifacts.abi.lending_pool_aave_v2_abi import LENDING_POOL_AAVE_V2_ABI
from artifacts.abi.erc20_abi import ERC20_ABI
from artifacts.abi.trava_oracle_abi import TRAVA_ORACLE_ABI
from artifacts.abi.lending_pool_geist_abi import LENDING_POOL_GEIST_ABI
from artifacts.abi.lending_pool_aave_v1_abi import LENDING_POOL_AAVE_V1_ABI


class ABI:
    mapping = {
        "bep20_abi": BEP20_ABI,
        "trava_lending_abi": LENDING_POOL_ABI,
        "aave_v1_abi": LENDING_POOL_AAVE_V1_ABI,
        "aave_v2_abi": LENDING_POOL_AAVE_V2_ABI,
        "erc20_abi": ERC20_ABI,
        "oracle_abi": TRAVA_ORACLE_ABI,
        "geist_abi": LENDING_POOL_GEIST_ABI
    }
