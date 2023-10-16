# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 SciCat Project (https://github.com/SciCatProject/sciwyrm)

import os

import pytest
import scitacean
from scitacean.testing.backend import add_pytest_option as add_backend_option
from scitacean.testing.sftp import add_pytest_option as add_sftp_option
from scitacean.transfer.sftp import SFTPFileTransfer

from .seed import seed_scicat

# Silence warning from Jupyter
os.environ["JUPYTER_PLATFORM_DIRS"] = "1"

pytest_plugins = (
    "scitacean.testing.backend.fixtures",
    "scitacean.testing.sftp.fixtures",
)


def pytest_addoption(parser: pytest.Parser) -> None:
    add_backend_option(parser)
    add_sftp_option(parser)


@pytest.fixture(scope="session")
def _local_scicat(
    scicat_access,
    sftp_access,
    sftp_connect_with_username_password,
    scicat_backend,
    sftp_fileserver,
):
    client = scitacean.Client.from_credentials(
        url=scicat_access.url,
        **scicat_access.user.credentials,
        file_transfer=SFTPFileTransfer(
            host=sftp_access.host,
            port=sftp_access.port,
            connect=sftp_connect_with_username_password,
        ),
    )
    seed_scicat(client, scicat_access)


@pytest.fixture(scope="function")
def scicat_client(
    real_client, _local_scicat, require_scicat_backend, require_sftp_fileserver
) -> scitacean.Client:
    return real_client
