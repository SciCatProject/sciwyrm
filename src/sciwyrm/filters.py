# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2024 SciCat Project (https://github.com/SciCatProject/sciwyrm)
"""Template filters."""


def quote(value: str) -> str:
    """Surround a string in appropriate quotes."""
    if '"' in value:
        if "'" in value:
            return f'"""{value}"""'
        return f"'{value}'"
    return f'"{value}"'


def json_escape(value: str) -> str:
    """Escape a string to be used in JSON."""
    return value.replace("\\", "\\\\").replace('"', '\\"')
