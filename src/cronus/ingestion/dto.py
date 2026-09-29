from pydantic import BaseModel, ConfigDict, Field, TypeAdapter

class ApiAddress(BaseModel):
    """ Bloque 'address' del API """

    city: str

class ApiCompany(BaseModel):
    """ Bloque company del API. """

    name: str
    catch_phrase: str = Field(alias="catchPhrase")

class ApiUser(BaseModel):
    """ Espejo de playload de /users del API. 
    
    extra="ignore" es deliberado: si el API agrega campos nuevos,
    el pipeline no debe romperse.

    """

    model_config = ConfigDict(extra="ignore")

    id: int
    name: str
    username: str
    email: str
    address: ApiAddress
    company: ApiCompany

API_USER_LIST = TypeAdapter(list[ApiUser])

    