# RealTime-map API

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?style=flat&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=flat&logo=postgresql)

---

## Table of Contents

- [1. About The Project](#1-about-the-project)
- [2. Tech Stack](#2-tech-stack)
- [3. Features](#3-features)
- [4. Getting Started with Docker](#4-getting-started-with-docker)
    - [Prerequisites](#prerequisites)
    - [Setup and Configuration](#setup-and-configuration)
    - [Running the Application](#running-the-application)

---

## 1. About The Project (Для чего сделан)

*[This is where you should write a detailed description of your project. Explain the problem it solves, its purpose, the target audience, and your motivation for creating it. For example: "The RealTime-map API serves as the central hub for a live location tracking system..."]*

---

## 2. Tech Stack (Стэк)

This project is built with a modern, high-performance Python stack, ensuring scalability and reliability.

* **Language:** [Python 3.13](https://www.python.org/)
* **API Framework:** [FastAPI](https://fastapi.tiangolo.com/) for high-performance, asynchronous API development.
* **Database:** [PostgreSQL](https://www.postgresql.org/) for robust data storage.
* **Geospatial Extension:** [PostGIS](https://postgis.net/) for efficient location-based queries.
* **In-Memory Store:** [Redis](https://redis.io/) for caching and message brokering.
* **Background Tasks:** [Celery](https://docs.celeryq.dev/) for handling asynchronous, long-running tasks.
* **Real-time Communication:** [Socket.IO](https://socket.io/) for broadcasting live updates to clients.
* **Data Validation:** [Pydantic](https://docs.pydantic.dev/) is used extensively for data validation, serialization,
  and settings management.
* **Package Management:** [uv](https://github.com/astral-sh/uv) for extremely fast dependency installation and
  management.

---

## 3. Features (Особенности)

* 🚀 **Asynchronous from the Ground Up:** Built on FastAPI (which uses Starlette and Uvicorn), the API is fully
  asynchronous, making it highly efficient and capable of handling many concurrent connections.
* ✅ **Modern & Type-Safe Code:** The entire codebase is strictly type-hinted using Python's `typing` module and enforced
  by **Pydantic**. This leads to robust, self-documenting code with fewer bugs and excellent editor support.
* ⚡ **Fast Development Cycle:** Utilizes `uv`, a next-generation Python package manager, for lightning-fast dependency
  installation within the Docker build process.
* 🌍 **Geospatial Capabilities:** Leverages the power of PostGIS to perform complex and efficient geographical queries.
* ⚙️ **Background Task Processing:** Offloads heavy or long-running operations to Celery workers, ensuring the API
  remains responsive.
* 📡 **Real-time Broadcasting:** Uses Socket.IO to push data (like location updates) to connected clients instantly.
* 📚 **Automatic Interactive Docs:** FastAPI automatically generates interactive API documentation (via Swagger UI and
  ReDoc), which is always up-to-date with the code.

---

## 4. Getting Started with Docker (Как запустить)

The easiest way to get the project running locally is by using Docker and Docker Compose. This will set up the API
server, database, Redis instance, and Celery worker.

### Prerequisites

* [Docker](https://www.docker.com/get-started)
* [Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker Desktop)
* [Git](https://git-scm.com/)

### Setup and Configuration

1. **Clone the repository**
   ```sh
   git clone https://github.com/your_username/RealTime-map.git
   cd RealTime-map
   ```

2. **Create your environment configuration file**
   In the root directory of the project, copy the example environment file. This file contains all the necessary
   configuration variables for the application services.
   ```sh
   cp .env.example .env
   ```

3. **Configure your environment**
   Open the newly created `.env` file with a text editor. You will need to adjust the hostnames for the database and
   Redis to match the service names defined in your `docker-compose.yml` file.

   > **Important:** When running inside Docker Compose, services communicate using their service names, not `localhost`.
   For example, if your PostgreSQL service is named `db` in `docker-compose.yml`, the host in the connection URL should
   be `db`.

   Here is an example configuration assuming your services are named `db` and `redis`:

   ```env
   # .env

   # DATABASE (Connect to the 'db' service in Docker)
   APP_CONFIG__DB__URL=postgresql+asyncpg://postgres:admin@db:5432/Postgres
   APP_CONFIG__DB__ECHO=0
   APP_CONFIG__DB__ECHO_POOL=0
   APP_CONFIG__DB__MAX_OVERFLOW=10
   APP_CONFIG__DB__POOL_SIZE=10

   # SERVER
   APP_CONFIG__SERVER__HOST=0.0.0.0
   APP_CONFIG__SERVER__PORT=8001
   APP_CONFIG__SERVER__TIMEOUT=900
   APP_CONFIG__SERVER__WORKERS=4
   APP_CONFIG__SERVER__DOMAINS=*

   # REDIS (Connect to the 'redis' service in Docker)
   APP_CONFIG__REDIS__URL=redis://redis
   APP_CONFIG__REDIS__PREFIX=cache_prefix

   # CELERY (Uses the 'redis' service as broker and backend)
   APP_CONFIG__CELERY__BROKER=redis://redis
   APP_CONFIG__CELERY__BACKEND=redis://redis

   # SOCKET
   APP_CONFIG__SOCKET__USERNAME=admin
   APP_CONFIG__SOCKET__PASSWORD=admin

   # PAYMENT
   APP_CONFIG__PAYMENT__SECRET_KEY=secret_key
   APP_CONFIG__PAYMENT__SHOP_ID=shop_id
   ```

### Running the Application

Once your `.env` file is configured, you can start all the services with a single command from the project's root
directory:

```sh
docker-compose up -d --build
```

* --build: Rebuilds the images if the Dockerfile or source code has changed.

* -d: Runs the containers in detached mode (in the background).

The API will be running and accessible at http://localhost:8001.

To view the automatically generated interactive documentation, navigate to:

Swagger UI: http://localhost:8001/docs

ReDoc: http://localhost:8001/redoc