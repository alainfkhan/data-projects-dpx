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
current_main = "main"


# Groups
class GroupsManager:
    """Manager of groups."""

    base_name = PROJECTS_DIR.name
    reserved_projects = ["main", "playground", ".hidden"]

    def _is_group(self, filepath: Path) -> bool:
        """Whether this filepath is a group.

        A filepath is a group iff:
            in projects/
            a folder
            doesnt start with '.'
        """

        reject_prefix: tuple[str, ...] = (".",)

        is_in_base = filepath.parent.name == self.base_name
        is_folder = filepath.is_dir()

        is_rejected_prefix = True if filepath.name.startswith(reject_prefix) else False

        is_valid = is_in_base and is_folder and not is_rejected_prefix
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

    def list_projects_paths(
        self,
        groups: list[str] = [current_main],
        *,
        show_temps: bool = True,
        show_non_temps: bool = True,
    ) -> list[Path]:
        """List the project inside a group given a selection of groups"""

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

    def list_projects(
        self,
        # *args,
        # **kwargs
        groups: list[str] = [current_main],
        *,
        show_temps: bool = True,
        show_non_temps: bool = True,
    ) -> list[str]:
        """List project names given a selection of groups"""

        # project_paths: list[Path] = self.list_projects_paths(*args, **kwargs)
        project_paths: list[Path] = self.list_projects_paths(
            groups=groups, show_temps=show_temps, show_non_temps=show_non_temps
        )
        return [p.name for p in project_paths]

    def __init__(self) -> None:
        super().__init__()
        self.projects = self.list_projects(self.groups)
        self.project_paths = self.list_projects_paths(self.groups)

    def verify_project(self, project_candidate: str) -> None:
        """Raises an error if the input is not a valid project."""

        pass

    def get_group_from_project(self, project: str) -> str:
        """Get group name from project name."""

        for project_path in self.list_projects_paths(self.groups):
            if project_path.name == project:
                return project_path.parent.name

        raise FileNotFoundError(f"Cannot find group from project: '{project}'.")

    def can_create_project(self, new_project: str) -> bool:
        """Checks whether a project with this name can be created.
        Can create new project iff
            unique name
        """

        # unique project name
        if new_project in self.projects:
            raise FileExistsError(
                f"'{new_project}' already exists in the project group: '{self.get_group_from_project(new_project)}'."
            )

        return True


class FileManager:
    """Manages files within the project"""

    data_folder_names = {
        "raw": "raw",
        "interim": "interim",
        "processed": "processed",
        "external": "external",
    }

    def __init__(
        self, project_path: Path, data_folder_names=data_folder_names.values()
    ) -> None:
        self.project_path = project_path
        self.data_folder_names = data_folder_names
        pass

    def mkdir_data_folders(self) -> None:
        pass

    def mkdir_other_files(self) -> None:
        pass

    def add_db(self) -> None:
        pass


class Project:
    pm = ProjectsManager()
