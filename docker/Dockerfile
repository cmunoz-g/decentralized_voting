FROM python:3.9-slim

WORKDIR /app

# Copiamos los archivos necesarios del proyecto Truffle
COPY cli/ ./cli/
COPY requirements.txt .
COPY truffle-config.js .
COPY docker/start.sh .
COPY contracts ./contracts
COPY migrations ./migrations
COPY test/ ./test/

# Instalamos dependencias
RUN apt-get update && apt-get install -y nodejs npm jq \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && npm install -g truffle ganache \
    && npm install -g web3 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN chmod +x start.sh
