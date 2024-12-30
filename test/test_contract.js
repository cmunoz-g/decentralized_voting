/**
 * Las pruebas en blockchain son clave porque los contratos inteligentes, una vez desplegados,
 * no se pueden cambiar. Un error puede salir caro, ya sea por pérdida de fondos o porque algo
 * no funciona como debería. Truffle nos ayuda a evitar esto, permitiendo probar los contratos
 * en una red local (como Ganache) antes de lanzarlos "al mundo real".
 * 
 * En este archivo probamos las funciones principales del contrato VotingSystem, como añadir
 * propuestas, votar y cerrar propuestas, para asegurarnos de que todo funciona como se espera.
 */

const { Contract } = require("web3")

// Testeo del setup y deployment
const VotingSystem = artifacts.require("VotingSystem")

contract("VotingSystem", (accounts => { // Accounts es un array de direcciones Eth que Ganache proporciona
	// Con beforeEach nos aseguramos de que cada test comienza con una nueva instancia de VotingSystem
	beforeEach(async () => {
		// instance representa un contrato VotingSystem
		instance = await VotingSystem.new({ from: accounts[0] });
	});

	it("should set the correct owner of the VotingSystem instance", async() => {
		const owner = await instance.owner(); // Llamamos al getter de owner 
		assert.equal(owner, accounts[0], "Directions should match");
	})
}))