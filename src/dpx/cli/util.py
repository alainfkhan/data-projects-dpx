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
all         refers to all groups
"""

import os
from pathlib import Path

from icecream import ic

from src.dpx.utils.paths import PROJECTS_DIR


temp_prefix = "~"


# Groups
class GroupsManager:
    """Manager of groups."""

    base_name = PROJECTS_DIR.name
    reserved_projects = ["main", "playground", ".trash"]
    main_group = "main"

    def _is_group(self, filepath: Path) -> bool:
        """Whether this filepath is a group.

        A filepath is a group iff:
            in projects/
            a folder
        """

        is_in_base = filepath.parent.name == self.base_name
        is_folder = filepath.is_dir()

        is_valid = is_in_base and is_folder
        return is_valid

    def _list_groups(self) -> list[str]:
        """Returns a list of all groups (names)."""

        files: list[str] = os.listdir(PROJECTS_DIR)

        valid_groups: list[str] = [
            file for file in files if self._is_group(PROJECTS_DIR / file)
        ]
        # valid_groups: list[str] = []
        # for obj in objects:
        #     if is_group(PROJECTS_DIR / obj):
        #         valid_groups.append(obj)
        return valid_groups

    def __init__(self) -> None:
        self.groups: list[str] = self._list_groups()
        self.groups_paths = [PROJECTS_DIR / group for group in self.groups]

    def verify_group(self, group_candidate: str) -> None:
        """Raises an error if the input is not a valid group."""

        if not self._is_group(PROJECTS_DIR / group_candidate):
            raise ValueError(f"'{group_candidate}' is not a valid group.")

    def can_create_group(self, new_group: str) -> bool:
        """Checks whether a group with this name can be created.
        Can create new group iff
            name not main nor playground
            unique name
        """

        if new_group in self.reserved_projects:
            raise ValueError(f"'{new_group}' is reserved.")

        if new_group in self.groups:
            raise FileExistsError(f"'{new_group}' already exists.")

        return True


class ProjectsManager(GroupsManager):
    """Manager of all projects of all groups."""

    def is_project(self, filepath: Path) -> bool:
        """Whether this filepath is a project.

        A filepath is a project iff:
            in a group
            a folder
        """

        is_under_group = self._is_group(filepath.parent)
        is_folder = filepath.is_dir()

        is_valid = is_under_group and is_folder
        return is_valid

    def is_temp_project(self, filepath: Path) -> bool:
        """Whether this filepath is a temp project.

        A filepath is a temp project iff:
            a project
            some prefix
        """

        is_id = filepath.name.startswith(temp_prefix)

        is_valid = self.is_project(filepath) and is_id
        return is_valid

    # Projects

    def list_project_paths(
        self,
        groups: list[str] = ["main"],
        show_temps: bool = True,
        show_non_temps: bool = True,
    ) -> list[Path]:
        to_show: list[Path] = []

        for group in groups:
            self.verify_group(group)
            group_path = PROJECTS_DIR / group

            # Filepaths in group
            files = os.listdir(group_path)

            project_paths: list[Path] = [
                group_path / file
                for file in files
                if self.is_project(group_path / file)
            ]
            temp_project_paths: list[Path] = [
                group_path / file
                for file in files
                if self.is_temp_project(group_path / file)
            ]
            non_temp_project_paths: list[Path] = list(
                set(project_paths).difference(set(temp_project_paths))
            )

            if show_temps:
                to_show: list[Path] = to_show + temp_project_paths

            if show_non_temps:
                to_show: list[Path] = to_show + non_temp_project_paths

        return to_show

    def list_projects_OLD(self, group_name: str) -> list[str]:
        """Returns a list of all projects in a group."""

        group_path: Path = PROJECTS_DIR / group_name
        objects: list[str] = os.listdir(group_path)

        project_names: list[str] = [
            obj for obj in objects if self.is_project(group_path / obj)
        ]
        # project_names: list[str] = []
        # for file in files:
        #     if is_valid_project(group_path / file):
        #         project_names.append(file)

        return project_names

    def _list_all_project_paths_OLD(self) -> list[Path]:
        """Returns a list of all project paths in each group."""

        all_project_paths: list[Path] = []
        for group in self._list_groups():
            home = PROJECTS_DIR / group

            projects = self.list_projects_OLD(group)
            for project in projects:
                all_project_paths.append(home / project)

        return all_project_paths

    def _list_all_projects_OLD(self) -> list[str]:
        """Returns a list of all projects (names) in each group."""

        all_projects: list[str] = []
        for project_path in self._list_all_project_paths_OLD():
            all_projects.append(project_path.name)

        return all_projects

    # Temp projects
    def list_temp_projects_OLD(self, group: str) -> list[str]:
        """Returns a list of all temp projects in a group."""
        projects = self.list_projects_OLD(group)
        temp_projects = [
            project
            for project in projects
            if self.is_temp_project(PROJECTS_DIR / group / project)
        ]

        return temp_projects

    def _list_all_temp_project_paths_OLD(self) -> list[Path]:
        all_temp_project_paths: list[Path] = []
        for group in self.groups:
            temp_project_path: list[Path] = [
                PROJECTS_DIR / group / temp_project
                for temp_project in self.list_temp_projects_OLD(group)
            ]
            all_temp_project_paths = all_temp_project_paths + temp_project_path

        return all_temp_project_paths

    def __init__(self) -> None:
        super().__init__()
        self.all_projects = self._list_all_projects_OLD()
        self.all_project_paths = self._list_all_project_paths_OLD()

        self.all_temps_paths = self._list_all_temp_project_paths_OLD()

    def verify_project(self, project_candidate: str) -> None:
        """Raises an error if the input is not a valid project."""

        pass

    def get_group_from_project(self, project: str) -> str:
        """Get group name from project name."""

        for project_path in self._list_all_project_paths_OLD():
            if project_path.name == project:
                return project_path.parent.name

        raise FileNotFoundError(f"Cannot find group from project: '{project}'.")

    def can_create_project(self, new_project: str) -> bool:
        """Checks whether a project with this name can be created.
        Can create new project iff
            unique name
        """

        # unique project name
        if new_project in self._list_all_projects_OLD():
            raise FileExistsError(
                f"'{new_project}' already exists in the project group: '{self.get_group_from_project(new_project)}'."
            )

        return True


"""









"""
