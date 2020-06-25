# encoding: utf-8


import re
from datetime import datetime

import requests
from responses import Response
from tqdm import tqdm

from . import session
from .util import copyfileobj
from typing import Tuple

__data_endpoint__ = "data"

base_url = f"{session.params.get('api_base_url')}/{__data_endpoint__}"


class Data(object):
    @classmethod
    def download(cls, uuid: str, name: str = None) -> Tuple[Response, str]:
        url = f"{base_url}/{uuid}"
        local_filename = uuid if not name else name
        with requests.get(url, stream=True) as r:
            total_size = int(r.headers.get("content-length", 0))
            bar = tqdm(total=total_size, unit="iB", unit_scale=True)
            with open(local_filename, "wb") as f:
                copyfileobj(r.raw, f, bar)
        return r, local_filename

    @classmethod
    def download_multiple(cls, uuid_list: list) -> str:
        url = f"{session.params.get('api_base_url')}/{__data_endpoint__}"
        with requests.post(url, stream=True, data={"ids": uuid_list}) as r:
            d = r.headers["content-disposition"]
            fname = re.findall("filename=(.+)", d)[0]
            local_filename = (
                fname
                if fname
                else f"gdc_download_{datetime.now().strftime('%Y%m%d%H%M%S')}.tar.gz"
            )
            total_size = int(r.headers.get("content-length", 0))
            bar = tqdm(total=total_size, unit="iB", unit_scale=True)
            with open(local_filename, "wb") as f:
                for data in r.iter_content(chunk_size=1024):
                    size = f.write(data)
                    bar.update(size)
        return local_filename
