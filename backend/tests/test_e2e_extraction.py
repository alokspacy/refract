import io
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.job import ProcessingJob
from app.providers.storage import StorageProvider
from app.workers.tasks import process_document_job
from tests.fixtures.generator import create_sample_pdf, create_sample_docx, create_sample_pptx


def test_e2e_pdf_upload_process_and_preview(client: TestClient, auth_headers: dict, db_session: Session, temp_storage: StorageProvider):
    # 1. Upload PDF
    pdf_bytes = create_sample_pdf()
    files = {"file": ("biology_chapter_1.pdf", io.BytesIO(pdf_bytes), "application/pdf")}
    upload_res = client.post("/documents", files=files, headers=auth_headers)
    assert upload_res.status_code == 201
    doc_data = upload_res.json()
    doc_id = doc_data["id"]
    job_id = doc_data["latest_job_id"]

    # 2. Run extraction synchronously with test database & storage overrides
    result = process_document_job(
        job_id=job_id,
        document_id=doc_id,
        db_override=db_session,
        storage_override=temp_storage
    )
    assert result["status"] == "success"

    # 3. Query Document Metadata
    doc_get_res = client.get(f"/documents/{doc_id}", headers=auth_headers)
    assert doc_get_res.status_code == 200
    doc_meta = doc_get_res.json()
    assert doc_meta["extraction_status"] == "COMPLETED"
    assert doc_meta["status"] == "READY"

    # 4. Query Normalized Content JSON
    content_res = client.get(f"/documents/{doc_id}/content", headers=auth_headers)
    assert content_res.status_code == 200
    content_data = content_res.json()
    assert content_data["schema_version"] == "1.0.0"
    assert content_data["id"] == doc_id
    assert len(content_data["sections"]) == 2
    
    # Verify Traceability
    all_blocks = [b for sec in content_data["sections"] for b in sec["blocks"]]
    assert len(all_blocks) > 0
    for block in all_blocks:
        assert "id" in block
        assert "type" in block
        assert block["page_or_slide"] in [1, 2]
        assert "metadata" in block

    # 5. Query Frontend Source Preview
    preview_res = client.get(f"/documents/{doc_id}/preview", headers=auth_headers)
    assert preview_res.status_code == 200
    preview_data = preview_res.json()
    assert preview_data["document_id"] == doc_id
    assert preview_data["extraction_status"] == "COMPLETED"
    assert len(preview_data["sections"]) == 2


def test_e2e_docx_upload_process_and_preview(client: TestClient, auth_headers: dict, db_session: Session, temp_storage: StorageProvider):
    docx_bytes = create_sample_docx()
    files = {"file": ("notes.docx", io.BytesIO(docx_bytes), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
    upload_res = client.post("/documents", files=files, headers=auth_headers)
    assert upload_res.status_code == 201
    doc_id = upload_res.json()["id"]
    job_id = upload_res.json()["latest_job_id"]

    # Execute task synchronously
    result = process_document_job(
        job_id=job_id,
        document_id=doc_id,
        db_override=db_session,
        storage_override=temp_storage
    )
    assert result["status"] == "success"

    # Verify Preview
    preview_res = client.get(f"/documents/{doc_id}/preview", headers=auth_headers)
    assert preview_res.status_code == 200
    preview_data = preview_res.json()
    assert preview_data["extraction_status"] == "COMPLETED"


def test_e2e_pptx_upload_process_and_preview(client: TestClient, auth_headers: dict, db_session: Session, temp_storage: StorageProvider):
    pptx_bytes = create_sample_pptx()
    files = {"file": ("slides.pptx", io.BytesIO(pptx_bytes), "application/vnd.openxmlformats-officedocument.presentationml.presentation")}
    upload_res = client.post("/documents", files=files, headers=auth_headers)
    assert upload_res.status_code == 201
    doc_id = upload_res.json()["id"]
    job_id = upload_res.json()["latest_job_id"]

    # Execute task synchronously
    result = process_document_job(
        job_id=job_id,
        document_id=doc_id,
        db_override=db_session,
        storage_override=temp_storage
    )
    assert result["status"] == "success"

    # Verify Content
    content_res = client.get(f"/documents/{doc_id}/content", headers=auth_headers)
    assert content_res.status_code == 200
    assert len(content_res.json()["sections"]) == 2
