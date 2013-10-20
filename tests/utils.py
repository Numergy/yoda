import mock
from mock import Mock
from mock import MagicMock
from yoda import Config


@mock.patch('yoda.config.Config.__init__',
            Mock(return_value=None))
def mock_config(data):
    config = Config()
    config.get = MagicMock(return_value=data)
    config.write = MagicMock(return_value=None)
    return config
