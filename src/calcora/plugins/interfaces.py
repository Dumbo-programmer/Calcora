from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, Sequence

from ..engine.models import Domain, StepGraph


@dataclass(frozen=True)
class PluginManifest:
    name: str
    version: str
    description: str


@dataclass(frozen=True)
class RuleCapabilities:
    name: str
    operation: str
    priority: int
    domains: Sequence[Domain]


class RulePlugin(Protocol):
    manifest: PluginManifest
    capabilities: RuleCapabilities

    @property
    def name(self) -> str:  # convenience
        ...

    def matches(self, *, expression: str) -> bool:
        ...

    def apply(self, *, expression: str, graph: StepGraph) -> tuple[str, str, Sequence[str], dict[str, Any]]:
        """Return (output_expr, explanation, dependency_ids, metadata)."""
        ...


@dataclass(frozen=True)
class SolverCapabilities:
    name: str
    operation: str
    domains: Sequence[Domain]


class SolverPlugin(Protocol):
    manifest: PluginManifest
    capabilities: SolverCapabilities

    @property
    def name(self) -> str:
        ...

    def solve(self, *, expression: str) -> tuple[str, dict[str, Any]]:
        ...


@dataclass(frozen=True)
class RendererCapabilities:
    name: str
    formats: Sequence[str]


class RendererPlugin(Protocol):
    manifest: PluginManifest
    capabilities: RendererCapabilities

    @property
    def name(self) -> str:
        ...

    def render(self, *, result: Any, format: str, verbosity: str) -> str:
        ...
