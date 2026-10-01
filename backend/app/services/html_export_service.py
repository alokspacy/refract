"""HTML5 standalone bundle generation service."""
from app.schemas.content import ContentDocument, BlockType
from app.storage.export_packager import ExportPackager

class HtmlExportService:
    """Generates standalone accessible HTML5 offline bundles."""

    def render_document(self, doc: ContentDocument) -> str:
        body_parts = []
        for sec in doc.sections:
            if sec.title:
                body_parts.append(f"<section><h2>{sec.title}</h2>")
            else:
                body_parts.append("<section>")

            for b in sec.blocks:
                text = b.source_text or ""
                if b.type == BlockType.HEADING:
                    body_parts.append(f"<h3>{text}</h3>")
                elif b.type == BlockType.PARAGRAPH:
                    body_parts.append(f"<p>{text}</p>")
                elif b.type == BlockType.LIST:
                    items = b.metadata.get("items", [text])
                    body_parts.append("<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>")
                elif b.type == BlockType.IMAGE:
                    alt = b.metadata.get("alt", "Educational illustration")
                    body_parts.append(f'<figure><img src="" alt="{alt}"><figcaption>{alt}</figcaption></figure>')
            body_parts.append("</section>")

        html_content = "".join(body_parts)

        # Basic template injection
        from app.templates.accessible_viewer import HTML_TEMPLATE if False else None
        # Using built-in template replacement
        from pathlib import Path
        tmpl_path = Path(__file__).parent.parent / "templates" / "accessible_viewer.html"
        if tmpl_path.exists():
            tmpl = tmpl_path.read_text(encoding="utf-8")
            rendered = tmpl.replace("{{ title }}", doc.title).replace("{{ content_html | safe }}", html_content)
        else:
            rendered = f"<!DOCTYPE html><html><body><h1>{doc.title}</h1>{html_content}</body></html>"
        return rendered

    def create_package(self, doc: ContentDocument) -> bytes:
        html = self.render_document(doc)
        files = {
            "index.html": html,
            "manifest.json": '{"name": "' + doc.title + '", "display": "standalone"}'
        }
        return ExportPackager.create_zip_archive(files)
