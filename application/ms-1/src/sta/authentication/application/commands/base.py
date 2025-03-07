from sta.seedwork.application.commands import CommandHandler

class CreateSessionBaseHandler(CommandHandler) :
    def __init__(self):
        self._factory_repository = 