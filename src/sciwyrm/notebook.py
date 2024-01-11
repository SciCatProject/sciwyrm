# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2024 SciCat Project (https://github.com/SciCatProject/sciwyrm)
"""Notebook handling."""

from typing import Any

import jsonschema
from pydantic import BaseModel, ValidationInfo, field_validator
from pydantic_core import PydanticCustomError

from .config import app_config
from .templates import get_template_config


class NotebookSpec(BaseModel):
    """Specifies which notebook to return and how to format it."""

    template_name: str
    template_version: str
    parameters: dict[str, Any]

    @field_validator("parameters")
    @classmethod
    def validate_parameters(
        cls, parameters: Any, info: ValidationInfo
    ) -> dict[str, Any]:
        """Validate parameters against the template schema."""
        if not isinstance(parameters, dict):
            raise AssertionError("'parameters' must be a dict.")

        schema = get_template_config(
            info.data["template_name"], info.data["template_version"], app_config()
        )
        try:
            jsonschema.validate(parameters, schema)
        except jsonschema.ValidationError as err:
            raise PydanticCustomError(
                "Validation Error",
                "{message}",
                {
                    "message": err.message,
                    "template_name": info.data["template_name"],
                    "template_version": info.data["template_version"],
                    "instance": err.instance,
                    "jsonpath": err.json_path,
                    "schema": err.schema,
                    "schema_path": err.schema_path,
                    "validator": err.validator,
                    "validator_value": err.validator_value,
                },
            ) from None
        return parameters


def render_context(spec: NotebookSpec) -> dict[str, Any]:
    """Return a dict that can be used to render a notebook template."""
    return {key.upper(): value for key, value in spec.parameters.items()}