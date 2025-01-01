#!/bin/bash

rm -rf ganache-data
npx ganache --deterministic --db ganache-data --chain.networkId 1337 --account_keys_path keys.json &
sleep 5

npx truffle migrate --network development

ADDRESS=$(jq -r '.addresses | keys[0]' keys.json)
PRIVATE_KEY=$(jq -r ".private_keys[\"$ADDRESS\"]" keys.json)
CONTRACT_ADDRESS=$(npx truffle networks | grep -A 1 "VotingSystem" | grep "0x" | awk '{print $2}')

ABI_PATH="/app/build/contracts/VotingSystem.json"
ABI_NEWPATH="/app/cli/abi.json"
jq '.abi' $ABI_PATH > $ABI_NEWPATH

echo "PRIVATE_KEY=$PRIVATE_KEY"
echo "CONTRACT_ADDRESS=$CONTRACT_ADDRESS"

cat <<EOT > /app/cli/.env
RPC_URL=http://127.0.0.1:8545
PRIVATE_KEY=$PRIVATE_KEY
CONTRACT_ADDRESS=$CONTRACT_ADDRESS
EOT

npm install web3
npx truffle test
python ./cli/main.py

