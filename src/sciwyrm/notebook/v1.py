# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2024 SciCat Project (https://github.com/SciCatProject/sciwyrm)
"""Version 1 notebooks."""

from typing import Any

from fastapi import Request, Response
from pydantic import BaseModel

from ..assets import render_notebook_template


class NotebookSpecV1(BaseModel):
    """Specifies which notebook to return and how to format it.

    This is for version 1 of the endpoint.
    The template version is independent of that.
    """

    template_name: str
    template_version: str
    dataset_pids: list[str]
    file_server_host: str
    file_server_port: int
    scicat_url: str
    scicat_token: str = "INSERT-YOUR-SCICAT-TOKEN-HERE"


def _build_context(spec: NotebookSpecV1) -> dict[str, Any]:
    return {
        key.upper(): value for key, value in spec.model_dump(exclude_none=True).items()
    }


def format_notebook(request: Request, spec: NotebookSpecV1) -> Response:
    """Return a formatted notebook."""
    return render_notebook_template(
        name=spec.template_name,
        version=spec.template_version,
        request=request,
        context=_build_context(spec),
    )
