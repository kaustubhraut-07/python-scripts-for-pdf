# # import pdfplumber
# # from reportlab.pdfgen import canvas
# # from reportlab.lib.pagesizes import letter
# # from pypdf import PdfWriter, PdfReader
# # import io
# # import json
# # import csv
# # import os

# # # Load the JSON data from frontend
# # json_data = [
# #     {"pageNumber": 1, "x": 265, "y": 176, "text": "Tag 1"},
# #     {"pageNumber": 2, "x": 282, "y": 306, "text": "Tag 3"},
# #     {"pageNumber": 3, "x": 300, "y": 200, "text": "Tag 1"},
# #     {"pageNumber": 9, "x": 325, "y": 192, "text": "Tag 1"},
# #     {"pageNumber": 9, "x": 222, "y": 195, "text": "Tag 2"},
# #     {"pageNumber": 10, "x": 168, "y": 364, "text": "Tag 4"}
# # ]

# # # Path to the input files
# # csv_file_path = "New Csv Format - Sheet1.csv"
# # pdf_input_path = "sample.pdf"
# # output_directory = "output_files"

# # # Ensure output directory exists
# # os.makedirs(output_directory, exist_ok=True)

# # # Read the CSV file
# # rows = []
# # with open(csv_file_path, 'r') as csv_file:
# #     csv_reader = csv.DictReader(csv_file)
# #     for row in csv_reader:
# #         rows.append(row)

# # # Function to create a subset PDF
# # def create_subset_pdf(input_pdf, pages_to_include):
# #     reader = PdfReader(input_pdf)
# #     writer = PdfWriter()

# #     for page_number in pages_to_include:
# #         writer.add_page(reader.pages[page_number - 1])

# #     subset_pdf_path = io.BytesIO()
# #     writer.write(subset_pdf_path)
# #     subset_pdf_path.seek(0)
# #     return subset_pdf_path

# # # Function to add text to a PDF
# # def add_text_to_pdf(input_pdf_path, output_pdf_path, text_positions):
# #     """
# #     Add text to specific positions in a PDF using pdfplumber, reportlab, and pypdf.
# #     :param input_pdf_path: Path to the input PDF file.
# #     :param output_pdf_path: Path to save the output PDF file.
# #     :param text_positions: List of dictionaries with 'page', 'x', 'y', 'text'.
# #     """
# #     # Open the original PDF
# #     reader = PdfReader(input_pdf_path)
# #     writer = PdfWriter()

# #     # Group positions by page for easy processing
# #     grouped_positions = {}
# #     for item in text_positions:
# #         page_number = item['pageNumber'] - 1  # Convert to 0-based index
# #         if page_number not in grouped_positions:
# #             grouped_positions[page_number] = []
# #         grouped_positions[page_number].append(item)

# #     # Open pdfplumber to read page dimensions
# #     with pdfplumber.open(input_pdf_path) as pdf:
# #         for page_number in range(len(reader.pages)):
# #             page = reader.pages[page_number]
# #             pdf_page = pdf.pages[page_number]  # Get page size from pdfplumber

# #             # Extract page dimensions
# #             page_width = pdf_page.width
# #             page_height = pdf_page.height

# #             if page_number in grouped_positions:
# #                 # Create overlay with reportlab
# #                 overlay_pdf_stream = create_overlay_pdf(
# #                     grouped_positions[page_number], page_width, page_height
# #                 )
# #                 overlay_pdf = PdfReader(overlay_pdf_stream)
# #                 overlay_page = overlay_pdf.pages[0]

# #                 # Merge overlay with original page
# #                 page.merge_page(overlay_page)

# #             # Add the updated page to the writer
# #             writer.add_page(page)

# #     # Save the final PDF
# #     with open(output_pdf_path, "wb") as output_file:
# #         writer.write(output_file)

# # # Function to create an overlay PDF with text at specified positions
# # def create_overlay_pdf(text_positions, page_width, page_height):
# #     """
# #     Create an overlay PDF with text at specified positions.
# #     :param text_positions: List of dictionaries with 'x', 'y', 'text'.
# #     :param page_width: Width of the page.
# #     :param page_height: Height of the page.
# #     :return: BytesIO object of the overlay PDF.
# #     """
# #     packet = io.BytesIO()
# #     can = canvas.Canvas(packet, pagesize=(page_width, page_height))

# #     for item in text_positions:
# #         x, y, text = item['x'], page_height - item['y'], item['text']
# #         can.drawString(x, y, text)

# #     can.save()
# #     packet.seek(0)
# #     return packet

