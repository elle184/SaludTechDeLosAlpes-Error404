# Proyecto sagas
## STA Saga Service usando FastAPI

Esta implementación muestra una saga paso a paso que cumple con los siguientes requisitos:

1. **Step 1:** Llamada HTTP al servicio *Anonymizer*.
2. **Step 2:** Publicación de un evento al servicio *Tokenizer*.
3. **Step 3:** Llamada HTTP al servicio *AI Model Process*.
   - Si el Step 1 o Step 2 fallan, se retorna el error inmediatamente.
   - Si el Step 3 falla, se envía un evento de compensación al *Tokenizer* y se retorna el error.
4. Se persiste el estado de cada saga en una base de datos SQLite (cada request se almacena con un identificador y el estado de cada paso).
5. Se exponen endpoints para disparar la saga (invocado por el BFF) y para consultar el estado asíncrono de la misma.


## Cómo Ejecutar la Aplicación

1. **Instalar dependencias:**
   ```bash
   pip install fastapi uvicorn httpx aiosqlite
   ```

2. **Ejecutar la aplicación:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 5000 --reload
   ```

3. **Probar la Saga:**
   - **Iniciar la saga:**  
     Enviar un `POST` a `http://localhost:5000/saga` con un JSON de ejemplo:
     ```json
     {
         "image_id": "img_123",
         "data": "datos de prueba"
     }
     ```
   - **Consultar el estado de la saga:**  
     Enviar un `GET` a `http://localhost:5000/saga/<saga_id>`, reemplazando `<saga_id>` con el identificador retornado.

## Integración con Apache Pulsar

Actualmente, la función `publish_event` simula la publicación de eventos. Para integrar con Apache Pulsar:
- Reemplace la función `publish_event` en `application/ms-1/src/sta/modulos/sagas/coordinadores/saga_imagenes.py` por una implementación que use el cliente oficial de Pulsar.
- Configure la conexión al clúster de Pulsar según su entorno.


## Estructura del Proyecto

``` bash
application\ms-1/src
 └── sta/
      ├── modulos/
      │    └── sagas/
      │         ├── aplicacion/
      │         │      └── comandos.py          # Comando para actualizar el estado de la saga
      │         └── coordinadores/
      │                └── saga_imagenes.py       # Implementación de la saga
      └── seedwork/
           ├── aplicacion/
           │      └── sagas.py                   # Interfaz base para la saga
           └── infrastructure/
                  └── saga_repository.py          # Repositorio para persistir estados (SQLite)
main.py                                         # Aplicación FastAPI
README.md                                       # Documentación del proyecto
```

---

## Código Completo

### 1. Interfaz Base para la Saga  
*Archivo: `application/ms-1/src/sta/seedwork/aplicacion/sagas.py`*

```python
# application/ms-1/src/sta/seedwork/aplicacion/sagas.py

from abc import ABC, abstractmethod

class SagaBase(ABC):
    @abstractmethod
    async def execute(self, data: dict) -> dict:
        """Ejecuta la saga paso a paso."""
        pass

    @abstractmethod
    async def compensate(self, data: dict, saga_id: str):
        """Ejecuta la lógica de compensación en caso de error en el Step 3."""
        pass

    async def save_saga(self, saga_record: dict):
        from sta.seedwork.infrastructure.saga_repository import SagaRepository
        repo = SagaRepository()
        await repo.save_saga(saga_record)
```

---

### 2. Repositorio para Persistencia con SQLite  
*Archivo: `application/ms-1/src/sta/seedwork/infrastructure/saga_repository.py`*

