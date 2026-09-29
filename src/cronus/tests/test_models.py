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

def test_user_valid():
    user = User(**OK_DATA)
    assert user.name == "Charly"
    assert user.city == "Morelia"

def test_user_inmutable():
    user = User(**OK_DATA)
    with pytest.raises(ValidationError):
        user.name = "Another"