import pytest
from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.user import User
from app.models.variant import GeneratedVariant
from app.pipeline.planner import AccessibilityPlanner
from app.pipeline.transform import TransformationEngine
from app.pipeline.cache import TransformationCacheManager
from app.providers.mock_llm import MockLLMProvider


def test_transformation_engine_and_caching(db_session: Session, test_user: User):
    doc = Document(
        owner_id=test_user.id,
        original_filename="bio.pdf",
        stored_filename="stored_bio.pdf",
        file_size=500,
        mime_type="application/pdf",
        storage_key="users/test/stored_bio.pdf",
        status="READY",
        extraction_status="COMPLETED",
        normalized_content={
            "schema_version": "1.0.0",
            "id": "doc_t",
            "title": "Bio Lesson",
            "sections": [
                {
                    "id": "sec_1",
                    "title": "Part 1",
                    "blocks": [
                        {
                            "id": "blk_101",
                            "type": "paragraph",
                            "source_text": "Water boils at 100°C under 1 atmosphere pressure.",
                            "page_or_slide": 1
                        }
                    ]
                }
            ]
        }
    )
    db_session.add(doc)
    db_session.commit()
    db_session.refresh(doc)

    variant = GeneratedVariant(
        document_id=doc.id,
        name="Dyslexia Variant",
        status="PENDING",
        profile_ids=["dyslexia"],
        profile_versions={"dyslexia": "1.0.0"}
    )
    db_session.add(variant)
    db_session.commit()
    db_session.refresh(variant)

    planner = AccessibilityPlanner()
    plan = planner.create_plan(
        document_id=doc.id,
        normalized_content=doc.normalized_content,
        analysis=None,
        profile_ids=["dyslexia"]
    )

    mock_llm = MockLLMProvider()
    cache_mgr = TransformationCacheManager()
    engine = TransformationEngine(llm_provider=mock_llm, cache_manager=cache_mgr)

    # 1. First run: Generates via MockLLM and caches result
    blocks_1 = engine.transform_variant(
        variant=variant,
        document=doc,
        analysis=None,
        plan=plan,
        db=db_session
    )

    assert len(blocks_1) == 1
    assert blocks_1[0].source_block_id == "blk_101"
    assert blocks_1[0].status == "COMPLETED"
    assert blocks_1[0].provider == "mock"
    assert "simplified_text" in blocks_1[0].content

    # 2. Second run for a new variant with identical block: should hit cache!
    variant2 = GeneratedVariant(
        document_id=doc.id,
        name="Dyslexia Variant 2",
        status="PENDING",
        profile_ids=["dyslexia"],
        profile_versions={"dyslexia": "1.0.0"}
    )
    db_session.add(variant2)
    db_session.commit()
    db_session.refresh(variant2)

    blocks_2 = engine.transform_variant(
        variant=variant2,
        document=doc,
        analysis=None,
        plan=plan,
        db=db_session
    )

    assert len(blocks_2) == 1
    assert blocks_2[0].source_block_id == "blk_101"
    assert blocks_2[0].provider == "cache"
