# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2024 SciCat Project (https://github.com/SciCatProject/sciwyrm)
"""Asset loaders for SciWyrm."""

from functools import lru_cache
from pathlib import Path
from typing import Annotated

from fastapi import Depends
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader

from ..config import AppConfig, app_config


def get_templates(config: Annotated[AppConfig, Depends(app_config)]) -> Jinja2Templates:
    """Return a handler for loading and rendering templates."""
    return _make_template_handler(config.template_dir)


@lru_cache(maxsize=1)
def _make_template_handler(template_dir: Path) -> Jinja2Templates:
    from .. import filters
    from ..logging import get_logger

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
