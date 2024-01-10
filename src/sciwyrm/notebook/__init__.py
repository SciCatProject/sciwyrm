# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2024 SciCat Project (https://github.com/SciCatProject/sciwyrm)
"""Notebook handling."""

from typing import Any

from pydantic import BaseModel


class NotebookSpec(BaseModel):
    """Specifies which notebook to return and how to format it."""

    template_name: str
    template_version: str
    parameters: dict[str, Any]


def render_context(spec: NotebookSpec) -> dict[str, Any]:
    """Return a dict that can be used to render a notebook template."""
    return {key.upper(): value for key, value in spec.parameters.items()}
