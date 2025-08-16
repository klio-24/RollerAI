# RollerAI


This goal of this project is to create a website which allows users to create AI-generated images based on a text prompt. The cloud-based architecture is designed to be low-cost and scalable

Redis queue: The jobs are are queued in a Redis message queue acting as a job queue. The jobs themselves are a Redis hash, with a random Job ID assigned as the key and multiple values assigned to each key (status of job, text prompt, image storage URL).


The project did not utilise full-scale CI/CD systems during development, however at an early stage of development the frontend and backend EC2 instances were configured so that on restart they pulled the latest changes from the repository and automatically built and deployed their respective applications

The auto-scaling custom Python script works on the principle of hysterisis (similar to a central heating controller), whereby it activates more pods if the queue exceeds a certain length, but does not shutdown the spare pod until the queue is back to a manageable length. This prevents excessive activation and deactivation of the spare pod.

Due to the VM/pod architecture, running costs means the website is not always up, however a demo can be seen below.

![Demo](./demo.gif)



```
+---------------------------------------+
|              Frontend VM              |
|         --------------------          |
|           Firebase Auth SDK      (EC2)|
+---------------------------------------+
     ^                        |   ^
     |                        v   |
     |    +------------------------------+
     |    | Redis + Python script   (EC2)|
     |    +------------------------------+
     |                        |  ^
     |                        v  |
     |              +---------------------+
     |              |       RunPod        |
     v              |  +---------------+  |
+------------+      |  |     Pod 1     |  |
|     S3     |<-----|  +---------------+  |
+------------+      |  |     Pod 2     |  |
                    |  +---------------+  |
                    +---------------------+
```



```                       
                          +======+
        ----------------->|  S3  |<-----------------
        |                 +======+                 | 
        |                                          |
+================+                        +================+   
|     POD 1      |   +================+   |     POD 1      |
|----------------|<--|   Autoscaler   |-->|----------------|
|    worker.py   |   +================+   |    worker.py   |   
+================+           ^            +================+
          ^                  |                  ^
          |                  |                  |
          v                  v                  v
+--------------------------------------------------------+
|                     Redis Queue                        |
+--------------------------------------------------------+
                            ^
                            |
                    +---------------+
                    |    Backend    |
                    +---------------+
```

Although the project has achieved its aims, there is still room to introduce more features and technologies to increase flexiblity and usefulness:
- Allow the user to choose from multiple stable diffusion models
- Implement real payment options through a Stripe API, credits system, and user/authorisation system
- Create a subpage for users to access previous images generated

