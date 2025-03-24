import fastapi
from snippet.route import snippet_router
from database import Base, engine

app = fastapi.FastAPI()

# Base.metadata.drop_all(bind=engine) # will not work if you have foreign key constraints
# Base.metadata.create_all(bind=engine)

print('hello')
@app.get("/")
def health_check():
    return {"status" : "okay! I am alive"}


app.include_router(snippet_router)