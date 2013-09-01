from mock import Mock


def mock_config(data):
    config = Mock()
    config.get.return_value = data
    config.write.return_value = None
    return config
