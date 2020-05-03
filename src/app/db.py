import pymongo
import datetime


client = pymongo.MongoClient('mongodb', 27017)
db = client['db-secrets']
secrets = db['secrets']


def get_from_db(secret_key: str) -> dict:
    """It takes one parameter (secret_key), checks the existence of a secret with this secret_key
    and returns the encoded secret and code_phrase or error (secret with this secret_key doesn't exist)

    Parameters
    ----------
    secret_key: str
        the unique identifier of the secret

    Returns
    -------
    dict
        a dict like {'code_phrase': code_phrase, 'secret': secret}
        or error
    """
    result = secrets.find_one({'secret_key': secret_key})
    if not result:
        return {"error": "secret with this secret_key doesn't exist"}
    else:
        return {'code_phrase': result['code_phrase'], 'secret': result['secret']}


def add_to_db_with_ttl(secret_key: str, code_phrase: str, secret: str, seconds: int):
    """It takes four parameters and add data with ttl index to database
    (data may be automatically deleted after a certain period of time)

    Parameters
    ----------
    secret_key: str
        the unique identifier of the secret
    code_phrase: str
        code phrase for accessing a secret (max_length=200)
    secret: str
        some your secret (max_length=800)
    seconds: int
        time-to-live index in seconds (default = 0 the secret will not be deleted)
        must be >= 0
    """
    unique_ttl_index = secret_key[1:5]
    secrets.create_index(unique_ttl_index, expireAfterSeconds=seconds)

    secret_with_ttl = {
        unique_ttl_index: datetime.datetime.utcnow(),
        'secret_key': secret_key,
        'code_phrase': code_phrase,
        'secret': secret
    }
    secrets.insert_one(secret_with_ttl)


def add_to_db(secret_key: str, code_phrase: str, secret: str):
    """It takes three parameters and add data without ttl index to database
    (the secret will not be deleted automatically)

    Parameters
    ----------
    secret_key: str
        the unique identifier of the secret
    code_phrase: str
        code phrase for accessing a secret (max_length=200)
    secret: str
        some your secret (max_length=800)
    """
    secret_without_ttl = {
        'secret_key': secret_key,
        'code_phrase': code_phrase,
        'secret': secret
    }
    secrets.insert_one(secret_without_ttl)


def delete_from_db(secret_key: str):
    """It takes one parameter (secret_key), and delete one secret with this secret_key

    Parameters
    ----------
    secret_key: str
        the unique identifier of the secret
    """
    secrets.delete_one({'secret_key': secret_key})
