# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2024 SciCat Project (https://github.com/SciCatProject/sciwyrm)
"""Asset loaders for SciWyrm."""

from pathlib import Path
from typing import Any

from fastapi import Request
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader


def _make_template_handler() -> Jinja2Templates:
    from .. import filters

    templates = Jinja2Templates(
        env=Environment(
            loader=FileSystemLoader(Path(__file__).resolve().parent / "templates"),
            autoescape=True,
        )
    )
    templates.env.filters["quote"] = filters.quote
    templates.env.filters["je"] = filters.json_escape
    return templates


_templates = _make_template_handler()


def render_notebook_template(
    *, name: str, version: str, request: Request, context: dict[str, Any]
) -> Any:
    """Render a given notebook template into a response-compatible object.

    Parameters
    ----------
    name:
        Name of the template.
    version:
        Version of the template.
    request:
        FastAPI request that requested the notebook.
    context:
        Values to insert into the template.

    Returns
    -------
    :
        An objects that can be returned from an endpoint as a JSONResponse.
    """
    return _templates.TemplateResponse(
        name=f"notebook/{name}_v{version}.ipynb",
        request=request,
        context={**context},
    )
