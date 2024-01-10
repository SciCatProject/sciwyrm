# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2024 SciCat Project (https://github.com/SciCatProject/sciwyrm)
"""The SciWym application."""

from typing import Annotated

from fastapi import Depends, FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from .notebook import v1
from .templates import get_templates, notebook_template_path

app = FastAPI()


@app.post("/notebook/v1", response_class=JSONResponse)
async def format_notebook(
    request: Request,
    spec: v1.NotebookSpecV1,
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
) -> Response:
    """Format and return a notebook."""
    return templates.TemplateResponse(
        name=notebook_template_path(spec.template_name, spec.template_version),
        request=request,
        context=v1.render_context(spec),
    )
