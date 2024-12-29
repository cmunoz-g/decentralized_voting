from config import voting_system, web3, account, contract_address
from web3 import Web3
from datetime import datetime
import os
import sys

# Añadir un Proposal nuevo
def add_proposal():
	os.system("clear")
	name = input("Enter the proposal name: ")
	deadline_str = input("Enter the proposal deadline (YYYY-MM-DD): ")
	try:
		deadline = int(datetime.strptime(deadline_str, "%Y-%m-%d").timestamp())
		nonce = web3.eth.get_transaction_count(account.address)
		gas_price = web3.eth.gas_price # obtenemos un valor para el precio del gas en base a las condiciones de la red (en este caso es el default de Ganache)
		transaction = voting_system.functions.addProposal(name, deadline).build_transaction({
			'from': account.address,
			'nonce': nonce,
			'gas': 300000,
			'gasPrice': gas_price 
		})
		signed_transaction = web3.eth.account.sign_transaction(transaction, account.key) # Firmamos la transacción con la private key de la cuenta
		tx_hash = web3.eth.send_raw_transaction(signed_transaction.raw_transaction)
		receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
		if receipt.status == 1:
			print(f"Proposal added successfully | Transaction hash: {tx_hash.hex()}")
		else:
			print(f"Error: Transaction failed | Transaction hash: {tx_hash.hex()}", file=sys.stderr) 
	except Exception as e:
		print(f"Error: {e}", file=sys.stderr)
	print("\nPress any key to continue")
	input()
	os.system("clear")

# Adornos
ascii_art = r"""
 __      __   _   _                _____           _                 
 \ \    / /  | | (_)              / ____|         | |                
  \ \  / /__ | |_ _ _ __   __ _  | (___  _   _ ___| |_ ___ _ __ ___  
   \ \/ / _ \| __| | '_ \ / _` |  \___ \| | | / __| __/ _ \ '_ ` _ \ 
    \  / (_) | |_| | | | | (_| |  ____) | |_| \__ \ ||  __/ | | | | |
     \/ \___/ \__|_|_| |_|\__, | |_____/ \__, |___/\__\___|_| |_| |_|
                           __/ |          __/ |                      
                          |___/          |___/                       

		Welcome! Press any key to enter
"""
menu = """=== Voting System CLI ===
1. 📝 Add Proposal
2. 🗳️ Vote on Proposal
3. 🚪 Close Proposal
4. 📊 View Proposal Results
5. ❌ Exit
	"""
thank_you_art = r"""
 _____ _                 _                        _ 
|_   _| |               | |                      | |
  | | | |__   __ _ _ __ | | __  _   _  ___  _   _| |
  | | | '_ \ / _` | '_ \| |/ / | | | |/ _ \| | | | |
  | | | | | | (_| | | | |   <  | |_| | (_) | |_| |_|
  \_/ |_| |_|\__,_|_| |_|_|\_\  \__, |\___/ \__,_(_)
                                 __/ |              
                                |___/               
"""

