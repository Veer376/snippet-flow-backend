import fastapi
import model 
from snippet.route import snippet_router
from database import Base, engine
app = fastapi.FastAPI()

Base.metadata.drop_all(bing=engine)
Base.metadata.create_all(bind=engine)

print('hello')
@app.get("/")
def health_check():
    return {"status" : "okay! I am alive"}


app.include_router(snippet_router)