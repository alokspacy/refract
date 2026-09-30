import io
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.providers.storage import StorageProvider
from app.workers.tasks import process_document_job, generate_variant_job
from tests.fixtures.generator import create_sample_pdf


def test_e2e_full_ai_core_pipeline(
    client: TestClient,
    auth_headers: dict,
    db_session: Session,
    temp_storage: StorageProvider
):
    # 1. Upload Educational PDF
    pdf_bytes = create_sample_pdf()
    files = {"file": ("ap_biology_chapter_1.pdf", io.BytesIO(pdf_bytes), "application/pdf")}
    upload_res = client.post("/documents", files=files, headers=auth_headers)
    assert upload_res.status_code == 201
    doc_data = upload_res.json()
    doc_id = doc_data["id"]
    job_id = doc_data["latest_job_id"]

    # 2. Run Phase 2 Extraction & Normalization
    extract_result = process_document_job(
        job_id=job_id,
        document_id=doc_id,
        db_override=db_session,
        storage_override=temp_storage
    )
    assert extract_result["status"] == "success"

    # 3. Verify Normalized Content JSON
    content_res = client.get(f"/documents/{doc_id}/content", headers=auth_headers)
    assert content_res.status_code == 200
    content_doc = content_res.json()
    assert len(content_doc["sections"]) >= 1

    # 4. Trigger Phase 3 Content Analysis
    analyze_res = client.post(f"/documents/{doc_id}/analyze", headers=auth_headers)
    assert analyze_res.status_code == 200
    analyze_job_id = analyze_res.json()["id"]

    # Execute Analysis Job in-process with test DB session
    from app.workers.tasks import analyze_document_job
    analyze_result = analyze_document_job(
        job_id=analyze_job_id,
        document_id=doc_id,
        db_override=db_session
    )
    assert analyze_result["status"] == "success"

    # 5. Fetch and Verify Content Analysis
    analysis_res = client.get(f"/documents/{doc_id}/analysis", headers=auth_headers)
    assert analysis_res.status_code == 200
    analysis = analysis_res.json()
    assert analysis["subject"] == "Biology"
    assert len(analysis["learning_objectives"]) >= 1
    assert len(analysis["concepts"]) >= 1
    assert len(analysis["vocabulary"]) >= 1

    # 6. Select Profiles (Dyslexia + Cognitive) and Generate Variant
    variant_create_res = client.post(
        f"/documents/{doc_id}/variants",
        json={"profile_ids": ["dyslexia", "cognitive"]},
        headers=auth_headers
    )
    assert variant_create_res.status_code == 201
    variant_data = variant_create_res.json()
    variant_id = variant_data["variant_id"]
    var_job_id = variant_data["job_id"]

    # 7. Execute Variant Generation Task Synchronously
    var_result = generate_variant_job(
        job_id=var_job_id,
        document_id=doc_id,
        variant_id=variant_id,
        profile_ids=["dyslexia", "cognitive"],
        db_override=db_session
    )
    assert var_result["status"] == "success"
    assert var_result["is_valid"] is True
    assert var_result["grounded"] is True

    # 8. Fetch Generated Variant Details
    get_variant_res = client.get(f"/variants/{variant_id}", headers=auth_headers)
    assert get_variant_res.status_code == 200
    assert get_variant_res.json()["status"] == "COMPLETED"

    # 9. Verify Generated Blocks and Traceability
    blocks_res = client.get(f"/variants/{variant_id}/blocks", headers=auth_headers)
    assert blocks_res.status_code == 200
    blocks = blocks_res.json()
    assert len(blocks) >= 2
    for b in blocks:
        assert b["source_block_id"] is not None
        assert b["profile_id"] in ["dyslexia", "cognitive"]
        assert b["status"] == "COMPLETED"
        assert b["prompt_version"] == "1.0.0"
        assert b["provider"] in ["mock", "cache"]

    # 10. Verify Validation Record
    val_res = client.get(f"/variants/{variant_id}/validation", headers=auth_headers)
    assert val_res.status_code == 200
    val_data = val_res.json()
    assert val_data["is_valid"] is True
    assert val_data["grounded"] is True
