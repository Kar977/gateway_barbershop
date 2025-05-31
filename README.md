# BarberShop API

## 📋 Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Technologies](#technologies)
- [Setup & Deployment](#setup--deployment)
- [Application View](#application-view)
- [Sources](#sources)

## 🧾 Overview

**BarberShop API** is a distributed backend system designed using a microservices architecture to support the full operational workflow of a modern barbershop. The application serves three types of users:

- **Customers** – browse available time slots, book appointments, manage reservations, and view service history.
- **Salon Employees** – log in, manage and update work schedules, and view upcoming bookings.
- **Business Owner** – manage the organization via Auth0, create employee accounts, and oversee salon operations.

## 🏗 Architecture

The system follows a **polyrepo microservices** structure, with each service developed independently using **FastAPI**. An **API Gateway** handles incoming client requests and routes them to the appropriate microservice.

> This architecture promotes modularity, scalability, and maintainability through clear separation of concerns.

## 🧰 Technologies

- **Language & Framework**: Python 3.11, FastAPI 0.111.0
- **Database**: PostgreSQL 15, Adminer
- **Containerization**: Docker 24.0.7, Portainer 2.27
- **Monitoring**: Prometheus 3.4.0
- **Auth & Security**: Auth0, AuthLib 1.3.2, PyJWT 2.9.0
- **Testing**: Pytest 8.3.5, Pytest-asyncio 0.26.0
- **HTTP Clients**: Httpx 0.27.0, Requests 2.32.3
- **ASGI Server**: Uvicorn 0.30.1
- **Data Validation**: Pydantic 2.7.4

## ⚙️ Setup & Deployment

The application runs as a set of Docker containers orchestrated via **Portainer** on an **AWS EC2** instance. Each microservice lives in its own repository:

- [`gateway_barbershop`](https://github.com/Kar977/gateway_barbershop)
- [`employee_manager`](https://github.com/Kar977/employee_manager)
- [`users_manager`](https://github.com/Kar977/users_manager)
- [`customers_manager`](https://github.com/Kar977/customers_manager)
- [`notification_manager`](https://github.com/Kar977/notification-manager)

### Steps to Deploy:

1. **Fork** all the listed repositories above.
2. **Add required secrets** in GitHub for each microservice (see below).
3. **Trigger GitHub Actions** (`push-docker-image-to-ecr.yml`) to build and push Docker images to AWS ECR.
4. **Create an AWS EC2 instance** (recommended: `t2.xlarge`, 4 vCPUs, 16 GiB RAM).
5. **Install Docker** on the EC2 instance.
6. **Install and run Portainer**, then deploy the application using the provided `stack.yml`.

### 🔐 Secrets Overview

Each microservice requires a specific set of GitHub secrets, for example:

#### For `gateway_barbershop`:
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_ACCOUNT_ID`
- `POSTGRES_NAME`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`
- `AUTH0_DOMAIN`, `AUTH0_CLIENT_ID`, `AUTH0_CLIENT_SECRET`
- `AUTH0_CALLBACK_URL`, `AUTH0_API_AUDIENCE`, `AUTH0_ALGORITHMS`
- Service URLs:  
  - `CUSTOMER_MANAGER_MICROSERVICE_URL`  
  - `USER_MANAGER_MICROSERVICE_URL`  
  - `EMPLOYEE_MANAGER_MICROSERVICE_URL`

#### For other microservices:
Each repository contains its own `README` or deployment guide listing the specific secrets it requires. Be sure to configure them before triggering GitHub Actions.

## 🖼 Application View

![simple_architecture_barbershop drawio](https://github.com/user-attachments/assets/3697ebf1-cd91-465f-afbe-cc0a7c943373)


## 📚 Sources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Auth0 Docs](https://auth0.com/docs)
- [AWS ECR & EC2 Docs](https://docs.aws.amazon.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
