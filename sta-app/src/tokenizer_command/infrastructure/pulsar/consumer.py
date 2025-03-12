import pulsar
from application.service_tokenizer_cmd import ITokenizerCmdService
import json
from application.dto_raw_data import MedicalRecordDTO

class Config:
    def __init__(self, service_url, topic, subscription):
        self.service_url = service_url
        self.topic = topic
        self.subscription = subscription

class Consumer:
    def __init__(self, config, tokenizer_cmd_service: ITokenizerCmdService):
            self.client = pulsar.Client(config.service_url)
            self.consumer = self.client.subscribe(config.topic, subscription_name=config.subscription)
            self.tokenizer_cmd_service = tokenizer_cmd_service

    def run(self):
        try:
            while True:
                msg = self.consumer.receive()
                data = json.loads(msg.data())
                medical_record_dto = MedicalRecordDTO(**data)
                print("Received message: '%s'" % medical_record_dto)
                self.tokenizer_cmd_service.tokenize(medical_record_dto)
                self.consumer.acknowledge(msg)
        finally:
            self.client.close()