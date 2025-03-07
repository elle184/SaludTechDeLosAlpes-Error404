from dataclasses import dataclass
from sta.seedwork.application.commands import Command

@dataclass
class CreateSession(Command) :
    username : str
    password : str

class CreateSessionHandler() :