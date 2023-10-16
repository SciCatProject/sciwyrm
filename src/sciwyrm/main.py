# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 SciCat Project (https://github.com/SciCatProject/sciwyrm)
"""The SciWym application."""

from __future__ import annotations

from fastapi import FastAPI

from .notebook import v1
from .typing import Notebook

app = FastAPI()


@app.post("/notebook/v1")
def notebook_v1(spec: v1.NotebookSpecV1) -> Notebook:
    """Format and return a notebook."""
    return v1.format_notebook(spec)
