from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Sequence

from ..engine.models import Domain, StepGraph
from .interfaces import PluginManifest, RuleCapabilities


@dataclass(frozen=True)
class _RulePlugin:
    manifest: PluginManifest
    capabilities: RuleCapabilities
    _fn: Callable[[str, StepGraph], tuple[str, str, Sequence[str], dict[str, Any]]]
    _matches: Callable[[str], bool]

    @property
    def name(self) -> str:
        return self.capabilities.name

    def matches(self, *, expression: str) -> bool:
        return bool(self._matches(expression))

    def apply(self, *, expression: str, graph: StepGraph):
        return self._fn(expression, graph)


def rule(
    *,
    name: str,
    operation: str,
    priority: int = 0,
    domains: Sequence[Domain] = ("general",),
    plugin_name: str = "builtin",
    plugin_version: str = "0.0.0",
    plugin_description: str = "",
    matches: Callable[[str], bool] | None = None,
):
    """Decorator for authoring rule plugins.

    A rule plugin must be deterministic: for a given expression, it should either not match
    or produce the same output.
    """

    def _decorate(fn: Callable[[str, StepGraph], tuple[str, str, Sequence[str], dict[str, Any]]]):
        m = matches or (lambda _expr: True)
        return _RulePlugin(
            manifest=PluginManifest(name=plugin_name, version=plugin_version, description=plugin_description),
            capabilities=RuleCapabilities(
                name=name,
                operation=operation,
                priority=priority,
                domains=tuple(domains),
            ),
            _fn=fn,
            _matches=m,
        )

    return _decorate
