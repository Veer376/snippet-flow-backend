# Snippet Flow :sparkles:

This is the backend of snippet-flow 
Here is the fronend : 

## :rocket: Quick Start

### Prerequisites
- **Docker** (if you plan to use Docker Compose)
- **Python 3.9+** (if you plan to use a virtual environment)
- **pip** for installing Python dependencies

---

## :whale: Using Docker Compose

```bash
# 1. Clone the repository
git clone <repo-name>

# 2. Navigate to the backend directory
cd backend

# 3. Start Docker containers in the background
docker compose up -d

Note: If you uncomment the service for your application in the docker-compose.yml, you can skip the manual Python setup entirely.

:snake: Using Python Virtual Environment

# 1. Clone the repository
git clone <repo-name>

# 2. Navigate to the backend directory
cd backend

# 3. (Optional) Comment out the app service in docker-compose.yml 
#    if you only want to run PostgreSQL via Docker

# 4. Create and activate a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 5. Install dependencies
pip install -r requirements.txt

# 6. Start the FastAPI server
uvicorn main:app --reload

```
---

### **Chunk 3: Configuration, Features, Contributing**

```markdown
## :wrench: Configuration

### Environment Variables

Create a `.env` file or set `DATABASE_URL` in your environment to point to your database.  
**Example:**
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/snippet_db
```

# :sparkles: Features
FastAPI for high-performance Python web serving
PostgreSQL for robust relational storage
Docker for containerized deployment (optional)
User & Snippet Management with minimal endpoints
Optional Virtual Environment for local Python dev