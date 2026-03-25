from fastapi import FastAPI

app = FastAPI()

# This is a simple FastAPI application that returns a JSON response when the root endpoint is accessed. 
# You can run this application using Uvicorn or any ASGI server to see the output.
@app.get("/")
def read_root():
    return {"Hello": "Mom and Eduardo!"}