from web3 import Web3
from dotenv import load_dotenv
import os
import sys
import json

# Cargamos las variables de entorno .env
load_dotenv()
rpc = os.getenv("RPC_URL")
private_key = os.getenv("PRIVATE_KEY")
contract_address = os.getenv("CONTRACT_ADDRESS")

if not rpc or not private_key or not contract_address:
	raise ValueError("Error: Missing environment variables")

# Cargamos el archivo abi.json para poder crear instancias de VotingSystem
with open("abi.json", "r") as file:
	try:
		abi = json.load(file)
	except FileNotFoundError:
		print("Error: Could not find abi.json file", file=sys.stderr)
	except json.JSONDecodeError:
		print("Error: could not parse abi.json file", file=sys.stderr)
	except Exception as e:
		print(f"Error: {e}", file=sys.stderr)
	else:
		print("abi.json file was successfully parsed")
	
# Nos conectamos a Ganache a través de web3.py
web3 = Web3(Web3.HTTPProvider(rpc))
if web3.is_connected():
	print("Connection to the blockchain was successful")
else:
	print("Error: Connection to the blockchain was not successful", file=sys.stderr)

# Creamos un objeto VotingSystem
try:
	voting_system = web3.eth.contract(address=contract_address, abi=abi)
except Exception as e:
	print(f"Error: {e}", file=sys.stderr)