# # # Process each row in the CSV
# # for idx, row in enumerate(rows):
# #     # Handle missing or empty 'Pages' field
# #     cleaned_row = {key.strip(): value for key, value in row.items()}
# #     print(cleaned_row, "csv Row")

# #     # Accessing the value associated with the key 'Pages'
# #     pages = cleaned_row.get('Pages', '')

# #     # Printing the value
# #     print(pages)
# #     if pages:
# #         pages_to_include = [int(page.strip()) for page in pages.split(',') if page.strip().isdigit()]
# #         print(pages_to_include, "pages to include")
# #     else:
# #         # Include all pages if 'Pages' is empty
# #         print("in else full pdf")
# #         with pdfplumber.open(pdf_input_path) as pdf:
# #             pages_to_include = list(range(1, len(pdf.pages) + 1))

# #     print(pages_to_include, "pages to include")
# #     # Create a subset PDF for the specific pages
# #     subset_pdf = create_subset_pdf(pdf_input_path, pages_to_include)

# #     filtered_tags = [tag for tag in json_data if tag["pageNumber"] in pages_to_include]
# #     # print(filtered_tags, "filtered tags")
# #     for tag in filtered_tags:
# #         print(tag, "tag")
# #         tag_text = tag["text"]
# #         tag["text"] = cleaned_row.get(tag_text, "")

# #     print(filtered_tags, "filtered tags")

# #     # Generate the output PDF path
# #     output_pdf_path = os.path.join(output_directory, f"output_file_{idx + 1}.pdf")
# #     # print()
# #     # Add tags to the subset PDF
# #     add_text_to_pdf(subset_pdf, output_pdf_path, filtered_tags)

# # print(f"Tagged PDFs saved in directory: {output_directory}")



# # import pdfplumber
# # from reportlab.pdfgen import canvas
# # from reportlab.lib.pagesizes import letter
# # from pypdf import PdfWriter, PdfReader
# # import io
# # import os

# # # Sample JSON data
# # json_data = [
# #     {"pageNumber": 1, "x": 405, "y": 0, "text": "Tag 1"},
# #     {"pageNumber": 2, "x": 282, "y": 306, "text": "Tag 3"},
# #     {"pageNumber": 3, "x": 164, "y": 420, "text": "Tag 1"},
# #     {"pageNumber": 9, "x": 325, "y": 192, "text": "Tag 1"},
# #     {"pageNumber": 9, "x": 222, "y": 195, "text": "Tag 2"},
# #     {"pageNumber": 10, "x": 320, "y": 224, "text": "Tag 4"}
# # ]

# # # Input PDF path
# # pdf_input_path = "dummy_10_pages.pdf"
# # output_pdf_path = "output_debug.pdf"

# # # Function to create an overlay PDF with visual debugging
# # def create_overlay_pdf_debug(text_positions, page_width, page_height):
# #     """
# #     Creates an overlay PDF with text and visual markers.
# #     """
# #     packet = io.BytesIO()
# #     can = canvas.Canvas(packet, pagesize=(page_width, page_height))

# #     for item in text_positions:
# #         x, y, text = item['x'], item['y'], item['text']
# #         # Convert y to PDF coordinate system
# #         y = page_height - y
# #         can.drawString(x, y, text if text else "")

# #         # Draw a rectangle around the text for debugging
# #         can.setStrokeColorRGB(1, 0, 0)  # Red color
# #         can.rect(x - 5, y - 5, 50, 20)  # Adjust rectangle size as needed

# #     can.save()
# #     packet.seek(0)
# #     return packet

# # # Function to add overlay to a PDF
# # def add_overlay_to_pdf(input_pdf_path, output_pdf_path, text_positions):
# #     reader = PdfReader(input_pdf_path)
# #     writer = PdfWriter()

# #     grouped_positions = {}
# #     for item in text_positions:
# #         page_number = item['pageNumber'] - 1  # Convert to 0-based index
# #         if page_number not in grouped_positions:
# #             grouped_positions[page_number] = []
# #         grouped_positions[page_number].append(item)

# #     with pdfplumber.open(input_pdf_path) as pdf:
# #         for page_number in range(len(reader.pages)):
# #             page = reader.pages[page_number]
# #             pdf_page = pdf.pages[page_number]

# #             page_width = pdf_page.width
# #             page_height = pdf_page.height

# #             if page_number in grouped_positions:
# #                 overlay_pdf_stream = create_overlay_pdf_debug(
# #                     grouped_positions[page_number], page_width, page_height
# #                 )
# #                 overlay_pdf = PdfReader(overlay_pdf_stream)
# #                 overlay_page = overlay_pdf.pages[0]

# #                 page.merge_page(overlay_page)

# #             writer.add_page(page)

