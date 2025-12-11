"""Util functions specific to CLI app

projects/                       <- base
    .git
    .gitignore
    main/                       <- group one
        main_project_one/       <- project
        ...
        main_project_n/

    playground/                 <- group two
    folder_three/
    ...
    folder_n/
    .folder_one/                <- archived folder, not a group
    ...
    .folder_n/
    README.md

Define:
group       A visible collection of projects
    A group always implies its visible
archive     A collection of projects not indended to be seen
    archive != group
    An archive always implies its hidden
verify      if something is true
validate    if something can be done
all         refers to all groups
"""
# from __future__ import annotations

import os
import shutil
import warnings
import time
import threading
from pathlib import Path

import pandas as pd
from icecream import ic
from pandas import DataFrame
from rich import print

from src.dpx.cli.utils.url_manager import URLDispatcher
from src.dpx.utils.paths import PROJECTS_DIR
from src.dpx.utils.util import Tree, create_structure

# Custom definitions
temp_prefix = "~"
current_main = "main"

copy_appendage = "-copy"
# what to append to a copy
# eg file.ext -> file-copy.ext
# file-copy.ext -> file-copy-copy.ext
"""
TODO: 
file.ext -> file(1).ext
file(1).ext -> file(2).ext

if in a file, there exists:
    file.ext
    file(1).ext
    file(3).ext

and file(1).ext, file(3).ext are copies of file.ext
another copy of file.ext -> file(4).ext   
"""


# type Tree = dict[str, None | Tree]


class GroupManager:
    """Manager of groups."""

    base_path = PROJECTS_DIR
    base_name = base_path.name
    reserved_groups = ["main", "playground"]
    reserved_archives = [".hidden", ".trash"]

    def _is_group(self, filepath: Path) -> bool:
        """Whether this filepath is a group.

        A filepath is a group iff:
            in projects/
            a folder
            doesnt start with '.'

        A folder that starts with '.' is an 'archive'
        not indended to be searchable in this CLI app.
        """

        exclude: tuple[str, ...] = (".",)
        # exclude: tuple[str, ...] = (" ",)

        is_in_base = filepath.parent.name == self.base_name
        is_folder = filepath.is_dir()

        is_rejected_prefix = True if filepath.name.startswith(exclude) else False

        is_valid = is_in_base and is_folder and not is_rejected_prefix
        return is_valid

    def _order_groups(self, groups: list[str]) -> list[str]:
        groups.remove("main")
        groups.remove("playground")

        output: list[str] = ["main", "playground"] + sorted(groups)
        return output

    def _list_groups(self) -> list[str]:
        """Returns a list of all groups (names)."""

        files: list[str] = os.listdir(PROJECTS_DIR)

        valid_groups: list[str] = [
            file
            for file in files
            if self._is_group(
                PROJECTS_DIR / file,
            )
        ]
        # valid_groups: list[str] = []
        # for obj in objects:
        #     if is_group(PROJECTS_DIR / obj):
        #         valid_groups.append(obj)
        return valid_groups

    def __init__(self) -> None:
        groups = self._list_groups()

        self.groups: list[str] = self._order_groups(groups)
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

        if new_group in self.reserved_groups:
            raise ValueError(f"'{new_group}' is reserved.")

        if new_group in self.groups:
            raise FileExistsError(f"'{new_group}' already exists.")

        return True


