/**
 * Las pruebas en blockchain son clave porque los contratos inteligentes, una vez desplegados,
 * no se pueden cambiar. Un error puede salir caro, ya sea por pérdida de fondos o porque algo
 * no funciona como debería. Truffle nos ayuda a evitar esto, permitiendo probar los contratos
 * en una red local (como Ganache) antes de lanzarlos "al mundo real".
 * 
 * En este archivo probamos las funciones principales del contrato VotingSystem, como añadir
 * propuestas, votar y cerrar propuestas, para asegurarnos de que todo funciona como se espera.
 */

const { Contract, InvalidPropertiesForTransactionTypeError } = require("web3")

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
		assert.equal(owner, accounts[0], "Account addresses should match");
	})

	it("should allow the owner to add a proposal, information should be correct", async() => {
		//string memory propName, uint propDeadline
		const deadlineString = "2025-12-12"
		const deadlineObj = new Date(deadlineString)
		const unixTime = Math.floor(deadlineObj.getTime() / 1000)
		const proposalName = "Proposal 1"

		await instance.addProposal(proposalName, unixTime)
		const owner = await instance.owner();
		const proposal = await instance.proposals(0);

		assert.equal(proposalName, proposal.name, "Proposal names should match")
		assert.equal(unixTime, proposal.deadline.toNumber(), "Proposal deadlines should match")
		assert.equal(owner, proposal.proposedBy, "Account addresses should match")
		assert.equal(0, proposal.votesInFavor.toNumber(), "Votes should be initialized to 0")
		assert.equal(0, proposal.votesAgainst.toNumber(), "Votes should be initialized to 0")
		assert.equal(true, proposal.isOpen, "Proposal should be initialized as open")
	})
}))