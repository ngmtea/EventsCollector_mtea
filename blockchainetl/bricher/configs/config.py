import os


class MongoDBConfig:
    MONGODB_LOCAL_HOST = os.environ.get("MONGODB_LOCAL_HOST") or "localhost"
    MONGODB_LOCAL_PORT = os.environ.get("MONGODB_PORT") or "27017"
    USERNAME = os.environ.get("MONGODB_USERNAME") or "admin"
    PASSWORD = os.environ.get("MONGODB_PASSWORD") or "dev123"
    HOST = os.environ.get("MONGODB_HOST") or "0.0.0.0"
    PORT = os.environ.get("MONGODB_PORT") or "27017"
    LOCAL_CONNECTION_URL = f"mongodb://{MONGODB_LOCAL_HOST}:{MONGODB_LOCAL_PORT}"
    CONNECTION_URL = f"mongodb://{USERNAME}:{PASSWORD}@{HOST}:{PORT}"

    BRICHER_DATABASE = "BRicher"
    DAPPS_COLLECTION = "dapps"

    LOCAL_BRICHER_DAPPS_DATABASE = "bricher_dapps"
    LOCAL_CREAM_VENUS_EVENTS_COLLECTION = "cream_venus_events"
    LOCAL_CREAM_EVENTS_COLLECTION = "cream_events"
    LOCAL_VENUS_EVENTS_COLLECTION = "venus_events"


class Provider:
    BSC_PUBLIC_RPC_NODE: str = "https://bsc-dataseed1.binance.org/"
    ANKR_PUBLIC_ETH_RPC_NODE: str = "https://rpc.ankr.com/eth"
