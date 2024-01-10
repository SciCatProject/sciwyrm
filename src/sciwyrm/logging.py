# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2024 SciCat Project (https://github.com/SciCatProject/sciwyrm)
"""Logging tools and setup."""

import logging


def get_logger() -> logging.Logger:
    """Return the Sciwyrm logger."""
    return logging.getLogger("sciwyrm")


def _configure() -> None:
    logger = get_logger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(name)s [%(levelname)s]   %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S%z",
        )
    )
    logger.addHandler(handler)


_configure()
