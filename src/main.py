from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserMessage(BaseModel):
    user_message: str

@app.post("/get_response/")
def get_response(user_message: UserMessage):
    try:
        print(user_message)
        return {"bot_response": "OK"}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to get bot response")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
