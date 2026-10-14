"""Service bundling HTML5, SCORM, BRF, and JSON into a master archive."""
from app.schemas.content import ContentDocument
from app.services.html_export_service import HtmlExportService
from app.services.scorm_service import ScormExportService
from app.services.braille_service import BrailleService
from app.storage.export_packager import ExportPackager

class BundleService:
    def __init__(self):
        self.html_svc = HtmlExportService()
        self.scorm_svc = ScormExportService()
        self.braille_svc = BrailleService()

    def create_master_bundle(self, doc: ContentDocument) -> bytes:
        html = self.html_svc.render_document(doc)
        scorm_zip = self.scorm_svc.create_scorm_package(doc, "master_scorm")
        braille_doc = self.braille_svc.translate_document(doc)

        files = {
            "standalone/index.html": html,
            "scorm/scorm_package.zip": scorm_zip,
            "braille/embosser.brf": braille_doc.raw_brf_content,
            "data/content.json": doc.model_dump_json(indent=2),
        }
        return ExportPackager.create_zip_archive(files)
