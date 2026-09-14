from fastapi import FastAPI
from app.api.routes.underwriting import router as underwriting_router
from app.config import settings

app = FastAPI()


app.include_router(underwriting_router)

#endpoint for health check

@app.get("/health")
async def health_check():
    return {"status": "ok"}