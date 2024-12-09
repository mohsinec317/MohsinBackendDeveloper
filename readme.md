# Taxi Trip Data Microservice developed by Mohsin (mohsin.codingexpert@gmail.com)

## Overview
This microservice processes New York City taxi trip data, stores it in a PostgreSQL database, and provides APIs for data retrieval and analysis.

## Features
- FastAPI-based RESTful APIs
- GraphQL endpoint for flexible queries
- PostgreSQL database integration with SQLAlchemy
- Dockerized for easy deployment
- CI/CD pipeline support

## Getting Started
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `uvicorn app.main:app --reload`

## Initial database setup
1. Run  route /initialize-database/ (POST method) with csv_path as request payload {csv_path: "/path/to/csv/"}

## Test suite
1. Test setup: Available in the tests folder in the root directory
2. Package used: pytest v8.3.2
3. To run tests, use pytest

## Docker
1. To build a docker image: docker build -t MohsinBackendDeveloper .
2. To run it locally: docker run -d -p 8000:8000 MohsinBackendDeveloper

## Notes
1. Swagger: http://127.0.0.1:8000/docs
2. GraphQL: http://127.0.0.1:8000/graphql

## Scalability suggestions
1. Concurrency: We can utilize async processing of requests in FastAPI
2. Rate limiting: Implemented in the codebase
3. Server side scaling: Horizontal scaling using docker and orchestration with Kubernetes. Load balancing, Caching (redis/alternatives). 
4. Message queues (eg: Amazon SQS)
5. Database scalability: Implement sharding (we have only 2 vendor IDs for now, we can also explore areas in New York and have a summary to split the data). Note: It depends on the API use cases.
6. Code optimization: It can be optimized further, but as a good practice it has to be aligned with the end user requirement