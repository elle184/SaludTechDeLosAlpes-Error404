from abc import ABC, abstractmethod
from domain.model_tokenized_data import MedicalRecord

class ITokenizerRepository(ABC):
    @abstractmethod
    def insert_record(self, record: MedicalRecord):
        pass

    @abstractmethod
    def get_all_records(self):
        pass