from __future__ import annotations

from dataclasses import dataclass

from ..engine.models import EngineResult, Verbosity
from ..plugins.interfaces import PluginManifest, RendererCapabilities


@dataclass(frozen=True)
class TextRenderer:
    manifest: PluginManifest = PluginManifest(
        name="calcora-builtin-renderers",
        version="0.1.0",
        description="Built-in text renderer",
    )
    capabilities: RendererCapabilities = RendererCapabilities(name="text", formats=("text",))

    @property
    def name(self) -> str:
        return self.capabilities.name

    def render(self, *, result: EngineResult, format: str, verbosity: str) -> str:
        v = Verbosity(verbosity)
        lines: list[str] = []
        lines.append(f"Operation: {result.operation}")
        lines.append(f"Input: {result.input}")
        lines.append(f"Output: {result.output}")
        lines.append("")

        if not result.graph.nodes:
            lines.append("(no steps)")
            return "\n".join(lines)

        lines.append("Steps:")
        for node in result.graph.nodes:
            if v == Verbosity.concise:
                lines.append(f"- {node.input} -> {node.output}")
            elif v == Verbosity.detailed:
                lines.append(f"- [{node.rule}] {node.input} -> {node.output}")
                lines.append(f"  {node.explanation}")
            else:
                lines.append(f"- [{node.rule}] {node.input} -> {node.output}")
                lines.append(f"  Explanation: {node.explanation}")
                if node.metadata:
                    lines.append(f"  Notes: {node.metadata}")

        return "\n".join(lines)
