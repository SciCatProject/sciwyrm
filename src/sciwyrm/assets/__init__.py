# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 SciCat Project (https://github.com/SciCatProject/scitacean)

import importlib.resources
from ..typing import Notebook
import json


def _read_text(filename: str) -> str:
    return importlib.resources.files("sciwyrm.assets").joinpath(filename).read_text()


def notebook_template_v1() -> Notebook:
    return json.loads(_read_text("notebook_template_v1.ipynb"))
