# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 SciCat Project (https://github.com/SciCatProject/scitacean)
"""The SciWym application."""

from __future__ import annotations

from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel

from . import assets
from .typing import Notebook

_notebook_template_v1 = assets.notebook_template_v1()


class NotebookSpec(BaseModel):
    """Specifies which notebook to return and how to format it."""

    version: Literal["1"] = "1"
    dataset_pids: list[str]


app = FastAPI()


@app.post("/notebook")
async def notebook(spec: NotebookSpec) -> Notebook:
    """Format and return a notebook."""
    return _notebook_template_v1
