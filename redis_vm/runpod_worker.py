from diffusers import StableDiffusionXLPipeline
import torch
import boto3

pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",  # This downloads SDXL
    torch_dtype=torch.float16,
    variant="fp16",
    use_safetensors=True
).to("cuda")

prompt = "a futuristic city skyline at night, high detail, cinematic"
image = pipe(prompt).images[0]


s3 = boto3.client("s3")
bucket_name = "rollerai-generated-images"            
s3_key = "uploads/output.png"                    

s3.upload_file("output.png", bucket_name, s3_key)
