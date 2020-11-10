# encoding: utf-8

import os
import requests

from ..exceptions import APIBaseURLStatusError


TCGA_API_TOKEN = os.environ.get("TCGA_API_TOKEN", None)
TCGA_API_BASE_URL = os.environ.get("TCGA_API_BASE_URL", "https://api.gdc.cancer.gov/")


request = requests.get(f"{TCGA_API_BASE_URL}/status")


if request.status_code != 200:
    raise APIBaseURLStatusError(
        f"{TCGA_API_BASE_URL} status: {request.status_code}."
        "The resource seems to be unavailable"
    )

session = requests.Session()
session.params = {"api_token": TCGA_API_TOKEN, "api_base_url": TCGA_API_BASE_URL}

from .tcga import Data  # isort:skip # noqa
