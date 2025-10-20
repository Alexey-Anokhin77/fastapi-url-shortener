import os
import pathlib
import sys

import pytest


@pytest.mark.skip(
    reason="user schema not implemented yet",
)
def test_user_schema() -> None:
    user_data = {"username": "foobar"}
    assert user_data["username"] == "spam and eggs"


@pytest.mark.skipif(
    sys.platform != "darwin",
    reason="skip test on MacOs due reason",
)
def test_platform() -> None:
    assert sys.platform == "darwin"


# Тест условия для запуска на винде


@pytest.mark.skipif(
    os.name != "nt",
    reason="run only on Windows",
)
def test_only_for_windows() -> None:
    path = pathlib.Path(__file__)
    assert isinstance(path, pathlib.WindowsPath)
