# import pdfplumber
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter
# from pypdf import PdfWriter, PdfReader
# import io
# import json
# from reportlab.lib.colors import white
# from reportlab.lib.pagesizes import A4
# def create_overlay_pdf(text_positions, page_width, page_height):
#     """
#     Create an overlay PDF with text at specified positions.
#     :param text_positions: List of dictionaries with 'x', 'y', 'text'.
#     :param page_width: Width of the page.
#     :param page_height: Height of the page.
#     :return: BytesIO object of the overlay PDF.
#     """
#     packet = io.BytesIO()
#     can = canvas.Canvas(packet, pagesize=(int(A4[0]), int(A4[1])))
#                         # pagesize=(page_width, page_height)
#                         # )
#     can.setFillColor(white)
#     can.setFont('Helvetica', 40)
#     for item in text_positions:
#         x, y, text = item['x'], item['y'], item['text']
#         print(x, y, text , A4[1] -y, "x y and text")
#         can.drawString(x, A4[1] -y, text)
    
#     can.save()
#     packet.seek(0)
#     return packet


# def add_text_to_pdf(input_pdf_path, output_pdf_path, text_positions):
#     """
#     Add text to specific positions in a PDF using pdfplumber, reportlab, and pypdf.
#     :param input_pdf_path: Path to the input PDF file.
#     :param output_pdf_path: Path to save the output PDF file.
#     :param text_positions: List of dictionaries with 'page', 'x', 'y', 'text'.
#     """
#     # Open the original PDF
#     reader = PdfReader(input_pdf_path)
#     writer = PdfWriter()
    
#     # Group positions by page for easy processing
#     grouped_positions = {}
#     for item in text_positions:
#         page_number = item['page'] - 1  # Convert to 0-based index
#         if page_number not in grouped_positions:
#             grouped_positions[page_number] = []
#         grouped_positions[page_number].append(item)
    
#     # Open pdfplumber to read page dimensions
#     with pdfplumber.open(input_pdf_path) as pdf:
#         for page_number in range(len(reader.pages)):
#             page = reader.pages[page_number]
#             pdf_page = pdf.pages[page_number]  # Get page size from pdfplumber
            
#             # Extract page dimensions
#             page_width = pdf_page.width
#             page_height = pdf_page.height
            
#             if page_number in grouped_positions:
#                 # Create overlay with reportlab
#                 overlay_pdf_stream = create_overlay_pdf(
#                     grouped_positions[page_number], page_width, page_height
#                 )
#                 overlay_pdf = PdfReader(overlay_pdf_stream)
#                 overlay_page = overlay_pdf.pages[0]
                
#                 # Merge overlay with original page
#                 page.merge_page(overlay_page)
            
#             # Add the updated page to the writer
#             writer.add_page(page)
    
#     # Save the final PDF
#     with open(output_pdf_path, "wb") as output_file:
#         writer.write(output_file)


# # Example usage
# input_pdf_path = "House-Warming-Invitation-Card (1).pdf"
# output_pdf_path = "outputhousewarming.pdf"

# # JSON input from the frontend
# json_input = '''
# [
#     {"page": 1, "x": 200, "y": 120, "text": "Test 1234"}
    
# ]
# '''

# # {"page": 1, "x": 300, "y": 700, "text": "Test 6789"},
# #     {"page": 2, "x": 150, "y": 600, "text": "Another Text"},
# #     {"page": 8, "x": 200, "y": 500, "text": "Test 9999"}
# text_positions = json.loads(json_input)

# add_text_to_pdf(input_pdf_path, output_pdf_path, text_positions)
# print("Pdf genereated")




import pdfplumber
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import white,black
from pypdf import PdfWriter, PdfReader
import io
import json
from reportlab.lib.pagesizes import letter

def create_overlay_pdf(text_positions):
    """
    Create an overlay PDF with text at specified positions on an A4-sized page.
    :param text_positions: List of dictionaries with 'x', 'y', 'text'.
    :return: BytesIO object of the overlay PDF.
    """
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4, bottomup=0)
    can.setFillColor(black)
    can.setFont('Helvetica', 20)  
    print(A4[1], "A4 size" , A4[0], "A4 size")

    for item in text_positions:
        x, y, text = item['x'], item['y'], item['text']
        adjusted_x = A4[0] - x
        adjusted_y = A4[1] -  y 
        print(f"Drawing text '{text}' at (x: {x}, y: {adjusted_y}) on A4 size")
        can.drawString(x,  adjusted_y, text)
        packet.seek(0) 

    
    can.save()
    packet.seek(0)
    return packet

def add_text_to_pdf(input_pdf_path, output_pdf_path, text_positions):
    """
    Add text to specific positions in a PDF using an overlay on A4-sized pages.
    :param input_pdf_path: Path to the input PDF file.
    :param output_pdf_path: Path to save the output PDF file.
    :param text_positions: List of dictionaries with 'page', 'x', 'y', 'text'.
    """
    # Open the original PDF
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()
    
    
    grouped_positions = {}
    for item in text_positions:
        page_number = item['page'] - 1  
        if page_number not in grouped_positions:
            grouped_positions[page_number] = []
        grouped_positions[page_number].append(item)
    
    for page_number in range(len(reader.pages)):
        page = reader.pages[page_number]
        
        if page_number in grouped_positions:
            
            overlay_pdf_stream = create_overlay_pdf(grouped_positions[page_number])
            overlay_pdf = PdfReader(overlay_pdf_stream)
            overlay_page = overlay_pdf.pages[0]
            
            
            page.merge_page(overlay_page)
        
      
        writer.add_page(page)
    
    
    with open(output_pdf_path, "wb") as output_file:
        writer.write(output_file)


# input_pdf_path = "House-Warming-Invitation-Card (1).pdf"
# input_pdf_path = "sample.pdf"
# input_pdf_path = "dummy_10_pages.pdf"
# input_pdf_path = "A4_dummy_10_pages.pdf"
input_pdf_path = "A4size_House-Warming-Invitation-Card.pdf"
output_pdf_path = "outputhousewarming_a4.pdf"


json_input = '''
[
    {"page": 1, "x": 222, "y": 130, "text": "Test 1234"}
]
'''
text_positions = json.loads(json_input)

add_text_to_pdf(input_pdf_path, output_pdf_path, text_positions)
print(f"PDF with text annotations saved as {output_pdf_path}")
