from fastapi import FastAPI

app = FastAPI()

@app.post("/generate")
async def gen():
    return "I hear you"