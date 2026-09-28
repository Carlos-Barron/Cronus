import pytest
from pydantic import ValidationError

from cronus.domain.models import User

OK_DATA = {
    "id": 1,
    "name": "Charly",
    "email": "testChar@test.com",
    "city": "Morelia",
    "company_name": "ACME"
}

@pytest.fixture
def api_payload() -> dict:
    """ Un usuario tal como lo devuelve JSONPlaceholder """
    return {
        "id": 1,
        "name": "Charls David",
        "username": "CharlyBarron",
        "email": "CharTest@test.com",
        "address": {
            "street": "Loma blanca",
            "suite": "79",
            "city": "Morelia",
            "zipcode": "58087"
        },
        "phone": "9999999999",
        "website": "Test.com.mx",
        "company": {
            "name": "Wizeline",
            "catchPhrase": "The best software company",
            "bs": "real time solutions"
        }

    }


@pytest.mark.parametrize(
    "field, value",
    [
        ("id", 0),
        ("name", "A"),
        ("email", "not an email"),
        ("city", "none")
    ],
)

def test_invalid_user(field, value):
    data = OK_DATA | {field: value}
    with pytest.raises(ValidationError):
        User(**data)