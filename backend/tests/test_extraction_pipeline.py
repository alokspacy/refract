import io
import pytest
from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.job import ProcessingJob
from app.models.user import User
from app.providers.mock_ocr import MockOCRProvider
from app.services.extraction_service import ExtractionService
from app.storage.local import LocalStorageProvider
from tests.fixtures.generator import create_sample_pdf, create_scanned_pdf


def test_extraction_pipeline_with_pdf(db_session: Session, test_user: User, tmp_path):
    storage = LocalStorageProvider(base_path=str(tmp_path))
    pdf_bytes = create_sample_pdf()
    storage_key = f"users/{test_user.id}/sample.pdf"
    storage.save(pdf_bytes, storage_key)

    doc = Document(
        id="doc_pdf_test",
        owner_id=test_user.id,
        original_filename="sample.pdf",
        stored_filename="sample.pdf",
        mime_type="application/pdf",
        file_size=len(pdf_bytes),
        storage_key=storage_key,
        status="UPLOADED",
        extraction_status="PENDING"
    )
    db_session.add(doc)
    db_session.commit()

    stages_recorded = []
    def progress_callback(stage, progress):
        stages_recorded.append((stage, progress))

    service = ExtractionService(storage=storage, ocr_provider=MockOCRProvider())
    content_doc = service.process_document(document=doc, db=db_session, progress_callback=progress_callback)

    assert doc.extraction_status == "COMPLETED"
    assert doc.status == "READY"
    assert doc.normalized_content is not None
    assert len(content_doc.sections) == 2
    assert ("EXTRACTING", 25) in stages_recorded
    assert ("NORMALIZING", 75) in stages_recorded
    assert ("COMPLETED", 100) in stages_recorded


def test_extraction_pipeline_with_scanned_pdf_triggers_ocr(db_session: Session, test_user: User, tmp_path):
    storage = LocalStorageProvider(base_path=str(tmp_path))
    scanned_bytes = create_scanned_pdf()
    storage_key = f"users/{test_user.id}/scanned.pdf"
    storage.save(scanned_bytes, storage_key)

    doc = Document(
        id="doc_scanned_test",
        owner_id=test_user.id,
        original_filename="scanned.pdf",
        stored_filename="scanned.pdf",
        mime_type="application/pdf",
        file_size=len(scanned_bytes),
        storage_key=storage_key,
        status="UPLOADED",
        extraction_status="PENDING"
    )
    db_session.add(doc)
    db_session.commit()

    stages_recorded = []
    def progress_callback(stage, progress):
        stages_recorded.append((stage, progress))

    service = ExtractionService(storage=storage, ocr_provider=MockOCRProvider())
    content_doc = service.process_document(document=doc, db=db_session, progress_callback=progress_callback)

    assert doc.extraction_status == "COMPLETED"
    assert ("OCR", 50) in stages_recorded
    assert len(doc.extraction_warnings) > 0
