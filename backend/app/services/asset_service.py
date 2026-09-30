import io
import logging
import re
from typing import List, Optional
from app.parsers.base import ExtractedAsset
from app.providers.storage import StorageProvider

logger = logging.getLogger("accesslearn.services.asset")


class AssetService:
    """Handles saving extracted assets (embedded images/diagrams) into storage."""

    @staticmethod
    def persist_extracted_assets(
        assets: List[ExtractedAsset],
        user_id: str,
        document_id: str,
        storage: StorageProvider
    ) -> List[ExtractedAsset]:
        persisted = []

        for asset in assets:
            if not asset.data_bytes:
                continue

            try:
                clean_name = re.sub(r"[^\w\.-]", "_", asset.filename) or "image.png"
                storage_key = f"users/{user_id}/assets/{document_id}_{asset.asset_id}_{clean_name}"
                
                storage.save(
                    file_data=asset.data_bytes,
                    storage_key=storage_key
                )
                asset.storage_key = storage_key
                # Clear raw bytes from memory once saved
                asset.data_bytes = None
                persisted.append(asset)
                logger.debug(f"Persisted asset {asset.asset_id} to {storage_key}")
            except Exception as e:
                logger.warning(f"Failed to persist asset {asset.asset_id}: {e}")

        return persisted
