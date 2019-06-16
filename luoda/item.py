# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from pathlib import Path

from attr import attrib, attrs


@attrs(frozen=True, kw_only=True)
class Item:
    author = attrib(type=str, default="")
    content = attrib(type=str, default="")
    date = attrib(type=str, default="")
    keywords = attrib(type=str, default="")
    mtime = attrib(type=str, default="")
    path = attrib(type=Path)
    template = attrib(type=str, default="")
    title = attrib(type=str, default="")