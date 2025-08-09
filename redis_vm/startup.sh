#!/bin/bash
cd /workspace/RollerAI && git pull origin main

export PATH=/workspace/.local/bin:$PATH
source /workspace/venv/bin/activate

cd /workspace/RollerAI/redis_vm

python runpod_worker.py