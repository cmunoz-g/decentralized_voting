from config import voting_system, web3, account, contract_address
from web3 import Web3
from datetime import datetime
import os
import sys

# === 1 ===
# Añadir una Proposal nueva
def add_proposal():
	os.system("clear")
	print(f"{YELLOW}=== Adding a new proposal ==={RESET}")
	name = input("Enter the proposal name: ")
	deadline_str = input("Enter the proposal deadline (YYYY-MM-DD): ")
	try:
		 # Convertimos la fecha límite a un timestamp Unix
		deadline = int(datetime.strptime(deadline_str, "%Y-%m-%d").timestamp())
		# Obtenemos el nonce actual para la cuenta emisora con el objetivo de evitar ataques de relay (ataques en los que se intenta reutilizar una transacción válida)
		nonce = web3.eth.get_transaction_count(account.address)
		# obtenemos un valor para el precio del gas en base a las condiciones de la red (en este caso es el default de Ganache)
		gas_price = web3.eth.gas_price
		transaction = voting_system.functions.addProposal(name, deadline).build_transaction({
			'from': account.address,	# Dirección de Ethereum del remitente
			'nonce': nonce,
			'gas': 300000,				# Máximo gas permitido para la transacción
			'gasPrice': gas_price		# Precio del gas en Wei
		})
		# Firmamos la transacción con la private key de la cuenta
		signed_transaction = web3.eth.account.sign_transaction(transaction, account.key)
		tx_hash = web3.eth.send_raw_transaction(signed_transaction.raw_transaction)
		# Esperamos el recibo de la transaccion para comrobar si tuvo éxito
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

# === 2 ===
def	print_proposal(prop_id, name, votes_in_favor, votes_against, formatted_deadline):
	print(
            f"{BLUE}ID: {str(prop_id):<2}{RESET} | "
            f"Name: {name:<15} | "
            f"Votes ({GREEN}For{RESET}/{RED}Against{RESET}): "
            f"{GREEN}{votes_in_favor}{RESET}/{RED}{str(votes_against):<3}{RESET} | "
            f"Deadline: {formatted_deadline}"
        )

def show_active_proposals(total_proposals):
	if total_proposals:
		print(f"{YELLOW}=== Active Proposals ==={RESET}")
		for prop_id in range(total_proposals):
			proposal = voting_system.functions.proposals(prop_id).call()
			name, proposed_by, votes_in_favor, votes_against, is_open, deadline = proposal
			if (is_open == True):
				readable_time = datetime.fromtimestamp(deadline)
				formatted_deadline = readable_time.strftime("%Y-%m-%d")
				print_proposal(prop_id, name, votes_in_favor, votes_against, formatted_deadline)
	else:
		print("There are no active proposals")
		print("\nPress any key to continue")
		input()

def get_proposal_id(msg):
	while True:
		str_id = input(msg)
		try:
			id = int(str_id)
			return id
		except ValueError:
			print("Error: Please enter an integer", file=sys.stderr)

# Votar en una Proposal
def vote_on_proposal():
	os.system("clear")
	total_proposals = voting_system.functions.proposalId().call()
	show_active_proposals(total_proposals)

	if total_proposals != 0:
		# Obtenemos los detalles de la propuesta desde el contrato inteligente
		print(f"\nEnter {total_proposals} to go back to the main menu")
		id = get_proposal_id("\nEnter the proposal ID to vote on: ")

		if id != total_proposals:
			proposal = voting_system.functions.proposals(id).call()
			name, proposed_by, votes_in_favor, votes_against, is_open, deadline = proposal

			if str(name) and is_open:
				os.system("clear")
				print(f"{YELLOW}=== Proposal to vote on ==={RESET}")
				readable_time = datetime.fromtimestamp(deadline)
				formatted_deadline = readable_time.strftime("%Y-%m-%d")
				print_proposal(id, name, votes_in_favor, votes_against, formatted_deadline)

				# Recogemos el voto del usuario
				vote = input(f"\nOptions: {GREEN}yes{RESET}/{RED}no{RESET}: ").strip().lower()
				while vote not in ["yes", "y", "no", "n"]:
					print("Not a valid option. Please type 'yes' or 'no'")
					vote = input(f"\nOptions: {GREEN}yes{RESET}/{RED}no{RESET}: ").strip().lower()
				in_favor = vote in ["yes", "y"]
				
				try:
					nonce = web3.eth.get_transaction_count(account.address)
					gas_price = web3.eth.gas_price
					transaction = voting_system.functions.vote(id, in_favor).build_transaction({
						'from': account.address,
						'nonce': nonce,
						'gas': 300000,
						'gasPrice': gas_price
					})
					signed_transaction = web3.eth.account.sign_transaction(transaction, account.key)
					tx_hash = web3.eth.send_raw_transaction(signed_transaction.raw_transaction)
					receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
					if (receipt.status == 1):
						print(f"\nYour anonimous vote was casted successfully | Transaction hash: {tx_hash.hex()}")
					else:
						print(f"\nError: Could not cast your vote | Transaction hash: {tx_hash.hex()}", file=sys.stderr)
				
				except Exception as e:
					print(f"Error: {e}", file=sys.stderr)
			
			else:
				print("Error: There is not an open proposal with that ID", file=sys.stderr)
			print("\nPress any key to continue")
			input()
		os.system("clear")

