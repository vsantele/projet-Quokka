# Projet Quokka

Repository for the Quokka project.

<https://github.com/vsantele/projet-Quokka>

## Server

The server is made with [FastAPI](https://fastapi.tiangolo.com/).

### Installation

#### Requirements

- [Python 3.9](https://www.python.org/downloads/)
- [Docker](https://docs.docker.com/get-docker/)

#### Setup

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

- [Optionnal] Create a virtual environment

```bash
python -m venv venv
```

- Install dependencies

```bash
pip install -r requirements.txt
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

- [Optionnal] Build the project if you want to use docker

```bash
docker build -t quokka-server:latest .
```

### Start server

#### Docker

- Make sure you are in the root folder
- Launch docker compose if you build the quokka-server image

```bash
docker compose up -d
```

#### Python

- Make sure you are in the root folder
- Launch the database

```bash
docker compose up qdrant -d
```

- Go to `app/server`

```bash
cd app/server
```

- Launch the server

```bash
uvicorn app.main:app --reload
```

### Usage

You can find the OpenAPI documentation at `http://localhost:8000/docs`

## Client

The client is made with [Svelte](https://svelte.dev/).

### Installation

#### Requirements

- [Node.js](https://nodejs.org/en/download/)

#### Setup

- Go to `app/client`

```bash
cd app/client
```

- Install dependencies

```bash
npm install
```

### Start client

```bash
npm run dev
```

### Usage

You can find the client at `http://localhost:5173`
