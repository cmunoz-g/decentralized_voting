import config
import os
from utils import *
from web3 import Web3
from datetime import datetime

# Tests y to-do's
# No hay una forma sencilla de obtener el mensaje de error que tira require en Voting.sol, así que ahora mismo se rechaza la transacción pero no se indica por qué

def display_title():
	os.system("clear")
	print(ascii_art)
	input()
	os.system("clear")

def main():
	display_title()
	while (True):
		print(menu)
		option = int(input("Enter your option: "))
		if option == 1:
			add_proposal()
		elif option == 2:
			print("2")
		elif option == 3:
			print("3")
		elif option == 4:
			print("4")
		elif option == 5:
			break
		else:
			print("Select a correct option")
	#print(f"prpsal id {config.voting_system.functions.proposalId().call()}")
	print(thank_you_art)
	

if __name__ == "__main__":
	main()
