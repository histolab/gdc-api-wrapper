# encoding: utf-8

import os
from unittest import mock

import pytest
from requests.exceptions import ChunkedEncodingError

from gdcapiwrapper.tcga import Data as TCGAData
from gdcapiwrapper.tcia import Data as TCIAData

from ..mockserver import get_free_port, start_mock_server


class TestTCGAData(object):
    @classmethod
    def setup_class(cls):
        cls.mock_server_port = get_free_port()
        start_mock_server(cls.mock_server_port)

    def test_download(self, tmpdir):
        base_url = "http://localhost:{port}/data".format(port=self.mock_server_port)

        with mock.patch.dict(
            "gdcapiwrapper.tcga.tcga.__dict__", {"base_url": base_url}
        ):
            response, filename = TCGAData.download(
                uuid="fakeuuid", path=tmpdir, name="fakefilename"
            )

        assert response.ok is True
        assert os.path.exists(os.path.join(tmpdir, "fakefilename")) is True

    def test_download_multiple(self, tmpdir):
        base_url = "http://localhost:{port}".format(port=self.mock_server_port)
        try:
            with mock.patch.dict(
                "gdcapiwrapper.tcga.tcga.__dict__", {"base_url": base_url}
            ):
                response, filename = TCGAData.download_multiple(
                    uuid_list=["1", "2"], path=tmpdir
                )
        except ChunkedEncodingError:
            pytest.skip("Flaky ConnectionResetError")

        assert response.ok is True
        assert os.path.exists(os.path.join(tmpdir, "fake.gzip")) is True


class TestTCIAData(object):
    @classmethod
    def setup_class(cls):
        cls.mock_server_port = get_free_port()
        start_mock_server(cls.mock_server_port)

    def test_json_sop_instance_uids(self):
        base_url = "http://localhost:{port}/query".format(port=self.mock_server_port)
        with mock.patch.dict(
            "gdcapiwrapper.tcia.tcia.__dict__", {"base_url": base_url}
        ):
            response, json = TCIAData.sop_instance_uids(series_instance_uid="fakeuid")

        assert response.ok is True
        assert json == []

    def test_other_formats_sop_instance_uids(self, tmpdir):
        base_url = "http://localhost:{port}/query".format(port=self.mock_server_port)
        with mock.patch.dict(
            "gdcapiwrapper.tcia.tcia.__dict__", {"base_url": base_url}
        ):
            response, filename = TCIAData.sop_instance_uids(
                series_instance_uid="fakeuid", format_="CSV", path=tmpdir
            )

        assert response.ok is True
        assert os.path.exists(os.path.join(tmpdir, "fakeuid.csv")) is True

    def test_download_single_image(self, tmpdir):
        base_url = "http://localhost:{port}/query".format(port=self.mock_server_port)
        with mock.patch.dict(
            "gdcapiwrapper.tcia.tcia.__dict__", {"base_url": base_url}
        ):
            response, filename = TCIAData.download_single_image(
                series_instance_uid="fakeuid",
                sop_instance_uid="sopfakeuid",
                path=tmpdir,
            )

        assert response.ok is True
        assert os.path.exists(os.path.join(tmpdir, "sopfakeuid.dcm")) is True

    def download_series_instance_images(self, tmpdir):
        base_url = "http://localhost:{port}/query".format(port=self.mock_server_port)
        with mock.patch.dict(
            "gdcapiwrapper.tcia.tcia.__dict__", {"base_url": base_url}
        ):
            response, filename = TCIAData.download_series_instance_images(
                series_instance_uid="fakeuid", path=tmpdir
            )

        assert response.ok is True
        assert os.path.exists(os.path.join(tmpdir, "fakeuid.zip")) is True
