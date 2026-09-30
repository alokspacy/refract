import pytest
from app.storage.local import LocalStorageProvider


def test_local_storage_lifecycle(temp_storage: LocalStorageProvider):
    key = "documents/test_file.txt"
    content = b"Accessible Education Foundation Content"

    # Save
    saved_path = temp_storage.save(content, key)
    assert saved_path is not None

    # Exists
    assert temp_storage.exists(key) is True

    # Get
    retrieved = temp_storage.get(key)
    assert retrieved == content

    # Delete
    deleted = temp_storage.delete(key)
    assert deleted is True
    assert temp_storage.exists(key) is False


def test_local_storage_path_traversal_prevention(temp_storage: LocalStorageProvider):
    with pytest.raises(ValueError, match="Path traversal detected"):
        temp_storage.save(b"malicious", "../../etc/passwd")

    with pytest.raises(ValueError):
        temp_storage.get("../secret.txt")
