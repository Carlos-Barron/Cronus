""" Transformaciones de dominio: de modelos validados a un DataFrame """

from collections.abc import Sequence

import pandas as pd
import numpy as np

from cronus.domain.models import User

COLUMNS = list(User.model_fields)

def to_dataframe(users: Sequence[User]) -> pd.DataFrame:
    """ Convierte usuarios de dominio en una tabla. FUnción pura. """
    rows = [user.model_dump() for user in users]
    return pd.DataFrame(rows, columns=COLUMNS)

FREE_EMAIL_DOMAINS = frozenset({"gmail.com", "hotmail.com", "yahoo.com", "outlook.com"})

def enrich(df: pd.DataFrame) -> pd.DataFrame:
    """ Agrega columnas derivadas. No modifica el DataFrame recibido. """
    domain = df["email"].str.lower().str.split("@").str[1]
    city = df["city"].str.strip().str.title()

    return df.assign(
        email_domain=domain,
        is_free_email=domain.isin(FREE_EMAIL_DOMAINS),
        city=city,
        name_length=df["name"].str.len(),
        first_name=df["name"].str.split().str[0],
        segment=np.select(
            [domain.isin(FREE_EMAIL_DOMAINS), df["company_name"].str.len() > 10],
            ["personal", "big_corporate"],
            default="corporate"
        )
    )

def users_by_city(df: pd.DataFrame) -> pd.DataFrame:
    """ Cuenta usuarios por ciudad, de mayor a menor. """
    return (
        df.groupby("city")
        .size()
        .reset_index(name="users")
        .sort_values("users", ascending=False)
    )