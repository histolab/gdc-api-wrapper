# encoding: utf-8

import os
from unittest.mock import patch

import pytest
from requests.exceptions import ChunkedEncodingError

from gdcapiwrapper.data import Data

from ..mockserver import get_free_port, start_mock_server


class TestData(object):
    @classmethod
    def setup_class(cls):
        cls.mock_server_port = get_free_port()
        start_mock_server(cls.mock_server_port)

    def test_download(self, tmpdir):
        base_url = "http://localhost:{port}/data".format(port=self.mock_server_port)

        with patch.dict("gdcapiwrapper.data.__dict__", {"base_url": base_url}):
            response, filename = Data.download(
                uuid="fakeuuid", path=tmpdir, name="fakefilename"
            )

        assert response.ok is True
        assert os.path.exists(os.path.join(tmpdir, "fakefilename")) is True

    def test_download_multiple(self, tmpdir):
        base_url = "http://localhost:{port}".format(port=self.mock_server_port)
        try:
            with patch.dict("gdcapiwrapper.data.__dict__", {"base_url": base_url}):
                response, filename = Data.download_multiple(
                    uuid_list=["1", "2"], path=tmpdir
                )
        except ChunkedEncodingError:
            pytest.skip("Flaky ConnectionResetError")

        assert response.ok is True
        assert os.path.exists(os.path.join(tmpdir, "fake.gzip")) is True
