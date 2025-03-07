from sta.seedwork.application.dto import Mapper
from .dto import AuthenticationDTO

class AuthenticationMapperDTOJson(Mapper):
    def external_to_dto(self, external : dict) -> AuthenticationDTO :
        dto = AuthenticationDTO(external.get('username'), external.get('password'))

        return dto

    def dto_to_external(self):
        return 'DTO to external'