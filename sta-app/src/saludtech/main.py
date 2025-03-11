from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict
from modules.sagas.coordinadores.saga_imagenes import SagaImagenes
from seedwork.infrastructure.saga_repository import SagaRepository

app = FastAPI(title="STA Saga Service")

class SagaRequest(BaseModel):
    image_id: str
    data: Any

class SagaResponse(BaseModel):
    id: str
    result: str = None
    error: str = None
    data: Dict[str, Any] = None

@app.post("/saga", response_model=SagaResponse)
async def start_saga(request: SagaRequest):
    """
    Endpoint para iniciar la ejecución de la saga.
    Se espera un JSON con la información necesaria.
    """
    saga = SagaImagenes()
    result = await saga.execute(request.dict())
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return result

@app.get("/saga/{saga_id}")
async def get_saga_status(saga_id: str):
    """
    Endpoint para consultar el estado de la saga mediante su identificador.
    """
    repo = SagaRepository()
    record = await repo.get_saga_by_id(saga_id)
    if record:
        return record
    raise HTTPException(status_code=404, detail="Saga no encontrada")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
