import uuid
import httpx
import logging
from typing import Dict, Any
from seedwork.application.sagas import SagaBase
from ..application.comandos import actualizar_estado_saga
from seedwork.infrastructure.saga_repository import SagaRepository
# Importamos la función asíncrona de Pulsar
from seedwork.infrastructure.pulsar_client import publish_event_with_confirmation
# Configurar logging para una mejor trazabilidad
logger = logging.getLogger("SagaImagenes")
logging.basicConfig(level=logging.INFO)

class SagaImagenes(SagaBase):
    async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
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
        try:
            logger.info(f"[{saga_id}] Step 1: Llamando al servicio Anonymizer")
            async with httpx.AsyncClient() as client:
                # response = await client.post("http://anonymizer-service/anonymize", json=data, timeout=3.0)
                response = await client.get("http://34.132.113.112:5002/anonimizador/users", timeout=30)
                response.raise_for_status()
                anonymized_data = response.json()
            saga_record["processed_data"]["anonymized"] = anonymized_data
            saga_record["step1_status"] = "COMPLETED"
            await repo.update_saga_status(saga_id, overall_status="IN_PROGRESS", step1_status="COMPLETED", processed_data=saga_record["processed_data"])
        except Exception as e:
            error_msg = f"Error en Step 1 (Anonymizer): {str(e)}"
            logger.error(f"[{saga_id}] {error_msg}")
            saga_record["step1_status"] = "FAILED"
            saga_record["overall_status"] = "FAILED"
            await repo.update_saga_status(saga_id, overall_status="FAILED", step1_status="FAILED", processed_data=saga_record["processed_data"])
            return {"id": saga_id, "error": error_msg}
        
        # --- Step 2: Publicar evento al servicio Tokenizer utilizando Pulsar ---
        try:
            logger.info(f"[{saga_id}] Step 2: Publicando evento a Tokenizer mediante Pulsar")
            # Se publica el evento y se espera la confirmación de recepción
            pulsar_response = await publish_event_with_confirmation("tokenizer_event", data, saga_id)
            logger.info(f"[{saga_id}] Confirmación de Pulsar recibida: {pulsar_response}")
            saga_record["processed_data"]["tokenizer_event"] = "event_published"
            saga_record["step2_status"] = "COMPLETED"
            await repo.update_saga_status(saga_id, overall_status="IN_PROGRESS", step2_status="COMPLETED", processed_data=saga_record["processed_data"])
        except Exception as e:
            error_msg = f"Error en Step 2 (Tokenizer) con Pulsar: {str(e)}"
            logger.error(f"[{saga_id}] {error_msg}")
            saga_record["step2_status"] = "FAILED"
            saga_record["overall_status"] = "FAILED"
            await repo.update_saga_status(saga_id, overall_status="FAILED", step2_status="FAILED", processed_data=saga_record["processed_data"])
            return {"id": saga_id, "error": error_msg}
        
        # --- Step 3: Llamada HTTP al servicio de AI Model Process ---
        try:
            logger.info(f"[{saga_id}] Step 3: Llamando al servicio AI Model Process")
            async with httpx.AsyncClient() as client:
                # response = await client.post("http://ai-model-service/process", json=data, timeout=3.0)
                response = await client.get("http://35.193.187.114:5000/a-model/processed-data", timeout=30)
                response.raise_for_status()
                ai_result = response.json()
            saga_record["processed_data"]["ai_result"] = ai_result
            saga_record["step3_status"] = "COMPLETED"
            saga_record["overall_status"] = "COMPLETED"
            await repo.update_saga_status(saga_id, overall_status="COMPLETED", step3_status="COMPLETED", processed_data=saga_record["processed_data"])
        except Exception as e:
            error_msg = f"Error en Step 3 (AI Model Process): {str(e)}"
            logger.error(f"[{saga_id}] {error_msg}")
            saga_record["step3_status"] = "FAILED"
            saga_record["overall_status"] = "FAILED"
            await repo.update_saga_status(saga_id, overall_status="FAILED", step3_status="FAILED", processed_data=saga_record["processed_data"])
            # Ejecuta la compensación en caso de error en Step 3.
            await self.compensate(data, saga_id)
            return {"id": saga_id, "error": error_msg}
        
        # Actualización final del estado de la saga.
        await actualizar_estado_saga(saga_id, "COMPLETED")
        return {"id": saga_id, "result": "Saga completada exitosamente", "data": saga_record["processed_data"]}

    async def compensate(self, data: Dict[str, Any], saga_id: str) -> None:
        logger.info(f"[{saga_id}] Ejecutando compensación: Publicando evento de compensación a Tokenizer")
        # Se podría reutilizar la función de Pulsar o definir otro mecanismo para la compensación
        await publish_event_with_confirmation("tokenizer_compensation", data, saga_id)
