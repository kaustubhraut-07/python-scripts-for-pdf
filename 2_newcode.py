# import pdfplumber
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter
# from pypdf import PdfWriter, PdfReader
# import io
# import json
# import csv
# import os
# from reportlab.lib.units import inch
# from reportlab.lib.colors import white, black

# json_data = [
#     {"pageNumber": 1, "x": 303, "y": 180, "text": "Tag 1", "width": 800, "height": 1131.6129032258063},
# ]

# csv_file_path = "New Csv Format - Sheet1.csv"
# pdf_input_path = "House-Warming-Invitation-Card (1).pdf"
# output_directory = "output_files"

# # Ensure output directory exists
# os.makedirs(output_directory, exist_ok=True)

# # Read the CSV file
# rows = []
# with open(csv_file_path, 'r') as csv_file:
#     csv_reader = csv.DictReader(csv_file)
#     for row in csv_reader:
#         rows.append(row)


# def normalize_coordinates(x, y, standard_width, standard_height, actual_width, actual_height):
#     scale_x = actual_width / standard_width
#     scale_y = actual_height / standard_height
#     normalized_x = x * scale_x
#     normalized_y = y * scale_y
#     return normalized_x, normalized_y


# def create_overlay_pdf(text_positions, json_width, json_height):
#     """
#     Create an overlay PDF with text at specified positions using the dimensions from the JSON file.
#     :param text_positions: List of dictionaries with 'x', 'y', 'text'.
#     :param json_width: Width of the page from JSON.
#     :param json_height: Height of the page from JSON.
#     :return: BytesIO object of the overlay PDF.
#     """
#     packet = io.BytesIO()
#     can = canvas.Canvas(packet, pagesize=(json_width, json_height))

#     x_adjustment = 0
#     y_adjustment = -35
#     can.setFillColor(white)
#     can.setFont('Helvetica', 35)

#     for item in text_positions:
#         x, y, text = item['x'], letter[1] - item['y'], item['text']
#         # adjusted_x = x + x_adjustment
#         # adjusted_y = y + y_adjustment
#         can.drawString(x, y, text if text is not None else "")

#     can.save()
#     packet.seek(0)
#     return packet


# def create_subset_pdf(input_pdf, pages_to_include):
#     reader = PdfReader(input_pdf)
#     writer = PdfWriter()

#     for page_number in pages_to_include:
#         if 1 <= page_number <= len(reader.pages):
#             writer.add_page(reader.pages[page_number - 1])

#     subset_pdf_path = io.BytesIO()
#     writer.write(subset_pdf_path)
#     subset_pdf_path.seek(0)
#     return subset_pdf_path

# def add_text_to_pdf(input_pdf_path, output_pdf_path, text_positions):
#     """
#     Add text to specific positions in a PDF using pdfplumber, reportlab, and pypdf.
#     :param input_pdf_path: Path to the input PDF file.
#     :param output_pdf_path: Path to save the output PDF file.
#     :param text_positions: List of dictionaries with 'page', 'x', 'y', 'text'.
#     """
#     reader = PdfReader(input_pdf_path)
#     writer = PdfWriter()

#     grouped_positions = {}
#     for item in text_positions:
#         page_number = item['pageNumber'] - 1
#         if page_number not in grouped_positions:
#             grouped_positions[page_number] = []
#         grouped_positions[page_number].append(item)

#     with pdfplumber.open(input_pdf_path) as pdf:
#         for page_number in range(len(reader.pages)):
#             page = reader.pages[page_number]

#             if page_number in grouped_positions:
#                 tags = grouped_positions[page_number]
#                 json_width = tags[0]['width']
#                 json_height = tags[0]['height']
#                 print(json_width, json_height , "width and heigt")

#                 overlay_pdf_stream = create_overlay_pdf(
#                     tags, json_width, json_height
#                 )
#                 overlay_pdf = PdfReader(overlay_pdf_stream)
#                 overlay_page = overlay_pdf.pages[0]

#                 page.merge_page(overlay_page)

#             writer.add_page(page)

#     with open(output_pdf_path, "wb") as output_file:
#         writer.write(output_file)


# for idx, row in enumerate(rows):
#     cleaned_row = {key.strip(): value for key, value in row.items()}

#     pages = cleaned_row.get('Pages', '')
#     if pages:
#         pages_to_include = [int(page.strip()) for page in pages.split(',') if page.strip().isdigit()]
#     else:
#         with pdfplumber.open(pdf_input_path) as pdf:
#             valid_pages = list(range(1, len(pdf.pages) + 1))
#             pages_to_include = [page for page in pages_to_include if page in valid_pages]

