from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from main import main

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/insert")
def run_main():
    main()
    return {"message": "main() 실행 완료"}

@app.get("/")
def home():
    return {"message": "Hello, FastAPI!"}