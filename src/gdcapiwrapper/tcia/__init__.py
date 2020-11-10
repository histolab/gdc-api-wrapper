# encoding: utf-8

import os
import requests


TCIA_API_TOKEN = os.environ.get("TCIA_API_TOKEN", None)
TCIA_API_BASE_URL = os.environ.get(
    "TCIA_API_BASE_URL", "https://services.cancerimagingarchive.net/services/v4/TCIA"
)


session = requests.Session()
session.params = {"api_token": TCIA_API_TOKEN, "api_base_url": TCIA_API_BASE_URL}

from .tcia import Data  # isort:skip # noqa
