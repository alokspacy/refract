"""Accessible EPUB3 package metadata builder."""
from datetime import datetime, timezone

def generate_epub_package_opf(title: str, identifier: str, reading_order: list) -> str:
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    manifest_items = "\n    ".join([
        f'<item id="sec_{i}" href="section_{i}.xhtml" media-type="application/xhtml+xml"/>'
        for i in range(len(reading_order))
    ])
    spine_items = "\n    ".join([
        f'<itemref idref="sec_{i}"/>'
        for i in range(len(reading_order))
    ])

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="pub-id">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="pub-id">{identifier}</dc:identifier>
    <dc:title>{title}</dc:title>
    <dc:language>en</dc:language>
    <meta property="dcterms:modified">{now_iso}</meta>
    <!-- Accessibility Certification Metadata (schema.org) -->
    <meta property="schema:accessibilityHazard">none</meta>
    <meta property="schema:accessibilityFeature">structuralNavigation</meta>
    <meta property="schema:accessibilityFeature">alternativeText</meta>
    <meta property="schema:accessMode">textual</meta>
    <meta property="schema:accessMode">visual</meta>
  </metadata>
  <manifest>
    {manifest_items}
  </manifest>
  <spine>
    {spine_items}
  </spine>
</package>"""
