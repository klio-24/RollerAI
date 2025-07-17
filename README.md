# RollerAI


This goal of this project is to create a website which allows users to generate images based on a text prompt. The cloud-based architecture is designed to be focused around low-cost, scalability, and fault-tolerance.

Redis queue: The jobs are are queued in a Redis message queue acting as a job queue. The jobs themselves are a Redis hash, with a random Job ID assigned as the key and multiple values assigned to each key (status of job, text prompt, image storage URL).


The project did not utilise full-scale CI/CD systems during development, however at an early stage of development the frontend and backend EC2 instances were configured so that on restart they pulled the latest changes from the repository and automatically built and deployed their respective applications

The auto-scaling custom Python script works on the principle of hysterisis (similar to a central heating controller), whereby it activates more pods if the queue exceeds a certain length, but does not shutdown the spare pod until the queue is back to a manageable length. This prevents excessive activation and deactivation of the spare pod.



Although the project has achieved its aims, there is still room to introduce more features and technologies to increase flexiblity and usefulness:
- Implement Kubuernetes KEDA in place of the Python script for a fully-scalable architecutre
- Allow the user to choose from multiple stable diffusion models
- Implement real payment options through a Stripe API
- Create a subpage for users to access previous images generated

