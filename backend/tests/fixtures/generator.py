import io
import fitz
import docx
import pptx
from pptx.util import Inches, Pt
from PIL import Image, ImageDraw


def create_sample_pdf() -> bytes:
    """Create a sample multi-page born-digital PDF with headings, paragraphs, lists, and tables."""
    doc = fitz.open()
    
    # Page 1: Heading, Paragraph, List
    page1 = doc.new_page(width=595, height=842)
    # Heading
    page1.insert_text((50, 70), "Cellular Biology: Introduction to Photosynthesis", fontsize=18, fontname="helv", color=(0, 0, 0))
    # Paragraph
    page1.insert_text((50, 110), "Photosynthesis is the essential biological mechanism converting light energy into chemical sugars.", fontsize=11, fontname="helv", color=(0.1, 0.1, 0.1))
    page1.insert_text((50, 130), "It occurs primarily in the chloroplasts of eukaryotic plant cells containing chlorophyll pigments.", fontsize=11, fontname="helv", color=(0.1, 0.1, 0.1))
    # List items
    page1.insert_text((50, 170), "- Stage 1: Light-dependent reactions produce ATP and NADPH in the thylakoid membranes.", fontsize=11, fontname="helv", color=(0.1, 0.1, 0.1))
    page1.insert_text((50, 190), "- Stage 2: Light-independent reactions (Calvin cycle) fix CO2 in the stroma.", fontsize=11, fontname="helv", color=(0.1, 0.1, 0.1))

    # Page 2: Table and Subheading
    page2 = doc.new_page(width=595, height=842)
    page2.insert_text((50, 70), "Photosynthesis vs Cellular Respiration", fontsize=16, fontname="helv", color=(0, 0, 0))
    page2.insert_text((50, 100), "Process Comparison Table", fontsize=12, fontname="helv", color=(0.2, 0.2, 0.2))
    
    # Simple table lines
    page2.draw_rect(fitz.Rect(50, 120, 500, 220), color=(0.5, 0.5, 0.5), width=1)
    page2.draw_line(fitz.Point(50, 150), fitz.Point(500, 150), color=(0.5, 0.5, 0.5), width=1)
    page2.draw_line(fitz.Point(275, 120), fitz.Point(275, 220), color=(0.5, 0.5, 0.5), width=1)
    page2.insert_text((60, 140), "Characteristic", fontsize=11, fontname="helv")
    page2.insert_text((285, 140), "Photosynthesis", fontsize=11, fontname="helv")
    page2.insert_text((60, 175), "Organelle", fontsize=10, fontname="helv")
    page2.insert_text((285, 175), "Chloroplast", fontsize=10, fontname="helv")
    page2.insert_text((60, 205), "Energy Source", fontsize=10, fontname="helv")
    page2.insert_text((285, 205), "Solar Radiation", fontsize=10, fontname="helv")

    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


def create_scanned_pdf() -> bytes:
    """Create a scanned-like PDF with an image and negligible selectable text to trigger OCR."""
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)
    
    # Generate an image with text rendered graphically
    img = Image.new("RGB", (600, 800), color=(250, 250, 250))
    d = ImageDraw.Draw(img)
    d.rectangle([(20, 20), (580, 780)], outline=(100, 100, 100), width=2)
    d.text((50, 50), "Scanned Page: Ancient Photosynthesis Discoveries", fill=(20, 20, 20))
    d.text((50, 100), "This page was captured from an optical scanner.", fill=(40, 40, 40))
    
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="PNG")
    img_bytes = img_byte_arr.getvalue()
    
    page.insert_image(fitz.Rect(50, 50, 545, 750), stream=img_bytes)
    # Insert tiny 10-char text (below the 50 char threshold)
    page.insert_text((50, 790), "Page 1", fontsize=8)
    
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


def create_sample_docx() -> bytes:
    """Create a DOCX with title, headings, paragraphs, lists, and tables."""
    doc = docx.Document()
    doc.core_properties.title = "Cellular Biology Overview"
    
    doc.add_heading("Cellular Biology Overview", level=0)
    doc.add_heading("Section 1: Plant Cell Structure", level=1)
    doc.add_paragraph("Plant cells are eukaryotic cells with a prominent cell wall and large central vacuole.")
    
    doc.add_paragraph("Key Organelles:", style="List Bullet")
    doc.add_paragraph("Chloroplast: Site of photosynthesis.", style="List Bullet")
    doc.add_paragraph("Mitochondria: Cellular respiration and ATP synthesis.", style="List Bullet")
    
    doc.add_heading("Section 2: Comparison Grid", level=2)
    table = doc.add_table(rows=3, cols=2)
    table.cell(0, 0).text = "Feature"
    table.cell(0, 1).text = "Plant Cell"
    table.cell(1, 0).text = "Cell Wall"
    table.cell(1, 1).text = "Present (Cellulose)"
    table.cell(2, 0).text = "Chloroplasts"
    table.cell(2, 1).text = "Present"
    
    out = io.BytesIO()
    doc.save(out)
    return out.getvalue()


def create_sample_pptx() -> bytes:
    """Create a PPTX with multiple slides, titles, body text, and notes."""
    prs = pptx.Presentation()
    
    # Slide 1: Title
    slide1 = prs.slides.add_slide(prs.slide_layouts[0])
    slide1.shapes.title.text = "Introduction to Astrophysics"
    slide1.placeholders[1].text = "Chapter 4: Stellar Evolution"
    
    # Slide 2: Bullet points + Notes
    slide2 = prs.slides.add_slide(prs.slide_layouts[1])
    slide2.shapes.title.text = "Life Cycle of Stars"
    tf = slide2.placeholders[1].text_frame
    tf.text = "Main Sequence Phase: Hydrogen fusion in stellar core."
    p2 = tf.add_paragraph()
    p2.text = "Red Giant Phase: Expansion following hydrogen depletion."
    p2.level = 1
    
    # Add notes
    notes_slide = slide2.notes_slide
    notes_tf = notes_slide.notes_text_frame
    notes_tf.text = "Emphasize hydrostatic equilibrium during the main sequence stage."
    
    out = io.BytesIO()
    prs.save(out)
    return out.getvalue()


def create_sample_image() -> bytes:
    """Create a sample PNG image containing educational diagram text."""
    img = Image.new("RGB", (500, 300), color=(240, 248, 255))
    d = ImageDraw.Draw(img)
    d.rectangle([(10, 10), (490, 290)], outline=(30, 60, 120), width=3)
    d.text((40, 40), "Photosynthesis Equation", fill=(10, 30, 80))
    d.text((40, 90), "6CO2 + 6H2O + Light -> C6H12O6 + 6O2", fill=(20, 20, 20))
    out = io.BytesIO()
    img.save(out, format="PNG")
    return out.getvalue()


def create_sample_txt() -> bytes:
    """Create a sample plain text educational note."""
    text = (
        "# Introduction to Ecology\n\n"
        "Ecology is the scientific study of interactions among organisms and their environment.\n\n"
        "Key Levels of Organization:\n"
        "• Organism: An individual living entity.\n"
        "• Population: Group of individuals of the same species.\n"
        "• Community: Populations of different species living together.\n"
        "• Ecosystem: Community plus abiotic physical factors."
    )
    return text.encode("utf-8")
