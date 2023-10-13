# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 SciCat Project (https://github.com/SciCatProject/sciwyrm)
"""The SciWym application."""

from __future__ import annotations

from fastapi import FastAPI

from .notebook import v1
from .typing import Notebook

NotebookSpec = v1.NotebookSpecV1

app = FastAPI()


@app.post("/notebook")
async def notebook(spec: NotebookSpec) -> Notebook:
    """Format and return a notebook."""
    return v1.format_notebook(spec)
