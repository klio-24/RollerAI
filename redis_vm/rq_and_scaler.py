with open("api_key.txt", "r") as f:
    RUNPOD_API_KEY = f.read().strip()



# define hysterisis and time interval



# hysterisis loop with 3 stages (len 0 = 0 workers, len <= 2 = 1 worker, len >= 3 = 2 worker)