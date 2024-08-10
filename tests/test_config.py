from pmbuddy.config import CONFIG


class TestConfig:
    def test_default_config(self):
        """CONFIG must be a dictionary."""
        assert isinstance(CONFIG, dict)

    def test_config_content(self):
        """Minimum config must have 'request' and 'urls' keys."""
        assert "request" in CONFIG
        assert "urls" in CONFIG
