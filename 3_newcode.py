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
# from reportlab.lib.pagesizes import A4

# # Example JSON data (replace with your actual data)
# json_data = [
#     {"pageNumber": 1, "x": 212, "y": 123, "text": "Tag 1", "width": 800, "height": 1131.61},  # Standard letter size
# ]

# csv_file_path = "New Csv Format - Sheet1.csv"  # Replace with your CSV path
# pdf_input_path = "House-Warming-Invitation-Card (1).pdf"  # Replace with your PDF path
# output_directory = "output_files"

# # Ensure output directory exists
# os.makedirs(output_directory, exist_ok=True)

# # Read the CSV file
# rows = []
# with open(csv_file_path, 'r', encoding='utf-8') as csv_file:  # Added encoding
#     csv_reader = csv.DictReader(csv_file)
#     for row in csv_reader:
#         rows.append(row)

# def create_blank_pdf_with_text(text_positions, json_width, json_height):
#     packet = io.BytesIO()
#     can = canvas.Canvas(packet,bottomup=1,pagesize=A4
#                         # pagesize=(json_width, json_height)
#                         )
#     can.setFillColor(white)
#     can.setFont('Helvetica', 35)

#     for item in text_positions:
#         x = item['x']
#         y = item['y']
#         text = item['text']
#         print(x, y, text , "x y and text")
#         can.drawString(x, y, text if text is not None else "")  # Keep original y

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
#     original_pdf = PdfReader(input_pdf_path)
#     writer = PdfWriter()

#     grouped_positions = {}
#     for item in text_positions:
#         page_number = item['pageNumber'] - 1
#         if page_number not in grouped_positions:
#             grouped_positions[page_number] = []
#         grouped_positions[page_number].append(item)

#     with pdfplumber.open(input_pdf_path) as pdf_plumber: 
#         for page_number in range(len(original_pdf.pages)):
#             original_page = original_pdf.pages[page_number]

#             if page_number in grouped_positions:
#                 tags = grouped_positions[page_number]
#                 json_width = 595
#                 # tags[0]['width']
#                 json_height =841
#                 # tags[0]['height']

#                 plumber_page = pdf_plumber.pages[page_number]
#                 page_height = plumber_page.height
#                 print(page_height , "page height" , json_data[0]['height'] , letter)

#                 for tag in tags:
#                     tag['y'] =  json_data[0]['height'] - tag['y'] # Correct y coordinate
#                     print(tag['y'] , "tag y")
#                 text_pdf_stream = create_blank_pdf_with_text(tags, 595, 841)
#                                                             #  json_width, 
#                                                             #  json_height)
#                 text_pdf = PdfReader(text_pdf_stream)
#                 text_page = text_pdf.pages[0]

#                 original_page.merge_page(text_page)

#             writer.add_page(original_page)

#     with open(output_pdf_path, "wb") as output_file:
#         writer.write(output_file)

# for idx, row in enumerate(rows):
#     cleaned_row = {key.strip(): value for key, value in row.items()}

#     pages = cleaned_row.get('Pages', '')
#     if pages:
#         pages_to_include = [int(page.strip()) for page in pages.split(',') if page.strip().isdigit()]
#     else:
#         with pdfplumber.open(pdf_input_path) as pdf:
#             pages_to_include = list(range(1, len(pdf.pages) + 1))

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
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import white
from pypdf import PdfWriter, PdfReader
import io
import json
import csv
import os

# Example JSON data (replace with your actual data)
json_data = [
    {"pageNumber": 1, "x": 212, "y": 123, "text": "Tag 1"},
]

csv_file_path = "New Csv Format - Sheet1.csv"  # Replace with your CSV path
pdf_input_path = "House-Warming-Invitation-Card (1).pdf"  # Replace with your PDF path
output_directory = "output_files"

# Ensure output directory exists
os.makedirs(output_directory, exist_ok=True)

# Read the CSV file
rows = []
with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        rows.append(row)

def create_blank_pdf_with_text(text_positions):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    can.setFillColor(white)
    can.setFont('Helvetica', 40)  # Adjust font size as needed
    print(A4[0] , A4[1],"page size")
    for item in text_positions:
        x = item['x']
        y = item['y']
        text = item['text']
        print(f"Adding text '{text}' at ({x}, {y})")
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
    original_pdf = PdfReader(input_pdf_path)
    writer = PdfWriter()

    grouped_positions = {}
    for item in text_positions:
        page_number = item['pageNumber'] - 1
        if page_number not in grouped_positions:
            grouped_positions[page_number] = []
        grouped_positions[page_number].append(item)

    with pdfplumber.open(input_pdf_path) as pdf_plumber:
        for page_number in range(len(original_pdf.pages)):
            original_page = original_pdf.pages[page_number]

            if page_number in grouped_positions:
                tags = grouped_positions[page_number]

                # Adjust y-coordinates based on A4 page height (841 points)
                for tag in tags:
                    tag['y'] = A4[1] - tag['y']  # Flip y-coordinate for PDF coordinate system

                text_pdf_stream = create_blank_pdf_with_text(tags)
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

    subset_pdf = create_subset_pdf(pdf_input_path, pages_to_include)

    filtered_tags = [tag.copy() for tag in json_data if tag["pageNumber"] in pages_to_include]
    for tag in filtered_tags:
        tag_text = tag["text"]
        tag["text"] = cleaned_row.get(tag_text, "")

    output_pdf_path = os.path.join(output_directory, f"output_file_{idx + 1}.pdf")
    add_text_to_pdf(subset_pdf, output_pdf_path, filtered_tags)

print(f"Tagged PDFs saved in directory: {output_directory}")
