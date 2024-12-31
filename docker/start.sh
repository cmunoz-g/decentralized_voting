#!/bin/bash

rm -rf ganache-data
npx ganache --deterministic --db ganache-data --chain.networkId 1337 --account_keys_path keys.json &
sleep 5

npx truffle migrate --network development

PRIVATE_KEY=$(jq -r '.addresses | to_entries[0].value.privateKey' keys.json)
CONTRACT_ADDRESS=$(npx truffle networks | grep -A 1 "VotingSystem" | grep "0x" | awk '{print $2}')

ABI_PATH="/app/build/contracts/VotingSystem.json"
ABI_NEWPATH="/app/cli/abi.json"
jq '.abi' $ABI_PATH > $ABI_NEWPATH

cat <<EOT > /app/cli/.env
RPC_URL=http://127.0.0.1:8545
PRIVATE_KEY=$PRIVATE_KEY
CONTRACT_ADDRESS=$CONTRACT_ADDRESS
EOT

npx truffle test
python ./cli/main.py

