# encoding: utf-8

import os
import re
from datetime import datetime
from typing import Tuple

import requests
from responses import Response
from tqdm import tqdm

from . import session
from ..util import copyfileobj

__data_endpoint__ = "data"

base_url = f"{session.params.get('api_base_url')}/{__data_endpoint__}"


class Data(object):
    """Provides Data objects for https://api.gdc.cancer.gov/data/ `Data Endpoints`

    Includes endpoints for file(s) download
    """

    @classmethod
    def download(
        cls, uuid: str, path: str = ".", name: str = None
    ) -> Tuple[Response, str]:
        """Download file and return the related api response and the file path

        Parameters
        ---------
        uuid : str
            File UUID
        path: str
            Local path where save file (default: current path)
        name: str
            Filename. If not provided it will be saved with UUID as name

        Returns
        -------
        tuple
            response, filename absolute path
        """
        url = f"{base_url}/{uuid}"

        local_filename = name if name else uuid
        with requests.get(url, stream=True) as r:
            total_size = int(r.headers.get("content-length", 0))
            bar = tqdm(total=total_size, unit="iB", unit_scale=True)
            with open(os.path.join(path, local_filename), "wb") as f:
                copyfileobj(r.raw, f, bar)
        return r, local_filename

    @classmethod
    def download_multiple(
        cls, uuid_list: list, path: str = "."
    ) -> Tuple[Response, str]:
        """Download multiple files and return the related api response and the file path

        Parameters
        ---------
        uuid_list : list
            List of UUID(s) to save
        path: str
            Local path where save file (default: current path)

        Returns
        -------
        tuple
            response, filename absolute path
        """
        with requests.post(base_url, stream=True, data={"ids": uuid_list}) as r:
            d = r.headers["content-disposition"]
            fname = re.findall("filename=(.+)", d)[0]
            local_filename = (
                fname
                if fname
                else f"gdc_download_{datetime.now().strftime('%Y%m%d%H%M%S')}.tar.gz"
            )
            total_size = int(r.headers.get("content-length", 0))
            bar = tqdm(total=total_size, unit="iB", unit_scale=True)
            with open(os.path.join(path, local_filename), "wb") as f:
                for data in r.iter_content(chunk_size=1024):
                    size = f.write(data)
                    bar.update(size)
        return r, local_filename
