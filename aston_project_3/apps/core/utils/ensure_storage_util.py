"""Ensure storage."""
import os


def ensure_storage() -> None:
    """Ensure storage."""
    if not os.path.exists("storage"):
        os.makedirs("storage")
    if not os.path.exists("storage/bot"):
        os.makedirs("storage/bot")
