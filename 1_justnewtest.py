import pdfplumber
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pypdf import PdfWriter, PdfReader
import io
import json
import csv
import os

# Load the JSON data from frontend
json_data = [
    {"pageNumber": 1, "x": 265, "y": 176, "text": "Tag 1"},
    {"pageNumber": 2, "x": 282, "y": 306, "text": "Tag 3"},
    {"pageNumber": 3, "x": 300, "y": 200, "text": "Tag 1"},
    {"pageNumber": 9, "x": 325, "y": 192, "text": "Tag 1"},
    {"pageNumber": 9, "x": 222, "y": 195, "text": "Tag 2"},
    {"pageNumber": 10, "x": 168, "y": 364, "text": "Tag 4"}
]

# Path to the input files
csv_file_path = "New Csv Format - Sheet1.csv"
pdf_input_path = "sample.pdf"
output_directory = "output_files"

# Ensure output directory exists
os.makedirs(output_directory, exist_ok=True)

# Read the CSV file
rows = []
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        rows.append(row)

# Function to create a subset PDF
def create_subset_pdf(input_pdf, pages_to_include):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for page_number in pages_to_include:
        writer.add_page(reader.pages[page_number - 1])

    subset_pdf_path = io.BytesIO()
    writer.write(subset_pdf_path)
    subset_pdf_path.seek(0)
    return subset_pdf_path

# Function to add text to a PDF
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
        page_number = item['pageNumber'] - 1  # Convert to 0-based index
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

# Function to create an overlay PDF with text at specified positions
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
        x, y, text = item['x'], page_height - item['y'], item['text']
        can.drawString(x, y, text)

    can.save()
    packet.seek(0)
    return packet

# Process each row in the CSV
for idx, row in enumerate(rows):
    # Handle missing or empty 'Pages' field
    cleaned_row = {key.strip(): value for key, value in row.items()}
    print(cleaned_row, "csv Row")

    # Accessing the value associated with the key 'Pages'
    pages = cleaned_row.get('Pages', '')

    # Printing the value
    print(pages)
    if pages:
        pages_to_include = [int(page.strip()) for page in pages.split(',') if page.strip().isdigit()]
        print(pages_to_include, "pages to include")
    else:
        # Include all pages if 'Pages' is empty
        print("in else full pdf")
        with pdfplumber.open(pdf_input_path) as pdf:
            pages_to_include = list(range(1, len(pdf.pages) + 1))

    print(pages_to_include, "pages to include")
    # Create a subset PDF for the specific pages
    subset_pdf = create_subset_pdf(pdf_input_path, pages_to_include)

    filtered_tags = [tag for tag in json_data if tag["pageNumber"] in pages_to_include]
    # print(filtered_tags, "filtered tags")
    for tag in filtered_tags:
        print(tag, "tag")
        tag_text = tag["text"]
        tag["text"] = cleaned_row.get(tag_text, "")

    print(filtered_tags, "filtered tags")

    # Generate the output PDF path
    output_pdf_path = os.path.join(output_directory, f"output_file_{idx + 1}.pdf")
    # print()
    # Add tags to the subset PDF
    add_text_to_pdf(subset_pdf, output_pdf_path, filtered_tags)

print(f"Tagged PDFs saved in directory: {output_directory}")