"""Util functions specific to CLI app"""

import os
from pathlib import Path

from icecream import ic

from src.dpx.utils.paths import PROJECTS_DIR


def is_valid_project(file: Path) -> bool:
    return True


def list_project_names(group_name: str) -> list[str]:
    """List projects in some directory."""
    group_path: Path = PROJECTS_DIR / group_name
    files: list[str] = os.listdir(group_path)

    project_names: list[str] = [
        file for file in files if is_valid_project(group_path / file)
    ]
    # project_names: list[str] = []
    # for file in files:
    #     if is_valid_project(group_path / file):
    #         project_names.append(file)

    return project_names


class Group:
    def list_temps(self) -> list[str]:
        pass
        