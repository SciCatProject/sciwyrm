# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2024 SciCat Project (https://github.com/SciCatProject/sciwyrm)
"""The SciWym application."""

from __future__ import annotations

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from .notebook import v1

app = FastAPI()


@app.post("/notebook/v1", response_class=JSONResponse)
async def notebook_v1(request: Request, spec: v1.NotebookSpecV1) -> Response:
    """Format and return a notebook."""
    return v1.format_notebook(request, spec)