class ProjectManager(GroupManager):
    """Manager of projects."""

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
                if self.is_project(
                    group_path / file,
                )
            ]
            temp_project_paths: list[Path] = [
                group_path / file
                for file in files
                if self.is_temp_project(
                    group_path / file,
                )
            ]
            non_temp_project_paths: list[Path] = list(set(project_paths).difference(set(temp_project_paths)))

            if show_temps:
                # to_show: list[Path] = to_show + temp_project_paths
                to_show += temp_project_paths

            if show_non_temps:
                # to_show: list[Path] = to_show + non_temp_project_paths
                to_show += non_temp_project_paths

        return to_show

    # TODO: simplify args to match list_projects_paths()
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
            groups=groups,
            show_temps=show_temps,
            show_non_temps=show_non_temps,
        )
        return [p.name for p in project_paths]

    def __init__(self) -> None:
        super().__init__()
        self.projects = self.list_projects(self.groups)
        self.project_paths = self.list_projects_paths(self.groups)

    def verify_project(self, project_candidate: str) -> None:
        """Raises an error if the input is not a valid project."""
        if project_candidate not in self.projects:
            raise ValueError(f"'{project_candidate}' is not a valid project.")

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
            not temp type

        TODO: reduce coupling, temps defined by startswith char
        give warning if name starts with temp_prefix
        """

        # unique project name
        if new_project in self.projects:
            raise FileExistsError(
                f"'{new_project}' already exists in the project group: '{self.get_group_from_project(new_project)}'."
            )

        # Quick fix
        if new_project.startswith(temp_prefix):
            warnings.warn(f"'{new_project}' classified as a temporary project, susceptible to easy deletion.")

        return True


class Project:
    """Manages files within a chosen project."""

    default_data_folder_names_map = {
        "raw": "raw",
        "interim": "interim",
        "processed": "processed",
        "external": "external",
    }
    default_unlock_wait_lock_seconds = 10

    def __init__(
        self,
        this_project_path: Path,
        data_folder_names: list[str] = list(default_data_folder_names_map.values()),
        url: str | None = None,
    ) -> None:
        """Structure rules:
        folder:
            key = "name"
            does not end in .ext
            has value {}

        file:
            key = "name.ext"
            ends in .ext
            has value None

        Known files:
            .txt, .md
            .ipynb

        """
        self.this_project_path: Path = this_project_path
        self.data_folder_names: list[str] = data_folder_names
        self.url = url

        r = self.default_data_folder_names_map["raw"]
        i = self.default_data_folder_names_map["interim"]
        p = self.default_data_folder_names_map["processed"]
        e = self.default_data_folder_names_map["external"]

        # Plans to separate structures to be inputs in config
        data_folders_structure: Tree = {
            "data": {
                f"{r}": {},
                f"{i}": {},
                f"{p}": {},
                f"{e}": {},
            }
        }

        # Location of data dump
        # data_dump_folder a subjset of data_folders_structure
        data_dump_path: Path = self.this_project_path / "data" / r
        data_interim_path: Path = self.this_project_path / "data" / i
        data_external_path: Path = self.this_project_path / "data" / e
        # data_dump_folder: Tree = {
        #     "data": {
        #         f"{r}": {},
        #     }
        # }

        db_folder_structure: Tree = {
            "data": {
                "db": {},
            }
        }

        other_files_structure: Tree = {
            "docs": {
                "assets": {},
                "notes.txt": None,
            },
            "notebooks": {
                f"{self.this_project_path.name}.ipynb": None,
            },
            "references": {
                "sources.txt": None,
            },
            "reports": {
                "figures": {},
            },
            "README.md": None,
        }

        # The data source goes here
        # sources_folder a subset of other_files_structure
        sources_path: Path = self.this_project_path / "references" / "sources.txt"
        # sources_folder: Tree = {
        #     "references:": {
        #         "sources.txt": None,
        #     }
        # }

        self.name = this_project_path.name
        self.group = this_project_path.parent.name

        self.data_folders_structure: Tree = data_folders_structure
        self.db_folder_structure: Tree = db_folder_structure
        self.other_files_structure: Tree = other_files_structure

        # self.data_dump_folder = data_dump_folder
        # self.sources_folder = sources_folder

        self.data_dump_path: Path = data_dump_path
        self.data_interim_path: Path = data_interim_path
        self.data_external_path: Path = data_external_path
        self.sources_path: Path = sources_path

    def is_locked(self) -> bool:
        """Checks if a project is locked.

        A project is locked iff:
            contains a file: .locked in root
        """

        dirs = os.listdir(self.this_project_path)
        if ".locked" in dirs:
            return True

        return False

    def lock(self) -> None:
        """Locks a project."""

        if not self.is_locked():
            (self.this_project_path / ".locked").touch()
        return

    def unlock(self) -> None:
        """Unlocks a project."""

        if self.is_locked():
            os.remove(self.this_project_path / ".locked")
        return

    def unlock_wait_lock(self, seconds: int = default_unlock_wait_lock_seconds) -> None:
        self.unlock()
        # threading.Timer(seconds, self.lock).start()
        time.sleep(seconds)
        self.lock()

    def mkdir_data_folders(self) -> None:
        create_structure(base_path=self.this_project_path, tree=self.data_folders_structure)

    def mkdir_other_files(self) -> None:
        create_structure(base_path=self.this_project_path, tree=self.other_files_structure)

    def mkdir_db_folder(self) -> None:
        create_structure(base_path=self.this_project_path, tree=self.db_folder_structure)

    def append_source(self, source: str) -> None:
        """Append a source to sources.txt"""

        with open(self.sources_path, "a") as f:
            f.write(f"{source}")

    def handle_url(self, url: str) -> Path:
        dispatcher = URLDispatcher()
        return dispatcher.download(
            url,
            raw_path=self.data_dump_path,
            external_path=self.data_external_path,
        )

    def data_ls(self) -> DataFrame:
        """View the data filenames in this project."""

        df = pd.DataFrame()
        for f in self.data_folder_names:
            data_folder_path = self.this_project_path / "data" / f

            if not data_folder_path.exists():
                data_folder_path.mkdir(parents=True, exist_ok=True)

            data_files = os.listdir(data_folder_path)

            df_concat = pd.DataFrame(
                data_files,
                columns=[f],
            )
            df = pd.concat([df, df_concat], axis=1)
        return df

    def data_copy(self, overwrite: bool = False) -> list[Path]:
        """Copies all files from raw to interim.
        Force is force overwrite.

        Returns list of succefully created copies.
        """

        self.data_interim_path.mkdir(parents=True, exist_ok=True)

        raw_files = os.listdir(self.data_dump_path)
        # raw_file_paths = [self.data_dump_path / raw_file for raw_file in raw_files]

        created_copies: list[Path] = []
        for raw_filename in raw_files:
            stem, ext = os.path.splitext(raw_filename)
            new_stem = stem + copy_appendage
            new_raw_filename = new_stem + ext

            src = self.data_dump_path / raw_filename
            dst = self.data_interim_path / new_raw_filename

            if dst.exists():
                if not overwrite:
                    continue

            shutil.copyfile(src, dst)
            created_copies.append(dst)

        return created_copies

    def data_promote(self) -> None:
        self.data_copy()