```python
# application/ms-1/src/sta/seedwork/infrastructure/saga_repository.py

import aiosqlite
import json
import os
from datetime import datetime

# Se crea la base de datos en la misma carpeta que este archivo.
DB_FILE = os.path.join(os.path.dirname(__file__), "saga.db")

class SagaRepository:
    async def create_table(self):
        async with aiosqlite.connect(DB_FILE) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS saga_requests (
                    id TEXT PRIMARY KEY,
                    request_data TEXT,
                    step1_status TEXT,
                    step2_status TEXT,
                    step3_status TEXT,
                    overall_status TEXT,
                    processed_data TEXT,
                    created_at TEXT
                )
            """)
            await db.commit()

    async def save_saga(self, saga_record: dict):
        await self.create_table()
        async with aiosqlite.connect(DB_FILE) as db:
            await db.execute("""
                INSERT OR REPLACE INTO saga_requests 
                (id, request_data, step1_status, step2_status, step3_status, overall_status, processed_data, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                saga_record.get("id"),
                json.dumps(saga_record.get("request_data", {})),
                saga_record.get("step1_status", "PENDING"),
                saga_record.get("step2_status", "PENDING"),
                saga_record.get("step3_status", "PENDING"),
                saga_record.get("overall_status", "PENDING"),
                json.dumps(saga_record.get("processed_data", {})),
                datetime.utcnow().isoformat()
            ))
            await db.commit()

    async def update_saga_status(self, saga_id: str, overall_status: str, processed_data: dict = None, step1_status=None, step2_status=None, step3_status=None):
        record = await self.get_saga_by_id(saga_id)
        if not record:
            record = {
                "id": saga_id,
                "request_data": {},
                "step1_status": "PENDING",
                "step2_status": "PENDING",
                "step3_status": "PENDING",
                "overall_status": overall_status,
                "processed_data": {}
            }
        else:
            record["overall_status"] = overall_status
        if step1_status:
            record["step1_status"] = step1_status
        if step2_status:
            record["step2_status"] = step2_status
        if step3_status:
            record["step3_status"] = step3_status
        if processed_data is not None:
            record["processed_data"] = processed_data
        await self.save_saga(record)

    async def get_saga_by_id(self, saga_id: str):
        await self.create_table()
        async with aiosqlite.connect(DB_FILE) as db:
            cursor = await db.execute("SELECT * FROM saga_requests WHERE id = ?", (saga_id,))
            row = await cursor.fetchone()
            if row:
                keys = ["id", "request_data", "step1_status", "step2_status", "step3_status", "overall_status", "processed_data", "created_at"]
                record = dict(zip(keys, row))
                record["request_data"] = json.loads(record["request_data"])
                record["processed_data"] = json.loads(record["processed_data"])
                return record
            return None
```

---

### 3. Comando para Actualizar el Estado de la Saga  
*Archivo: `application/ms-1/src/sta/modulos/sagas/aplicacion/comandos.py`*

```python
# application/ms-1/src/sta/modulos/sagas/aplicacion/comandos.py

from sta.seedwork.infrastructure.saga_repository import SagaRepository

async def actualizar_estado_saga(saga_id: str, estado: str):
    repo = SagaRepository()
    await repo.update_saga_status(saga_id, overall_status=estado)
```

---

### 4. Implementación de la Saga (Procesamiento de Imágenes)  
*Archivo: `application/ms-1/src/sta/modulos/sagas/coordinadores/saga_imagenes.py`*

