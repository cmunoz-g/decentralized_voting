# Colors
DEF_COLOR 	= 	\033[0;39m
RED 		= 	\033[0;91m
GREEN 		=	\033[0;92m
BLUE 		=	\033[0;94m
CYAN 		= 	\033[0;96m

# Config
OBJF 		=	.cache_exists
MAKEFLAGS 	+=	--no-print-directory
#.SILENT:

# Docker Compose Configuration
COMPOSE_FILE = ./docker/docker-compose.yml
DOCKER_COMPOSE = docker-compose -f $(COMPOSE_FILE)

###

all: build

build:
	@$(DOCKER_COMPOSE) up -d --build
	@echo "$(GREEN)Project started successfully! Containers are up and running.$(DEF_COLOR)"

stop:
	@$(DOCKER_COMPOSE) stop
	@echo "$(BLUE)Containers stopped.$(DEF_COLOR)"

clean: 
	@$(DOCKER_COMPOSE) down -v --remove-orphans
	@echo "$(CYAN)Containers and volumes removed.$(DEF_COLOR)"

delete: clean
	@docker system prune -af --volumes
	@echo "$(RED)All unused Docker resources have been pruned.$(DEF_COLOR)"

logs:
	@$(DOCKER_COMPOSE) logs -f
	@echo "$(YELLOW)Showing logs for all services...$(DEF_COLOR)"

ps:
	@$(DOCKER_COMPOSE) ps
	@echo "$(MAGENTA)Listing all running containers for the project.$(DEF_COLOR)"

re: clean all
	@echo "$(GREEN)Project restarted successfully!$(DEF_COLOR)"

trufflecompile: 
	@npx truffle compile --all
	@echo "$(BLUE)Recompiled Voting.sol contract.$(DEF_COLOR)"

trufflemigrate:
	@npx truffle migrate --network development
	@echo "$(BLUE)Deployed Voting.sol contract in the blockchain.$(DEF_COLOR)"

run:
	@python cli/main.py

.PHONY: all build stop clean delete logs ps re trufflemigrate trufflecompile run