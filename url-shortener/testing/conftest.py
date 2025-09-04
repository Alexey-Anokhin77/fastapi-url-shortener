from os import getenv

import pytest

if getenv("TESTING") != "1":
    msg = "Environment is not ready for testing"
    pytest.exit(msg)
