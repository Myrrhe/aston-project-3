"""A function to create a secret key"""
import string

import random


def truc() -> str:
    """A function to create a secret key"""
    return "".join(
        [
            random.SystemRandom().choice(
                "{}{}{}".format(string.ascii_letters, string.digits, string.punctuation)
            )
            for _ in range(50)
        ]
    )
