import os
import pathlib
import uuid

from django.db import models
from slugify import slugify


def get_filename(filename, request):
    filename_uuid = str(uuid.uuid4())
    if filename and (suffix := pathlib.Path(filename).suffix):
        filename_uuid = f'{filename_uuid}{suffix}'
    return filename_uuid


def generate_filename(__filename: str | os.PathLike | None = None, /) -> str:
    filename = str(uuid.uuid4())
    if __filename and (suffix := pathlib.Path(__filename).suffix):
        filename = f'{filename}{suffix}'
    return filename


def generate_slug(text: str):
    return slugify(text)


def image_upload_to(instance: models.Model, filename: str) -> str:
    new_filename = generate_filename(filename)
    return f'{instance.__class__.__name__.lower()}/{new_filename}'
