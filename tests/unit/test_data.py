# Third-party imports...
from unittest.mock import patch

# Local imports...
from gdcapiwrapper.data import Data
from ..mockserver import get_free_port, start_mock_server
import os


class TestMockServer(object):
    @classmethod
    def setup_class(cls):
        cls.mock_server_port = get_free_port()
        start_mock_server(cls.mock_server_port)

    def test_download(self, tmpdir):
        base_url = "http://localhost:{port}/data".format(port=self.mock_server_port)

        # Patch USERS_URL so that the service uses the mock server URL instead of the real URL.
        with patch.dict("gdcapiwrapper.data.__dict__", {"base_url": base_url}):
            response, filename = Data.download(
                uuid="aaa", name=os.path.join(tmpdir, "bbb")
            )

        assert response.ok is True
        assert filename == os.path.join(tmpdir, "bbb")
