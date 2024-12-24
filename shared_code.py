import pdfplumber
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pypdf import PdfWriter, PdfReader
import io
import json


def create_overlay_pdf(text_positions, page_width, page_height):
    """
    Create an overlay PDF with text at specified positions.
    :param text_positions: List of dictionaries with 'x', 'y', 'text'.
    :param page_width: Width of the page.
    :param page_height: Height of the page.
    :return: BytesIO object of the overlay PDF.
    """
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(page_width, page_height))
    
    for item in text_positions:
        x, y, text = item['x'], item['y'], item['text']
        can.drawString(x, y, text)
    
    can.save()
    packet.seek(0)
    return packet


def add_text_to_pdf(input_pdf_path, output_pdf_path, text_positions):
    """
    Add text to specific positions in a PDF using pdfplumber, reportlab, and pypdf.
    :param input_pdf_path: Path to the input PDF file.
    :param output_pdf_path: Path to save the output PDF file.
    :param text_positions: List of dictionaries with 'page', 'x', 'y', 'text'.
    """
    # Open the original PDF
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()
    
    # Group positions by page for easy processing
    grouped_positions = {}
    for item in text_positions:
        page_number = item['page'] - 1  # Convert to 0-based index
        if page_number not in grouped_positions:
            grouped_positions[page_number] = []
        grouped_positions[page_number].append(item)
    
    # Open pdfplumber to read page dimensions
    with pdfplumber.open(input_pdf_path) as pdf:
        for page_number in range(len(reader.pages)):
            page = reader.pages[page_number]
            pdf_page = pdf.pages[page_number]  # Get page size from pdfplumber
            
            # Extract page dimensions
            page_width = pdf_page.width
            page_height = pdf_page.height
            
            if page_number in grouped_positions:
                # Create overlay with reportlab
                overlay_pdf_stream = create_overlay_pdf(
                    grouped_positions[page_number], page_width, page_height
                )
                overlay_pdf = PdfReader(overlay_pdf_stream)
                overlay_page = overlay_pdf.pages[0]
                
                # Merge overlay with original page
                page.merge_page(overlay_page)
            
            # Add the updated page to the writer
            writer.add_page(page)
    
    # Save the final PDF
    with open(output_pdf_path, "wb") as output_file:
        writer.write(output_file)


# Example usage
input_pdf_path = "sample.pdf"
output_pdf_path = "output.pdf"

# JSON input from the frontend
json_input = '''
[
    {"page": 1, "x": 100, "y": 700, "text": "Test 1234"},
    {"page": 1, "x": 300, "y": 700, "text": "Test 6789"},
    {"page": 2, "x": 150, "y": 600, "text": "Another Text"},
    {"page": 8, "x": 200, "y": 500, "text": "Test 9999"}
]
'''
text_positions = json.loads(json_input)

add_text_to_pdf(input_pdf_path, output_pdf_path, text_positions)