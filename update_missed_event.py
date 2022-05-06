from configs.config import *


def run(params):
    str = f"""bash update_missed_event.sh """
    str += params["start_block"]+" "
    str += params["end_block"]+" "
    str += params["address"]+" "
    str += params["provider"]+" "
    str += params["abi"]+" "
    str += params["mongo_db"]+" "
    str += params["arrango_db"]+" "
    str += params['last_synced_block']+" "
    str += params["enricher_id"]+" "
    str += params["timestamp"]+" "
    str += params["chain_id"]+" "
    str += params["oracle_address"]+" "
    str += params["db_prefix"]
    # print(str)
    # str += "15041790 15051890 0x75DE5f7c91a89C16714017c7443eca20C7a8c295 https://nd-384-319-366.p2pify.com/7e49b20f53222da5f0b4517cd1da43ef v1 "
    # str += "mongodb://localhost:27017/ arangodb@root:20011999@http://localhost:8529 last_synced_block.txt enricher-default-id 1644219999 0x38 0x7cd53b71bf56cc6c9c9b43719fe98e7c360c35df"

    os.system(str)
