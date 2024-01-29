# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2024 SciCat Project (https://github.com/SciCatProject/sciwyrm)
"""Notebook handling."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import jsonschema
from pydantic import BaseModel, model_validator
from pydantic_core import PydanticCustomError

from .templates import NotebookTemplateConfig


class NotebookSpec(BaseModel):
    """Specifies which notebook to return and how to format it."""

    template_id: str
    parameters: dict[str, Any]

    def with_config(self, config: NotebookTemplateConfig) -> NotebookSpecWithConfig:
        """Return a new spec with template config."""
        return NotebookSpecWithConfig(
            **{**self.model_dump(), "config": config},
        )


class NotebookSpecWithConfig(NotebookSpec):
    """Internal spec with added template config.

    This should not be exposed to the API because notebook template configs
    are provided by the server.
    """

    config: NotebookTemplateConfig

    @model_validator(mode="after")
    def validate_parameters(self) -> NotebookSpecWithConfig:
        """Validate parameters against the template schema."""
        schema = self.config.parameter_schema
        try:
            jsonschema.validate(self.parameters, schema)
        except jsonschema.ValidationError as err:
            raise PydanticCustomError(
                "Validation Error",
                "{message}",
                {
                    "message": err.message,
                    "template_id": self.template_id,
                    "instance": err.instance,
                    "jsonpath": err.json_path,
                    "schema": err.schema,
                    "schema_path": err.schema_path,
                    "validator": err.validator,
                    "validator_value": err.validator_value,
                },
            ) from None
        return self


def render_context(spec: NotebookSpecWithConfig) -> dict[str, Any]:
    """Return a dict that can be used to render a notebook template."""
    context = spec.parameters | notebook_metadata(spec)
    return {key.upper(): value for key, value in context.items()}


def notebook_metadata(spec: NotebookSpecWithConfig) -> dict[str, Any]:
    """Return metadata for a requested notebook.

    Here, metadata is any data that was not explicitly requested by the user.
    """
    return {
        "template_id": spec.template_id,
        "template_submission_name": spec.config.submission_name,
        "template_display_name": spec.config.display_name,
        "template_version": spec.config.version,
        "template_authors": [author.model_dump() for author in spec.config.authors],
        "template_rendered_at": datetime.now(tz=timezone.utc).isoformat(),
        "template_hash": spec.config.template_hash,
    }
