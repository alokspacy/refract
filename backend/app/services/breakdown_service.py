"""Cognitive task breakdown service for neurodivergent learners."""
import uuid
from typing import List
from app.schemas.task_breakdown import SubTaskStep, TaskDecompositionResponse

class TaskBreakdownService:
    """Breaks complex educational assignments into bite-sized, low-cognitive-load steps."""

    def break_down_assignment(self, prompt: str) -> TaskDecompositionResponse:
        steps = [
            SubTaskStep(
                step_number=1,
                title="Skim & Orient",
                description="Read only the main headings and bold vocabulary words to get familiar.",
                estimated_minutes=5,
                sensory_tip="Take a deep breath and check your posture before starting."
            ),
            SubTaskStep(
                step_number=2,
                title="Identify Core Concepts",
                description="Highlight 2 to 3 main concepts from the first section.",
                estimated_minutes=10,
                sensory_tip="Use the reading ruler to focus one line at a time."
            ),
            SubTaskStep(
                step_number=3,
                title="Active Check-in",
                description="Answer the first comprehension self-check question.",
                estimated_minutes=8,
                sensory_tip="Hydrate or stretch your arms for 30 seconds."
            ),
            SubTaskStep(
                step_number=4,
                title="Review & Summary",
                description="Write or dictate one sentence explaining what you discovered.",
                estimated_minutes=7,
                sensory_tip="Great job completing your learning cycle!"
            )
        ]

        total_min = sum(s.estimated_minutes for s in steps)
        return TaskDecompositionResponse(
            task_id=str(uuid.uuid4())[:8],
            original_objective=prompt,
            total_estimated_minutes=total_min,
            steps=steps
        )
