# encoding: utf-8

import os
from typing import Tuple

import requests
from responses import Response
from tqdm import tqdm

from ..enums import FORMAT_TYPE as FT
from . import session
from ..util import copyfileobj

__data_endpoint__ = "query"

base_url = f"{session.params.get('api_base_url')}/{__data_endpoint__}"


class Data(object):
    """Provides Data objects for
    https://services.cancerimagingarchive.net/services/v4/TCIA/ `Data Endpoints`
    """

    @classmethod
    def download_single_image(
        cls,
        series_instance_uid: str,
        sop_instance_uid: str,
        path: str = ".",
        name: str = None,
    ) -> Tuple[Response, str]:
        """Returns a SINGLE DICOM Object.

        A single image is identified by its SeriesInstanceUID and SOPInstanceUID.
        This API will always be used following the `sop_instance_uids`

        Parameters
        ---------
        series_instance_uid : str
            SeriesInstance UID
        sop_instance_uid: str
            SOPInstanceUID UID
        path: str
            Local path where save file (default: current path)
        name: str
            Filename. If not provided it will be saved with SOPInstance UID as name

        Returns
        -------
        tuple
            response, filename absolute path
        """
        url = (
            f"{base_url}/getSingleImage?SeriesInstanceUID={series_instance_uid}&"
            f"SOPInstanceUID={sop_instance_uid}"
        )
        local_filename = name if name else f"{sop_instance_uid}.dcm"
        with requests.get(url, stream=True) as r:
            total_size = int(r.headers.get("content-length", 0))
            bar = tqdm(total=total_size, unit="iB", unit_scale=True)
            with open(os.path.join(path, local_filename), "wb") as f:
                copyfileobj(r.raw, f, bar)
        return r, local_filename

    @classmethod
    def download_series_instance_images(
        cls, series_instance_uid: str, path: str = ".", name: str = None
    ) -> Tuple[Response, str]:
        """Returns a single Zip file with set of images for the given SeriesInstance.

        Parameters
        ---------
        series_instance_uid : str
            SeriesInstance UID
        path: str
            Local path where save file (default: current path)
        name: str
            Filename. If not provided it will be saved with SOPInstance UID as name

        Returns
        -------
        tuple
            response, filename absolute path
        """
        url = f"{base_url}/getImage?SeriesInstanceUID={series_instance_uid}"
        local_filename = name if name else f"{series_instance_uid}.zip"
        with requests.get(url, stream=True) as r:
            total_size = int(r.headers.get("content-length", 0))
            bar = tqdm(total=total_size, unit="iB", unit_scale=True)
            with open(os.path.join(path, local_filename), "wb") as f:
                copyfileobj(r.raw, f, bar)
        return r, local_filename

    @classmethod
    def sop_instance_uids(
        cls,
        series_instance_uid: str,
        format_: str = "JSON",
        path: str = ".",
        name: str = None,
    ) -> Tuple[Response, str]:
        """Return a list of SOPInstanceUID for a given SeriesInstanceUID

        Parameters
        ---------
        series_instance_uid : str
            SeriesInstance UID
        format_ : str
            Output format. This endpoint supports CSV/HTML/XML/JSON
        path: str
            Local path where save file (default: current path)
        name: str
            Filename. If not provided it will be saved with SeriesInstance UID as name

        Returns
        -------
        tuple
            response, filename absolute path or json
        """
        if format_.upper() not in FT.TCIA_ALLOWED_FORMATS.value:
            raise ValueError(
                f"Format not allowed. Allowed formats:"
                f"{list(FT.TCIA_ALLOWED_FORMATS.value)}, got {format_}."
            )
        url = (
            f"{base_url}/getSOPInstanceUIDs?SeriesInstanceUID={series_instance_uid}&"
            f"format={format_}"
        )
        r = requests.get(url)
        if format_.upper() == "JSON":
            return r, r.json()

        local_filename = name if name else f"{series_instance_uid}.{format_.lower()}"
        with open(os.path.join(path, local_filename), "wb") as f:
            f.write(r.content)
        return r, local_filename
