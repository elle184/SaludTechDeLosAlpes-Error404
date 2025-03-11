import aiosqlite
import json
import os
from datetime import datetime
from typing import Optional, Dict, Any

DB_FILE = os.path.join(os.path.dirname(__file__), "saga.db")

class SagaRepository:
    async def create_table(self) -> None:
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

    async def save_saga(self, saga_record: Dict[str, Any]) -> None:
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

    async def update_saga_status(
        self, 
        saga_id: str, 
        overall_status: str, 
        processed_data: Optional[Dict[str, Any]] = None, 
        step1_status: Optional[str] = None, 
        step2_status: Optional[str] = None, 
        step3_status: Optional[str] = None
    ) -> None:
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

    async def get_saga_by_id(self, saga_id: str) -> Optional[Dict[str, Any]]:
        await self.create_table()
        async with aiosqlite.connect(DB_FILE) as db:
            cursor = await db.execute("SELECT * FROM saga_requests WHERE id = ?", (saga_id,))
            row = await cursor.fetchone()
            if row:
                keys = [
                    "id", "request_data", "step1_status", "step2_status", 
                    "step3_status", "overall_status", "processed_data", "created_at"
                ]
                record = dict(zip(keys, row))
                record["request_data"] = json.loads(record["request_data"])
                record["processed_data"] = json.loads(record["processed_data"])
                return record
            return None

    async def get_all_registers(self) -> list[Dict[str, Any]]:
        """
        Obtiene todos los registros de la tabla saga_requests en formato de lista de diccionarios.
        Cada diccionario representa un registro con sus campos como llave-valor.
        """
        await self.create_table()
        async with aiosqlite.connect(DB_FILE) as db:
            # Hacer que SQLite devuelva filas como diccionarios
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT * FROM saga_requests")
            rows = await cursor.fetchall()
            
            # Convertir las filas a diccionarios completos con datos JSON parseados
            result = []
            for row in rows:
                # Convertir Row a diccionario
                record = dict(row)
                
                # Parsear los campos JSON
                record["request_data"] = json.loads(record["request_data"])
                record["processed_data"] = json.loads(record["processed_data"])
                
                result.append(record)
            
            return result