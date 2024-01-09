# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2024 SciCat Project (https://github.com/SciCatProject/sciwyrm)
"""Asset loaders for SciWyrm."""

import importlib.resources
import json

from ..typing import Notebook


def _read_text(filename: str) -> str:
    return importlib.resources.files("sciwyrm.assets").joinpath(filename).read_text()


def notebook_template_v1() -> Notebook:
    """Return notebook template version 1."""
    return json.loads(_read_text("notebook_template_v1.ipynb"))
