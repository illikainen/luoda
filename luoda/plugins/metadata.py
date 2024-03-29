# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

"""
Plugin that parses metadata.

The `mtime` property in `item` is always set.  The `author` and `date`
properties are set if the file is in a git repository.
"""

import re
from pathlib import Path
from typing import Any, Optional, Tuple

from attr import evolve
from dulwich.repo import Repo


def available() -> bool:
    return True


def run(item: Any, **_kwargs: Any) -> Any:
    git = find_git(item.path)
    if git:
        repo = Repo(git)
        relpath = Path(str(item.path)[len(git) + 1 if git != "." else 0:])
        file_date, author = get_commit(repo, relpath)
        dir_date, _ = get_commit(repo, relpath.parent)
        item = evolve(
            item,
            author=author,
            file_date=file_date,
            dir_date=dir_date,
        )
    return evolve(
        item,
        file_mtime=item.path.stat().st_mtime,
        dir_mtime=item.path.parent.stat().st_mtime,
    )


def find_git(path: Optional[Path]) -> Optional[str]:
    while path:
        if (path / ".git").is_dir():
            return str(path)
        path = path.parent if not path == path.parent else None
    return None


def get_commit(repo: Repo, path: Path) -> Tuple[float, str]:
    try:
        paths = [bytes(path)] if path.name else None
        walker = repo.get_walker(paths=paths, follow=True, reverse=True)
        commit = next(iter(walker)).commit
        return (commit.author_time, re.sub(" <.*", "", commit.author.decode()))
    except (KeyError, StopIteration):
        return (0.0, "")
