from __future__ import annotations

from collections import defaultdict, deque

from .models import StepGraph, StepNode


class StepValidationError(ValueError):
    pass


def validate_step_node(node: StepNode) -> None:
    if not node.id:
        raise StepValidationError("StepNode.id must be non-empty")
    if not node.operation:
        raise StepValidationError("StepNode.operation must be non-empty")
    if not node.rule:
        raise StepValidationError("StepNode.rule must be non-empty")
    if node.input is None or node.output is None:
        raise StepValidationError("StepNode input/output must be present")


def validate_step_graph(graph: StepGraph) -> None:
    seen: set[str] = set()
    for node in graph.nodes:
        validate_step_node(node)
        if node.id in seen:
            raise StepValidationError(f"Duplicate StepNode id: {node.id}")
        seen.add(node.id)

    # Dependencies must exist and be acyclic.
    edges: dict[str, list[str]] = defaultdict(list)
    indegree: dict[str, int] = {nid: 0 for nid in seen}

    for node in graph.nodes:
        for dep in node.dependencies:
            if dep not in seen:
                raise StepValidationError(f"Unknown dependency {dep} referenced by {node.id}")
            edges[dep].append(node.id)
            indegree[node.id] += 1

    q = deque([nid for nid, d in indegree.items() if d == 0])
    visited = 0
    while q:
        nid = q.popleft()
        visited += 1
        for nxt in edges.get(nid, []):
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                q.append(nxt)

    if visited != len(seen):
        raise StepValidationError("Cycle detected in StepGraph")
