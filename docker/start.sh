#!/bin/bash

sleep 5

npx truffle migrate --reset --network development

CONTRACT_ADDRESS=$(npx truffle networks | grep -A 1 "VotingSystem" | grep "0x" | awk '{print $2}')
PRIVATE_KEY=$(jq -r '.private_keys | to_entries | .[0].value' /ganache_shared/keys.json)

ABI_PATH="/app/build/contracts/VotingSystem.json"
ABI_NEWPATH="/app/cli/abi.json"
jq '.abi' $ABI_PATH > $ABI_NEWPATH

echo "ABI=$ABI_NEWPATH"

echo "PRIVATE_KEY=$PRIVATE_KEY"
echo "CONTRACT_ADDRESS=$CONTRACT_ADDRESS"

cat <<EOT > /app/cli/.env
RPC_URL=http://ganache:8545
PRIVATE_KEY=$PRIVATE_KEY
CONTRACT_ADDRESS=$CONTRACT_ADDRESS
EOT

npm install web3

python ./cli/config.py

echo "Configuration completed successfully"
