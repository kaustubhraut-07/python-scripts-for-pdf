# import pdfplumber
# from reportlab.pdfgen import canvas
# from pypdf import PdfWriter, PdfReader
# import io
# import pandas as pd

# # Predefined positions for each page
# predefined_positions = {
#     1: [{"x": 100, "y": 700}, {"x": 300, "y": 900}],  # Two positions on page 1
#     2: [{"x": 150, "y": 600}],  # One position on page 2
#     3: [{"x": 200, "y": 500}]   # One position on page 3
# }

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

#     for item in text_positions:
#         x, y, text = item['x'], item['y'], item['text']
#         can.drawString(x, y, text)

#     can.save()
#     packet.seek(0)
#     return packet

# def parse_content_csv(csv_path, predefined_positions):
#     """
#     Parse a simplified CSV to map content to predefined positions.
#     :param csv_path: Path to the CSV file.
#     :param predefined_positions: Dictionary of predefined positions by page.
#     :return: List of dictionaries with 'page', 'x', 'y', 'text'.
#     """
#     text_positions = []
#     csv_data = pd.read_csv(csv_path)
#     position_counters = {page: 0 for page in predefined_positions}

#     for _, row in csv_data.iterrows():
#         page = int(row["PageNo"])
#         content = row["content"]

#         if page in predefined_positions:
#             positions = predefined_positions[page]
#             counter = position_counters[page]

#             if counter < len(positions):
#                 position = positions[counter]
#                 print(page , position["x"], position["y"], content)
#                 text_positions.append({
#                     "page": page,
#                     "x": position["x"],
#                     "y": position["y"],
#                     "text": content
#                 })
#                 position_counters[page] += 1

#     return text_positions

# def add_text_to_pdf(input_pdf_path, output_pdf_path, csv_path):
#     """
#     Add text to specific positions in a PDF using pdfplumber, reportlab, and pypdf.
#     :param input_pdf_path: Path to the input PDF file.
#     :param output_pdf_path: Path to save the output PDF file.
#     :param csv_path: Path to the CSV file with content information.
#     """
#     # Open the original PDF
#     reader = PdfReader(input_pdf_path)
#     writer = PdfWriter()

#     # Parse the CSV to get text positions
#     text_positions = parse_content_csv(csv_path, predefined_positions)

#     # print(text_positions)

#     # Group positions by page for easy processing
#     grouped_positions = {}
#     for item in text_positions:
#         page_number = item['page'] - 1  # Convert to 0-based index
#         if page_number not in grouped_positions:
#             grouped_positions[page_number] = []
#         # print(grouped_positions )
#         grouped_positions[page_number].append(item)

#     print(grouped_positions , "grouped postions")

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
#                 print(page_number , "page number")
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
# input_pdf_path = "sample.pdf"
# output_pdf_path = "output-1.pdf"
# csv_path = "content.csv"

# add_text_to_pdf(input_pdf_path, output_pdf_path, csv_path)













import pdfplumber
from reportlab.pdfgen import canvas
from pypdf import PdfWriter, PdfReader
import io
import pandas as pd

# Predefined positions for each page
predefined_positions = {
    1: [{"x": 100, "y": 700}, {"x": 300, "y": 900}],  # Two positions on page 1
    2: [{"x": 150, "y": 600}],  # One position on page 2
    3: [{"x": 200, "y": 500}]   # One position on page 3
}

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

def parse_content_csv(csv_path, predefined_positions):
    """
    Parse a simplified CSV to map content to predefined positions.
    :param csv_path: Path to the CSV file.
    :param predefined_positions: Dictionary of predefined positions by page.
    :return: List of dictionaries with 'page', 'x', 'y', 'text'.
    """
    text_positions = []
    csv_data = pd.read_csv(csv_path)
    position_counters = {page: 0 for page in predefined_positions}

    for _, row in csv_data.iterrows():
        page = int(row["PageNo"])
        content = row["content"]

        if page in predefined_positions:
            positions = predefined_positions[page]
            counter = position_counters[page]

            if counter < len(positions):
                position = positions[counter]
                print(page, position["x"], position["y"], content)
                text_positions.append({
                    "page": page,
                    "x": position["x"],
                    "y": position["y"],
                    "text": content
                })
                position_counters[page] += 1

    return text_positions

