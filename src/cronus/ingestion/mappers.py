from collections.abc import Iterable

from cronus.domain.models import User
from cronus.ingestion.dto import ApiUser

def to_domain(dto: ApiUser) -> User:
    """ Convierte un usuario del APi en un usuario de dominio """
    return User(
        id=dto.id,
        name=dto.name,
        email=dto.email,
        city=dto.address.city,
        company_name=dto.company.name
    )

def to_domain_list(dtos: Iterable[ApiUser]) -> list[User]:
    """ Convierte varios usuarios. Falla si alguno no cumple el dominio. """
    return [to_domain(dto) for dto in dtos]