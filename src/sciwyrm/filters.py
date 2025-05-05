# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 SciCat Project (https://github.com/SciCatProject/sciwyrm)
"""Template filters."""

import json


def quote(value: object) -> str:
    """Surround a string in appropriate quotes."""
    escaped = str(value).replace('"', r"\"")
    return f'"{escaped}"'


def json_escape(value: str) -> str:
    """Escape a string to be used in JSON."""
    # Use json.dumps to escape any characters that JSON can't handle.
    # THis adds quotation marks around the result, so strip those off.
    return json.dumps(str(value))[1:-1]