# === 3 ===
# Cerrar una Proposal
def close_proposal():
	os.system("clear")
	total_proposals = voting_system.functions.proposalId().call()
	show_active_proposals(total_proposals)

	if total_proposals != 0:
		print(f"\nEnter {total_proposals} to go back to the main menu")
		id = get_proposal_id("\nEnter the proposal ID to close: ")

		if id != total_proposals:
			proposal = voting_system.functions.proposals(id).call()
			name, proposed_by, votes_in_favor, votes_against, is_open, deadline = proposal

			if str(name):
				os.system("clear")
				try:
					nonce = web3.eth.get_transaction_count(account.address)
					gas_price = web3.eth.gas_price
					transaction = voting_system.functions.closeProposal(id).build_transaction({
						'from': account.address,
						'nonce': nonce,
						'gas': 300000,
						'gasPrice': gas_price
					})
					signed_transaction = web3.eth.account.sign_transaction(transaction, account.key)
					tx_hash = web3.eth.send_raw_transaction(signed_transaction.raw_transaction)
					receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
					if receipt.status == 1:
						print(f"The proposal {id} was closed | Transaction hash: {tx_hash.hex()}")
					else:
						print(f"The proposal {id} could not be closed | Transaction hash: {tx_hash.hex()}", file=sys.stderr)
				
				except Exception as e:
					print(f"Error: {e}", file=sys.stderr)
			
			else:
				print("Error: There is not an open proposal with that ID", file=sys.stderr)
			print("\nPress any key to continue")
			input()
		os.system("clear")

# === 4 ===
def show_all_proposals(total_proposals):
	if total_proposals:
		print(f"{YELLOW}=== Proposals ==={RESET}")
		for prop_id in range(total_proposals):
			proposal = voting_system.functions.proposals(prop_id).call()
			name, proposed_by, votes_in_favor, votes_against, is_open, deadline = proposal
			print(
            f"{BLUE}ID: {str(prop_id):<2}{RESET} | "
            f"Name: {name:<15}"
        )
	else:
		print("There are no proposals yet")
		print("\nPress any key to continue")
		input()

# Visualizar los resultados
def view_proposal_results():
	os.system("clear")
	total_proposals = voting_system.functions.proposalId().call()
	show_all_proposals(total_proposals)
	
	if total_proposals != 0:
		print(f"\nEnter {total_proposals} to go back to the main menu")
		id = get_proposal_id("\nEnter the proposal ID to show: ")
		
		if id != total_proposals:
			proposal = voting_system.functions.proposals(id).call()
			name, proposed_by, votes_in_favor, votes_against, is_open, deadline = proposal
			if str(name):
				os.system("clear")
				print(f"{YELLOW}=== Proposal Results ===\n{RESET}"
					f"{BLUE}ID: {id}{RESET}\n"
					f"Name: {name}\n"
					f"Owner: {proposed_by}\n"
					f"Votes ({GREEN}For{RESET}/{RED}Against{RESET}): "
					f"{GREEN}{votes_in_favor}{RESET}/{RED}{votes_against}{RESET}\n"
					"Open? ", end=""
				)
				
				if is_open:
					print(f"{GREEN}Yes{RESET}")
					readable_time = datetime.fromtimestamp(deadline)
					formatted_deadline = readable_time.strftime("%Y-%m-%d")
					print(f"Deadline: {formatted_deadline}")
				
				else:
					print(f"{RED}No{RESET}")
					if votes_in_favor > votes_against:
						print(f"Proposal was {GREEN}accepted{RESET}")
					elif votes_in_favor == votes_against:
						print(f"Proposal was {YELLOW}a tie{RESET}")
					else:
						print(f"Proposal was {RED}rejected{RESET}")
			
			print("\nPress any key to continue")
			input()
			view_proposal_results()
		os.system("clear")

# Cerrar las propuestas que han expirado
def update_close_status():
	total_proposals = voting_system.functions.proposalId().call()
	for prop_id in range(total_proposals):
		proposal = voting_system.functions.proposals(prop_id).call()
		deadline = proposal[5]
		current_timestamp = int(datetime.now().timestamp())
		if deadline <= current_timestamp:
			try:
				nonce = web3.eth.get_transaction_count(account.address)
				gas_price = web3.eth.gas_price
				transaction = voting_system.functions.closeProposal(prop_id).build_transaction({
					'from': account.address,
					'nonce': nonce,
					'gas': 300000,
					'gasPrice': gas_price
				})
				signed_transaction = web3.eth.account.sign_transaction(transaction, account.key)
				tx_hash = web3.eth.send_raw_transaction(signed_transaction.raw_transaction)
				receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
				if receipt.status == 1:
					print(f"The proposal {prop_id} was closed | Transaction hash: {tx_hash.hex()}")
				else:
					print(f"The proposal {prop_id} could not be closed | Transaction hash: {tx_hash.hex()}", file=sys.stderr)
				
			except Exception as e:
				print(f"Error: {e}", file=sys.stderr)


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
menu = """\033[33m=== Voting System CLI ===\033[0m
1. 📝 Add Proposal
2. 🗳️  Vote on Proposal
3. 🚪 Close Proposal
4. 📊 View Proposal Results
5. ❌ \033[31mExit\033[0m
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

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"