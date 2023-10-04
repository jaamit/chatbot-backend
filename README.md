# chatbot-backend
Backend code for chatbot

# How to run
- Create a python virtual env (used python 3.10)
- pip install -r requirements.txt
- cd src
- uvicorn main:app --reload
- Application will start at 
- http://127.0.0.1:8000
- curl http://127.0.0.1:8000/ returns ["OK"]

# Production Deployments - Thoughts
- The UI and the backend are separated to begin with. This can enable scaling them independently and avoid tight coupling.
- Both UI & backend can be dockerized and run in an auto-scale environment (ECS/Fargate or Kubernetes deployment)
- Load balancers along with Auto-scaling policies can be used for handling surge in traffic
- backend health check end-point can be used to monitor the health of the system
- observability & monitoring should be used for production
- CI/CD pipelines need to be there
- at the bare minimum we should have dev & prod env.. ideally Dev -> QA -> UA -> PROD
