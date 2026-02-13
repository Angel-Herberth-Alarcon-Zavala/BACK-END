from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_methods = ["*"],
    allow_origins = ["*"],
    allow_headers = ["*"],
)

@app.get("/login")

