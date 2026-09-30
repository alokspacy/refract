import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.user import User
from app.workers.tasks import analyze_document_job, generate_variant_job


@pytest.fixture
def sample_ready_doc(db_session: Session, test_user: User) -> Document:
    doc = Document(
        owner_id=test_user.id,
        original_filename="photosynthesis_chapter.pdf",
        stored_filename="stored_photo.pdf",
        file_size=2048,
        mime_type="application/pdf",
        storage_key="users/test/stored_photo.pdf",
        status="READY",
        extraction_status="COMPLETED",
        normalized_content={
            "schema_version": "1.0.0",
            "id": "doc_api_test",
            "title": "Photosynthesis Chapter",
            "sections": [
                {
                    "id": "sec_1",
                    "title": "Chapter 1",
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
                            "source_text": "Chloroplasts capture photons of light to synthesize sugars.",
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
    return doc


def test_get_profiles_endpoint(client: TestClient):
    response = client.get("/profiles")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3
    profile_ids = [p["id"] for p in data]
    assert "dyslexia" in profile_ids
    assert "cognitive" in profile_ids


def test_analyze_and_get_analysis_endpoint(
    client: TestClient,
    auth_headers: dict,
    sample_ready_doc: Document,
    db_session: Session
):
    # 1. Trigger analysis via API
    analyze_res = client.post(f"/documents/{sample_ready_doc.id}/analyze", headers=auth_headers)
    assert analyze_res.status_code == 200
    job_data = analyze_res.json()
    assert "id" in job_data

    # 2. Run analysis task in-process with test DB session
    analyze_result = analyze_document_job(
        job_id=job_data["id"],
        document_id=sample_ready_doc.id,
        db_override=db_session
    )
    assert analyze_result["status"] == "success"

    # 3. Get Analysis via API
    get_res = client.get(f"/documents/{sample_ready_doc.id}/analysis", headers=auth_headers)
    assert get_res.status_code == 200
    analysis_data = get_res.json()
    assert analysis_data["document_id"] == sample_ready_doc.id
    assert analysis_data["subject"] == "Biology"
    assert len(analysis_data["learning_objectives"]) >= 1


def test_create_and_fetch_variant_endpoint(
    client: TestClient,
    auth_headers: dict,
    sample_ready_doc: Document,
    db_session: Session
):
    # 1. Create Variant via API
    create_res = client.post(
        f"/documents/{sample_ready_doc.id}/variants",
        json={"profile_ids": ["dyslexia", "cognitive"]},
        headers=auth_headers
    )
    assert create_res.status_code == 201
    variant_info = create_res.json()
    variant_id = variant_info["variant_id"]
    job_id = variant_info["job_id"]
    assert variant_id is not None

    # 2. Execute Variant generation task
    gen_result = generate_variant_job(
        job_id=job_id,
        document_id=sample_ready_doc.id,
        variant_id=variant_id,
        profile_ids=["dyslexia", "cognitive"],
        db_override=db_session
    )
    assert gen_result["status"] == "success"

    # 3. Fetch Variant Details via API
    var_res = client.get(f"/variants/{variant_id}", headers=auth_headers)
    assert var_res.status_code == 200
    var_data = var_res.json()
    assert var_data["id"] == variant_id
    assert "dyslexia" in var_data["profile_ids"]

    # 4. Fetch Variant Blocks via API
    blocks_res = client.get(f"/variants/{variant_id}/blocks", headers=auth_headers)
    assert blocks_res.status_code == 200
    blocks_data = blocks_res.json()
    assert len(blocks_data) >= 1
    assert "source_block_id" in blocks_data[0]

    # 5. Fetch Variant Validation via API
    val_res = client.get(f"/variants/{variant_id}/validation", headers=auth_headers)
    assert val_res.status_code == 200
    val_data = val_res.json()
    assert val_data["variant_id"] == variant_id
    assert val_data["is_valid"] is True


def test_unauthorized_user_cannot_access_other_user_variants(
    client: TestClient,
    auth_headers: dict,
    another_auth_headers: dict,
    sample_ready_doc: Document,
    db_session: Session
):
    # User 1 creates variant
    create_res = client.post(
        f"/documents/{sample_ready_doc.id}/variants",
        json={"profile_ids": ["dyslexia"]},
        headers=auth_headers
    )
    variant_id = create_res.json()["variant_id"]

    # User 2 tries to access User 1's variant
    user2_res = client.get(f"/variants/{variant_id}", headers=another_auth_headers)
    assert user2_res.status_code == 403
