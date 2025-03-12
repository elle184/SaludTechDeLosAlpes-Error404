from infrastructure.pulsar.consumer import Consumer, Config
from infrastructure.pulsar.adapter_tokenizer_query import TokenizerAdapterQuery
from application.service_tokenizer_cmd import TokenizerCmdService
from infrastructure.db.adapter_tokenizer_repo_mysql import TokenizerRepository
import pulsar

if __name__ == '__main__':
        tokenizer_query_config = Config(
            service_url='pulsar://localhost:6650',
            topic='tokenizer_query',
            subscription='tokenizer_query'
        )
        pulsar_client = pulsar.Client(tokenizer_query_config.service_url)
        tokenizer_query_adapter = TokenizerAdapterQuery(pulsar_client)
        tokenizer_repository = TokenizerRepository()
        tokenizer_service = TokenizerCmdService(tokenizer_repository, tokenizer_query_adapter)

        tokenizer_cmd_config = Config(
            service_url='pulsar://localhost:6650',
            topic='tokenizer_command',
            subscription='tokenizer_command'
        )
        subscriber = Consumer(tokenizer_cmd_config, tokenizer_service)
        subscriber.run()