```python
# application/ms-1/src/sta/modulos/sagas/coordinadores/saga_imagenes.py

import uuid
import httpx
from sta.seedwork.aplicacion.sagas import SagaBase
from sta.modulos.sagas.aplicacion.comandos import actualizar_estado_saga
from sta.seedwork.infrastructure.saga_repository import SagaRepository

# Función para simular la publicación de eventos (integración futura con Apache Pulsar)
async def publish_event(topic: str, data: dict):
    print(f"Publishing event to '{topic}': {data}")
    # Aquí se integrará el cliente de Apache Pulsar.
    return True

class SagaImagenes(SagaBase):
    async def execute(self, data: dict) -> dict:
        # Genera un identificador único para la saga.
        saga_id = str(uuid.uuid4())
        repo = SagaRepository()
        saga_record = {
            "id": saga_id,
            "request_data": data,
            "step1_status": "PENDING",
            "step2_status": "PENDING",
            "step3_status": "PENDING",
            "overall_status": "IN_PROGRESS",
            "processed_data": {}
        }
        await repo.save_saga(saga_record)
        
        # --- Step 1: Llamada HTTP al servicio de Anonymizer ---
        async with httpx.AsyncClient() as client:
            try:
                print(f"[{saga_id}] Step 1: Llamando al servicio Anonymizer")
                response = await client.post("http://anonymizer-service/anonymize", json=data, timeout=3.0)
                response.raise_for_status()
                anonymized_data = response.json()
                saga_record["processed_data"]["anonymized"] = anonymized_data
                saga_record["step1_status"] = "COMPLETED"
                await repo.update_saga_status(saga_id, overall_status="IN_PROGRESS", step1_status="COMPLETED", processed_data=saga_record["processed_data"])
            except Exception as e:
                error_msg = f"Error en Step 1 (Anonymizer): {e}"
                print(f"[{saga_id}] {error_msg}")
                saga_record["step1_status"] = "FAILED"
                saga_record["overall_status"] = "FAILED"
                await repo.update_saga_status(saga_id, overall_status="FAILED", step1_status="FAILED", processed_data=saga_record["processed_data"])
                return {"id": saga_id, "error": error_msg}
        
        # --- Step 2: Publicar evento al servicio Tokenizer ---
        try:
            print(f"[{saga_id}] Step 2: Publicando evento a Tokenizer")
            await publish_event("tokenizer_event", data)
            saga_record["processed_data"]["tokenizer_event"] = "event_published"
            saga_record["step2_status"] = "COMPLETED"
            await repo.update_saga_status(saga_id, overall_status="IN_PROGRESS", step2_status="COMPLETED", processed_data=saga_record["processed_data"])
        except Exception as e:
            error_msg = f"Error en Step 2 (Tokenizer): {e}"
            print(f"[{saga_id}] {error_msg}")
            saga_record["step2_status"] = "FAILED"
            saga_record["overall_status"] = "FAILED"
            await repo.update_saga_status(saga_id, overall_status="FAILED", step2_status="FAILED", processed_data=saga_record["processed_data"])
            return {"id": saga_id, "error": error_msg}
        
        # --- Step 3: Llamada HTTP al servicio de AI Model Process ---
        try:
            print(f"[{saga_id}] Step 3: Llamando al servicio AI Model Process")
            async with httpx.AsyncClient() as client:
                response = await client.post("http://ai-model-service/process", json=data, timeout=3.0)
                response.raise_for_status()
                ai_result = response.json()
                saga_record["processed_data"]["ai_result"] = ai_result
                saga_record["step3_status"] = "COMPLETED"
                saga_record["overall_status"] = "COMPLETED"
                await repo.update_saga_status(saga_id, overall_status="COMPLETED", step3_status="COMPLETED", processed_data=saga_record["processed_data"])
        except Exception as e:
            error_msg = f"Error en Step 3 (AI Model Process): {e}"
            print(f"[{saga_id}] {error_msg}")
            saga_record["step3_status"] = "FAILED"
            saga_record["overall_status"] = "FAILED"
            await repo.update_saga_status(saga_id, overall_status="FAILED", step3_status="FAILED", processed_data=saga_record["processed_data"])
            # Si falla el Step 3, se ejecuta la compensación: enviar evento de compensación al Tokenizer.
            await self.compensate(data, saga_id)
            return {"id": saga_id, "error": error_msg}
        
        # Actualización final del estado de la saga.
        await actualizar_estado_saga(saga_id, "COMPLETED")
        return {"id": saga_id, "result": "Saga completada exitosamente", "data": saga_record["processed_data"]}

    async def compensate(self, data: dict, saga_id: str):
        print(f"[{saga_id}] Ejecutando compensación: Publicando evento de compensación a Tokenizer")
        await publish_event("tokenizer_compensation", data)
```

---

### 5. Aplicación FastAPI  
*Archivo: `main.py`*

```python
# main.py

from fastapi import FastAPI, HTTPException
from sta.modulos.sagas.coordinadores.saga_imagenes import SagaImagenes
from sta.seedwork.infrastructure.saga_repository import SagaRepository

app = FastAPI(title="STA Saga Service")

@app.post("/saga")
async def start_saga(request_data: dict):
    """
    Endpoint para iniciar la ejecución de la saga.
    Se espera un JSON con la información necesaria.
    """
    saga = SagaImagenes()
    result = await saga.execute(request_data)
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
    else:
        raise HTTPException(status_code=404, detail="Saga no encontrada")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
```

---

### 6. Documentación del Proyecto  
*Archivo: `README.md`*


## Conclusión

Esta implementación:
- Ejecuta la saga paso a paso.
- Retorna errores inmediatamente si falla el Step 1 o el Step 2.
- Publica un evento de compensación si falla el Step 3.
- Persiste el estado en una base de datos SQLite para consulta asíncrona.
- Está diseñada para facilitar la integración con Apache Pulsar en el futuro.
- Se ejecutan los pasos de forma asíncrona usando *httpx* para llamadas HTTP.
- Se simula la publicación de eventos (fácil de reemplazar por Apache Pulsar).
- Se persiste el estado de la saga en SQLite (o se puede migrar a Redis en el futuro).
- Se exponen endpoints para disparar la saga y consultar su estado, permitiendo la integración con el BFF.
