# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 SciCat Project (https://github.com/SciCatProject/scitacean)
"""Version 1 notebooks."""

from copy import deepcopy
from typing import Literal

from pydantic import BaseModel

from .. import assets
from ..typing import Notebook

_notebook_template_v1 = assets.notebook_template_v1()


class NotebookSpecV1(BaseModel):
    """Specifies which notebook to return and how to format it."""

    version: Literal["1"] = "1"
    dataset_pids: list[str]
    scicat_url: str


def _pids_cell_source(pids: list[str]) -> list[str]:
    return ["input_dataset_pids = [\n", *(f'    "{pid}"\n' for pid in pids), "]"]


def _scicat_url_cell_source(scicat_url: str) -> list[str]:
    return [f'scicat_url = "{scicat_url}"']


def format_notebook(spec: NotebookSpecV1) -> Notebook:
    """Return a formatted version 1 notebook."""
    nb = deepcopy(_notebook_template_v1)
    cells = nb["cells"]
    cells[1]["source"] = _scicat_url_cell_source(spec.scicat_url)
    cells[2]["source"] = _pids_cell_source(spec.dataset_pids)
    return nb
