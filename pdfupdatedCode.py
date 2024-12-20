import csv
import json
import pdfplumber
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pypdf import PdfWriter, PdfReader
import io

def read_csv(file_path):
    """
    Read CSV file and extract text positions and page information.
    :param file_path: Path to the CSV file.
    :return: List of dictionaries with 'page', 'x', 'y', 'text'.
    """
    text_positions = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            pages = row[0].split(',')
            for i in range(1, len(row), 3):
                content = row[i]
                x = row[i + 1]
                y = row[i + 2]
                try:
                    text_positions.extend([{'page': int(page), 'x': int(x), 'y': int(y), 'text': content}
                                          for page in pages])
                except ValueError:
                    # Skip if x, y, or content cannot be converted to integers
                    continue
    return text_positions
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
        x, y, text = item['x'], item['y'], ''
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
output_pdf_path = "output10.pdf"
csv_input_path = 'updated-content.csv'  # Path to your CSV file

# Reading CSV
text_positions = read_csv(csv_input_path)

# Adding text to PDF
add_text_to_pdf(input_pdf_path, output_pdf_path, text_positions)
