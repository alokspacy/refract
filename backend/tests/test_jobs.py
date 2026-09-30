import io
from fastapi.testclient import TestClient


def test_job_status_retrieval(client: TestClient, auth_headers):
    # Upload document which generates a job
    upload_res = client.post(
        "/documents",
        headers=auth_headers,
        files={"file": ("syllabus.pdf", io.BytesIO(b"%PDF syllabus"), "application/pdf")}
    )
    assert upload_res.status_code == 201
    job_id = upload_res.json()["latest_job_id"]
    assert job_id is not None

    # Retrieve job status
    job_res = client.get(f"/jobs/{job_id}", headers=auth_headers)
    assert job_res.status_code == 200
    data = job_res.json()
    assert data["id"] == job_id
    assert data["status"] in ["QUEUED", "PROCESSING", "COMPLETED"]
    assert data["current_stage"] in ["EXTRACTING", "FOUNDATION"]
    assert "progress" in data


def test_unauthorized_job_access(client: TestClient, auth_headers, another_auth_headers):
    # User 1 uploads document
    upload_res = client.post(
        "/documents",
        headers=auth_headers,
        files={"file": ("user1_notes.txt", io.BytesIO(b"Notes"), "text/plain")}
    )
    job_id = upload_res.json()["latest_job_id"]

    # User 2 tries to access User 1's job
    response = client.get(f"/jobs/{job_id}", headers=another_auth_headers)
    assert response.status_code == 403
    data = response.json()
    assert data["error"]["code"] == "FORBIDDEN"


def test_nonexistent_job_returns_404(client: TestClient, auth_headers):
    response = client.get("/jobs/00000000-0000-0000-0000-000000000000", headers=auth_headers)
    assert response.status_code == 404
    data = response.json()
    assert data["error"]["code"] == "JOB_NOT_FOUND"
