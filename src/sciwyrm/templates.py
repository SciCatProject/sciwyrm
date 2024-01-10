# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2024 SciCat Project (https://github.com/SciCatProject/sciwyrm)
"""Template loading."""

import json
from functools import lru_cache
from pathlib import Path
from typing import Annotated, Any

from fastapi import Depends
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader

from .config import AppConfig, app_config


def get_templates(config: Annotated[AppConfig, Depends(app_config)]) -> Jinja2Templates:
    """Return a handler for loading and rendering templates."""
    return _make_template_handler(config.template_dir)


def get_template_config(name: str, version: str, config: AppConfig) -> dict[str, Any]:
    """Return a template configuration."""
    with config.template_dir.joinpath(
        "notebook", f"{name}_v{version}.json"
    ).open() as f:
        return json.load(f)


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


def list_notebook_templates(config: AppConfig) -> list[dict[str, str]]:
    """List available notebook templates."""
    return [
        _split_notebook_template_name(path.stem)
        for path in config.template_dir.joinpath("notebook").iterdir()
        if path.suffix == ".ipynb"
    ]


def _split_notebook_template_name(full_name: str) -> dict[str, str]:
    name, version = full_name.split("_v")
    return {"name": name, "version": version}


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
