from seedwork.infrastructure.saga_repository import SagaRepository
async def actualizar_estado_saga(saga_id: str, estado: str) -> None:
    repo = SagaRepository()
    await repo.update_saga_status(saga_id, overall_status=estado)
