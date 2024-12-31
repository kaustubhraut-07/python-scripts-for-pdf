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
from reportlab.lib.units import inch
from reportlab.lib.colors import white, black

# Load the JSON data from frontend
# json_data = [
#     {"pageNumber": 1, "x": 265, "y": 176, "text": "Tag 1"},
#     {"pageNumber": 2, "x": 282, "y": 306, "text": "Tag 3"},
#     {"pageNumber": 2, "x": 222, "y": 195, "text": "Tag 2", "textSize": 16},
#     {"pageNumber": 10, "x": 168, "y": 364, "text": "Tag 4"}
# ]
json_data = [
    {"pageNumber": 1, "x": 303, "y": 180, "text": "Tag 1"},
    # {"pageNumber": 1, "x": 422, "y": 756, "text": "Tag 1"},
    #  {"pageNumber": 1, "x": 0, "y": 0, "text": "Tag 1"},
    #   {"pageNumber": 1, "x": 0, "y": 754, "text": "Tag 1"},
    # # {"pageNumber": 1, "x": 222, "y": 195, "text": "Tag 2", "textSize": 16},
    # {"pageNumber": 2, "x": 282, "y": 306, "text": "Tag 3"},
    # # {"pageNumber": 2, "x": 222, "y": 195, "text": "Tag 2", "textSize": 16},
    # {"pageNumber": 3, "x": 164, "y": 420, "text": "Tag 1"},
    # # {"pageNumber": 3, "x": 222, "y": 195, "text": "Tag 2", "textSize": 16},
    # {"pageNumber": 9, "x": 325, "y": 192, "text": "Tag 1"},
    # {"pageNumber": 9, "x": 222, "y": 195, "text": "Tag 2"},
    # {"pageNumber": 10, "x": 320, "y": 224, "text": "Tag 4"}
]



# Path to the input files
csv_file_path = "New Csv Format - Sheet1.csv"
# pdf_input_path = "sample.pdf"
pdf_input_path = "House-Warming-Invitation-Card (1).pdf"
# pdf_input_path = "dummy_10_pages.pdf"
output_directory = "output_files"

# Ensure output directory exists
os.makedirs(output_directory, exist_ok=True)

# Read the CSV file
rows = []
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        rows.append(row)


def normalize_coordinates(x, y, standard_width, standard_height, actual_width, actual_height):
    """
    Normalize the coordinates to a standard size and then scale to the actual size.
    :param x: Original x coordinate.
    :param y: Original y coordinate.
    :param standard_width: Width of the standard size.
    :param standard_height: Height of the standard size.
    :param actual_width: Width of the actual page.
    :param actual_height: Height of the actual page.
    :return: Scaled x and y coordinates.
    """
    aspect_ratio_standard = standard_width / standard_height
    aspect_ratio_actual = actual_width / actual_height

    if aspect_ratio_standard > aspect_ratio_actual:
        scale_factor = actual_width / standard_width
        normalized_x = x * scale_factor
        normalized_y = y * scale_factor
    else:
        scale_factor = actual_height / standard_height
        normalized_x = x * scale_factor
        normalized_y = y * scale_factor

    standard_width=800
    standard_height=1100
    x_standard = (x / standard_width) * standard_width
    y_standard = (y / standard_height) * standard_height
    print(x_standard,y_standard , "x and y standeared")
    # Scaling from standard to original PDF
    x_original = (x_standard / standard_width) * actual_width
    y_original = (y_standard / standard_height) * actual_height
    print(x_original , y_original , "x and y origfinal")
    print(normalized_x, normalized_y, "normalized x and y")


    return normalized_x, normalized_y
    # return x_original,y_original

# Function to create a subset PDF
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
    # can = canvas.Canvas(packet, pagesize=(page_width * inch, page_height * inch))
    print(page_width , page_height , "with and heith")


    # 2480.0 3508.0 with and heith  client pdf
    # 612 792 with and heith dummy pdf
    # 595.27 841.89 with and heith sample pdf 

    # print(text_positions , "text_positions")
    print(letter, "letter")
    x_adjustment = 0  
    y_adjustment = -35
    can.setFillColor(white)
    # can.setFillColor(black)

    can.setFont('Helvetica', 35) 

    standard_width, standard_height = letter

    for item in text_positions:
        # print(item , "Item")
        print(item['x'], item['y'], letter[1] - item['y'], item['text'] , "in for loop")
        # x, y, text = item['x'], letter[1] -  item['y'], item['text']
        x, y, text = item['x'], item['y'], item['text']
        # y = page_height - y
        # print(y , "y value")
        x_original, y_original = normalize_coordinates(
            x, y, standard_width, standard_height, page_width, page_height
        )

        normalized_x, normalized_y = normalize_coordinates(x, y, standard_width, standard_height, page_width, page_height)
        # adjusted_x = normalized_x + x_adjustment
        # adjusted_y = normalized_y + y_adjustment

        adjusted_x = x + x_adjustment
        adjusted_y = y + y_adjustment
        # can.drawString(x_original, page_height - y_original, item['text'])  # Inverting  y for ReportLab

        # can.drawString(x, y, text if text is not None else "")
        can.drawString(normalized_x, normalized_y, text if text is not None else "")
        # can.drawString(adjusted_x, adjusted_y, text if text is not None else "")
        # can.drawString(x * inch, page_height * inch - y * inch, text if text is not None else "") # Changed line

    
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
        # print(item , "in text_postion")
        page_number = item['pageNumber'] -1 # Convert to 0-based index
        if page_number not in grouped_positions:
            grouped_positions[page_number] = []
        grouped_positions[page_number].append(item)
    
    # Open pdfplumber to read page dimensions
    with pdfplumber.open(input_pdf_path) as pdf:
        # for page in pdf.pages:
        #     print(page.bbox , "pdf bbox" )
        for page_number in range(len(reader.pages)):
            page = reader.pages[page_number]
            pdf_page = pdf.pages[page_number]  # Get page size from pdfplumber
            print(pdf_page.bbox[3] , "pdf page bbox" )
            # adjexted_y = page.bbox
            # Extract page dimensions
            page_width =   pdf_page.width
            page_height = pdf_page.height

            # page_width = float(page.mediabox.width)
            # page_height = float(page.mediabox.height)
            
            if page_number in grouped_positions:
                # Create overlay with reportlab
                # print(grouped_positions , "groupeddpotions" , page_number)
                scaled_width = 800 
                scaled_height = 1100 #taking this from frontend
                # print(adjexted_y , "adjexted_y")
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












