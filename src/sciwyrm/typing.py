# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 SciCat Project (https://github.com/SciCatProject/sciwyrm)
"""Utilities for type annotations."""

from typing import Any

Json = dict[str, "Json"] | list["Json"] | str | int | float | bool | None
Notebook = dict[str, Any]  # TODO
