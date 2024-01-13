# Software Engineering Lab - 9th Exp.

## Student Service:
This repository contains the implementation of a microservice, named `student`, designed for managing student data within a university system. It utilizes a Dockerized environment for easy deployment and scalability. The microservice is part of a larger system that includes a server and an Nginx reverse proxy for handling requests.

## Project Structure

```
.
├── docker-compose.yml
├── src
│   ├── microservice
│   │   ├── application
│   │   ├── config
│   │   ├── data_access
│   │   ├── domain
│   │   ├── Dockerfile
│   │   ├── app.py
│   │   └── requirements.txt
│   ├── nginx
│   │   ├── Dockerfile
│   │   └── nginx.conf
│   └── server
│       ├── app.py
│       ├── Dockerfile
│       └── requirements.txt
└── README.md
```
## Microservice
The student microservice offers the following functionalities:

- **Add Student**: Adds a new student record with fields like name, age, and education level.
- **Modify Student**: Updates an existing student's data using the student ID.
- **Get Student**: Retrieves information for a specific student using their student ID.
- **Get All Students**: Fetches details of all students.
- **Delete Student**: Removes a student's record from the system using their student ID.

## Nginx
The Nginx service in our architecture acts as a reverse proxy, efficiently managing and routing incoming HTTP requests to the appropriate backend service. The configuration for the Nginx service is designed to ensure optimal load distribution and seamless forwarding of client requests to the `microservice`. Below is an explanation of the key components of its `Dockerfile`:

```
events {}

http {
    upstream backend {
        least_conn;
        server microservice:5000;
    }

    server {
        listen 80;
        location / {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```
Following is the algorithm used to perform load balancing:

**Least Connections (least_conn)**: This algorithm directs traffic to the backend server with the fewest active connections. It's particularly useful in scenarios where the request load is unevenly distributed and some requests take longer to process than others. When a new request comes in, Nginx evaluates all the servers in the `upstream` block and forwards the request to the one with the least number of active connections.

## Server

## Docker Configuration
Docker Compose
The docker-compose.yml file at the root of the project defines the multi-container Docker application. It specifies the configuration of the `microservice`, `nginx`, and `server` along with the `PostgreSQL` database.
Here's a brief overview of the `docker-compose.yml`:
```
version: '3'

services:
  nginx:
    build: ./src/nginx
    ports:
      - "7000:80"
    depends_on:
      - server
      - microservice

  server:
    build: ./src/server
    ports:
      - "4000:4000"
    depends_on:
      - postgres

  microservice:
    build: ./src/microservice
    scale: 3
    depends_on:
      - postgres

  postgres:
    image: postgres:latest
    ports:
      - "5432:5432"
    environment:
      POSTGRES_PASSWORD: '1qaz2wsx@'
      POSTGRES_DB: 'postgres'
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```


## Dockerfiles

- **Microservice Dockerfile**: Sets up the Python environment, installs dependencies, and defines the command to start the Flask application.
- **Nginx Dockerfile**: Uses the official Nginx image and copies the custom `nginx.conf` for routing and load balancing.
- **Server Dockerfile**: Similar to the microservice, it sets up the environment for running the server application.

## Running the Application

To run the application, use Docker Compose:

```docker-compose up --scale microservice=3```

his command builds the Docker images for each service and starts the containers as defined in docker-compose.yml. Note that the `scale` argument can be dynamically set in each run.
 
## API Endpoints
The server exposes several endpoints that interact with the microservice, which in turn manages student data:

- `POST /student`: Adds a new student.
- `PUT /student`: Modifies an existing student.
- `GET /student`: Retrieves a student's information.
- `DELETE /student`: Deletes a student record.
- `GET /students`: Retrieves information for all students.
