from __future__ import annotations

from .engine.step_engine import StepEngine
from .engine.calculus_rules import BUILTIN_DIFFERENTIATION_RULES, BUILTIN_ALGEBRA_RULES
from .engine.linalg_rules import BUILTIN_LINALG_RULES
from .engine.sympy_rules import SympyDifferentiateRule
from .plugins.registry import PluginRegistry
from .renderers.json_renderer import JsonRenderer
from .renderers.text import TextRenderer


def default_registry(*, load_entry_points: bool = True) -> PluginRegistry:
    registry = PluginRegistry()

    # Built-in renderers
    registry.register_renderer(TextRenderer())
    registry.register_renderer(JsonRenderer())

    # Built-in / bundled rules (prefer explicit rules; keep SymPy as fallback)
    for r in BUILTIN_DIFFERENTIATION_RULES:
        registry.register_rule(r)
    for r in BUILTIN_ALGEBRA_RULES:
        registry.register_rule(r)
    for r in BUILTIN_LINALG_RULES:
        registry.register_rule(r)
    registry.register_rule(SympyDifferentiateRule())

    if load_entry_points:
        registry.load_entry_points()

    return registry


def default_engine(*, load_entry_points: bool = True) -> StepEngine:
    return StepEngine(registry=default_registry(load_entry_points=load_entry_points))
