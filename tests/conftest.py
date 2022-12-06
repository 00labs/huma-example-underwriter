import os

import pytest

from underwriter.settings import Env


@pytest.fixture(scope="session", autouse=True)
def ensure_test_env() -> None:
    """make sure the env is set to TEST"""
    assert os.getenv("ENV") == Env.TEST