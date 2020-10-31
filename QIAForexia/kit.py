"""
General toolkit.
"""

import os
import sys
from itertools import islice
from pathlib import Path
from typing import List, Union


class HiddenPrints:
    """To be used as:
    >>> with HiddenPrints:
        print("This will not be printed")
    print("This will be printed")
    """

    def __init__(self):
        self._original_stdout = None

    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


def tree(
    dir_path: Path,
    level: int = -1,
    limit_to_directories: bool = False,
    length_limit: int = 1000,
    summary: bool = False,
    no_parent: bool = False,
    ignore: Union[List[str], str] = None,
    show_only: Union[List[str], str] = None,
):
    """Given a directory Path object print a visual tree structure"""

    # pylint: disable=too-many-arguments,too-many-locals

    space = "    "
    branch = "│   "
    tee = "├── "
    last = "└── "
    dir_path = Path(dir_path)  # accept string coerceable to Path
    files = 0
    directories = 0
    if isinstance(ignore, str):
        ignore = [ignore]
    if isinstance(show_only, str):
        show_only = [show_only]

    def inner(dir_path: Path, prefix: str = "", level=-1):
        nonlocal files, directories
        if not level:
            return  # 0, stop iterating
        if limit_to_directories:
            contents = [d for d in dir_path.iterdir() if d.is_dir()]
        else:
            contents = list(dir_path.iterdir())
        if show_only:
            new_contents = []
            for content in contents:
                if content.name in show_only:
                    new_contents.append(content)
                    show_only.remove(content.name)
            contents = new_contents
        if ignore:
            contents = [
                content for content in contents if content.name not in ignore
            ]
        pointers = [tee] * (len(contents) - 1) + [last]
        for pointer, path in zip(pointers, contents):
            if path.is_dir():
                yield prefix + pointer + path.name
                directories += 1
                extension = branch if pointer == tee else space
                yield from inner(
                    path, prefix=prefix + extension, level=level - 1
                )
            elif not limit_to_directories:
                yield prefix + pointer + path.name
                files += 1

    if not no_parent:
        print(dir_path.name)
    iterator = inner(dir_path, level=level)
    for line in islice(iterator, length_limit):
        print(line)
    if next(iterator, None):
        print(f"... length_limit, {length_limit}, reached, counted:")
    if summary:
        print(
            f"\n{directories} directories"
            + (f", {files} files" if files else "")
        )


class Colors:
    """Colored prints"""

    # pylint: disable=too-few-public-methods

    NC = "\033[0m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    LIGHT_GRAY = "\033[37m"
    DARK_GRAY = "\033[90m"
    LIGHT_RED = "\033[91m"
    LIGHT_GREEN = "\033[92m"
    LIGHT_YELLOW = "\033[93m"
    LIGHT_BLUE = "\033[94m"
    LIGHT_MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    BOLD = "\033[2m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    INVERTED = "\033[7m"
    HIDDEN = "\033[8m"


def represent_int(string):
    """Test if string is integerable."""
    try:
        int(string)
        return True
    except ValueError:
        return False
