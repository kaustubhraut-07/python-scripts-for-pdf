# import pdfplumber
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter
# from pypdf import PdfWriter, PdfReader
# import io
# import json
# import csv
# import os

# # Load the JSON data from frontend
# json_data = [
#     {"pageNumber": 1, "x": 265, "y": 176, "text": "Tag 1"},
#     {"pageNumber": 2, "x": 282, "y": 306, "text": "Tag 3"},
#     {"pageNumber": 2, "x": 222, "y": 195, "text": "Tag 2", "textSize": 16},
#     {"pageNumber": 10, "x": 168, "y": 364, "text": "Tag 4"}
# ]

# # Path to the input files
# csv_file_path = "New Csv Format - Sheet1.csv"
# pdf_input_path = "sample.pdf"
# output_directory = "output_files"

# # Ensure output directory exists
# os.makedirs(output_directory, exist_ok=True)

# # Read the CSV file
# rows = []
# with open(csv_file_path, 'r') as csv_file:
#     csv_reader = csv.DictReader(csv_file)
#     for row in csv_reader:
#         rows.append(row)

# # Function to create a subset PDF
# def create_subset_pdf(input_pdf, pages_to_include):
#     reader = PdfReader(input_pdf)
#     writer = PdfWriter()

#     for page_number in pages_to_include:
#         writer.add_page(reader.pages[page_number - 1])

#     subset_pdf_path = io.BytesIO()
#     writer.write(subset_pdf_path)
#     subset_pdf_path.seek(0)
#     return subset_pdf_path

# # Function to add tags to a PDF
# def add_tags_to_pdf(input_pdf, output_pdf, tags):
#     packet = io.BytesIO()
#     can = canvas.Canvas(packet, pagesize=letter)

#     for tag in tags:
#         print(tag , "tag")
#         page_number = tag["pageNumber"]
#         x = tag["x"]
#         y = letter[1] - tag["y"]  # Convert y-coordinate to PDF coordinate system
#         text = tag["text"]
#         text_size = tag.get("textSize", 12)

#         can.setFont("Helvetica", text_size)
#         can.drawString(x, y, text)

#     can.save()

#     # Merge the canvas with the PDF
#     packet.seek(0)
#     overlay_pdf = PdfReader(packet)
#     input_reader = PdfReader(input_pdf)
#     output_pdf_writer = PdfWriter()

#     for i, page in enumerate(input_reader.pages):
#         if i < len(overlay_pdf.pages):
#             page.merge_page(overlay_pdf.pages[i])
#         output_pdf_writer.add_page(page)

#     with open(output_pdf, "wb") as output:
#         output_pdf_writer.write(output)

# # Process each row in the CSV
# for idx, row in enumerate(rows):
#     # Handle missing or empty 'Pages' field
#     cleaned_row = {key.strip(): value for key, value in row.items()}

# # Accessing the value associated with the key 'Pages'
#     pages = cleaned_row['Pages']

# # Printing the value
#     print(pages)
#     if 'Pages' in cleaned_row and cleaned_row['Pages']:
#         pages_to_include = [int(page.strip()) for page in cleaned_row['Pages'].split(',') if page.strip().isdigit()]
#         print(pages_to_include , "pages to include")
#     else:
#         # Include all pages if 'Pages' is empty
#         print("in else full pdf")
#         with pdfplumber.open(pdf_input_path) as pdf:
#             pages_to_include = list(range(1, len(pdf.pages) + 1))

#     # Create a subset PDF for the specific pages
#     subset_pdf = create_subset_pdf(pdf_input_path, pages_to_include)

#     # Filter tags for the pages in this subset
#     filtered_tags = [tag for tag in json_data if tag["pageNumber"] in pages_to_include]

#     # Generate the output PDF path
#     output_pdf_path = os.path.join(output_directory, f"output_file_{idx + 1}.pdf")

#     # Add tags to the subset PDF
#     add_tags_to_pdf(subset_pdf, output_pdf_path, filtered_tags)

