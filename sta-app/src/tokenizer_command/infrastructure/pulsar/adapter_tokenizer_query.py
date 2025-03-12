import pulsar
import json
from domain.port_tokenizer_query import ITokenizerQueryPort
from domain.model_tokenized_data import MedicalRecord

class TokenizerAdapterQuery(ITokenizerQueryPort):
    def __init__(self, pc: pulsar.Client):
        self.pulsar_client = pc

    def query_event_emit(self, tokenized_data: MedicalRecord) -> bool:
        try:
            producer = self.pulsar_client.create_producer('tokenizer_query')
           #  producer.send(json.dumps(tokenized_data).encode('utf-8'))
            producer.send(json.dumps(tokenized_data.to_json()).encode('utf-8'))
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
