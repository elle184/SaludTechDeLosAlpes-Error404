from dataclasses import dataclass, field

@dataclass(frozen = True)
class AuthenticationDTO() :
    username : str = field(default_factory = str)
    password : str = field(default_factory = str)