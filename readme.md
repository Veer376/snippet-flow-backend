# Snippet Flow :sparkles:

Snippet-flow is the personalised book exerpts recommendation system. 
1. It utilized the fastapi for the API endpoint for getting the recommedations, saving the book exerpts
2. Event driven Architecture for generating the embeddings for newly added snippets using kafka
3. Microservices architecture using Docker compose. 
Services : fastapi server, kafka, zookeeper, kafka_consumer, postgres DB.

## :rocket: Quick Start

## Prerequisites
- Docker
---

### :whale: Using Docker Compose
```bash
# 1. Clone the repository
git clone <repo-name>

docker compose up -d
## Sit back, relax and cross your fingers. Everything should work without errors
# to checks the logs for each of the services or all.
docker compose logs -f service
```
---
### Finally
```bash
# we are using the postgres image which has preinstalled pgvector, we need to add the extension to the every database we will use. 
# Although init.sql file may do this, if not, then try this.
docker exec -it snippet-flow-db bash 
psql -U username -d snippet-flow-db

\dx # check the extensions
create extension vector
\dx # check again.
```

## :sparkles: Features
FastAPI for high-performance Python web serving
PostgreSQL for robust relational storage
Docker for containerized deployment (optional)
User & Snippet Management with minimal endpoints
Optional Virtual Environment for local Python dev