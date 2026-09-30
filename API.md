# AccessLearn AI — REST API Specification (Phase 2)

Base URL: `http://localhost:8000`

---

## 1. Authentication Endpoints

### Register Teacher
- **`POST /auth/register`**
- **Body**: `{"email": "teacher@school.edu", "password": "SecurePassword123!", "name": "Jane Doe", "role": "teacher"}`
- **Response 201**: `{"access_token": "...", "token_type": "bearer", "user": {...}}`

### Login
- **`POST /auth/login`**
- **Body**: `{"email": "teacher@school.edu", "password": "SecurePassword123!"}`
- **Response 200**: `{"access_token": "...", "token_type": "bearer", "user": {...}}`

### Current User Profile
- **`GET /auth/me`**
- **Headers**: `Authorization: Bearer <token>`
- **Response 200**: `{"id": "...", "email": "...", "name": "...", "role": "teacher"}`

---

## 2. Document & Extraction Endpoints

### Upload Educational Document
- **`POST /documents`**
- **Headers**: `Authorization: Bearer <token>`
- **Body**: `multipart/form-data` with `file` field (PDF, DOCX, PPTX, PNG, JPG, TXT)
- **Response 201**:
  ```json
  {
    "id": "c71a3994-2790-482a-a5f1-326ea02e86c0",
    "owner_id": "...",
    "original_filename": "biology_chapter_1.pdf",
    "stored_filename": "c71a3994..._biology_chapter_1.pdf",
    "mime_type": "application/pdf",
    "file_size": 123456,
    "storage_key": "users/.../c71a3994..._biology_chapter_1.pdf",
    "status": "UPLOADED",
    "extraction_status": "PENDING",
    "extraction_warnings": null,
    "extracted_at": null,
    "latest_job_id": "job_001"
  }
  ```

### List Documents
- **`GET /documents`**
- **Headers**: `Authorization: Bearer <token>`
- **Response 200**: `{"items": [...], "total": 1}`

### Get Document Details
- **`GET /documents/{id}`**
- **Headers**: `Authorization: Bearer <token>`
- **Response 200**: Single `DocumentResponse` object.

### Trigger / Reprocess Document Extraction
- **`POST /documents/{id}/process`**
- **Headers**: `Authorization: Bearer <token>`
- **Response 200**:
  ```json
  {
    "id": "job_uuid",
    "document_id": "c71a3994-...",
    "status": "QUEUED",
    "current_stage": "EXTRACTING",
    "progress": 0.0,
    "error_message": null
  }
  ```

### Get Normalized Content JSON
- **`GET /documents/{id}/content`**
- **Headers**: `Authorization: Bearer <token>`
- **Response 200**: Returns full `ContentDocument` JSON schema representation.

### Get Frontend Source Preview
- **`GET /documents/{id}/preview`**
- **Headers**: `Authorization: Bearer <token>`
- **Response 200**:
  ```json
  {
    "document_id": "c71a3994-...",
    "title": "Cellular Biology Overview",
    "original_filename": "bio.docx",
    "mime_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "extraction_status": "COMPLETED",
    "extraction_warnings": [],
    "extracted_at": "2026-08-30T10:00:00Z",
    "schema_version": "1.0.0",
    "sections": [
      {
        "id": "sec_1",
        "title": "Section 1: Plant Cell Structure",
        "blocks": [
          {
            "id": "blk_1",
            "type": "paragraph",
            "source_text": "Plant cells are eukaryotic cells...",
            "page_or_slide": 1,
            "metadata": {"source_type": "docx", "order": 1},
            "accessibility_annotations": {}
          }
        ]
      }
    ]
  }
  ```

---

## 3. Background Job Status Endpoint

### Get Job Status
- **`GET /jobs/{id}`**
- **Headers**: `Authorization: Bearer <token>`
- **Response 200**:
  ```json
  {
    "id": "job_uuid",
    "document_id": "doc_uuid",
    "status": "PROCESSING",
    "current_stage": "NORMALIZING",
    "progress": 75.0,
    "error_message": null
  }
  ```

---

## 4. System Health Check

### Health Check
- **`GET /health`**
- **Response 200**:
  ```json
  {
    "status": "healthy",
    "app": "AccessLearn AI Backend",
    "version": "0.1.0",
    "services": {
      "database": "healthy",
      "redis": "healthy"
    }
  }
  ```
