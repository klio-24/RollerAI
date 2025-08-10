import runpod
import os
import time
import redis

from runpod.api.ctl_commands import resume_pod, stop_pod, get_pod

home_dir = os.path.expanduser("~")
key_path = os.path.join(home_dir, "runpodkey.txt")
with open(key_path, "r") as f:
    RUNPOD_API_KEY = f.read().strip()

runpod.api_key = RUNPOD_API_KEY 

pod1_id = "k7lm6thxq3kf8e"
pod2_id = "0roqcxw1i9d2wp"

r = redis.Redis(host='localhost', port=6379, db=0)

UPPER_THRESHOLD = 7
LOWER_THRESHOLD = 3
CHECK_INTERVAL = 5 

while True:

    queue_length = r.llen('default') 
    
    if queue_length < LOWER_THRESHOLD and get_pod(pod2_id)['desiredStatus'] == 'RUNNING':
        stop_pod(pod2_id)

    elif queue_length > UPPER_THRESHOLD and get_pod(pod2_id)['desiredStatus'] == 'EXITED':
        resume_pod(pod2_id,1)
    time.sleep(CHECK_INTERVAL)

