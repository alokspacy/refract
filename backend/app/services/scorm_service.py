"""SCORM 1.2 & 2004 LMS package exporter."""
from pathlib import Path
from app.schemas.content import ContentDocument
from app.services.html_export_service import HtmlExportService
from app.storage.export_packager import ExportPackager

class ScormExportService:
    """Builds SCORM 1.2 compliant LMS distribution packages."""

    def __init__(self):
        self.html_service = HtmlExportService()

    def create_scorm_package(self, doc: ContentDocument, package_id: str) -> bytes:
        html = self.html_service.render_document(doc)
        manifest_path = Path(__file__).parent.parent / "templates" / "imsmanifest.xml"
        if manifest_path.exists():
            tmpl = manifest_path.read_text(encoding="utf-8")
            manifest = tmpl.replace("{{ package_id }}", package_id).replace("{{ title }}", doc.title)
        else:
            manifest = f'<manifest identifier="{package_id}"><organizations/><resources/></manifest>'

        files = {
            "imsmanifest.xml": manifest,
            "index.html": html,
        }
        return ExportPackager.create_zip_archive(files)
