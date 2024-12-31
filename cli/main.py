import config
import os
from utils import *
from web3 import Web3
from datetime import datetime

def display_title():
	os.system("clear")
	print(ascii_art)
	input()
	os.system("clear")

def main():
	display_title()
	while (True):
		print(menu)
		update_close_status()
		option = int(input("Enter your option: "))
		if option == 1:
			add_proposal()
		elif option == 2:
			vote_on_proposal()
		elif option == 3:
			close_proposal()
		elif option == 4:
			view_proposal_results()
		elif option == 5:
			break
		else:
			print("Select a correct option")
	print(thank_you_art)
	

if __name__ == "__main__":
	main()
