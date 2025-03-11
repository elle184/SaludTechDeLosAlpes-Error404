from tokenizador.modules.tokenizador.domain.events import TokenCreated
from tokenizador.seedwork.application.handlers import Handler
from tokenizador.modules.tokenizador.infrastructure.dispatcher import Dispatcher

class HandlerReservaIntegracion(Handler) :
    @staticmethod
    def handle_token_created(event) :
        dispatcher = Dispatcher()
        dispatcher.publish_event(event, 'eventos-procesar-anonimizacion')