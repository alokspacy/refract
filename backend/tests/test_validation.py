import pytest
from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.user import User
from app.models.variant import GeneratedVariant, GeneratedBlock
from app.pipeline.validate import ContentValidator
from app.providers.mock_llm import MockLLMProvider


def test_content_validator_number_preservation_and_grounding(db_session: Session, test_user: User):
    doc = Document(
        owner_id=test_user.id,
        original_filename="thermo.pdf",
        stored_filename="stored_thermo.pdf",
        file_size=500,
        mime_type="application/pdf",
        storage_key="users/test/stored_thermo.pdf",
        status="READY",
        extraction_status="COMPLETED",
        normalized_content={
            "schema_version": "1.0.0",
            "id": "doc_th",
            "title": "Thermodynamics",
            "sections": [
                {
                    "id": "sec_1",
                    "title": "Boiling Points",
                    "blocks": [
                        {
                            "id": "blk_num",
                            "type": "paragraph",
                            "source_text": "Water boils at exactly 100°C and freezes at 0°C under normal pressure.",
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
        name="Validation Test Variant",
        status="PROCESSING",
        profile_ids=["dyslexia"],
        profile_versions={"dyslexia": "1.0.0"}
    )
    db_session.add(variant)
    db_session.commit()
    db_session.refresh(variant)

    # Generated block with missing number
    gen_block = GeneratedBlock(
        variant_id=variant.id,
        source_block_id="blk_num",
        profile_id="dyslexia",
        content={
            "title": "Water Temperature",
            "simplified_text": "Water boils when it gets very hot and turns to ice when cold.",
            "key_points": ["Boils when hot", "Freezes when cold"],
            "important_terms": []
        },
        status="COMPLETED",
        prompt_version="1.0.0",
        model="mock-gpt-4o",
        provider="mock"
    )
    db_session.add(gen_block)
    db_session.commit()
    db_session.refresh(gen_block)

    validator = ContentValidator(llm_provider=MockLLMProvider())
    val_result = validator.validate_variant(
        variant=variant,
        document=doc,
        generated_blocks=[gen_block],
        db=db_session
    )

    assert val_result is not None
    assert val_result.variant_id == variant.id
    assert val_result.is_valid is True
    assert val_result.grounded is True
    # Verify that missing numeric token '100°C' or '0°C' triggered a warning
    assert len(val_result.warnings) >= 1
    assert any("100°C" in w or "0°C" in w for w in val_result.warnings)
