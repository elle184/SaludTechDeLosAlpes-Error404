from .dto import AuthenticationDTO

class AuthenticationMapperDTOJson():
    def external_to_dto(self, external : dict) -> AuthenticationDTO :
        dto = AuthenticationDTO()

        return external

    def dto_to_external(self):
        return 'DTO to external'