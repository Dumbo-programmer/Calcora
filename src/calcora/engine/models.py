from __future__ import annotations

from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field


class Verbosity(str, Enum):
    concise = "concise"
    detailed = "detailed"
    teacher = "teacher"


class StepNode(BaseModel):
    id: str
    operation: str
    rule: str
    input: str
    output: str
    explanation: str
    dependencies: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class StepGraph(BaseModel):
    """A deterministic, auditable reasoning DAG."""

    nodes: list[StepNode] = Field(default_factory=list)

    def node_ids(self) -> set[str]:
        return {n.id for n in self.nodes}


class EngineResult(BaseModel):
    operation: str
    input: str
    output: str
    graph: StepGraph


Domain = Literal["calculus", "algebra", "linear_algebra", "graph_theory", "numerical", "general"]