# print(f"Tagged PDFs saved in directory: {output_directory}")



# import pdfplumber
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter
# from pypdf import PdfWriter, PdfReader
# import io
# import json
# import csv
# import os

# # Load the JSON data from frontend
# json_data = [
#     {"pageNumber": 1, "x": 265, "y": 176, "text": "Tag 1"},
#     {"pageNumber": 2, "x": 282, "y": 306, "text": "Tag 3"},
#     {"pageNumber": 2, "x": 222, "y": 195, "text": "Tag 2", "textSize": 16},
#     {"pageNumber": 10, "x": 168, "y": 364, "text": "Tag 4"}
# ]

# # Path to the input files
# csv_file_path = "New Csv Format - Sheet1.csv"
# pdf_input_path = "sample.pdf"
# output_directory = "output_files"

# # Ensure output directory exists
# os.makedirs(output_directory, exist_ok=True)

# # Read the CSV file
# rows = []
# with open(csv_file_path, 'r') as csv_file:
#     csv_reader = csv.DictReader(csv_file)
#     for row in csv_reader:
#         rows.append(row)

# # Function to create a subset PDF
# def create_subset_pdf(input_pdf, pages_to_include):
#     reader = PdfReader(input_pdf)
#     writer = PdfWriter()

#     for page_number in pages_to_include:
#         writer.add_page(reader.pages[page_number - 1])

#     subset_pdf_path = io.BytesIO()
#     writer.write(subset_pdf_path)
#     subset_pdf_path.seek(0)
#     return subset_pdf_path

# # Function to add tags to a PDF
# def add_tags_to_pdf(input_pdf, output_pdf, tags, csv_row):
#     packet = io.BytesIO()
#     can = canvas.Canvas(packet, pagesize=letter)

#     for tag in tags:
#         page_number = tag["pageNumber"]
#         x = tag["x"]
#         y = letter[1] - tag["y"]  # Convert y-coordinate to PDF coordinate system
#         text = tag["text"]
#         text_size = tag.get("textSize", 12)

#         # Get the corresponding value from the CSV row
#         tag_value = csv_row.get(text.strip(), "")

#         # Ensure tag_value is a string
#         if tag_value is None:
#             tag_value = ""

#         can.setFont("Helvetica", text_size)
#         can.drawString(x, y, tag_value)

#     can.save()

#     # Merge the canvas with the PDF
#     packet.seek(0)
#     overlay_pdf = PdfReader(packet)
#     input_reader = PdfReader(input_pdf)
#     output_pdf_writer = PdfWriter()

#     for i, page in enumerate(input_reader.pages):
#         if i < len(overlay_pdf.pages):
#             page.merge_page(overlay_pdf.pages[i])
#         output_pdf_writer.add_page(page)

#     with open(output_pdf, "wb") as output:
#         output_pdf_writer.write(output)

# # Process each row in the CSV
# for idx, row in enumerate(rows):
#     # Handle missing or empty 'Pages' field
#     cleaned_row = {key.strip(): value for key, value in row.items()}

#     # Accessing the value associated with the key 'Pages'
#     pages = cleaned_row.get('Pages', '')

#     # Printing the value
#     print(pages)
#     if pages:
#         pages_to_include = [int(page.strip()) for page in pages.split(',') if page.strip().isdigit()]
#         print(pages_to_include, "pages to include")
#     else:
#         # Include all pages if 'Pages' is empty
#         print("in else full pdf")
#         with pdfplumber.open(pdf_input_path) as pdf:
#             pages_to_include = list(range(1, len(pdf.pages) + 1))

#     # Create a subset PDF for the specific pages
#     subset_pdf = create_subset_pdf(pdf_input_path, pages_to_include)

#     # Filter tags for the pages in this subset
#     filtered_tags = [tag for tag in json_data if tag["pageNumber"] in pages_to_include]

#     # Generate the output PDF path
#     output_pdf_path = os.path.join(output_directory, f"output_file_{idx + 1}.pdf")

