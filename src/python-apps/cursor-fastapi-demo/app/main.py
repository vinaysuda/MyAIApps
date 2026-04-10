from fastapi import FastAPI
from router import router as process_router


''' # Run below two lines on Terminal to start the server.
cd app
uvicorn main:app --reload
'''

app = FastAPI()
app.include_router(process_router)
