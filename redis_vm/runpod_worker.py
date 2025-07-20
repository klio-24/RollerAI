from diffusers import StableDiffusionXLPipeline
import torch
import boto3
import redis
from io import BytesIO # this allows straight upload using a buffer instead of saving (saves space overall)
from redis import Redis
from rq import Worker,Queue

r = redis.Redis(host="18.132.136.177", port=6379, db=0, password="redis123", decode_responses=True)

pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",  # This downloads SDXL
    torch_dtype=torch.float16,
    variant="fp16",
    use_safetensors=True
).to("cuda")

s3 = boto3.client("s3")  

def generate_image_rq(job_id: str, prompt: str):
    image = pipe(prompt).images[0]
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0) # resets pointer of buffer back to start so upload_file reads the buffer correctly

    key = f"{job_id}.png"
    s3.upload_fileobj(buffer, bucket_name, key)
    s3_url = f"https://rollerai-generated-images.s3.amazonaws.com/{key}"

    r.hset(job_id, mapping={
        "status": "complete",
        "s3_url": s3_url
    })

if __name__ == "__main__": # ensures code only runs if this script is run directly
    queue = Queue('default', connection = r)
    worker = Worker(queues = [queue],connection = r)
    worker.work() # starts the work loop which makes the pod a worker on the queue, connecting to redis
