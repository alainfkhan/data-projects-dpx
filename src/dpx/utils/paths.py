"""
Absolute paths

data-projects/
    dpx/
        src/
    dp-projects/
        main/
        playground/

Let:
DP_DIR = data-projects/
DPX_DIR = dpx/
PROJECTS_DIR = projects/
"""

from icecream import ic
from pathlib import Path

DPX_DIR = Path(__file__).parent.parent.parent.parent

DP_DIR = DPX_DIR.parent

PROJECTS_DIR = DP_DIR / "dp-projects"

MAIN_DIR = PROJECTS_DIR / "main"
PLAYGROUND_DIR = PROJECTS_DIR / "playground"


def main() -> None:
    ic(DPX_DIR)
    ic(DP_DIR)
    ic(PROJECTS_DIR)
    ic(MAIN_DIR)
    ic(PLAYGROUND_DIR)


if __name__ == "__main__":
    main()
