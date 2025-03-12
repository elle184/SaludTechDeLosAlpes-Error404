from abc import ABC, abstractmethod
from application.dto_raw_data import MedicalRecordDTO
from domain.port_tokenizer_repo import ITokenizerRepository
from domain.port_tokenizer_query import ITokenizerQueryPort
import time

class ITokenizerCmdService(ABC):
    @abstractmethod
    def tokenize(self, dto: MedicalRecordDTO) -> bool:
        pass

class TokenizerCmdService(ITokenizerCmdService):
    def __init__(self, repo: ITokenizerRepository, query_port: ITokenizerQueryPort):
        self.repo = repo
        self.query_port = query_port

    def tokenize(self, dto: MedicalRecordDTO) -> bool:
        print("saving data...")
        medical_report = dto.to_entity()
        print("medical report: ", medical_report)

        # se implementa una pausa de 5 segundos para simular el tiempo     de procesamiento
        time.sleep(5)
        self.repo.insert_record(medical_report)
        print("emitting event...")
        self.query_port.query_event_emit(medical_report)
        return True