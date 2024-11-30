from fastapi import FastAPI

app=FastAPI()


@app.get("/")
def read_root():
    return {"message":"Welcome to the AI Sales Assistant Backend"}

@app.get("/health")
def health_check():
    return {"status":"Healthy"}


