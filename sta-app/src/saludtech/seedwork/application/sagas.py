from abc import ABC, abstractmethod
from typing import Dict, Any

class SagaBase(ABC):
    @abstractmethod
    async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta la saga paso a paso."""
        pass

    @abstractmethod
    async def compensate(self, data: Dict[str, Any], saga_id: str) -> None:
        """Ejecuta la lógica de compensación en caso de error."""
        pass

    async def save_saga(self, saga_record: Dict[str, Any]) -> None:
        from ..infrastructure.saga_repository import SagaRepository
        repo = SagaRepository()
        await repo.save_saga(saga_record)
