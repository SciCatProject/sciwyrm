# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 SciCat Project (https://github.com/SciCatProject/scitacean)

from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from . import assets
from .typing import Notebook

_notebook_template_v1 = assets.notebook_template_v1()


class NotebookSpec(BaseModel):
    version: str = "1"
    dataset_pids: list[str]


app = FastAPI()


@app.post("/notebook")
async def notebook(spec: NotebookSpec) -> Notebook:
    return _notebook_template_v1
