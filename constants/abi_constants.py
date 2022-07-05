from artifacts.abi.bep20_abi import BEP20_ABI
from artifacts.abi.lending.lending_pool_abi import LENDING_POOL_ABI
from artifacts.abi.lending.lending_pool_aave_v2_abi import LENDING_POOL_AAVE_V2_ABI
from artifacts.abi.erc20_abi import ERC20_ABI
from artifacts.abi.trava_oracle_abi import TRAVA_ORACLE_ABI
from artifacts.abi.lending.lending_pool_geist_abi import LENDING_POOL_GEIST_ABI
from artifacts.abi.lending.lending_pool_aave_v1_abi import LENDING_POOL_AAVE_V1_ABI
from artifacts.abi.lending.lp_token_events_abi import LP_TOKEN_EVENT_ABI
from artifacts.abi.vault.nft_vault_events import NFT_VAULT_EVENT_ABI
from artifacts.abi.vault.vault_events import VAULT_EVENT_ABI
from artifacts.abi.cross_chain_abi.multi_sig_wallet_event_abi import MULTI_SIG_WALLET_EVENT_ABI



class ABI:
    mapping = {
        "bep20_abi": BEP20_ABI,
        "trava_lending_abi": LENDING_POOL_ABI,
        "aave_v1_abi": LENDING_POOL_AAVE_V1_ABI,
        "aave_v2_abi": LENDING_POOL_AAVE_V2_ABI,
        "erc20_abi": ERC20_ABI,
        "oracle_abi": TRAVA_ORACLE_ABI,
        "geist_abi": LENDING_POOL_GEIST_ABI,
        "lp_token_event_abi": LP_TOKEN_EVENT_ABI,
        "vault_event_abi": VAULT_EVENT_ABI,
        "nft_vault_event_abi": NFT_VAULT_EVENT_ABI,
        "multi_sig_event_abi": MULTI_SIG_WALLET_EVENT_ABI
    }
