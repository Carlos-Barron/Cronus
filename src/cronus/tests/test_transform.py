import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from cronus.domain.models import User
from cronus.domain.transform import enrich, to_dataframe, users_by_city

@pytest.fixture
def users() -> list[User]:
    return [
        User(id=1, name="Charly", email="charly@test.com", city="Morelia", company_name="ACME"),
        User(id=2, name="David", email="david@test.com", city="Morelia", company_name="ACME")
    ]

def test_to_dataframe(users):
    df = to_dataframe(users)

    assert list(df.columns) == ["id", "name", "email", "city", "company_name"]
    assert len(df) == 2
    assert df["id"].dtype == "int64"

def test_toempty_dataframe():
    df = to_dataframe([])

    assert df.empty
    assert list(df.columns) == ["id", "name", "email", "city", "company_name"]

def test_enrich(users):
    df = enrich(to_dataframe(users))

    assert df["email_domain"].tolist() == ["gmail.com", "company.com"]

def test_enrich_with_original_modified(users):
    df = to_dataframe(users)
    copy = df.copy()

    enrich(df)

    assert_frame_equal(df, copy)

def test_users_by_city(users):
    result = users_by_city(enrich(to_dataframe(users)))

    expected = pd.DataFrame({"city": ["Morelia"], "users": [2]})
    assert_frame_equal(result.reset_index(drop=True), expected)