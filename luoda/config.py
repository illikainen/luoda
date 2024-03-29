# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from pathlib import Path
from typing import Any, Dict, cast

import toml
from pygments.styles import get_style_by_name
from voluptuous import (
    ALLOW_EXTRA,
    All,
    Coerce,
    Invalid,
    IsDir,
    Required,
    Schema,
)


class ConfigError(Exception):
    pass


Dir = Coerce(Path, "expected a directory")
ExistingDir = All(IsDir(None), Dir)
Highlight = Coerce(get_style_by_name, "expected a pygments style")

schema = Schema({
    Required("build", default={}): {
        Required("build-dir", default="build"): Dir,
        Required("collection-dir", default="collections"): ExistingDir,
        Required("template-dir", default="templates"): ExistingDir,
        Required("highlight", default="default"): Highlight,
        Required("plugins", default=[]): [str],
    },
    Required("collections", default=[]): [{  # yapf: ignore
        Required("name"): str,
        Required("template", default=""): str,
        Required("paths"): [str],
        Required("ignore-paths", default=[]): [str],
    }],
    Required("serve", default={}): {
        Required("host", default="127.0.0.1"): str,
        Required("port", default=8000): int,
    },
    Required("extra", default={}): {
    },
}, extra=ALLOW_EXTRA)


def read(path: Path) -> Dict[str, Any]:
    """
    Read and validate a TOML configuration.
    """
    try:
        return cast(Dict[str, Any], schema(toml.load(path)))
    except Invalid as e:
        msg = e.error_message
        paths = ".".join(str(p) for p in e.path)
        raise ConfigError("{}: {}".format(msg, paths))
