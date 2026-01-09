from __future__ import annotations

import json
from dataclasses import dataclass

from ..engine.models import EngineResult
from ..plugins.interfaces import PluginManifest, RendererCapabilities


@dataclass(frozen=True)
class JsonRenderer:
    manifest: PluginManifest = PluginManifest(
        name="calcora-builtin-renderers",
        version="0.1.0",
        description="Built-in JSON renderer",
    )
    capabilities: RendererCapabilities = RendererCapabilities(name="json", formats=("json",))

    @property
    def name(self) -> str:
        return self.capabilities.name

    def render(self, *, result: EngineResult, format: str, verbosity: str) -> str:
        # Verbosity affects *other* renderers; JSON is canonical and stable.
        payload = result.model_dump()
        return json.dumps(payload, indent=2, sort_keys=True)
