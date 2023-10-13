# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 SciCat Project (https://github.com/SciCatProject/scitacean)
"""Version 1 notebooks."""

from typing import Literal

from pydantic import BaseModel

from .. import assets
from ..typing import Notebook

_notebook_template_v1 = assets.notebook_template_v1()


class NotebookSpecV1(BaseModel):
    """Specifies which notebook to return and how to format it."""

    version: Literal["1"] = "1"
    dataset_pids: list[str]


def format_notebook(spec: NotebookSpecV1) -> Notebook:
    """Return a formatted version 1 notebook."""
    return _notebook_template_v1
