# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2024 SciCat Project (https://github.com/SciCatProject/sciwyrm)
"""Notebook templates for SciWyrm."""

import importlib.resources
import json
from copy import deepcopy
from functools import lru_cache

from ....typing import Notebook


@lru_cache()
def _load(*, name: str, version: str) -> Notebook:
    filename = f"{name}_v{version}.ipynb"
    source = (
        importlib.resources.files("sciwyrm.assets.templates.notebook")
        .joinpath(filename)
        .read_text()
    )
    return json.loads(source)


def notebook_template(*, name: str, version: str) -> Notebook:
    """Return a notebook template."""
    return deepcopy(_load(name=name, version=version))
