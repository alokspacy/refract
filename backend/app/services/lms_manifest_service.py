"""Service generating SCORM / IMS package manifests for Learning Management Systems."""
import uuid
from app.schemas.content import ContentDocument
from app.schemas.lms_manifest import LMSManifest, LMSResource

class LMSManifestService:
    def build_imsmanifest_xml(self, doc: ContentDocument) -> str:
        manifest_id = f"MANIFEST-{str(uuid.uuid4())[:8]}"
        res_id = f"RES-{str(uuid.uuid4())[:8]}"

        xml = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<manifest identifier="{manifest_id}" version="1.3"\n'
            '          xmlns="http://www.imsglobal.org/xsd/imscp_v1p1"\n'
            '          xmlns:adlcp="http://www.adlnet.org/xsd/adlcp_v1p3">\n'
            '  <metadata>\n'
            '    <schema>ADL SCORM</schema>\n'
            '    <schemaversion>2004 4th Edition</schemaversion>\n'
            '    <adlcp:accessibilityStandards>WCAG 2.2 Level AA</adlcp:accessibilityStandards>\n'
            '  </metadata>\n'
            '  <organizations default="DEFAULT_ORG">\n'
            '    <organization identifier="DEFAULT_ORG">\n'
            f'      <title>{doc.title}</title>\n'
            f'      <item identifier="ITEM-1" identifierref="{res_id}">\n'
            f'        <title>{doc.title} - Adapted Material</title>\n'
            '      </item>\n'
            '    </organization>\n'
            '  </organizations>\n'
            '  <resources>\n'
            f'    <resource identifier="{res_id}" type="webcontent" adlcp:scormType="sco" href="index.html">\n'
            '      <file href="index.html"/>\n'
            '    </resource>\n'
            '  </resources>\n'
            '</manifest>'
        )
        return xml
