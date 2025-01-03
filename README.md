# 🗳️ Sistema de Votación Descentralizado 🗳️

## 1. Definición del proyecto

Este proyecto implementa un **sistema de votación descentralizado** que permite:

- Crear propuestas para ser votadas.
- Registrar votos de forma segura y anónima.
- Consultar los resultados de las votaciones.

### Stack utilizado:

- **Docker**: Para el despliegue del proyecto.
- **Ethereum y Solidity**: Para el desarrollo del contrato inteligente.
- **Python (web3.py)**: Para la interfaz de línea de comandos.
- **JavaScript**: Para los tests unitarios del contrato.
- **Truffle y Ganache**: Para la configuración y pruebas de la blockchain local.

## 2. Estructura y configuración

### Estructura del proyecto

El proyecto está estructurado de la siguiente forma:

- **cli/**: Contiene el cliente de línea de comandos (CLI):
  - **config.py**: Configura la conexión a la blockchain.
  - **main.py**: Archivo principal para ejecutar el CLI.
  - **utils.py**: Funciones auxiliares para las operaciones del CLI.

- **contracts/**: Contiene el contrato Voting.sol, que implementa el sistema de votación.

- **docker/**: Contiene los archivos relacionados con la configuración de Docker.

- **migrations/**: Scripts para desplegar contratos.

- **test/**: Contiene las pruebas automatizadas para los contratos.

- **truffle-config.js**: Archivo de configuración para Truffle.

- **Makefile**: Proporciona comandos para facilitar tareas comunes como construcción, migración y pruebas.

### Configuración de Docker

#### Dockerfile

- Usamos **python:3.9-slim** como imagen base.
- Copiamos los archivos del proyecto al contenedor.
- Instalamos las dependencias necesarias de Python y Node.js.
- El contenedor no comienza directamente el proceso, sino que instala todas las dependencias.
- `start.sh` es llamado posteriormente con `make migrate` para configurar y lanzar el proyecto.

#### Compose

Declaramos dos servicios:

- **Ganache**:

  - Crea una red Ethereum local para pruebas.
  - Usa `--mnemonic` para mantener las mismas claves privadas entre reinicios.
  - `--account_keys_path /data/keys.json` guarda las claves privadas en un archivo JSON.

- **App**:

  - Construye la imagen desde el Dockerfile.
  - Volúmenes:
    - Permiten compartir archivos entre los contenedores
  - Variables de entorno:
    - Configuran el CLI para conectarse a la blockchain local.

### Desarrollo

#### Desarrollo del Smart Contract

El contrato **VotingSystem** implementa las siguientes funcionalidades:

- Crear propuestas con `addProposal`.
- Votar propuestas con `vote` (usuarios no pueden votar más de una vez por propuesta).
- Cerrar propuestas con `closeProposal` (solo el propietario puede hacerlo).
- Consultar resultados con `getProposalResults`.

#### Compilación y conexión con el CLI

- **Configuración con ****`start.sh`****:**
  Este script realiza las siguientes tareas:

  1. Inicia Ganache con parámetros como `--deterministic` y `--account_keys_path`.
  2. Realiza las migraciones con Truffle y despliega el contrato.
  3. Extrae las claves privadas y direcciones del contrato desde Ganache y Truffle, generando un archivo `.env` para el CLI.
  4. Copia el ABI necesario al directorio del CLI.

- **Conexión con ****`config.py`****:**
  Este archivo:

  1. Carga las variables de entorno desde `.env`.
  2. Se conecta a Ganache a través de RPC.
  3. Crea un objeto `VotingSystem` en base al ABI.
  4. Configura una cuenta Ethereum para firmar transacciones.

#### CLI

El CLI permite a los usuarios:

1. **Crear propuestas:** Permite registrar propuestas nuevas con nombre y fecha límite para votar.
2. **Votar en propuestas:** Los usuarios pueden votar a favor o en contra de las propuestas activas.
3. **Cerrar propuestas:** Solo el propietario puede cerrar propuestas manualmente.
4. **Consultar resultados:** Muestra el estado actual y los resultados de las propuestas cerradas o activas.
5. **Cerrar automáticamente propuestas expiradas:** Se realiza al inicio del CLI y mediante una función llamada `update_close_status`.

## 3. Tests

Las pruebas son fundamentales para garantizar la correcta ejecución del contrato inteligente, dado que los errores en blockchain son irreversibles.

### Pruebas con Truffle

Truffle permite realizar pruebas automatizadas sobre la blockchain local (Ganache). Se cubren los siguientes casos:

1. Verificar que solo el propietario pueda agregar propuestas.
2. Comprobar que se rechacen propuestas con entradas inválidas.
3. Verificar que las votaciones se registren correctamente y de forma anónima.
4. Garantizar que las propuestas no puedan ser cerradas por usuarios no propietarios.
5. Validar los resultados retornados por `getProposalResults`.
6. Comprobar que los eventos se emitan correctamente.

Ejecución:

```bash
make test
```

## 4. Instalación y guía de uso

### Clonación e instalación del proyecto

1. Clona este repositorio:

   ```bash
   git clone https://github.com/cmunoz-g/decentralized_voting.git
   cd decentralized_voting
   ```

2. Construye los contenedores:

   ```bash
   make build
   ```

3. Configura el proyecto:

   ```bash
   make migrate
   ```

4. Ejecuta el CLI:

   ```bash
   make run
   ```

### Comandos adicionales

- **Detener los contenedores:**

  ```bash
  make stop
  ```

- **Eliminar contenedores y volúmenes:**

  ```bash
  make clean
  ```

- **Pruebas:**

  ```bash
  make test
  ```

- **Ver logs:**

  ```bash
  make logs
  ```

- **Recrear todo:**

  ```bash
  make re
  ```