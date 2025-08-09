#!/bin/bash
cd /workspace/RollerAI && git pull origin main


export AWS_SHARED_CREDENTIALS_FILE=/workspace/.aws/credentials
export AWS_CONFIG_FILE=/workspace/.aws/config

export PATH=/workspace/.local/bin:$PATH
source /workspace/venv/bin/activate

cd /workspace/RollerAI/redis_vm

python runpod_worker.py