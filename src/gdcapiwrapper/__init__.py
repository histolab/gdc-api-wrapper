# encoding: utf-8

import os
import requests

__version__ = "0.1b"
GDC_API_TOKEN = os.environ.get("GCC_API_TOKEN", None)
GDC_API_BASE_URL = os.environ.get("GDC_API_BASE_URL", "https://api.gdc.cancer.gov/")


class APIBaseURLStatusError(Exception):
    pass


class APITokenMissingError(Exception):
    pass


request = requests.get(f"{GDC_API_BASE_URL}/status")


if request.status_code != 200:
    raise APIBaseURLStatusError(
        f"{GDC_API_BASE_URL} status: {request.status_code}."
        "The resource seems to be unavailable"
    )

session = requests.Session()
session.params = {"api_token": GDC_API_TOKEN, "api_base_url": GDC_API_BASE_URL}

from .data import Data  # isort:skip # noqa
