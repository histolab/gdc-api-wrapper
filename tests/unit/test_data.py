# encoding: utf-8

import os
from unittest.mock import patch

from gdcapiwrapper.data import Data

from ..mockserver import get_free_port, start_mock_server


class TestMockServer(object):
    @classmethod
    def setup_class(cls):
        cls.mock_server_port = get_free_port()
        start_mock_server(cls.mock_server_port)

    def test_download(self, tmpdir):
        base_url = "http://localhost:{port}/data".format(port=self.mock_server_port)

        with patch.dict("gdcapiwrapper.data.__dict__", {"base_url": base_url}):
            response, filename = Data.download(
                uuid="fakeuuid", name=os.path.join(tmpdir, "fakefilename")
            )

        assert response.ok is True
        assert filename == os.path.join(tmpdir, "fakefilename")
