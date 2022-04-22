## cài đặt môi trường 
----------------------
* python3 -m venv .venv
* source .venv/bin/activate
* pip3 install -r equirements.txt

## crawl event

* python3 ethereumetl.py stream_lending_log_collector -ca 0x75DE5f7c91a89C16714017c7443eca20C7a8c295 -oa 0x7Cd53b71Bf56Cc6C9c9B43719FE98e7c360c35DF -pf "https://bsc-dataseed.binance.org/" --max-workers 5 -a trava_lending_abi -pa "https://speedy-nodes-nyc.moralis.io/fcc133b4fbd050375c7202e9/bsc/mainnet/archive" -o "mongodb://localhost:27017/" -B 300
