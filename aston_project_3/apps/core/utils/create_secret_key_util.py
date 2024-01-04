"""A function to create a secret key."""
import string

import random


def create_django_key() -> str:
    """Create a secret key."""
    return "".join(
        [
            random.SystemRandom().choice(
                f"{string.ascii_letters}{string.digits}{string.punctuation}",
            )
            for _ in range(50)
        ]
    )
