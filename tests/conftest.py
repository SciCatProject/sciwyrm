# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2024 SciCat Project (https://github.com/SciCatProject/sciwyrm)

import os
from pathlib import Path

import pytest
import scitacean
from fastapi.testclient import TestClient
from scitacean.testing.backend import add_pytest_option as add_backend_option
from scitacean.testing.sftp import add_pytest_option as add_sftp_option
from scitacean.transfer.sftp import SFTPFileTransfer

from sciwyrm.config import AppConfig, app_config

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


def _app_config_override():
    return AppConfig(
        template_dir=Path(__file__).resolve().parent.parent
        / "src"
        / "sciwyrm"
        / "assets"
        / "templates"
    )


@pytest.fixture(scope="session")
def app():
    from sciwyrm.main import app

    old_overrides = dict(app.dependency_overrides)
    app.dependency_overrides[app_config] = _app_config_override
    yield app
    app.dependency_overrides = old_overrides


@pytest.fixture
def sciwyrm_client(app):
    return TestClient(app)
