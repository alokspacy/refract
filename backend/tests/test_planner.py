import pytest
from app.pipeline.planner import AccessibilityPlanner


def test_accessibility_planner_deterministic_mapping():
    planner = AccessibilityPlanner()
    normalized_content = {
        "schema_version": "1.0.0",
        "id": "doc_abc",
        "title": "Physics Laws",
        "sections": [
            {
                "id": "sec_1",
                "title": "Newton's First Law",
                "blocks": [
                    {
                        "id": "blk_1",
                        "type": "heading",
                        "source_text": "Inertia and Motion",
                        "page_or_slide": 1
                    },
                    {
                        "id": "blk_2",
                        "type": "paragraph",
                        "source_text": "An object at rest stays at rest unless acted upon by an external force.",
                        "page_or_slide": 1
                    }
                ]
            }
        ]
    }

    plan = planner.create_plan(
        document_id="doc_abc",
        normalized_content=normalized_content,
        analysis=None,
        profile_ids=["dyslexia", "cognitive"]
    )

    assert plan.document_id == "doc_abc"
    assert len(plan.profiles) == 2
    # 2 blocks * 2 profiles = 4 transformations
    assert len(plan.transformations) == 4
    
    # Verify deterministic block ID mapping
    block_ids = [t.source_block_id for t in plan.transformations]
    assert "blk_1" in block_ids
    assert "blk_2" in block_ids