# #     with open(output_pdf_path, "wb") as output_file:
# #         writer.write(output_file)

# # # Apply the overlay
# # add_overlay_to_pdf(pdf_input_path, output_pdf_path, json_data)

# # print(f"Debugging PDF saved at: {output_pdf_path}")



# from reportlab.pdfgen import canvas
# from pypdf import PdfWriter, PdfReader
# import io
# import os

# # Example JSON data
# json_data = [
#     {"pageNumber": 1, "x": 0, "y": 0, "text": "Tag 1"},
#     {"pageNumber": 2, "x": 282, "y": 306, "text": "Tag 3"},
#     {"pageNumber": 3, "x": 164, "y": 420, "text": "Tag 1"},
#     {"pageNumber": 9, "x": 325, "y": 192, "text": "Tag 1"},
#     {"pageNumber": 9, "x": 222, "y": 195, "text": "Tag 2"},
#     {"pageNumber": 10, "x": 320, "y": 224, "text": "Tag 4"}
# ]

# # Path to the input PDF
# pdf_input_path = "dummy_10_pages.pdf"
# output_directory = "output_files"
# os.makedirs(output_directory, exist_ok=True)

# def create_overlay_pdf(text_positions, page_width, page_height):
#     """
#     Create an overlay PDF with text at specified positions, handling y-axis alignment issues.
#     :param text_positions: List of dictionaries with 'x', 'y', 'text'.
#     :param page_width: Width of the page.
#     :param page_height: Height of the page.
#     :return: BytesIO object of the overlay PDF.
#     """
#     packet = io.BytesIO()
#     can = canvas.Canvas(packet, pagesize=(page_width, page_height))

#     # Adjustments for alignment
#     for item in text_positions:
#         x = item['x']
#         y = page_height - item['y']  # Invert y-axis for correct positioning
#         text = item.get('text', "")
        
#         # Optional: Add text size adjustment if provided
#         text_size = item.get('textSize', 12)
#         can.setFont("Helvetica", text_size)

#         # Draw the text at the adjusted coordinates
#         can.drawString(x, y, text)

#     can.save()
#     packet.seek(0)
#     return packet

# def add_text_to_pdf(input_pdf_path, output_pdf_path, text_positions):
#     """
#     Add text to specific positions in a PDF using ReportLab only, resolving y-axis issues.
#     :param input_pdf_path: Path to the input PDF file.
#     :param output_pdf_path: Path to save the output PDF file.
#     :param text_positions: List of dictionaries with 'page', 'x', 'y', 'text'.
#     """
#     reader = PdfReader(input_pdf_path)
#     writer = PdfWriter()

#     for page_number in range(len(reader.pages)):
#         page = reader.pages[page_number]
#         page_width = float(page.mediabox.width)
#         page_height = float(page.mediabox.height)

#         # Filter text positions for the current page
#         page_text_positions = [
#             pos for pos in text_positions if pos["pageNumber"] - 1 == page_number
#         ]

#         if page_text_positions:
#             overlay_pdf_stream = create_overlay_pdf(page_text_positions, page_width, page_height)
#             overlay_pdf = PdfReader(overlay_pdf_stream)
#             overlay_page = overlay_pdf.pages[0]
            
#             # Merge overlay with original page
#             page.merge_page(overlay_page)

#         # Add the updated page to the writer
#         writer.add_page(page)

#     # Save the final PDF
#     with open(output_pdf_path, "wb") as output_file:
#         writer.write(output_file)

# # Apply text to the PDF and save
# output_pdf_path = os.path.join(output_directory, "output_with_tags.pdf")
# add_text_to_pdf(pdf_input_path, output_pdf_path, json_data)

# print(f"Tagged PDF saved at: {output_pdf_path}")



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
#     {"pageNumber": 1, "x": 302, "y": 173, "text": "Tag 1"},  
# ]
# csv_file_path = "New Csv Format - Sheet1.csv"
# pdf_input_path = "House-Warming-Invitation-Card (1).pdf"  
# # pdf_input_path = "dummy_10_pages.pdf"
# output_directory = "output_files"
# os.makedirs(output_directory, exist_ok=True)


# rows = []
# with open(csv_file_path, 'r') as csv_file:
#     csv_reader = csv.DictReader(csv_file)
#     for row in csv_reader:
#         rows.append(row)

# def normalize_coordinates(x_scaled, y_scaled, scaled_width, scaled_height, original_width, original_height, standard_width=800, standard_height=600):
#     x_standard = (x_scaled / scaled_width) * standard_width
#     y_standard = (y_scaled / scaled_height) * standard_height
#     x_original = (x_standard / standard_width) * original_width
#     y_original = (y_standard / standard_height) * original_height
#     return x_original, y_original

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

