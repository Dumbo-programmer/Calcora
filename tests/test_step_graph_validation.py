from calcora.engine.models import StepGraph, StepNode
from calcora.engine.validation import StepValidationError, validate_step_graph


def test_step_graph_rejects_cycles():
    g = StepGraph(
        nodes=[
            StepNode(
                id="step_001",
                operation="differentiate",
                rule="r1",
                input="x",
                output="1",
                explanation="",
                dependencies=["step_002"],
            ),
            StepNode(
                id="step_002",
                operation="differentiate",
                rule="r2",
                input="x",
                output="1",
                explanation="",
                dependencies=["step_001"],
            ),
        ]
    )

    try:
        validate_step_graph(g)
    except StepValidationError:
        return

    raise AssertionError("Expected StepValidationError for a cycle")
