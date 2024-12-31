// SPDX-License-Identifier: Unlicense
pragma solidity	^0.8.0;

contract VotingSystem {
	struct Proposal {
		string	name;
		address	proposedBy;
		uint	votesInFavor;
		uint	votesAgainst;
		bool	isOpen;
		uint	deadline;	
	}

	// State variables
	address public immutable owner;
	uint public proposalId; // Inicializado a 0 por defecto
	mapping(uint => Proposal) public proposals;
	mapping(bytes32 => bool) private proposalExists; // Usamos un mapping para comprobar si una Proposal tiene un nombre repetido (complejidad O(1))
	mapping(uint => mapping(address => bool)) public hasVoted; // uint representa la proposalId, utilizamos el mapping para comprobar que una dirección no vota dos veces en la misma Proposal. Inicializado a false por defecto
	uint constant MAX_NAME_LENGTH = 64; // Límite para evitar usar demasiado 'gas'

	// Modifiers

	modifier onlyOwner() {
		require(msg.sender == owner, "Error: Caller is not the owner");
		_; 
	}

	// Events
	event ProposalAdded(uint indexed proposalId, string propName, address indexed proposedBy); // Indexeamos los valores Id y proposedBy para filtrar de manera mas eficiente off-chain
	event ProposalClosed(uint indexed proposalId, string propName, uint votesInFavor, uint votesAgainst, uint closedAt); 
	event VotedCasted(uint indexed proposalId);	// Registramos cada voto como un evento, para facilitar la auditoría
	// Constructor

	constructor() {
		owner = msg.sender; // Constructor se llama una única vez, cuando el contrato se despliega en la blockchain
	}

	// Member functions

	function addProposal(string memory propName, uint propDeadline) public onlyOwner {
		require(bytes(propName).length != 0, "Error: Cannot add: Proposal name must not be empty");
		require(bytes(propName).length < MAX_NAME_LENGTH, "Error: Cannot add: Proposal name exceeds 64 characters");
		require(propDeadline > block.timestamp, "Error: Cannot add: Deadline is already expired");

		bytes32 hashedName = keccak256(abi.encodePacked(propName)); 
		// Encodear la string propName con keccak256 hace que no tengamos que controlar mayúsculas/minúsculas y reduce los gastos de almacenamiento. 
		// También aumenta la privacidad, aunque no es relevante en este caso

		require(!proposalExists[hashedName], "Error: Cannot add: Proposal with this name already exists");
		proposals[proposalId] = Proposal(propName, msg.sender, 0, 0, true, propDeadline);
		proposalExists[hashedName] = true;
		emit ProposalAdded(proposalId, propName, msg.sender);
		proposalId++;
	}

	// Se hace la comprobación de deadline en python (off-chain) para ahorrar recursos
	function closeProposal(uint propToCloseId) public onlyOwner {
		require(propToCloseId < proposalId, "Error: Cannot close: Proposal does not exist");
		Proposal storage proposal = proposals[propToCloseId];
		require(proposal.isOpen == true, "Error: Cannot close: Proposal is already marked as closed");
		proposal.isOpen = false;
		emit ProposalClosed(propToCloseId, proposal.name, proposal.votesInFavor, proposal.votesAgainst, block.timestamp);
	}

	function vote(uint propToVoteId, bool inFavor) public {
		require(propToVoteId < proposalId, "Error: Cannot vote: Proposal does not exist");
		Proposal storage proposal = proposals[propToVoteId];	// La keyword storage indica que se trata de una referencia a una state variable del contrato. Similar a memory, pero nos permite modificar la variable.
		
		require(!hasVoted[propToVoteId][msg.sender], "Error: Cannot vote: You have already voted on this proposal");
		require(proposal.isOpen == true, "Error: Cannot vote: Voting for the proposal is closed"); 
		if (inFavor)
			proposal.votesInFavor++;
		else
			proposal.votesAgainst++;
		hasVoted[propToVoteId][msg.sender] = true;
		// Únicamente emitimos como evento si ha habido un voto (no de quién, o qué ha votado), para preservar el anonimato.
		// Esta necesidad de anonimato presenta oportunidades para incorporar técnicas criptográficas como las Zero-Knowledge Proofs (ZKPs), que permiten a cada individuo demostrar de manera segura que ha emitido su voto sin comprometer su identidad.
		emit VotedCasted(propToVoteId);
	}

	function getProposalResults(uint propToGetId) public view returns (uint, uint, bool) {
		require(propToGetId < proposalId, "Error: Cannot get proposal results: Proposal does not exist");
		Proposal storage proposal = proposals[propToGetId];
		return (proposal.votesInFavor, proposal.votesAgainst, proposal.isOpen);
	}
}


