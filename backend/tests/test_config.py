from backend.app.core.config import get_settings


def test_config_defaults():
    settings = get_settings()
    assert settings.database_url
    assert settings.redis_url
    assert settings.secret_key
