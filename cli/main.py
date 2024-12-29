import config
import os
from utils import *
from web3 import Web3
from datetime import datetime

# === Tests y to-do's ===

# Añadir una forma de ir para atrás durante el menú
# bugfix para cuando se introduce un no int
# bugfix para cuadno no hay proposals, deberia no ejecutar el resto del codigo
# quality of life fix: para permitir mirar los resultados de diferentes elecciones sin tener que pasar por el menu principal
# No hay una forma sencilla de obtener el mensaje de error que tira require en Voting.sol, así que ahora mismo se rechaza la transacción pero no se indica por qué
# Formatear y comentar codigo

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