# Function to add tags to a PDF
# def add_tags_to_pdf(input_pdf, output_pdf, tags, csv_row):
#     packet = io.BytesIO()
#     # page_width = pdf_page.width
#     # page_height = pdf_page.height
#     can = canvas.Canvas(packet
#                         # ,pagesize=(page_width, page_height)
#                         )
#     # print(csv_row['Tag 1'], "csv_row")
#     # print(csv_row, "csv_row")
#     # Create a dictionary to hold tags for each page
#     page_tags = {}
#     # print(page_tags, "page tags")
#     for tag in tags:
#         page_number = tag["pageNumber"]
#         if page_number not in page_tags:
#             page_tags[page_number] = []
#         page_tags[page_number].append(tag)

#     print(page_tags, "page tags")
#     print(letter , "letter")
#     # Create a canvas for each page and add the tags
#     # print(csv_row['Pages'] ,  "csv_row pages")
#     print(csv_row , "cav_row")
#     for page_number, tags in page_tags.items():
#         can = canvas.Canvas(packet, pagesize=letter)
#         for tag in tags:
#             if csv_row[tag['text']] :
#                 # print(tag['text'] , "tag" , csv_row[tag['text']])
                
#                 # for tags in csv_row:
#                 #     print(tags , "tags")

#                 # if tag['text'] == csv_row[]
#                 x = tag["x"]
#                 y = letter[1] - tag["y"]  # Convert y-coordinate to PDF coordinate system
#                 text = tag["text"]
#                 text_size = tag.get("textSize", 12)

#                 tag_value = csv_row.get(text.strip(), "")
#                 print(tag_value , "tag_value")

           
#                 if tag_value is None:
#                     tag_value = ""
#                 if tag_value:
#                     can.setFont("Helvetica", text_size)
#                     can.drawString(x, y, tag_value)
#             # can.setFont("Helvetica", text_size)
#             # can.drawString(x, y, tag_value)

#         can.save()

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

# Process each row in the CSV
for idx, row in enumerate(rows):
    # Handle missing or empty 'Pages' field
    cleaned_row = {key.strip(): value for key, value in row.items()}
    print(cleaned_row , "csv Row")

    # Accessing the value associated with the key 'Pages'
    pages = cleaned_row.get('Pages', '')

    # Printing the value
    # print(pages)
    if pages:
        pages_to_include = [int(page.strip()) for page in pages.split(',') if page.strip().isdigit()]
        # print(pages_to_include, "pages to include")
    else:
        # Include all pages if 'Pages' is empty
        # print("in else full pdf")
        with pdfplumber.open(pdf_input_path) as pdf:
            valid_pages = list(range(1, len(pdf.pages) + 1))
            pages_to_include = [page for page in pages_to_include if page in valid_pages]


    # print(pages_to_include , "pages to include  ")
    # Create a subset PDF for the specific pages
    subset_pdf = create_subset_pdf(pdf_input_path, pages_to_include)

    
    # filtered_tags = [tag for tag in json_data if tag["pageNumber"] in pages_to_include]
    filtered_tags = [tag.copy() for tag in json_data if tag["pageNumber"] in pages_to_include]
    # print(filtered_tags, "filtered tags 1")
    for tag in filtered_tags:
        # print(tag, "tag")
        tag_text = tag["text"]
        # print(tag_text, "tag_text")
        tag["text"] = cleaned_row.get(tag_text, "") 
        print(cleaned_row.get(tag_text, "") )

    print(filtered_tags, "filtered tags")


    # Generate the output PDF path
    output_pdf_path = os.path.join(output_directory, f"output_file_{idx + 1}.pdf")
    # print()
    # Add tags to the subset PDF
    # add_tags_to_pdf(subset_pdf, output_pdf_path, filtered_tags, cleaned_row)
    add_text_to_pdf(subset_pdf, output_pdf_path, filtered_tags)

print(f"Tagged PDFs saved in directory: {output_directory}")






