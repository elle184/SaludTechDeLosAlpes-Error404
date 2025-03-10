from bff.seedwork.application.dto import Mapper as mapper
from .dto import UserDTO

class LoginMapperDTOJson(mapper) : 
    def external_to_dto(self, external : dict) -> UserDTO : 
        user_dto = UserDTO()
        user_dto.username = external.get('username')
        user_dto.password = external.get('password')

        return user_dto

    def dto_to_external(self, dto : UserDTO) -> dict :
        return dto.__dict__        
