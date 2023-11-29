# Projet Quokka

## Installation

### Prérequis

- [Python 3.9](https://www.python.org/downloads/)
- [Docker](https://docs.docker.com/get-docker/)

### Preparation

- Clone the project

```bash
git clone https://github.com/vsantele/projet-Quokka
```

- Launch QDrant

```bash
docker compose up qdrant -d
```

- Go to `app/server`

```bash
cd app/server
```

- Create vectors for QDrant

```bash
python -m app.scripts.create_vectors
```

- Import vectors

```bash
python -m app.scripts.import_vectors
```

- Create SVD model

```bash
python -m app.scripts.init_collaborative
```

- Build the project

```bash
docker build -t quokka-server:latest .
```

## Start server

- Make sure you are in the root folder
- Launch docker compose

```bash
docker compose up -d
```