# def create_overlay_pdf(text_positions, original_width, original_height, scaled_width, scaled_height):
#     packet = io.BytesIO()
#     can = canvas.Canvas(packet, pagesize=(original_width, original_height))
#     can.setFillColor(white)
#     can.setFont('Helvetica', 40)

#     for item in text_positions:
#         x_original, y_original = normalize_coordinates(
#             item['x'], item['y'], scaled_width, scaled_height, original_width, original_height
#         )
#         can.drawString(x_original, original_height - y_original, item['text'])
#     can.save()
#     packet.seek(0)
#     return packet

# def add_text_to_pdf(input_pdf_path, output_pdf_path, text_positions, scaled_width, scaled_height): # Added scaled width and height
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
#             pdf_page = pdf.pages[page_number]
#             page_width = pdf_page.width
#             page_height = pdf_page.height

#             if page_number in grouped_positions:
#                 overlay_pdf_stream = create_overlay_pdf(
#                     grouped_positions[page_number], page_width, page_height, scaled_width, scaled_height  # Pass scaled dimensions
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
#             pages_to_include = list(range(1, len(pdf.pages) + 1))

#     subset_pdf = create_subset_pdf(pdf_input_path, pages_to_include)
#     filtered_tags = [tag.copy() for tag in json_data if tag["pageNumber"] in pages_to_include]

#     for tag in filtered_tags:
#         tag_text = tag["text"]
#         tag["text"] = cleaned_row.get(tag_text, "")


#     scaled_width = 800  
#     scaled_height = 1100 

#     output_pdf_path = os.path.join(output_directory, f"output_file_{idx + 1}.pdf")
#     add_text_to_pdf(subset_pdf, output_pdf_path, filtered_tags, scaled_width, scaled_height) # Pass scaled dimensions

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
    {"pageNumber": 1, "x": 244.17864999999995, "y": 349, "text": "Tag 1"},  
]
csv_file_path = "New Csv Format - Sheet1.csv"
# pdf_input_path = "House-Warming-Invitation-Card (1).pdf"  
pdf_input_path = "sample.pdf"  
# pdf_input_path = "dummy_10_pages.pdf"
output_directory = "output_files"
os.makedirs(output_directory, exist_ok=True)

rows = []
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        rows.append(row)

def normalize_coordinates(x_scaled, y_scaled, scaled_width, scaled_height, original_width, original_height, standard_width=800, standard_height=600):
    x_standard = (x_scaled / scaled_width) * standard_width
    y_standard = (y_scaled / scaled_height) * standard_height
    x_original = (x_standard / standard_width) * original_width
    y_original = (y_standard / standard_height) * original_height
    return x_original, y_original

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

def create_overlay_pdf(text_positions, original_width, original_height, scaled_width, scaled_height):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(original_width, original_height))
    can.setFillColor(white)
    can.setFont('Helvetica', 40)

    for item in text_positions:
        x_original, y_original = normalize_coordinates(
            item['x'], item['y'], scaled_width, scaled_height, original_width, original_height
        )
        # Adjust y-coordinate to account for the coordinate system difference
        y_original_corrected = original_height - y_original
        can.drawString(x_original, y_original_corrected, item['text'])
    can.save()
    packet.seek(0)
    return packet

def add_text_to_pdf(input_pdf_path, output_pdf_path, text_positions, scaled_width, scaled_height): # Added scaled width and height
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()
    grouped_positions = {}
    for item in text_positions:
        page_number = item['pageNumber'] - 1
        if page_number not in grouped_positions:
            grouped_positions[page_number] = []
        grouped_positions[page_number].append(item)

    with pdfplumber.open(input_pdf_path) as pdf:
        for page_number in range(len(reader.pages)):
            page = reader.pages[page_number]
            pdf_page = pdf.pages[page_number]
            page_width = pdf_page.width
            page_height = pdf_page.height

            if page_number in grouped_positions:
                overlay_pdf_stream = create_overlay_pdf(
                    grouped_positions[page_number], page_width, page_height, scaled_width, scaled_height  # Pass scaled dimensions
                )
                overlay_pdf = PdfReader(overlay_pdf_stream)
                overlay_page = overlay_pdf.pages[0]
                page.merge_page(overlay_page)
            writer.add_page(page)

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

    scaled_width = 800  
    scaled_height = 1100 

    output_pdf_path = os.path.join(output_directory, f"output_file_{idx + 1}.pdf")
    add_text_to_pdf(subset_pdf, output_pdf_path, filtered_tags, scaled_width, scaled_height) # Pass scaled dimensions

print(f"Tagged PDFs saved in directory: {output_directory}")