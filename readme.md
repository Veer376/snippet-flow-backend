# Snippet Flow :sparkles:

This is the backend of snippet-flow 
Here is the fronend : 

## :rocket: Quick Start

## Prerequisites
- Docker
---

### :whale: Using Docker Compose
```bash
# 1. Clone the repository
git clone <repo-name>
# Note: If you uncomment the service for your application in the docker-compose.yml, you can skip the manual Python setup entirely. To continue with the current setup uncomment the backend service in docker compose.
docker compose up -d
uvicorn main:app
```

Recommeded in developement as docker compose takes time for every build...
### :snake: Using Python Virtual Environment
```bash
# clone the repo 
git clone <repo-name>
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
pip install -r requirements.txt
docker compose up
uvicorn main:app --reload
```
---
### Finally
```bash
# we are using the postgres image which has preinstalled pgvector, you we need to add the extension to the every database we will use. 
# Although init.sql file may do this, if not, then try this.
docker exec -it snippet-flow-db bash 
psql -U username -d snippet-flow-db

\dx # check the extensions
create extension vector
\dx # check again.
```

### Configuration
```markdown
Environment Variables
Create a `.env` file or set `DATABASE_URL` in your environment to point to your database.  
Example:
DATABASE_URL=postgresql://user_name:user_password@localhost:5432/db_name
```

## :sparkles: Features
FastAPI for high-performance Python web serving
PostgreSQL for robust relational storage
Docker for containerized deployment (optional)
User & Snippet Management with minimal endpoints
Optional Virtual Environment for local Python dev