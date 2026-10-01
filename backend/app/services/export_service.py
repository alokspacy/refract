"""Central coordinator for all accessibility exports."""
import uuid
from datetime import datetime, timezone
from typing import Dict
from app.schemas.content import ContentDocument
from app.schemas.export import ExportFormat, ExportPackageResponse, ExportRequest
from app.services.html_export_service import HtmlExportService
from app.services.scorm_service import ScormExportService
from app.storage.export_packager import ExportPackager

class ExportService:
    _package_store: Dict[str, bytes] = {}

    def __init__(self):
        self.html_service = HtmlExportService()
        self.scorm_service = ScormExportService()

    def generate_package(self, doc: ContentDocument, req: ExportRequest) -> ExportPackageResponse:
        pkg_id = str(uuid.uuid4())[:8]
        if req.format == ExportFormat.SCORM_12:
            zip_bytes = self.scorm_service.create_scorm_package(doc, pkg_id)
            filename = f"{doc.title.lower().replace(' ', '_')}_scorm12.zip"
        else:
            zip_bytes = self.html_service.create_package(doc)
            filename = f"{doc.title.lower().replace(' ', '_')}_html5.zip"

        self._package_store[pkg_id] = zip_bytes
        checksum = ExportPackager.compute_sha256(zip_bytes)

        return ExportPackageResponse(
            package_id=pkg_id,
            variant_id=req.variant_id,
            format=req.format,
            filename=filename,
            file_size_bytes=len(zip_bytes),
            download_url=f"/api/export/{pkg_id}/download",
            checksum_sha256=checksum,
            created_at=datetime.now(timezone.utc).isoformat(),
        )

    def get_package_bytes(self, package_id: str) -> bytes | None:
        return self._package_store.get(package_id)
