# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 SciCat Project (https://github.com/SciCatProject/scitacean)

from typing import Any  # TODO

Json = dict[str, "Json"] | list["Json"] | str | int | float | bool | None
Notebook = dict[str, Any]
