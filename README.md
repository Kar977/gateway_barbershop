# Content of Project
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Application view](#application-view)
* [Sources](#sources)

## General info
General information about <b>BarberShop API</b>.<br><br>
BarberShop API is a distributed backend application designed using a microservices architecture to support the full operational needs of a modern barbershop. 
The system serves three main types of users:
<ul>
<li>End customers – can browse available time slots, book appointments, manage their reservations, and view their service history.</li>
<li>Salon employees – can log in, manage and update their work schedules, and view their upcoming bookings.</li>
<li>Business owner – manages the barbershop's organization in Auth0, creates employee accounts, and oversees the overall setup and operations of the salon.</li>
</ul>
  
The application follows a polyrepo structure and is composed of five independent FastAPI microservices, each responsible for a distinct business domain. A dedicated API Gateway handles incoming client requests and routes them to the appropriate services.
This architecture ensures modularity, scalability, and clear separation of concerns, making the system easy to maintain and extend.


## Technologies
<ul>
<li>Python 3.11</li>
<li>FastAPI 0.111.0</li>
<li>PostgreSQL 15</li>
<li>Docker 24.0.7</li>
<li>AuthLib 1.3.2</li>
<li>Adminer 5.3.0</li>
<li>Portainer 2.27</li>
<li>Prometheus 3.4.0</li>
<li>Pytest 8.3.5</li>
<li>Pytest-asyncio 0.26.0</li>
<li>Pydantic 2.7.4</li>
<li>Httpx 0.27.0</li>
<li>Requests 2.32.3</li>
<li>PyJWT 2.9.0</li>
<li>uvicorn 0.30.1</li>
</ul>

## Setup

This application runs as a set of Docker containers orchestrated via Portainer on AWS. Each microservice has its own repository and Dockerfile.

To run the system locally or deploy to a server:

1. Fork all microservice repositories.
<ul>
  <li>gateway_barbershop - https://github.com/Kar977/gateway_barbershop</li>
  <li>employee_manager - https://github.com/Kar977/employee_manager</li>
  <li>users_manager - https://github.com/Kar977/users_manager</li>
  <li>customers_manager - https://github.com/Kar977/customers_manager</li>
  <li>notification_manager - https://github.com/Kar977/notification-manager</li>
</ul>

2. Set Secrets for barbershop_gateway microservice:
- AWS_ACCESS_KEY_ID
- AWS_ACCOUNT_ID
- AWS_SECRET_ACCESS_KEY
- GATEWAY_ENV_FILE which consists of multiple lines of:
  - POSTGRES_NAME
  - POSTGRES_USER
  - POSTGRES_PASSWORD
  - POSTGRES_HOST
  - POSTGRES_PORT
  - AUTH0_DOMAIN
  - AUTH0_CLIENT_ID
  - AUTH0_CLIENT_SECRET
  - AUTH0_DOMAIN
  - AUTH0_CALLBACK_URL=http://localhost:8000/auth0/callback
  - AUTH0_API_AUDIENCE=http://localhost/api/barbershop
  - AUTH0_ALGORITHMS=RS256
  - CUSTOMER_MANGER_MICROSERVICE_URL=http://customer-service:8001
  - USER_MANAGER_MICROSERVICE_URL=http://user-service:8002
  - EMPLOYEE_MANAGER_MICROSERVICE_URL=http://employee-service:8003
   
4. 2. Build and tag Docker images for each service:
   ```bash
   docker build -t barbershop-service-name ./path-to-service


## Sources

