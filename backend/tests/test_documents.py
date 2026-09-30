import io
from fastapi.testclient import TestClient


def test_upload_document_authenticated(client: TestClient, auth_headers):
    file_content = b"%PDF-1.4 sample accessible syllabus content for biology 101"
    files = {"file": ("biology_syllabus.pdf", io.BytesIO(file_content), "application/pdf")}
    response = client.post("/documents", headers=auth_headers, files=files)

    assert response.status_code == 201
    data = response.json()
    assert data["original_filename"] == "biology_syllabus.pdf"
    assert data["mime_type"] == "application/pdf"
    assert data["file_size"] == len(file_content)
    assert data["status"] == "UPLOADED"
    assert "latest_job_id" in data
    assert data["latest_job_id"] is not None


def test_upload_document_unauthenticated_fails(client: TestClient):
    file_content = b"Sample text"
    files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
    response = client.post("/documents", files=files)
    assert response.status_code == 401


def test_list_user_documents(client: TestClient, auth_headers):
    # Upload 2 documents
    client.post(
        "/documents",
        headers=auth_headers,
        files={"file": ("doc1.txt", io.BytesIO(b"Doc 1"), "text/plain")}
    )
    client.post(
        "/documents",
        headers=auth_headers,
        files={"file": ("doc2.pdf", io.BytesIO(b"%PDF-1.4 Doc 2"), "application/pdf")}
    )

    response = client.get("/documents", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 2
    filenames = [d["original_filename"] for d in data["items"]]
    assert "doc1.txt" in filenames
    assert "doc2.pdf" in filenames


def test_get_document_by_id(client: TestClient, auth_headers):
    upload_res = client.post(
        "/documents",
        headers=auth_headers,
        files={"file": ("lesson_plan.docx", io.BytesIO(b"PK\x03\x04 Sample DOCX"), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
    )
    assert upload_res.status_code == 201
    doc_id = upload_res.json()["id"]

    response = client.get(f"/documents/{doc_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == doc_id
    assert data["original_filename"] == "lesson_plan.docx"


def test_upload_unsupported_file_type_fails(client: TestClient, auth_headers):
    files = {"file": ("malicious.exe", io.BytesIO(b"MZ executable content"), "application/x-msdownload")}
    response = client.post("/documents", headers=auth_headers, files=files)
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "UNSUPPORTED_FILE_TYPE"


def test_upload_oversized_file_fails(client: TestClient, auth_headers, monkeypatch):
    # Simulate low MAX_FILE_SIZE_MB for testing
    from app.core.config import settings
    monkeypatch.setattr(settings, "MAX_FILE_SIZE_MB", 1)  # 1 MB

    large_content = b"A" * (1024 * 1024 + 100)  # slightly over 1 MB
    files = {"file": ("large_text.txt", io.BytesIO(large_content), "text/plain")}
    response = client.post("/documents", headers=auth_headers, files=files)
    assert response.status_code == 413
    data = response.json()
    assert data["error"]["code"] == "FILE_TOO_LARGE"
