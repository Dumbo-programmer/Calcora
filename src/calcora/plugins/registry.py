from __future__ import annotations

from dataclasses import dataclass
from importlib import metadata
from typing import Iterable

from .interfaces import RendererPlugin, RulePlugin, SolverPlugin


class PluginLoadError(RuntimeError):
    pass


@dataclass(frozen=True)
class RegisteredRule:
    plugin: RulePlugin

    @property
    def name(self) -> str:
        return self.plugin.capabilities.name

    @property
    def operation(self) -> str:
        return self.plugin.capabilities.operation

    @property
    def priority(self) -> int:
        return int(self.plugin.capabilities.priority)

    def matches(self, *, expression: str) -> bool:
        return bool(self.plugin.matches(expression=expression))

    def apply(self, *, expression: str, graph):
        return self.plugin.apply(expression=expression, graph=graph)


class PluginRegistry:
    def __init__(self) -> None:
        self._rules: list[RegisteredRule] = []
        self._solvers: list[SolverPlugin] = []
        self._renderers: list[RendererPlugin] = []

    # --- Manual registration (useful for tests / local dev) ---
    def register_rule(self, plugin: RulePlugin) -> None:
        self._rules.append(RegisteredRule(plugin=plugin))

    def register_solver(self, plugin: SolverPlugin) -> None:
        self._solvers.append(plugin)

    def register_renderer(self, plugin: RendererPlugin) -> None:
        self._renderers.append(plugin)

    # --- Discovery via entry points ---
    def load_entry_points(self) -> None:
        self._load_group("calcora.rule_plugins", self.register_rule)
        self._load_group("calcora.solver_plugins", self.register_solver)
        self._load_group("calcora.renderer_plugins", self.register_renderer)

    def _load_group(self, group: str, registrar) -> None:
        try:
            eps = metadata.entry_points(group=group)
        except TypeError:
            # Python <3.10 compatibility: entry_points() returns dict-like
            all_eps = metadata.entry_points()
            eps = all_eps.get(group, []) if hasattr(all_eps, 'get') else []  # type: ignore[union-attr]

        for ep in eps:
            try:
                plugin_obj = ep.load()
            except Exception as e:  # noqa: BLE001
                raise PluginLoadError(f"Failed to load entry point {ep.name} ({group}): {e}") from e

            # Convention: entry point can be an instance or a factory.
            plugin = plugin_obj() if callable(plugin_obj) else plugin_obj
            registrar(plugin)

    # --- Rule selection ---
    def list_rules(self, *, operation: str) -> Iterable[RegisteredRule]:
        return sorted(
            (r for r in self._rules if r.operation == operation),
            key=lambda r: r.priority,
            reverse=True,
        )

    def select_rule(self, *, operation: str, expression: str) -> RegisteredRule | None:
        for rule in self.list_rules(operation=operation):
            if rule.matches(expression=expression):
                return rule
        return None

    # --- Renderers ---
    def get_renderer(self, *, format: str) -> RendererPlugin | None:
        for r in self._renderers:
            if format in r.capabilities.formats:
                return r
        return None
