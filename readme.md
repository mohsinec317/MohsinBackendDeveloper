# Taxi Trip Data Service

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
