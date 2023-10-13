# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 SciCat Project (https://github.com/SciCatProject/sciwyrm)
"""Version 1 notebooks."""

from copy import deepcopy
from typing import Literal

from pydantic import BaseModel

from .. import assets
from ..typing import Notebook

_notebook_template_v1 = assets.notebook_template_v1()


class NotebookSpecV1(BaseModel):
    """Specifies which notebook to return and how to format it."""

    dataset_pids: list[str]
    file_server_host: str
    file_server_port: int
    scicat_url: str
    scicat_token: str | None = None
    version: Literal["1"] = "1"


def _scicat_url_cell_source(
    scicat_url: str, file_server_host: str, file_server_port: int
) -> list[str]:
    return [
        f'scicat_url = "{scicat_url}"\n',
        f'file_server_host = "{file_server_host}"\n',
        f'file_server_port = "{file_server_port}"',
    ]


def _scicat_token_cell_source(scicat_token: str | None) -> list[str]:
    return [f'scicat_token = "{scicat_token or "INSERT-YOUR-SCICAT-TOKEN-HERE"}"']


def _pids_cell_source(pids: list[str]) -> list[str]:
    return ["input_dataset_pids = [\n", *(f'    "{pid}",\n' for pid in pids), "]"]


def format_notebook(spec: NotebookSpecV1) -> Notebook:
    """Return a formatted version 1 notebook."""
    nb = deepcopy(_notebook_template_v1)
    cells = nb["cells"]
    cells[1]["source"] = _scicat_url_cell_source(
        spec.scicat_url, spec.file_server_host, spec.file_server_port
    )
    cells[2]["source"] = _scicat_token_cell_source(spec.scicat_token)
    cells[3]["source"] = _pids_cell_source(spec.dataset_pids)
    return nb
