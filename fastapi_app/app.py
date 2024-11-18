from fastapi import FastAPI
from mangum import Mangum

app = FastAPI(root_path="/prod")

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/ping")
def read_root():
    return {"message": "pong"}



handler = Mangum(app)
