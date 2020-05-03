import base64


def str_encode(some_str: str) -> str:
    """It takes string and returns encoded string

    Parameters
    ----------
    some_str: str
        any string

    Returns
    -------
    str
        encoded string
    """
    string_to_bytes = some_str.encode("UTF-8")  # Encoding the string into bytes
    encode_bytes = base64.b64encode(string_to_bytes)  # Base64 Encode the bytes
    return encode_bytes.decode("UTF-8")  # Decoding the Base64 bytes to string


def str_decode(some_str: str) -> str:
    """It takes encoded string and returns decoded string

    Parameters
    ----------
    some_str: str
        encoded string

    Returns
    -------
    str
        decoded string
    """
    encoding_base64 = some_str.encode("UTF-8")  # Encoding the Base64 encoded string into bytes
    decoding_base64 = base64.b64decode(encoding_base64)  # Decoding the Base64 bytes
    return decoding_base64.decode("UTF-8")  # Decoding the bytes to string
