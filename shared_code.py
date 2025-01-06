import pdfplumber
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pypdf import PdfWriter, PdfReader
import io
import json
from reportlab.lib.colors import white,black
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4

from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont

# def create_overlay_pdf(text_positions, page_width, page_height):
#     """
#     Create an overlay PDF with text at specified positions.
#     :param text_positions: List of dictionaries with 'x', 'y', 'text'.
#     :param page_width: Width of the page.
#     :param page_height: Height of the page.
#     :return: BytesIO object of the overlay PDF.
#     """
#     packet = io.BytesIO()
#     can = canvas.Canvas(packet, pagesize=(page_width, page_height))
#     # can.showOutline()

#     can.setFillColor(black)
#     print(letter , page_width , page_height, "page width and height")
    
#     for item in text_positions:
#         x, y, text = item['x'], item['y'], item['text']
#         print(x, page_height - y ,letter[1] - y , y, "values")

#         # text_width = can.stringWidth(text, 'Helvetica', 12)
#         # ascent = pdfmetrics.getFont('Helvetica').face.ascent / 1000 * 12 
#         # descent = pdfmetrics.getFont('Helvetica').face.descent / 1000 * 12 
#         # inverted_y = page_height - y
#         # adjusted_y = inverted_y - descent
      
       
#         can.drawString(x, page_height - y, text)
    
#     can.save()
#     packet.seek(0)
#     return packet


# replicated belwo
# def create_overlay_pdf(text_positions, page_width, page_height):
#     """
#     Create an overlay PDF with text at specified positions.
#     :param text_positions: List of dictionaries with 'x', 'y', 'text'.
#     :param page_width: Width of the page.
#     :param page_height: Height of the page.
#     :return: BytesIO object of the overlay PDF.
#     """
#     packet = io.BytesIO()
#     can = canvas.Canvas(packet, pagesize=(page_width, page_height)) # we can pass a4 size direclt here so that pdf will came propely
#     can.setFillColor(white)

#     for item in text_positions:
#         x, y, text = item['x'], item['y'], item['text']

#         # Invert y-coordinate to align with PDF coordinate system
#         inverted_y = page_height - y

#         # Calculate text width to handle overflow
#         text_width = can.stringWidth(text, 'Helvetica', 12)

#         # Adjust x if text overflows the right edge
#         if x + text_width > page_width:
#             print(f"Warning: Adjusting text '{text}' at ({x}, {y}) to fit page width.")
#             x = page_width - text_width

#         # Adjust y if text overflows the bottom edge
#         if inverted_y < 0:
#             print(f"Warning: Adjusting text '{text}' at ({x}, {y}) to fit page height.")
#             inverted_y = 0

#         # Draw the string on the canvas
#         can.drawString(x, inverted_y - 7, text)
#         print(f"Placing text '{text}' at ({x}, {inverted_y}) on page with dimensions ({page_width}, {page_height})")

#     can.save()
#     packet.seek(0)
#     return packet


def create_overlay_pdf(text_positions, page_width, page_height):
    """
    Create an overlay PDF with text at specified positions.
    :param text_positions: List of dictionaries with 'x', 'y', 'text'.
    :param page_width: Width of the page.
    :param page_height: Height of the page.
    :return: BytesIO object of the overlay PDF.
    """
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(A4)) # we can pass a4 size direclt here so that pdf will came propely
    can.setFillColor(white)

    for item in text_positions:
        x, y, text = item['x'], item['y'], item['text']

        # Invert y-coordinate to align with PDF coordinate system
        inverted_y = page_height - y

        # Calculate text width to handle overflow
        text_width = can.stringWidth(text, 'Helvetica', 12)

        # Adjust x if text overflows the right edge
        if x + text_width > A4[0]:
            print(f"Warning: Adjusting text '{text}' at ({x}, {y}) to fit page width.")
            x = A4[0] - text_width

        # Adjust y if text overflows the bottom edge
        if inverted_y < 0:
            print(f"Warning: Adjusting text '{text}' at ({x}, {y}) to fit page height.")
            inverted_y = 0

        # Draw the string on the canvas
        can.drawString(x, inverted_y -7 , text)
        print(f"Placing text '{text}' at ({x}, {inverted_y}) on page with dimensions ({A4[0]}, {A4[1]})")

    can.save()
    packet.seek(0)
    return packet



# def create_overlay_pdf(text_positions, page_width, page_height):
#     """
#     Create an overlay PDF with text at specified positions.
#     :param text_positions: List of dictionaries with 'x', 'y', 'text'.
#     :param page_width: Width of the page.
#     :param page_height: Height of the page.
#     :return: BytesIO object of the overlay PDF.
#     """
#     packet = io.BytesIO()
#     can = canvas.Canvas(packet, pagesize=(page_width, page_height))

#     can.setFillColor(black)

#     for item in text_positions:
#         x, y, text = item['x'], item['y'], item['text']
        
#         # Get font metrics for adjustment
#         font_name = 'Helvetica'
#         font_size = 12
#         ascent = pdfmetrics.getFont(font_name).face.ascent / 1000 * font_size
#         descent = pdfmetrics.getFont(font_name).face.descent / 1000 * font_size
        
#         # Adjust y to account for the descent
#         adjusted_y = page_height - y - descent
        
#         # Draw the text
#         can.setFont(font_name, font_size)
#         can.drawString(x, adjusted_y, text)

#     can.save()
#     packet.seek(0)
#     return packet

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
# input_pdf_path = "sample.pdf"
# input_pdf_path = "dummy_10_pages.pdf"
input_pdf_path = "A4size_House-Warming-Invitation-Card.pdf"
# input_pdf_path = "House-Warming-Invitation-Card (1).pdf"

output_pdf_path = "1_test_output.pdf"

# JSON input from the frontend
json_input = '''
[
    {"page": 1, "x": 101, "y": 46, "text": "Test 1"},

    {"page": 1, "x": 99, "y": 95, "text": "Test 2"},
    {"page": 1, "x": 542.27, "y": 2, "text": "Test 3"},
      {"page": 1, "x": 245.26999999999998, "y": 349, "text": "Test 4"},
        {"page": 1, "x": 3, "y": 3, "text": "Test 5"},
          {"page": 1, "x": 1, "y": 834.89, "text": "Test 6"}, 
          {"page": 1, "x": 542.27, "y": 835, "text": "Test 7 "}
]
'''

#   {"page": 1, "x": 1, "y": 834.89, "text": "Test 1234"},   for this added 20 as the height of input box in frontedn
#    {"page": 1, "x": 300, "y": 700, "text": "Test 6789"},
#     {"page": 2, "x": 150, "y": 600, "text": "Another Text"},
#     {"page": 8, "x": 200, "y": 500, "text": "Test 9999"}
text_positions = json.loads(json_input)




add_text_to_pdf(input_pdf_path, output_pdf_path, text_positions)