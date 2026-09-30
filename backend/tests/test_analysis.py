import pytest
from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.user import User
from app.pipeline.analyze import ContentAnalyzer
from app.providers.mock_llm import MockLLMProvider


def test_content_analyzer_pedagogical_extraction(db_session: Session, test_user: User):
    # Setup document with normalized content
    doc = Document(
        owner_id=test_user.id,
        original_filename="biology_lesson.pdf",
        stored_filename="stored_bio.pdf",
        file_size=1024,
        mime_type="application/pdf",
        storage_key="users/test/stored_bio.pdf",
        status="READY",
        extraction_status="COMPLETED",
        normalized_content={
            "schema_version": "1.0.0",
            "id": "doc_123",
            "title": "Photosynthesis and Cell Energy",
            "sections": [
                {
                    "id": "sec_1",
                    "title": "Introduction",
                    "blocks": [
                        {
                            "id": "blk_1",
                            "type": "heading",
                            "source_text": "Photosynthesis Overview",
                            "page_or_slide": 1
                        },
                        {
                            "id": "blk_2",
                            "type": "paragraph",
                            "source_text": "Photosynthesis is the process by which plants use sunlight, water, and carbon dioxide to create glucose.",
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

    analyzer = ContentAnalyzer(llm_provider=MockLLMProvider())
    analysis = analyzer.analyze_document(document=doc, db=db_session)

    assert analysis is not None
    assert analysis.document_id == doc.id
    assert analysis.language == "en"
    assert analysis.subject == "Biology"
    assert analysis.complexity in ["beginner", "elementary", "intermediate", "advanced"]
    assert len(analysis.learning_objectives) >= 1
    assert len(analysis.concepts) >= 1
    assert len(analysis.vocabulary) >= 1
    assert any("blk_1" in c.get("source_block_ids", []) or "blk_2" in c.get("source_block_ids", []) for c in analysis.concepts)
