start_block=$1
end_block=$2
lending=$3
provider_archive_node=$4
abi=$5
importer=$6
exporter=$7
last_synced_block=$8
enricher_id=$9
timestamp=${10}
chain_id=${11}
oracle_address=${12}
db_prefix=${13}

lower_lending="${lending,,}"

echo start update from $start_block to $end_block

echo start update enricher
cd ../Enricher
source venv/bin/activate
if [ "$db_prefix" == "" ]
then
  python3 main.py stream_lending_enricher --lending-abi $abi -p $provider_archive_node -i $importer -o $importer -ca $lending -b 1000 -B 5000 --collector-id "lending_events" -s $start_block -e $end_block -l $last_synced_block
else
  python3 main.py stream_lending_enricher --lending-abi $abi -p $provider_archive_node -i $importer -o $importer -ca $lending -b 1000 -B 5000 --collector-id "lending_events" -s $start_block -e $end_block -l $last_synced_block --db-prefix $db_prefix
fi
rm $last_synced_block

echo update enricher done!

echo start update graploader
cd ../GraphLoader
source venv/bin/activate
if [ "$db_prefix" == "" ]
then
  python3 ekg.py stream -i $importer -o $exporter -b 20 -B 100 -w 1 --enrich-id $enricher_id --streaming-types "lending" -t $lower_lending -l $last_synced_block -s $start_block -e $end_block
else
  python3 ekg.py stream -i $importer -o $exporter -b 20 -B 100 -w 1 --enrich-id $enricher_id --streaming-types "lending" -t $lower_lending -l $last_synced_block -s $start_block -e $end_block --db-prefix $db_prefix
fi
rm $last_synced_block

echo update graphloader done!

echo start update stategraphloader

cd ../StateGraphLoader
source .venv/bin/activate
python3 run.py lending_data -p $provider_archive_node -m $importer -g $exporter -l $lower_lending -o $oracle_address -c $chain_id -t $timestamp -r 3600 --abi $abi
echo update stategraphloader done!