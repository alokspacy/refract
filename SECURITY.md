# AccessLearn AI — Security Policy & Technical Safeguards

## 1. Authentication & Cryptographic Standards

### Password Hashing
- All user passwords are encrypted using **bcrypt** with randomly generated cryptographic salts (`bcrypt.gensalt()`).
- Plaintext passwords are never stored in databases, logs, caches, or serialized tokens.

### JWT Access Tokens
- Signed using HMAC SHA-256 (`HS256`) with a cryptographically strong secret configured via `JWT_SECRET`.
- Tokens have strict expiration lifespans (`ACCESS_TOKEN_EXPIRE_MINUTES`, default 24 hours).
- The token payload only contains identity claims (`sub` = user UUID, `email`, `role`, `iat`, `exp`).

---

## 2. File Upload & Storage Security

### Input Sanitization & Path Traversal Mitigation
1. **Filename Sanitization**: Original client filenames are sanitized by stripping any leading paths, null bytes, and directory traversal sequences (`..`, `/`, `\`). Non-alphanumeric characters are replaced with safe characters.
2. **Deterministic UUID Storage Keys**: Stored files are renamed using randomly generated UUIDs: `users/{user_id}/{uuid}_{safe_filename}`. The physical filename on disk never directly mirrors user input.
3. **MIME & Extension Whitelisting**: The system rejects any file whose extension or MIME type is not explicitly permitted. Executable and script formats (`.exe`, `.bat`, `.cmd`, `.sh`, `.php`, `.js`, `.vbs`, `.ps1`, `.jar`) are strictly rejected.
4. **Enforced File Size Limits**: Requests exceeding `MAX_FILE_SIZE_MB` (default: 50MB) are rejected with HTTP `413 Request Entity Too Large` before disk persistence.
5. **Private Storage Isolation**: File storage directories are not exposed directly as static web roots. All downloads must route through authenticated application endpoints that verify user identity and ownership.

---

## 3. Authorization & Tenant Data Isolation

- All document and job endpoints enforce tenant isolation by validating that the authenticated user is the direct owner of the requested resource.
- Cross-user access attempts (e.g. User B requesting `GET /documents/{user_a_doc_id}`) yield HTTP `403 Forbidden`.
- Database Foreign Key relationships use `ON DELETE CASCADE` so deleting a user cleanly cascades to their documents and jobs without orphan leaks.

---

## 4. Environment & Secrets Management

- Zero secrets, database passwords, or cryptographic keys are stored in source code or Git repositories.
- `.gitignore` strictly ignores `.env`, `.env.*`, `uploads/`, `storage/*` (except `.gitkeep`), build caches, and test artifacts.
- Production deployments must supply credentials via container environment variables or secrets managers.

---

## 5. Logging Restrictions

Application loggers strictly prohibit recording:
- Plaintext passwords or login credentials.
- Full JWT tokens or authentication bearer strings.
- Cloud API keys or database connection strings with credentials.
- Full uploaded document contents (only file metadata such as size, MIME, and IDs are logged).

---

## 6. Future AI & Prompt-Injection Safeguards (Phase 2+)

In upcoming phases involving LLMs and document transformations:
- All student and course material text will be treated as untrusted data.
- Strict system prompts and schema delimiters will prevent prompt-injection or instructional override attempts.
- Transformed content will undergo automated WCAG validation before rendering.
