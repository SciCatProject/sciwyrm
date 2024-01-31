# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2024 SciCat Project (https://github.com/SciCatProject/sciwyrm)
"""Template loading."""

import hashlib
import json
from functools import lru_cache
from pathlib import Path
from typing import Annotated, Any

from fastapi import Depends
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel, EmailStr

from .config import AppConfig, app_config


class Author(BaseModel):
    """Author of the template."""

    name: str
    email: EmailStr | None = None


class NotebookTemplateConfig(BaseModel):
    """Template configuration."""

    submission_name: str
    display_name: str
    version: str
    description: str
    authors: list[Author]
    parameter_schema: dict[str, Any]
    template_hash: str


def get_templates(config: Annotated[AppConfig, Depends(app_config)]) -> Jinja2Templates:
    """Return a handler for loading and rendering templates."""
    return _make_template_handler(config.template_dir)


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


def get_notebook_template_config(
    template_id: str, config: AppConfig
) -> NotebookTemplateConfig:
    """Return a template configuration."""
    return _load_notebook_template_config(template_id, config.template_dir)


@lru_cache()
def _load_notebook_template_config(
    template_id: str, template_dir: Path
) -> NotebookTemplateConfig:
    # AppConfig cannot be hashed and used with lru_cache.
    path = template_dir.joinpath("notebook", f"{template_id}.json")
    with path.open() as f:
        fields = json.load(f)
        fields["template_hash"] = _notebook_template_hash(path)
        return NotebookTemplateConfig(**fields)


def notebook_template_path(template_id: str) -> str:
    """Return the relative path to a given notebook template.

    Parameters
    ----------
    template_id:
        Unique ID of the template.

    Returns
    -------
    :
        The path to the template relative to the base template directory.
    """
    return f"notebook/{template_id}.ipynb"


def list_notebook_templates(config: AppConfig) -> list[str]:
    """List available notebook templates."""
    return [
        path.stem
        for path in config.template_dir.joinpath("notebook").iterdir()
        if path.suffix == ".ipynb"
    ]


def _notebook_template_hash(path: Path) -> str:
    """Return a hash for a notebook template."""
    return "blake2b:" + hashlib.blake2b(path.read_bytes()).hexdigest()
