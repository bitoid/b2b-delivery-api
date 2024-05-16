# b2b-delivery-api - deliverow

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installing

1. **Clone the Repository**

```bash
git clone https://github.com/bitoid/b2b-delivery-api/
cd b2b-delivery-api
```
2. **Environment Configuration**

- Copy the `.env.example` file to a new file named `.env` and edit it to include your specific configurations:

```bash
cp .env.example .env
```
- You also have to copy `.env.db.example` to a new file named `.env.db` and edit it to include your specific configurations:
```bash
cp .env.db.example .env.db
```

3. **Build and Run the Docker Containers**
```bash
docker-compose up --build
```

4. Accessing the Application
Once the containers are up and running, you can access the web application by navigating to `http://localhost:1337` in your web browser (adjust the port according to your configuration).
