import fastapi
import model 

app = fastapi.FastAPI()
print('hello')
@app.get("/")
def health_check():
    return {"status" : "okay! I am alive"}
