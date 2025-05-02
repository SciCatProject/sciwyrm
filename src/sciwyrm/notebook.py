# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 SciCat Project (https://github.com/SciCatProject/sciwyrm)
"""Notebook handling."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

import jsonschema
from pydantic import BaseModel, Field, model_validator
from pydantic_core import PydanticCustomError

from .config import AppConfig
from .templates import (
    NotebookTemplateConfig,
    get_notebook_template_config,
    list_notebook_templates,
)


class NotebookSpec(BaseModel):
    """Specifies which notebook to return and how to format it."""

    template_id: str = Field(description="ID of the template to render.")
    parameters: dict[str, Any] = Field(
        description="Parameters for the template. "
        "The schema depends on the concrete template."
    )

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


class TemplateSummary(BaseModel):
    """Short overview of a notebook template."""

    template_id: str = Field(description="ID of the template.")
    submission_name: str = Field(description="Template name given during submission.")
    display_name: str = Field(description="Template name meant for display to users.")
    version: str = Field(description="Template version.")

    @classmethod
    def from_config(
        cls, template_id: str, config: NotebookTemplateConfig
    ) -> TemplateSummary:
        """Construct from a template config."""
        return cls(
            template_id=template_id,
            submission_name=config.submission_name,
            display_name=config.display_name,
            version=config.version,
        )


def available_templates(config: AppConfig) -> list[TemplateSummary]:
    """Summarise available templates."""
    return [
        TemplateSummary.from_config(tid, get_notebook_template_config(tid, config))
        for tid in list_notebook_templates(config)
    ]


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


def insert_notebook_metadata(
    notebook: dict[str, Any], spec: NotebookSpecWithConfig
) -> None:
    """Insert template metadata into a rendered notebook."""
    metadata = notebook_metadata(spec)
    notebook["metadata"]["sciwyrm"] = metadata
    notebook["cells"].insert(
        0,
        {
            "cell_type": "markdown",
            "id": uuid.uuid4().hex[:16],
            "metadata": {},
            "source": [
                '<div style="font-size:x-small;padding-left:10pt">\n',
                f"<span style=\"color:rgba(128,128,128,128)\">Template:</span> {metadata['template_submission_name']}<br>\n",  # noqa: E501
                f"<span style=\"color:rgba(128,128,128,128)\">Id:</span> {metadata['template_id']} "  # noqa: E501
                f"<span style=\"color: rgba(128,128,128,128);margin-left:10pt\"|>Version:</span> {metadata['template_version']} "  # noqa: E501
                f"<span style=\"color: rgba(128,128,128,128);margin-left:10pt\"|>Rendered at:</span> {metadata['template_rendered_at']}\n",  # noqa: E501
                "</div>",
            ],
        },
    )
