from dataclasses import dataclass, field
from anonimizador.modules.anonimizador.application.dto import DTO

@dataclass(frozen = True)
class UserDTO(DTO) : 
    username : str
    password : str
    access_token : str
    