from diffusers import StableDiffusionXLPipeline
import torch
import boto3
from io import BytesIO # this allows straight upload using a buffer instead of saving (saves space overall)

pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",  # This downloads SDXL
    torch_dtype=torch.float16,
    variant="fp16",
    use_safetensors=True
).to("cuda")

prompt = "a futuristic city skyline at night, high detail, cinematic"
image = pipe(prompt).images[0]

buffer = BytesIO()
image.save(buffer, format="PNG")
buffer.seek(0) # resets pointer of buffer back to start so upload_file reads the buffer correctly


s3 = boto3.client("s3")
bucket_name = "rollerai-generated-images"            

key = "output.png"
s3.upload_fileobj(buffer, bucket_name, key)



