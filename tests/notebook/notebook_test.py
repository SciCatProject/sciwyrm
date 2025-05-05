# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2024 SciCat Project (https://github.com/SciCatProject/sciwyrm)

import re
from io import StringIO
from typing import Any

import nbformat
import pytest
from nbconvert import PythonExporter

from ..seed import SEED

TEMPLATE_IDS = {"generic": "b32f6992-0355-4759-b780-ececd4957c23"}


@pytest.fixture
def scicat_token(scicat_client):
    return scicat_client.scicat._token.get_str()


def exec_notebook(nb_code: str) -> dict[str, Any]:
    buffer = StringIO(nb_code)
    nb = nbformat.read(buffer, as_version=4)
    body, _ = PythonExporter().from_notebook_node(nb)
    namespace = {}
    exec(body, namespace)  # noqa: S102
    return namespace


def test_list_notebook_templates(sciwyrm_client):
    response = sciwyrm_client.get("/notebook/templates")
    assert response.status_code == 200
    assert response.json() == [
        {
            "template_id": TEMPLATE_IDS["generic"],
            "submission_name": "generic",
            "display_name": "Generic",
            "version": "1",
        }
    ]


def test_template_parameter_schema(sciwyrm_client):
    response = sciwyrm_client.get(f"/notebook/schema/{TEMPLATE_IDS['generic']}")
    assert response.is_success
    params = response.json()["properties"]
    assert params == {
        "dataset_pids": {
            "items": {"type": "string"},
            "title": "Dataset Pids",
            "type": "array",
        },
        "file_server_host": {"title": "File Server Host", "type": "string"},
        "file_server_port": {"title": "File Server Port", "type": "integer"},
        "scicat_url": {
            "format": "uri",
            "maxLength": 2083,
            "minLength": 1,
            "title": "Scicat Url",
            "type": "string",
        },
        "scicat_token": {
            "default": "INSERT-YOUR-SCICAT-TOKEN-HERE",
            "format": "password",
            "title": "Scicat Token",
            "type": "string",
            "writeOnly": True,
        },
    }


def test_notebook_is_valid_json(sciwyrm_client):
    response = sciwyrm_client.post(
        "/notebook",
        json={
            "template_id": TEMPLATE_IDS["generic"],
            "parameters": {
                "scicat_url": "https://test-url.sci.cat",
                "file_server_host": "login",
                "file_server_port": 22,
                "dataset_pids": ["abcd/123.522"],
            },
        },
    )
    assert response.status_code == 200
    assert response.json() is not None


def test_notebook_contains_expected_url(sciwyrm_client):
    url = "https://test-url.sci.cat"
    response = sciwyrm_client.post(
        "/notebook",
        json={
            "template_id": TEMPLATE_IDS["generic"],
            "parameters": {
                "scicat_url": url,
                "file_server_host": "login",
                "file_server_port": 22,
                "dataset_pids": [],
            },
        },
    )
    assert response.status_code == 200
    assert url in response.text


def test_notebook_contains_expected_pids(sciwyrm_client):
    pids = ["7192983", "7ca7/31a.2as"]
    response = sciwyrm_client.post(
        "/notebook",
        json={
            "template_id": TEMPLATE_IDS["generic"],
            "parameters": {
                "scicat_url": "https://test-url.sci.cat",
                "file_server_host": "login",
                "file_server_port": 22,
                "dataset_pids": pids,
            },
        },
    )
    assert response.status_code == 200
    assert "7192983" in response.text
    assert "7ca7/31a.2as" in response.text


def test_notebook_contains_only_expected_pids(sciwyrm_client):
    pids0 = ["7192983", "7ca7/31a.2as"]
    pids1 = ["9391"]

    response = sciwyrm_client.post(
        "/notebook",
        json={
            "template_id": TEMPLATE_IDS["generic"],
            "parameters": {
                "scicat_url": "https://test-url.sci.cat",
                "file_server_host": "login",
                "file_server_port": 22,
                "dataset_pids": pids0,
            },
        },
    )
    assert response.status_code == 200

    response = sciwyrm_client.post(
        "/notebook",
        json={
            "template_id": TEMPLATE_IDS["generic"],
            "parameters": {
                "scicat_url": "https://test-url.sci.cat",
                "file_server_host": "login",
                "file_server_port": 22,
                "dataset_pids": pids1,
            },
        },
    )
    assert response.status_code == 200
    # Previous request has not affected the template on the server.
    assert "7192983" not in response.text
    assert "7ca7/31a.2as" not in response.text
    assert "9391" in response.text


def test_notebook_contains_expected_file_server_host(sciwyrm_client):
    file_server_host = "test.host.cat"
    response = sciwyrm_client.post(
        "/notebook",
        json={
            "template_id": TEMPLATE_IDS["generic"],
            "parameters": {
                "scicat_url": "https://test-url.sci.cat",
                "file_server_host": file_server_host,
                "file_server_port": 22,
                "dataset_pids": [],
            },
        },
    )
    assert response.status_code == 200
    assert file_server_host in response.text


def test_notebook_contains_expected_file_server_port(sciwyrm_client):
    file_server_port = 2200
    response = sciwyrm_client.post(
        "/notebook",
        json={
            "template_id": TEMPLATE_IDS["generic"],
            "parameters": {
                "scicat_url": "https://test-url.sci.cat",
                "file_server_host": "login",
                "file_server_port": file_server_port,
                "dataset_pids": [],
            },
        },
    )
    assert response.status_code == 200
    assert str(file_server_port) in response.text


