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
