import uvicorn
import uuid

from fastapi import FastAPI
from pydantic import BaseModel
from pydantic import Field

from app.db import get_from_db
from app.db import add_to_db
from app.db import add_to_db_with_ttl
from app.db import delete_from_db

from app.crypt import str_encode
from app.crypt import str_decode


app = FastAPI(title="Storage of secrets")


# @app.on_event("startup")
# async def create_db_client():
#     # start client here and reuse in future requests
#
#
# @app.on_event("shutdown")
# async def shutdown_db_client():
#     # stop your client here


class SecretInput(BaseModel):
    """
    A class used to represent the data model of Secret input
    ...
    Attributes
    ----------
    code_phrase: str
        code phrase for accessing a secret (max_length=200)
    secret: str
        some your secret (max_length=800)
    remove_after_seconds: int
        time-to-live index in seconds (default = 0 the secret will not be deleted)
        must be >= 0

    """
    code_phrase: str = Field(..., title="Text", description="Code phrase", max_length=200)
    secret: str = Field(..., title="Text", description="Secret", max_length=800)
    remove_after_seconds: int = 0


@app.get(
    "/secrets/{secret_key}",
    response_description="Secret with a secret key",
    description="Get secret with a secret key from database",
)
def secrets(secret_key: str, code_phrase: str) -> dict:
    """It takes two parameters (secret_key, code_phrase) and returns the decoded secret

    Parameters
    ----------
    secret_key: str
        the unique identifier of the secret
    code_phrase: str
        code phrase for accessing a secret (max_length=200)

    Returns
    -------
    dict
        a dict like {"secret": returned_secret}
    """
    data_from_database = get_from_db(secret_key)
    if "error" in data_from_database.keys():
        return data_from_database

    decoded_code_phrase = str_decode(data_from_database["code_phrase"])
    if decoded_code_phrase == code_phrase:
        delete_from_db(secret_key)
        decoded_secret = str_decode(data_from_database["secret"])
        return {"secret": decoded_secret}
    else:
        return {"error": "code phrase isn't correct"}


@app.post(
    "/generate/",
    response_description="Generated secret key of secret",
    description="Add secret and code phrase",
)
def generate(secret: SecretInput) -> dict:
    """It takes two  or three parameters (secret, code_phrase, optional parameter: remove_after_seconds)
    and returns the secret_key (unique identifier of the secret)

    Parameters
    ----------
    secret: SecretInput
        object of the SecretInput class that represent the data model of input

    Returns
    -------
    dict
        a dict like {"secret_key": generated_secret_key}
    """
    secret_key = str(uuid.uuid4())  # generate random sequence with uuid
    encoded_code_phrase = str_encode(secret.code_phrase)
    encoded_secret = str_encode(secret.secret)

    if secret.remove_after_seconds < 0:
        return {"error": "remove_after_seconds isn't correct"}
    if secret.remove_after_seconds > 0:
        add_to_db_with_ttl(secret_key, encoded_code_phrase, encoded_secret, secret.remove_after_seconds)
    if secret.remove_after_seconds == 0:
        add_to_db(secret_key, encoded_code_phrase, encoded_secret)

    return {"secret_key": secret_key}
