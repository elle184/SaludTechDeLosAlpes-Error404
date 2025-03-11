from fastapi import FastAPI
from api.saga import router as saga_router

app = FastAPI(title="STA Saga Service")
app.include_router(saga_router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5004, reload=True)
