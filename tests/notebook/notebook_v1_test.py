# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 SciCat Project (https://github.com/SciCatProject/sciwyrm)

from io import StringIO
from typing import Any

import nbformat
import pytest
from fastapi.testclient import TestClient
from nbconvert import PythonExporter
from scitacean.testing.backend.seed import (
    INITIAL_DATASETS,
)

from sciwyrm.main import app


@pytest.fixture
def sciwyrm_client():
    return TestClient(app)


@pytest.fixture
def scicat_token(require_scicat_backend, real_client):
    return real_client.scicat._token.get_str()


def exec_notebook(nb_code: str) -> dict[str, Any]:
    buffer = StringIO(nb_code)
    nb = nbformat.read(buffer, as_version=4)
    body, _ = PythonExporter().from_notebook_node(nb)
    namespace = {}
    exec(body, namespace)  # noqa: S102
    return namespace


def test_notebook_contains_expected_url(sciwyrm_client):
    url = "https://test-url.sci.cat"
    response = sciwyrm_client.post(
        "/notebook/v1",
        json={
            "scicat_url": url,
            "file_server_host": "login",
            "file_server_port": 22,
            "dataset_pids": [],
        },
    )
    assert response.status_code == 200
    assert url in response.text


def test_notebook_contains_expected_pids(sciwyrm_client):
    pids = ["7192983", "7ca7/31a.2as"]
    response = sciwyrm_client.post(
        "/notebook/v1",
        json={
            "scicat_url": "https://test-url.sci.cat",
            "file_server_host": "login",
            "file_server_port": 22,
            "dataset_pids": pids,
        },
    )
    assert response.status_code == 200
    assert "7192983" in response.text
    assert "7ca7/31a.2as" in response.text


def test_notebook_contains_only_expected_pids(sciwyrm_client):
    pids0 = ["7192983", "7ca7/31a.2as"]
    pids1 = ["9391"]

    response = sciwyrm_client.post(
        "/notebook/v1",
        json={
            "scicat_url": "https://test-url.sci.cat",
            "file_server_host": "login",
            "file_server_port": 22,
            "dataset_pids": pids0,
        },
    )
    assert response.status_code == 200

    response = sciwyrm_client.post(
        "/notebook/v1",
        json={
            "scicat_url": "https://test-url.sci.cat",
            "file_server_host": "login",
            "file_server_port": 22,
            "dataset_pids": pids1,
        },
    )
    assert response.status_code == 200
    # Previous request has not affected the template on the server.
    assert "7192983" not in response.text
    assert "7ca7/31a.2as" not in response.text
    assert "9391" in response.text


def test_notebook_contains_expected_file_serve_host(sciwyrm_client):
    file_server_host = "test.host.cat"
    response = sciwyrm_client.post(
        "/notebook/v1",
        json={
            "scicat_url": "https://test-url.sci.cat",
            "file_server_host": file_server_host,
            "file_server_port": 22,
            "dataset_pids": [],
        },
    )
    assert response.status_code == 200
    assert file_server_host in response.text


def test_notebook_contains_expected_file_serve_port(sciwyrm_client):
    file_server_port = 2200
    response = sciwyrm_client.post(
        "/notebook/v1",
        json={
            "scicat_url": "https://test-url.sci.cat",
            "file_server_host": "login",
            "file_server_port": file_server_port,
            "dataset_pids": [],
        },
    )
    assert response.status_code == 200
    assert str(file_server_port) in response.text


def test_notebook_run(sciwyrm_client, scicat_access, scicat_token, sftp_access):
    pids = [str(INITIAL_DATASETS["raw"].pid), str(INITIAL_DATASETS["derived"].pid)]
    response = sciwyrm_client.post(
        "/notebook/v1",
        json={
            "scicat_url": scicat_access.url,
            "file_server_host": sftp_access.host,
            "file_server_port": sftp_access.port,
            "scicat_token": scicat_token,
            "dataset_pids": pids,
        },
    )
    assert response.status_code == 200

    namespace = exec_notebook(response.text)
    datasets = namespace["datasets"]
    assert len(datasets) == 2
    assert str(datasets[0].pid) in pids
    assert str(datasets[1].pid) in pids
