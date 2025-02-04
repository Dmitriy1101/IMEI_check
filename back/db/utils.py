import hashlib


def generate_token_id(token: str) -> str:
    """
    Generate token_id as SHA-256.
    """
    return hashlib.sha256(token.encode()).hexdigest()