def test_notebook_contains_no_placeholders(sciwyrm_client):
    response = sciwyrm_client.post(
        "/notebook",
        json={
            "template_id": TEMPLATE_IDS["generic"],
            "parameters": {
                "scicat_url": "https://test-url.sci.cat",
                "file_server_host": "login",
                "file_server_port": 22,
                "dataset_pids": ["abcd/123.522"],
            },
        },
    )
    assert response.status_code == 200
    assert not re.search(r"{{[^}]*}}", response.text)
    assert not re.search(r"{%[^}]*%}", response.text)


def test_notebook_contains_metadata(sciwyrm_client):
    response = sciwyrm_client.post(
        "/notebook",
        json={
            "template_id": TEMPLATE_IDS["generic"],
            "parameters": {
                "scicat_url": "https://test-url.sci.cat",
                "file_server_host": "login",
                "file_server_port": 22,
                "dataset_pids": ["abcd/123.522"],
            },
        },
    )
    assert response.status_code == 200
    metadata = response.json()["metadata"]["sciwyrm"]
    assert metadata["template_id"] == TEMPLATE_IDS["generic"]
    assert metadata["template_submission_name"] == "generic"
    assert metadata["template_version"] == "1"
    assert metadata["template_authors"] == [
        {"name": "Jan-Lukas Wynen", "email": "jan-lukas.wynen@ess.eu"}
    ]


@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("login", r"\"login\""),
        ("'login'", r'''\"'login'\"'''),
        ("\\login", r"\"\\login\""),
        ('"""login"""', r"\"\\\"\\\"\\\"login\\\"\\\"\\\"\""),
        ('"login', r"\"\\\"login\""),
    ],
)
def test_notebook_string_quoting(sciwyrm_client, input_str: str, expected: str):
    file_server_port = 2200
    response = sciwyrm_client.post(
        "/notebook",
        json={
            "template_id": TEMPLATE_IDS["generic"],
            "parameters": {
                "scicat_url": "https://test-url.sci.cat",
                "file_server_host": input_str,
                "file_server_port": file_server_port,
                "dataset_pids": [],
            },
        },
    )
    assert response.status_code == 200
    assert expected in response.text


def test_notebook_bad_parameter(sciwyrm_client):
    response = sciwyrm_client.post(
        "/notebook",
        json={
            "template_id": TEMPLATE_IDS["generic"],
            "parameters": {
                "scicat_url": "https://test-url.sci.cat",
                "file_server_host": "login",
                "file_server_port": 22,
                "dataset_pids": "abcd/123.522",
            },
        },
    )
    assert response.status_code == 422
    assert "dataset_pids" in response.text


def test_notebook_missing_parameter(sciwyrm_client):
    response = sciwyrm_client.post(
        "/notebook",
        json={
            "template_id": TEMPLATE_IDS["generic"],
            "parameters": {
                "scicat_url": "https://test-url.sci.cat",
                "file_server_port": 22,
                "dataset_pids": ["abcd/123.522"],
            },
        },
    )
    assert response.status_code == 422
    assert "file_server_host" in response.text


def test_notebook_extra_parameter(sciwyrm_client):
    response = sciwyrm_client.post(
        "/notebook",
        json={
            "template_id": TEMPLATE_IDS["generic"],
            "parameters": {
                "scicat_url": "https://test-url.sci.cat",
                "file_server_host": "login",
                "file_server_port": 22,
                "dataset_pids": ["abcd/123.522"],
                "extra": "not allowed",
            },
        },
    )
    assert response.status_code == 422
    assert "extra" in response.text


def test_notebook_escapes_control_sequence(sciwyrm_client):
    response = sciwyrm_client.post(
        "/notebook",
        json={
            "template_id": TEMPLATE_IDS["generic"],
            "parameters": {
                "scicat_url": "https://test-url.sci.cat",
                "file_server_host": "\x1f",
                "file_server_port": 22,
                "dataset_pids": ["abcd/123.522"],
            },
        },
    )
    assert response.status_code == 200
    assert '\\"\\u001f\\"' in response.text


def test_notebook_escapes_newline(sciwyrm_client):
    response = sciwyrm_client.post(
        "/notebook",
        json={
            "template_id": TEMPLATE_IDS["generic"],
            "parameters": {
                "scicat_url": "https://test-url.sci.cat",
                "file_server_host": "login",
                "file_server_port": 22,
                "dataset_pids": ["abc\n123"],
            },
        },
    )
    assert response.status_code == 200
    assert '\\"abc\\\\n123\\"' in response.text


# This requires a way to either pass a custom connect function to the
# SFTPFileTransfer in the notebook or a proper auth through SciCat.
# The former is very tricky; so waiting for the latter for now.
@pytest.mark.skip(reason="Authorization with the file server does not work yet.")
def test_notebook_run(
    sciwyrm_client,
    scicat_access,
    scicat_token,
    sftp_access,
    require_scicat_backend,
    require_sftp_fileserver,
):
    response = sciwyrm_client.post(
        "/notebook",
        json={
            "template_id": TEMPLATE_IDS["generic"],
            "parameters": {
                "scicat_url": scicat_access.url,
                "file_server_host": sftp_access.host,
                "file_server_port": sftp_access.port,
                "scicat_token": scicat_token,
                "dataset_pids": list(map(str, SEED)),
            },
        },
    )
    assert response.status_code == 200

    namespace = exec_notebook(response.text)
    datasets = namespace["datasets"]
    assert len(datasets) == len(SEED)
    for ds in datasets.values():
        assert ds == SEED[ds.pid]
