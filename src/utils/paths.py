"""
Absolute paths of superproject: data-projects.
Do not include data folders generated from initialisation.
"""

from pathlib import Path


BASE_DIR = Path(__file__).parent.parent.parent.resolve()
PROJECTS_DIR = BASE_DIR / "projects"
PLAYGROUND_DIR = BASE_DIR / "playground"
