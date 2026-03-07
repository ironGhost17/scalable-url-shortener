import random
import string
from sqlalchemy.orm import Session
from . import models


def generate_short_code(length: int = 6) -> str:
    """
    Generate a random alphanumeric short code.
    """
    return ''.join(
        random.choices(string.ascii_letters + string.digits, k=length)
    )


def create_short_url(db: Session, original_url: str):
    """
    Create a short URL entry.
    - If original URL already exists, return existing entry.
    - Ensure generated short code is unique.
    """

    # 🔹 Check if URL already exists
    existing_url = db.query(models.URL).filter(
        models.URL.original_url == original_url
    ).first()

    if existing_url:
        return existing_url

    # 🔹 Generate unique short code
    while True:
        short_code = generate_short_code()

        existing_code = db.query(models.URL).filter(
            models.URL.short_code == short_code
        ).first()

        if not existing_code:
            break

    # 🔹 Create new DB entry
    db_url = models.URL(
        original_url=original_url,
        short_code=short_code
    )

    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    return db_url


def get_url_by_code(db: Session, short_code: str):
    """
    Retrieve URL entry using short code.
    """
    return db.query(models.URL).filter(
        models.URL.short_code == short_code
    ).first()