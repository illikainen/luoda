# pylint: disable=W0621
#
# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from pathlib import Path

from jinja2 import FileSystemLoader
from jinja2.exceptions import SecurityError
from pytest import raises

from luoda.item import Item
from luoda.plugins.render import Sandbox, available, run

from ..fixtures import tmpdir  # pylint: disable=W0611


def test_sandbox(tmpdir: Path) -> None:
    (tmpdir / "template").write_text("{{ func() }}")

    loader = FileSystemLoader(".")
    env = Sandbox(loader=loader)
    template = env.get_template("template")

    with raises(SecurityError):
        template.render(func=lambda: 123)


def test_available() -> None:
    assert available()


def test_render(tmpdir: Path) -> None:
    (tmpdir / "template").write_text("x {{ item.content }} y")

    item = Item(content="abc", path=tmpdir / "foo", template="template")
    config = {"build": {"template-dir": "."}}

    new_item = run(item, items=[], config=config)
    assert new_item.content == "x abc y"
    assert new_item != item


def test_template_not_found(tmpdir: Path) -> None:
    item = Item(content="abc", path=tmpdir / "foo", template="template")
    config = {"build": {"template-dir": "."}}

    assert run(item, items=[], config=config) == item
