# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2024 SciCat Project (https://github.com/SciCatProject/sciwyrm)
"""The SciWym application."""

from typing import Annotated

from fastapi import Depends, FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from . import notebook
from .config import AppConfig, app_config
from .templates import get_templates, list_notebook_templates, notebook_template_path

app = FastAPI()


@app.get("/notebook/templates")
async def list_templates(
    config: Annotated[AppConfig, Depends(app_config)]
) -> JSONResponse:
    """Return a list of available notebook templates."""
    return JSONResponse(list_notebook_templates(config))


@app.post("/notebook", response_class=JSONResponse)
async def format_notebook(
    request: Request,
    spec: notebook.NotebookSpec,
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
) -> Response:
    """Format and return a notebook."""
    return templates.TemplateResponse(
        name=notebook_template_path(spec.template_name, spec.template_version),
        request=request,
        context=notebook.render_context(spec),
    )
