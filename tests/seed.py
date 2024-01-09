# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2024 SciCat Project (https://github.com/SciCatProject/sciwyrm)
import tempfile
from contextlib import contextmanager
from pathlib import Path

import scitacean

SEED = {}


def seed_scicat(scicat_client: scitacean.Client, scicat_access) -> None:
    with _tempdir() as seed_dir:
        for ds in _datasets(seed_dir):
            ds.owner = scicat_access.user.username
            ds.owner_group = scicat_access.user.group
            finalized = scicat_client.upload_new_dataset_now(ds)
            SEED[finalized.pid] = finalized


@contextmanager
def _tempdir():
    with tempfile.TemporaryDirectory() as d:
        yield Path(d)


def _datasets(seed_dir: Path) -> list[scitacean.Dataset]:
    ds1 = scitacean.Dataset(
        type="raw",
        name="Test Dataset 1",
        contact_email="ponder.stibbons@uu.am",
        creation_location="AM/UU",
        owner="stibbons",
        owner_group="faculty",
        principal_investigator="Ponder Stibbons",
        source_folder="/data/sciwyrm/test_dataset_1/",
    )
    seed_dir.joinpath("file1.txt").write_text("this is file no. 1")
    ds1.add_local_files(seed_dir.joinpath("file1.txt"), base_path=seed_dir)
    return [ds1]
