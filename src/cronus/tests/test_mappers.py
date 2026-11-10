from cronus.ingestion.dto import ApiUser
from cronus.ingestion.mappers import to_domain, to_domain_list

def test_to_domain(api_payload):
    dto = ApiUser.model_validate(api_payload)

    user = to_domain(dto)

    assert user.id == 1
    assert user.city == "Morelia"
    assert user.company_name == "Wizeline"

def test_to_domain_empty_list():
    assert to_domain_list([]) == []