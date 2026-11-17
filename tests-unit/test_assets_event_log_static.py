"""Static discipline check for the ``[assets-event]`` log lines.

Pure :mod:`ast` analysis: no module under ``app/assets`` is imported or
executed, so this check never needs a running ComfyUI. It deliberately lives at
the ``tests-unit`` root rather than under ``tests-unit/assets_test/``, whose
autouse fixture boots a ComfyUI subprocess for every test in that subtree.

Three rules are enforced over every emit call site:

a. keyword fields come from the closed vocabulary, the event is a string literal
b. no other log line anywhere carries the tag, so the tap only ever sees emits
c. ``error_type=`` values come from ``event_log.error_type()``, never a string
"""

from __future__ import annotations

import ast
from collections.abc import Iterator
from pathlib import Path
from typing import NamedTuple

from app.assets.event_log import ALLOWED_EVENTS, ALLOWED_FIELDS, TAG

REPO_ROOT = Path(__file__).resolve().parents[1]
EVENT_LOG_NAME = "event_log"
LOG_METHODS = frozenset({"debug", "info", "warning", "error", "exception", "critical", "log"})


class Aliases(NamedTuple):
    """The names one module binds to the event_log module and its functions."""

    module: frozenset[str]
    emit: frozenset[str]
    error_type: frozenset[str]


class Scan(NamedTuple):
    """Everything the AST walk learned about the tree."""

    files: tuple[str, ...]
    vocabulary: tuple[str, ...]
    event_names: tuple[str, ...]
    error_types: tuple[str, ...]
    tagged_logs: tuple[str, ...]


def _scanned_files(root: Path) -> tuple[str, ...]:
    """Every assets module, plus server.py for its single assets.enabled emit."""
    assets = sorted(p.relative_to(root).as_posix() for p in root.glob("app/assets/**/*.py"))
    return (*assets, "server.py")


def _resolve_aliases(tree: ast.Module) -> Aliases:
    module: set[str] = set()
    emit: set[str] = set()
    error_type: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[-1] == EVENT_LOG_NAME:
                    module.add(alias.asname or alias.name)
        elif isinstance(node, ast.ImportFrom):
            from_event_log = (node.module or "").rsplit(".", 1)[-1] == EVENT_LOG_NAME
            for alias in node.names:
                if from_event_log and alias.name == "emit":
                    emit.add(alias.asname or alias.name)
                elif from_event_log and alias.name == "error_type":
                    error_type.add(alias.asname or alias.name)
                elif not from_event_log and alias.name == EVENT_LOG_NAME:
                    module.add(alias.asname or alias.name)
    return Aliases(frozenset(module), frozenset(emit), frozenset(error_type))


def _is_emit_call(func: ast.expr, aliases: Aliases) -> bool:
    if isinstance(func, ast.Attribute) and func.attr == "emit" and isinstance(func.value, ast.Name):
        return func.value.id in aliases.module
    return isinstance(func, ast.Name) and func.id in aliases.emit


def _is_error_type_call(value: ast.expr, aliases: Aliases) -> bool:
    """True only for a call to the sanctioned event_log.error_type()."""
    if not isinstance(value, ast.Call):
        return False
    func = value.func
    if isinstance(func, ast.Attribute) and func.attr == "error_type" and isinstance(func.value, ast.Name):
        return func.value.id in aliases.module
    return isinstance(func, ast.Name) and func.id in aliases.error_type


def _carries_tag(node: ast.Call) -> bool:
    return any(
        isinstance(child, ast.Constant) and isinstance(child.value, str) and TAG in child.value
        for child in ast.walk(node)
    )


def _is_log_call(func: ast.expr) -> bool:
    return isinstance(func, ast.Attribute) and func.attr in LOG_METHODS


def _event_of(call: ast.Call) -> str | None:
    """The literal event name, or None when it is not a plain string literal."""
    if len(call.args) != 1:
        return None
    first = call.args[0]
    if not isinstance(first, ast.Constant) or not isinstance(first.value, str):
        return None
    return first.value


def _field_faults(call: ast.Call, aliases: Aliases) -> Iterator[tuple[str, str]]:
    """(category, reason) for every keyword that breaks rule (a) or rule (d)."""
    for keyword in call.keywords:
        if keyword.arg is None:
            yield "vocabulary", "**splat fields cannot be checked statically"
        elif keyword.arg not in ALLOWED_FIELDS:
            yield "vocabulary", f"field {keyword.arg!r} is not in ALLOWED_FIELDS"
        elif keyword.arg == "error_type" and not _is_error_type_call(keyword.value, aliases):
            yield (
                "error_types",
                "error_type= must be a call to event_log.error_type(), got "
                f"{ast.unparse(keyword.value)!r}",
            )


def _file_faults(call: ast.Call, aliases: Aliases) -> Iterator[tuple[str, str]]:
    if _is_emit_call(call.func, aliases):
        event = _event_of(call)
        if event not in ALLOWED_EVENTS:
            yield "event_names", "the event must be one string literal in the allowed vocabulary"
        yield from _field_faults(call, aliases)
    elif _is_log_call(call.func) and _carries_tag(call):
        yield "tagged_logs", f"log line carries {TAG} outside event_log.emit()"


def scan_repository(root: Path = REPO_ROOT) -> Scan:
    files = _scanned_files(root)
    found: dict[str, list[str]] = {"vocabulary": [], "event_names": [], "error_types": [], "tagged_logs": []}
    for relative in files:
        tree = ast.parse((root / relative).read_text(encoding="utf-8"), filename=relative)
        aliases = _resolve_aliases(tree)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                for category, reason in _file_faults(node, aliases):
                    found[category].append(f"{relative}:{node.lineno}: {reason}")
    return Scan(
        files=files,
        vocabulary=tuple(found["vocabulary"]),
        event_names=tuple(found["event_names"]),
        error_types=tuple(found["error_types"]),
        tagged_logs=tuple(found["tagged_logs"]),
    )


SCAN = scan_repository()


def test_the_walk_actually_covers_the_assets_tree() -> None:
    """Guards every other check: a broken glob would make them all vacuous."""
    assert "app/assets/event_log.py" in SCAN.files
    assert "app/assets/seeder.py" in SCAN.files
    assert "server.py" in SCAN.files
    assert len(SCAN.files) > 20


def test_emit_fields_stay_inside_the_closed_vocabulary() -> None:
    assert SCAN.vocabulary == ()


def test_emit_events_are_literals_in_the_allowed_vocabulary() -> None:
    assert SCAN.event_names == ()


def test_error_type_values_come_from_event_log_error_type() -> None:
    assert SCAN.error_types == ()


def test_no_other_log_line_carries_the_event_tag() -> None:
    assert SCAN.tagged_logs == ()
