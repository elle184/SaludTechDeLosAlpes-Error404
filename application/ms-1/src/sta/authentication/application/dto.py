from dataclasses import dataclass, field
from sta.seedwork.application.dto import DTO

@dataclass(frozen = True)
class AuthenticationDTO(DTO) :
    username : str = field(default_factory = str)
    password : str = field(default_factory = str)