#     # Add tags to the subset PDF
#     add_tags_to_pdf(subset_pdf, output_pdf_path, filtered_tags, cleaned_row)

# print(f"Tagged PDFs saved in directory: {output_directory}")





import pdfplumber
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pypdf import PdfWriter, PdfReader
import io
import json
import csv
import os

# Load the JSON data from frontend
# json_data = [
#     {"pageNumber": 1, "x": 265, "y": 176, "text": "Tag 1"},
#     {"pageNumber": 2, "x": 282, "y": 306, "text": "Tag 3"},
#     {"pageNumber": 2, "x": 222, "y": 195, "text": "Tag 2", "textSize": 16},
#     {"pageNumber": 10, "x": 168, "y": 364, "text": "Tag 4"}
# ]
json_data = [
    {"pageNumber": 1, "x": 265, "y": 176, "text": "Tag 1"},
    {"pageNumber": 1, "x": 222, "y": 195, "text": "Tag 2", "textSize": 16},
    {"pageNumber": 2, "x": 282, "y": 306, "text": "Tag 3"},
    {"pageNumber": 2, "x": 222, "y": 195, "text": "Tag 2", "textSize": 16},
    {"pageNumber": 3, "x": 265, "y": 176, "text": "Tag 1"},
    {"pageNumber": 3, "x": 222, "y": 195, "text": "Tag 2", "textSize": 16},
    {"pageNumber": 9, "x": 265, "y": 176, "text": "Tag 1"},
    {"pageNumber": 9, "x": 222, "y": 195, "text": "Tag 2", "textSize": 16},
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

# Function to add tags to a PDF
def add_tags_to_pdf(input_pdf, output_pdf, tags, csv_row):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    # Create a dictionary to hold tags for each page
    page_tags = {}
    for tag in tags:
        page_number = tag["pageNumber"]
        if page_number not in page_tags:
            page_tags[page_number] = []
        page_tags[page_number].append(tag)

    # Create a canvas for each page and add the tags
    for page_number, tags in page_tags.items():
        can = canvas.Canvas(packet, pagesize=letter)
        for tag in tags:
            print(tag['text'] , "tag" )
            # for tags in csv_row:
            #     print(tags , "tags")

            # if tag['text'] == csv_row[]
            x = tag["x"]
            y = letter[1] - tag["y"]  # Convert y-coordinate to PDF coordinate system
            text = tag["text"]
            text_size = tag.get("textSize", 12)

            # Get the corresponding value from the CSV row
            tag_value = csv_row.get(text.strip(), "")
            print(tag_value , "tag_value")

            # Ensure tag_value is a string
            if tag_value is None:
                tag_value = ""

            can.setFont("Helvetica", text_size)
            can.drawString(x, y, tag_value)

        can.save()

    # Merge the canvas with the PDF
    packet.seek(0)
    overlay_pdf = PdfReader(packet)
    input_reader = PdfReader(input_pdf)
    output_pdf_writer = PdfWriter()

    for i, page in enumerate(input_reader.pages):
        if i < len(overlay_pdf.pages):
            page.merge_page(overlay_pdf.pages[i])
        output_pdf_writer.add_page(page)

    with open(output_pdf, "wb") as output:
        output_pdf_writer.write(output)

# Process each row in the CSV
for idx, row in enumerate(rows):
    # Handle missing or empty 'Pages' field
    cleaned_row = {key.strip(): value for key, value in row.items()}

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

    # Create a subset PDF for the specific pages
    subset_pdf = create_subset_pdf(pdf_input_path, pages_to_include)

    # Filter tags for the pages in this subset
    filtered_tags = [tag for tag in json_data if tag["pageNumber"] in pages_to_include]

    # Generate the output PDF path
    output_pdf_path = os.path.join(output_directory, f"output_file_{idx + 1}.pdf")

    # Add tags to the subset PDF
    add_tags_to_pdf(subset_pdf, output_pdf_path, filtered_tags, cleaned_row)

print(f"Tagged PDFs saved in directory: {output_directory}")
