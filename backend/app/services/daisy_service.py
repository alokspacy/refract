"""DAISY talking book manifest builder."""
from typing import List
from app.schemas.daisy import DAISYNavPoint, DAISYManifestResponse
from app.schemas.content import ContentDocument, BlockType

class DaisyService:
    """Builds DAISY 2.02 / 3.0 NCC navigation markup for talking book hardware players."""

    def build_ncc(self, doc: ContentDocument) -> DAISYManifestResponse:
        nav_points: List[DAISYNavPoint] = []
        html_lines = [
            '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">',
            '<html xmlns="http://www.w3.org/1999/xhtml">',
            '<head>',
            f'<title>{doc.title}</title>',
            '<meta name="dc:format" content="DAISY 2.02" />',
            '</head>',
            '<body>',
            f'<h1>{doc.title}</h1>'
        ]

        order = 1
        for sec in doc.sections:
            if sec.title:
                np = DAISYNavPoint(
                    id=f"nav_{order}",
                    play_order=order,
                    heading_text=sec.title,
                    content_src=f"text.html#sec_{order}"
                )
                nav_points.append(np)
                html_lines.append(f'<h2 id="sec_{order}"><a href="text.html#sec_{order}">{sec.title}</a></h2>')
                order += 1

        html_lines.extend(['</body>', '</html>'])

        return DAISYManifestResponse(
            document_id=doc.id,
            title=doc.title,
            ncc_html="\n".join(html_lines),
            nav_points=nav_points
        )
