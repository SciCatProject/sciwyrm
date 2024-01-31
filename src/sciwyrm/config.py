# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2024 SciCat Project (https://github.com/SciCatProject/sciwyrm)
"""Application and template configuration."""

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Generator

from pydantic.fields import FieldInfo
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)


class _JSONFileSettingsSource(PydanticBaseSettingsSource):
    def __init__(
        self, *, filename: Path | str, settings_cls: type[BaseSettings]
    ) -> None:
        super().__init__(settings_cls)
        try:
            self._file_content = json.loads(Path(filename).read_text(encoding="utf-8"))
        except FileNotFoundError:
            self._file_content = {}

    def get_field_value(
        self, field: FieldInfo, field_name: str
    ) -> tuple[Any, str, bool]:
        field_value = self._file_content.get(field_name)
        return field_value, field_name, field_name == "nums"

    def prepare_field_value(
        self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool
    ) -> Any:
        # Json.loads already decoded complex fields.
        return value

    def _get_fields(self) -> Generator[tuple[str, Any], None, None]:
        for field_name, field in self.settings_cls.model_fields.items():
            field_value, field_key, value_is_complex = self.get_field_value(
                field, field_name
            )
            field_value = self.prepare_field_value(
                field_name, field, field_value, value_is_complex
            )
            yield field_key, field_value

    def __call__(self) -> dict[str, Any]:
        return dict(self._get_fields())


class AppConfig(BaseSettings):
    """Sciwyrm application config."""

    template_dir: Path

    model_config = SettingsConfigDict(env_prefix="sciwyrm_")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Select settings sources."""
        _ = dotenv_settings
        return (
            init_settings,
            env_settings,
            _JSONFileSettingsSource(
                filename="./settings.json", settings_cls=settings_cls
            ),
            file_secret_settings,
        )


@lru_cache(maxsize=1)
def app_config() -> AppConfig:
    """Return the application config.

    This function should only be called by the app.
    Otherwise, tests cannot override the configuration.
    """
    from .logging import get_logger

    config = AppConfig()
    get_logger().info("Loaded app config: %r", config)
    return config
