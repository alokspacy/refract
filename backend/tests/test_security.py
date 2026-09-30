import io
from fastapi.testclient import TestClient


def test_path_traversal_filename_sanitization(client: TestClient, auth_headers):
    # Attacker tries to provide a filename with directory traversal
    traversal_filename = "../../../etc/passwd.txt"
    files = {"file": (traversal_filename, io.BytesIO(b"Safe content"), "text/plain")}

    response = client.post("/documents", headers=auth_headers, files=files)
    assert response.status_code == 201
    data = response.json()
    # Stored filename must NOT contain '..' or '/'
    assert ".." not in data["stored_filename"]
    assert "/" not in data["stored_filename"]
    assert "\\" not in data["stored_filename"]
    assert data["storage_key"].startswith("users/")


def test_executable_extension_rejection(client: TestClient, auth_headers):
    dangerous_files = [
        ("payload.exe", b"MZ...", "application/octet-stream"),
        ("script.sh", b"#!/bin/bash\nrm -rf /", "application/x-sh"),
        ("exploit.php", b"<?php phpinfo(); ?>", "application/x-php"),
        ("virus.bat", b"@echo off", "application/x-bat"),
    ]

    for fname, content, mtype in dangerous_files:
        files = {"file": (fname, io.BytesIO(content), mtype)}
        response = client.post("/documents", headers=auth_headers, files=files)
        assert response.status_code == 400, f"Expected {fname} to be rejected"
        assert response.json()["error"]["code"] == "UNSUPPORTED_FILE_TYPE"


def test_cross_user_document_isolation(client: TestClient, auth_headers, another_auth_headers):
    # Teacher 1 uploads private syllabus
    upload_res = client.post(
        "/documents",
        headers=auth_headers,
        files={"file": ("teacher1_exam.pdf", io.BytesIO(b"%PDF exam"), "application/pdf")}
    )
    doc_id = upload_res.json()["id"]

    # Teacher 2 tries to access Teacher 1's document
    get_res = client.get(f"/documents/{doc_id}", headers=another_auth_headers)
    assert get_res.status_code == 403
    assert get_res.json()["error"]["code"] == "FORBIDDEN"


def test_invalid_and_malformed_jwt_tokens(client: TestClient):
    # Malformed token
    res1 = client.get("/auth/me", headers={"Authorization": "Bearer malformed.jwt.token"})
    assert res1.status_code == 401
    assert res1.json()["error"]["code"] == "INVALID_TOKEN"

    # Missing Bearer prefix
    res2 = client.get("/auth/me", headers={"Authorization": "SomeRandomString"})
    assert res2.status_code == 401

    # Completely missing header
    res3 = client.get("/auth/me")
    assert res3.status_code == 401
