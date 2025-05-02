# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 SciCat Project (https://github.com/SciCatProject/sciwyrm)
"""The SciWyrm application."""

import json
from typing import Annotated

from fastapi import Depends, FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from . import notebook
from .config import AppConfig, app_config
from .templates import (
    get_notebook_template_config,
    get_templates,
    notebook_template_path,
)

app = FastAPI()


@app.get("/notebook/templates", response_description="Available templates")
async def list_templates(
    config: Annotated[AppConfig, Depends(app_config)]
) -> list[notebook.TemplateSummary]:
    """Return a list of available notebook templates."""
    return notebook.available_templates(config)


def _inject_app_config(
    spec: notebook.NotebookSpec, config: Annotated[AppConfig, Depends(app_config)]
) -> notebook.NotebookSpecWithConfig:
    try:
        return spec.with_config(get_notebook_template_config(spec.template_id, config))
    except ValidationError as exc:
        # FastAPI cannot handle a ValidationError at this point.
        # So make it look like this came from the initial spec.
        errors = exc.errors()
        for error in errors:
            error["input"].pop("config")
        raise RequestValidationError(errors) from None


@app.post("/notebook", response_model=dict, response_description="Rendered notebook")
async def format_notebook(
    request: Request,
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
    spec: notebook.NotebookSpecWithConfig = Depends(_inject_app_config),  # noqa: B008
) -> Response:
    """Format and return a notebook."""
    formatted = templates.TemplateResponse(
        name=notebook_template_path(spec.template_id),
        request=request,
        context=notebook.render_context(spec),
    )
    nb = json.loads(formatted.body)
    notebook.insert_notebook_metadata(nb, spec)
    return JSONResponse(nb)
