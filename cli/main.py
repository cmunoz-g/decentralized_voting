import config
import os
from utils import *
from web3 import Web3
from datetime import datetime

def display_title():
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
	print(thank_you_art)
	

if __name__ == "__main__":
	main()
