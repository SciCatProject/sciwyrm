# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2024 SciCat Project (https://github.com/SciCatProject/sciwyrm)
"""Template loading."""

from functools import lru_cache
from pathlib import Path
from typing import Annotated

from fastapi import Depends
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader

from .config import AppConfig, app_config


def get_templates(config: Annotated[AppConfig, Depends(app_config)]) -> Jinja2Templates:
    """Return a handler for loading and rendering templates."""
    return _make_template_handler(config.template_dir)


def notebook_template_path(name: str, version: str) -> str:
    """Return the relative path to a given notebook template.

    Parameters
    ----------
    name:
        Name of the template.
    version:
        Version of the template.

    Returns
    -------
    :
        The path to the template relative to the base template directory.
    """
    return f"notebook/{name}_v{version}.ipynb"


@lru_cache(maxsize=1)
def _make_template_handler(template_dir: Path) -> Jinja2Templates:
    from . import filters
    from .logging import get_logger

    get_logger().info("Loading templates from %s", template_dir)
    templates = Jinja2Templates(
        env=Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=True,
        )
    )
    templates.env.filters["quote"] = filters.quote
    templates.env.filters["je"] = filters.json_escape
    return templates