def add_text_to_pdf(input_pdf_path, output_pdf_path, csv_path):
    """
    Add text to specific positions in a PDF using pdfplumber, reportlab, and pypdf.
    :param input_pdf_path: Path to the input PDF file.
    :param output_pdf_path: Path to save the output PDF file.
    :param csv_path: Path to the CSV file with content information.
    """
    # Open the original PDF
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    # Parse the CSV to get text positions
    text_positions = parse_content_csv(csv_path, predefined_positions)

    # Group positions by page for easy processing
    grouped_positions = {}
    for item in text_positions:
        page_number = item['page'] - 1  # Convert to 0-based index
        if page_number not in grouped_positions:
            grouped_positions[page_number] = []
        grouped_positions[page_number].append(item)

    print(grouped_positions, "grouped positions")

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
                print(page_number, "page number")
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
output_pdf_path = "output-1.pdf"
csv_path = "content.csv"

add_text_to_pdf(input_pdf_path, output_pdf_path, csv_path)












# import pdfplumber
# from reportlab.pdfgen import canvas
# from pypdf import PdfWriter, PdfReader
# import io
# import pandas as pd

# # Predefined positions for each page
# predefined_positions = {
#     1: [{"x": 100, "y": 700}, {"x": 300, "y": 900}],  # Two positions on page 1
#     2: [{"x": 150, "y": 600}],  # One position on page 2
#     3: [{"x": 200, "y": 500}]   # One position on page 3
# }

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

#     for item in text_positions:
#         x, y, text = item['x'], item['y'], item['text']
#         can.drawString(x, y, text)

#     can.save()
#     packet.seek(0)
#     return packet

# def parse_content_csv(csv_path, predefined_positions):
#     """
#     Parse a simplified CSV to map content to predefined positions.
#     :param csv_path: Path to the CSV file.
#     :param predefined_positions: Dictionary of predefined positions by page.
#     :return: List of dictionaries with 'page', 'x', 'y', 'text'.
#     """
#     text_positions = []
#     csv_data = pd.read_csv(csv_path)
#     position_counters = {page: 0 for page in predefined_positions}

#     for _, row in csv_data.iterrows():
#         page = int(row["PageNo"])
#         content = row["content"]

#         if page in predefined_positions:
#             positions = predefined_positions[page]
#             print(len(positions),"page apper")
#             counter = position_counters[page]
#             print(counter,"counter")

#             if counter < len(positions):
#                 position = positions[counter]
#                 text_positions.append({
#                     "page": page,
#                     "x": position["x"],
#                     "y": position["y"],
#                     "text": content
#                 })
#                 position_counters[page] += 1

#     return text_positions

# def add_text_to_pdf(input_pdf_path, output_pdf_path, csv_path):
#     """
#     Add text to specific positions in a PDF using pdfplumber, reportlab, and pypdf.
#     :param input_pdf_path: Path to the input PDF file.
#     :param output_pdf_path: Path to save the output PDF file.
#     :param csv_path: Path to the CSV file with content information.
#     """
#     # Open the original PDF
#     reader = PdfReader(input_pdf_path)
#     writer = PdfWriter()

#     # Parse the CSV to get text positions
#     text_positions = parse_content_csv(csv_path, predefined_positions)

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
# input_pdf_path = "sample.pdf"
# output_pdf_path = "output-1.pdf"
# csv_path = "content.csv"

# add_text_to_pdf(input_pdf_path, output_pdf_path, csv_path)
