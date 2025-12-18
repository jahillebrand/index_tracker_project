import os

class AppConfig:
    """Application configuration loaded from environment variables"""

    def __init__(self):
        # Required settings (will fail fast if missing)
        self.api_key = self._get_required('API_KEY')
        self.database_url = self._get_required('DATABASE_URL')

        # Optional settings with defaults
        self.debug = self._get_bool('DEBUG', False)
        self.port = self._get_int('PORT', 8000)
        self.log_level = os.environ.get('LOG_LEVEL', 'INFO')
        self.max_workers = self._get_int('MAX_WORKERS', 4)

    def _get_required(self, key):
        """Get a required environment variable or raise an error"""
        value = os.environ.get(key)
        if value is None:
            raise ValueError(f"Required environment variable '{key}' is not set")
        return value

    def _get_bool(self, key, default):
        """Convert environment variable to boolean"""
        value = os.environ.get(key)
        if value is None:
            return default
        return value.lower() in ('true', '1', 'yes', 'on')

    def _get_int(self, key, default):
        """Convert environment variable to integer"""
        value = os.environ.get(key)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            raise ValueError(f"Environment variable '{key}' must be an integer, got '{value}'")

    def __repr__(self):
        """Safe string representation (masks sensitive data)"""
        return (f"AppConfig(debug={self.debug}, port={self.port}, "
                f"log_level={self.log_level}, api_key={'*' * 8})")
