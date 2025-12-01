"""Util functions specific to CLI app

TODO: put functions in class for easy imports

projects/                       <- base
    .git
    .gitignore
    main/                       <- group
        main_project_one/       <- project
        ...
        main_project_n/

    playground/
    group_one/
    ...
    group_n/
    README.md

Define:
verify      if something is true
validate    if something can be done

"""

import os
from pathlib import Path

from icecream import ic

from src.dpx.utils.paths import PROJECTS_DIR


base_name = PROJECTS_DIR.name
temp_prefix = "~"


# Groups
class GroupsManager:
    """Manager of groups."""

    pass


def is_group(obj: Path) -> bool:
    """Whether this path is a group.
    A path is a group iff:
        in projects/
        a folder
    """
    is_in_base = obj.parent.name == base_name
    is_folder = obj.is_dir()

    is_valid = is_in_base and is_folder
    return is_valid


def verify_group(group_candidate: str) -> None:
    """Raises an error if the input is not a valid group."""
    if not is_group(PROJECTS_DIR / group_candidate):
        raise ValueError(f"'{group_candidate}' is not a valid group.")


def list_groups() -> list[str]:
    """Returns a list of all groups."""
    objects: list[str] = os.listdir(PROJECTS_DIR)

    valid_groups: list[str] = [obj for obj in objects if is_group(PROJECTS_DIR / obj)]
    # valid_groups: list[str] = []
    # for obj in objects:
    #     if is_group(PROJECTS_DIR / obj):
    #         valid_groups.append(obj)

    return valid_groups


# Projects


class ProjectsManager:
    """Manager of all projects of all groups."""

    pass


def is_project(obj: Path) -> bool:
    """Whether this path is a project.
    A path is a project iff:
        in a group
        a folder
    """
    is_under_group = is_group(obj.parent)
    is_folder = obj.is_dir()

    is_valid = is_under_group and is_folder
    return is_valid


def is_temp_project(obj: Path) -> bool:
    """Whether this path is a temp project.
    A path is a temp project iff:
        a project
        some prefix
    """
    is_id = obj.name.startswith(temp_prefix)

    is_valid = is_project(obj) and is_id
    return is_valid


def verify_project(project_candidate: str) -> None:
    """Raises an error if the input is not a valid project."""
    pass


def list_projects(group_name: str) -> list[str]:
    """Returns a list of all projects in a group."""
    group_path: Path = PROJECTS_DIR / group_name
    files: list[str] = os.listdir(group_path)

    project_names: list[str] = [file for file in files if is_project(group_path / file)]
    # project_names: list[str] = []
    # for file in files:
    #     if is_valid_project(group_path / file):
    #         project_names.append(file)

    return project_names


def list_all_project_paths() -> list[Path]:
    """Returns a list of all project paths in each group."""
    all_project_paths: list[Path] = []
    for group in list_groups():
        home = PROJECTS_DIR / group

        projects = list_projects(group)
        for project in projects:
            all_project_paths.append(home / project)

    return all_project_paths


def list_all_projects() -> list[str]:
    """Returns a list of all projects names in each group."""

    all_projects: list[str] = []
    for project_path in list_all_project_paths():
        all_projects.append(project_path.name)

    return all_projects


def get_group_from_project(project: str) -> str:
    """Get group name from project name."""
    for project_path in list_all_project_paths():
        if project_path.name == project:
            return project_path.parent.name

    raise FileNotFoundError(f"Cannot find group from project: '{project}'.")


# Can create


def can_create_project(new_project: str) -> bool:
    """Checks whether a project with this name can be created.
    Can create new project iff
        unique name
    """
    # unique project name
    if new_project in list_all_projects():
        raise FileExistsError(
            f"'{new_project}' already exists in the project group: '{get_group_from_project(new_project)}'."
        )

    return True


def can_create_group(new_group: str) -> bool:
    """Checks whether a group with this name can be created.
    Can create new group iff
        name not main nor playground
        unique name
    """
    if new_group in ["main", "playground"]:
        raise ValueError(f"'{new_group}' is reserved.")

    if new_group in list_groups():
        raise FileExistsError(f"'{new_group}' already exists.")

    return True
