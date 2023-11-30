"""A function to create a secret key."""
import string

import random


def create_django_key() -> str:
    """Create a secret key."""
    return "".join(
        [
            random.SystemRandom().choice("{}{}{}".format(
                string.ascii_letters,
                string.digits,
                string.punctuation
            ))
            for _ in range(50)
        ]
    )
