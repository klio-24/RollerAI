from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import redis
import uuid
from rq import Queue

app = FastAPI()

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True) # generic redis startup line (redis server running on localhost, default comm port is 6379)
# q = Queue(connection=r)  # Connects RQ queue to Redis

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://rollerai.xyz"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
async def generate(request: Request): # initiates promptrequest object to handle the passed in html file

    data = await request.json() # gets raw JSON body
    prompt = data.get("prompt") # gets the 'prompt' string we defined on frontend

    job_id = str(uuid.uuid4()) # generate a unique job id

    r.hset(job_id, mapping={
        "status": "started",
        "prompt": prompt,
        "s3_url": ""
    })

    # q.enqueue(generate_image, job_id, prompt)

    return {"job_id": job_id}  

@app.get('/status')
def get_status(job_id: str): 

    status = r.hget(job_id, "status")
    s3_url = r.hget(job_id, "s3_url")

    return {
        "status": status,
        "s3_url": s3_url
    }