#     subset_pdf = create_subset_pdf(pdf_input_path, pages_to_include)

#     filtered_tags = [tag.copy() for tag in json_data if tag["pageNumber"] in pages_to_include]
#     for tag in filtered_tags:
#         tag_text = tag["text"]
#         tag["text"] = cleaned_row.get(tag_text, "")

#     output_pdf_path = os.path.join(output_directory, f"output_file_{idx + 1}.pdf")
#     add_text_to_pdf(subset_pdf, output_pdf_path, filtered_tags)

# print(f"Tagged PDFs saved in directory: {output_directory}")







import pdfplumber
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pypdf import PdfWriter, PdfReader
import io
import json
import csv
import os
from reportlab.lib.units import inch
from reportlab.lib.colors import white, black

json_data = [
    {"pageNumber": 1, "x": 301, "y": 173, "text": "Tag 1", "width": 800, "height": 1131.6129032258063},
]

csv_file_path = "New Csv Format - Sheet1.csv"
pdf_input_path = "House-Warming-Invitation-Card (1).pdf"
output_directory = "output_files"

# Ensure output directory exists
os.makedirs(output_directory, exist_ok=True)

# Read the CSV file
rows = []
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        rows.append(row)

def create_blank_pdf_with_text(text_positions, json_width, json_height):
    """
    Create a blank PDF with the specified dimensions and add text at the given positions.
    """
    packet = io.BytesIO()
    
    # Create canvas with JSON-specified dimensions
    print(json_width, json_height , "json width json height") 
    can = canvas.Canvas(packet, pagesize=(json_width, json_height))
    
    # Make the page transparent (don't fill with any color)
    can.setFillColor(white)
    can.setFont('Helvetica', 35)

    for item in text_positions:
        x = item['x']
        y =   letter[1] - item['y'] 
        text = item['text']
        
        # Draw the text
        print(x, y, text , "x y text" , letter[1] , letter[0])
        can.drawString(x, y, text if text is not None else "")

    can.save()
    packet.seek(0)
    return packet

def create_subset_pdf(input_pdf, pages_to_include):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for page_number in pages_to_include:
        if 1 <= page_number <= len(reader.pages):
            writer.add_page(reader.pages[page_number - 1])

    subset_pdf_path = io.BytesIO()
    writer.write(subset_pdf_path)
    subset_pdf_path.seek(0)
    return subset_pdf_path

def add_text_to_pdf(input_pdf_path, output_pdf_path, text_positions):
    """
    Create a new PDF with text overlays and merge with the input PDF.
    """
    # Read the input PDF
    original_pdf = PdfReader(input_pdf_path)
    writer = PdfWriter()

    # Group text positions by page
    grouped_positions = {}
    for item in text_positions:
        page_number = item['pageNumber'] - 1
        if page_number not in grouped_positions:
            grouped_positions[page_number] = []
        grouped_positions[page_number].append(item)

    # Process each page
    for page_number in range(len(original_pdf.pages)):
        # Get the original page
        original_page = original_pdf.pages[page_number]

        if page_number in grouped_positions:
            tags = grouped_positions[page_number]
            json_width = tags[0]['width']
            json_height = tags[0]['height']

            
            text_pdf_stream = create_blank_pdf_with_text(tags, json_width, json_height)
            text_pdf = PdfReader(text_pdf_stream)
            text_page = text_pdf.pages[0]

        
            original_page.merge_page(text_page)

        writer.add_page(original_page)


    with open(output_pdf_path, "wb") as output_file:
        writer.write(output_file)

for idx, row in enumerate(rows):
    cleaned_row = {key.strip(): value for key, value in row.items()}


    pages = cleaned_row.get('Pages', '')
    if pages:
        pages_to_include = [int(page.strip()) for page in pages.split(',') if page.strip().isdigit()]
    else:
        with pdfplumber.open(pdf_input_path) as pdf:
            pages_to_include = list(range(1, len(pdf.pages) + 1))

    # Create subset PDF
    subset_pdf = create_subset_pdf(pdf_input_path, pages_to_include)

    # Filter and update tags
    filtered_tags = [tag.copy() for tag in json_data if tag["pageNumber"] in pages_to_include]
    for tag in filtered_tags:
        tag_text = tag["text"]
        tag["text"] = cleaned_row.get(tag_text, "")

    # Generate output PDF
    output_pdf_path = os.path.join(output_directory, f"output_file_{idx + 1}.pdf")
    add_text_to_pdf(subset_pdf, output_pdf_path, filtered_tags)

print(f"Tagged PDFs saved in directory: {output_directory}")