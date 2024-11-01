from fastapi import FastAPI
from v1.api import router as v1_router

app = FastAPI()
app.include_router(v1_router)


@app.get("/")
async def root():
    return {"message": "Backend is running"}
