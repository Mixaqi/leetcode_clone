from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()


def hash_password(password: str) -> str:
    """
    Hash a plain-text password using Argon2.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return ph.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """
    Verify a password against a given Argon2 hash.

    Args:
        password (str): The plain-text password to check.
        hashed (str): The Argon2 hash to verify against.

    Returns:
        bool: True if password matches the hash, False otherwise.
    """
    try:
        ph.verify(hashed, password)
        return True
    except VerifyMismatchError:
        return False
