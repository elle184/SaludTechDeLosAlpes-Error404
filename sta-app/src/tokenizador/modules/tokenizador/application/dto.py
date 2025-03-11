from dataclasses import dataclass, field
from tokenizador.modules.tokenizador.application.dto import DTO

@dataclass(frozen = True)
class UserDTO(DTO) : 
    username : str
    password : str
    access_token : str
    