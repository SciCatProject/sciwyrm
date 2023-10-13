# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 SciCat Project (https://github.com/SciCatProject/sciwyrm)

import os

import pytest
from scitacean.testing.backend import add_pytest_option as add_backend_option
from scitacean.testing.sftp import add_pytest_option as add_sftp_option

# Silence warning from Jupyter
os.environ["JUPYTER_PLATFORM_DIRS"] = "1"

pytest_plugins = (
    "scitacean.testing.backend.fixtures",
    "scitacean.testing.sftp.fixtures",
)


def pytest_addoption(parser: pytest.Parser) -> None:
    add_backend_option(parser)
    add_sftp_option(parser)
