import pytest

from underwriter import settings


@pytest.fixture(scope="session", autouse=True)
def ensure_test_env() -> None:
    """make sure the env is set to TEST"""
    assert settings.settings.env == settings.Env.TEST
