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

// Variables deadline y name para diferentes tests
const deadlineString = "2025-12-12"
const deadlineObj = new Date(deadlineString)
const unixTime = Math.floor(deadlineObj.getTime() / 1000)
const proposalName = "Proposal 1"

contract("VotingSystem", (accounts => { // Accounts es un array de direcciones Eth que Ganache proporciona
	// Con beforeEach nos aseguramos de que cada test comienza con una nueva instancia de VotingSystem
	beforeEach(async () => {
		// instance representa un contrato VotingSystem
		instance = await VotingSystem.new({ from: accounts[0] });
	});

	// Testeamos que el owner se setee de forma correcta
	it("should set the correct owner of the VotingSystem instance", async() => {
		const owner = await instance.owner(); // Llamamos al getter de owner 
		assert.equal(owner, accounts[0], "Account addresses should match");
	})

	// Testeamos que addProposal() funcione correctamente
	it("should allow the owner to add a proposal, information should be correct", async() => {
		//string memory propName, uint propDeadline
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

	// Testeamos que addProposal() rechace inputs incorrectos
	it("should not allow adding a proposal with wrong inputs", async() => {
		const wrongDeadlineString = "2024-12-12"
		const wrongDeadlineObj = new Date(wrongDeadlineString)
		const wrongUnixTime = Math.floor(wrongDeadlineObj.getTime() / 1000)
		
		try {
			await instance.addProposal(proposalName, wrongUnixTime)
			assert.fail("The transaction should have reverted")
		}
		catch (err) {
			assert.include(err.message, "Error: Cannot add: Deadline is already expired", "Expected revert with reason")
		}

		try {
			await instance.addProposal("", unixTime)
			assert.fail("The transaction should have reverted") 
		}
		catch (err) {
			assert.include(err.message, "Error: Cannot add: Proposal name must not be empty", "Expected revert with reason")
		}

		const wrongProposalName = "ThisStringIsDefinitelyOverSixtyFourCharactersSoItShouldRevert,OfCourse"

		try {
			await instance.addProposal(wrongProposalName, unixTime)
			assert.fail("The transaction should have reverted") 
		}
		catch (err) {
			assert.include(err.message, "Error: Cannot add: Proposal name exceeds 64 characters", "Expected revert with reason")
		}
	})

	// Testeamos la función vote()
	it("a valid vote should increment the appropiate counter, and mark the address as having voted", async() => {
		await instance.addProposal(proposalName, unixTime);
		await instance.addProposal(proposalName + "Against", unixTime);
		
		// Voto a favor
		await instance.vote(0, true);
		const proposalInFavor = await instance.proposals(0);
		assert.equal(proposalInFavor.votesInFavor.toNumber(), 1, "The vote should have incremented votesInFavor by 1");
		
		// Voto en contra
		await instance.vote(1, false);
		const proposalAgainst = await instance.proposals(1);
		assert.equal(proposalAgainst.votesAgainst.toNumber(), 1, "The vote should have incremented votesAgainst by 1");

		// Comprobamos que el address se haya guardado en hasVoted para ambas Proposal
		const address = await instance.owner();
		const hasVotedFirstProposal = await instance.hasVoted(0, address);
		const hasVotedSecondProposal = await instance.hasVoted(1, address);
		assert.equal(hasVotedFirstProposal, true, "Address should have been saved as having voted");
		assert.equal(hasVotedSecondProposal, true, "Address should have been saved as having voted");
		
	})

	it("a voter should not be able to vote twice on the same proposal", async() => {
		await instance.addProposal(proposalName, unixTime);
		await instance.vote(0, true);

		try {
			await instance.vote(0, true);
			assert.fail("The same address should not be able to vote twice on the same proposal");
		}
		catch (err) {
			assert.include(err.message, "Error: Cannot vote: You have already voted on this proposal", "Expected revert with reason");
		}
	})

	it("a voter should not be able to vote on a non-existant proposal", async() => {
		try {
			await instance.vote(1, true);
			assert.fail("Should not be able to vote on a non-existant proposal");
		}
		catch (err) {
			assert.include(err.message, "Error: Cannot vote: Proposal does not exist", "Expected revert with reason")
		}
	})

	it("non-owners should be able to vote on a proposal", async() => {
		await instance.addProposal(proposalName, unixTime);
		
		// Votamos desde otra address en la proposal creada por accounts[0]
		await instance.vote(0, true, { from: accounts[1] });
		const proposal = await instance.proposals(0)
		assert.equal(proposal.votesInFavor.toNumber(), 1, "Votes in favor should increment")
		assert.equal(proposal.votesAgainst.toNumber(), 0, "Votes against should remain 0")	
	})

	// Testeamos la función closeProposal()

	it("owner should be able to close proposals, state should change appropiately", async() => {
		await instance.addProposal(proposalName, unixTime);
		await instance.closeProposal(0);

		const proposal = await instance.proposals(0);
		assert.equal(proposal.isOpen, false, "Proposal should be closed");
	})

	it("a voter should not be able to vote on a closed proposal", async() => {
		await instance.addProposal(proposalName, unixTime);
		await instance.closeProposal(0)

		try {
			await instance.vote(0, true);
			assert.fail("Should not be able to vote on a closed proposal");
		}
		catch (err) {
			assert.include(err.message, "Error: Cannot vote: Voting for the proposal is closed", "Expected revert with reason")
		}
	})

	it("a non-existant proposal should not be able to be closed", async() => {
		try {
			await instance.closeProposal(0);
			assert.fail("Should not be able to close a non-existant proposal");
		}
		catch (err) {
			assert.include(err.message, "Error: Cannot close: Proposal does not exist", "Expected revert with reason");
		}
	})

	it("an already closed proposal should not be able to be closed", async() => {
		await instance.addProposal(proposalName, unixTime);
		await instance.closeProposal(0);
		try {
			await instance.closeProposal(0);
			assert.fail("Should not be able to close an already closed proposal");
		}
		catch (err) {
			assert.include(err.message, "Error: Cannot close: Proposal is already marked as closed", "Expected revert with reason")
		}
	})
	
	it("a non owner should not be able to close a proposal", async() => {
		await instance.addProposal(proposalName, unixTime);
		try {
			await instance.closeProposal(0, { from: accounts[1]})
			assert.fail("Non-owner should not be able to close a proposal");
		}
		catch (err) {
			assert.include(err.message, "Error: Caller is not the owner", "Expected revert with reason")
		}
	})

}))