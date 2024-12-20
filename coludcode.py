import pandas as pd
import pdfplumber
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pypdf import PdfWriter, PdfReader
import io
import json

def parse_csv_content(csv_file):
    """
    Parse CSV file and return list of dictionaries with content and page numbers
    """
    # Read CSV file
    df = pd.read_csv(csv_file)
    
    # Process each row
    all_rows_data = []
    for _, row in df.iterrows():
        # Parse the page numbers string into a list
        page_numbers = [int(x.strip()) for x in row['PageNo'].split(',')]
        
        # Create a list of content items (excluding PageNo column)
        content_items = row.drop('PageNo').dropna().tolist()
        
        # Pair each content with its corresponding page number
        row_data = []
        for page_num, content in zip(page_numbers, content_items):
            if isinstance(content, str) and content.strip():  # Check if content is non-empty
                row_data.append({
                    'page': page_num,
                    'content': content
                })
        
        if row_data:  # Only add if there's valid data
            all_rows_data.append(row_data)
    
    return all_rows_data

def create_overlay_pdf(text_positions, page_width, page_height):
    """
    Create an overlay PDF with text at specified positions
    """
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(page_width, page_height))
    
    for item in text_positions:
        x, y = item['x'], item['y']
        text = item['content']
        can.drawString(x, y, text)
    
    can.save()
    packet.seek(0)
    return packet

# def add_text_to_pdf(input_pdf_path, output_pdf_path, text_data, coordinates_json):
    """
    Add text to PDF using the specified coordinates
    """
    # Load coordinates from JSON
    coordinates = json.loads(coordinates_json)
    coord_map = {item['page']: {'x': item['x'], 'y': item['y']} for item in coordinates}
    
    # Process PDF
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()
    
    # Group positions by page
    grouped_positions = {}
    for item in text_data:
        page_num = item['page']
        if page_num <= len(reader.pages):  # Check if page exists in PDF
            if page_num not in grouped_positions:
                grouped_positions[page_num] = []
            
            if page_num in coord_map:
                # Add coordinates to the text data
                # position_data = {
                #     'x': coord_map[page_num]['x'],
                #     'y': coord_map[page_num]['y'],
                #     'content': item['content']
                # }
                # grouped_positions[page_num].append(position_data)
                for coord in coord_map[page_num]:
                    position_data = {
                        'x': coord['x'],
                        'y': coord['y'],
                        'content': item['content']
                    }
                    grouped_positions[page_num].append(position_data)
    
    # Create PDF with overlays
    with pdfplumber.open(input_pdf_path) as pdf:
        for page_number in range(len(reader.pages)):
            page = reader.pages[page_number]
            pdf_page = pdf.pages[page_number]
            
            page_width = pdf_page.width
            page_height = pdf_page.height
            
            if page_number + 1 in grouped_positions:  # Add 1 because pages are 1-indexed
                overlay_pdf_stream = create_overlay_pdf(
                    grouped_positions[page_number + 1],
                    page_width,
                    page_height
                )
                overlay_pdf = PdfReader(overlay_pdf_stream)
                overlay_page = overlay_pdf.pages[0]
                page.merge_page(overlay_page)
            
            writer.add_page(page)
    
    # Save the final PDF
    with open(output_pdf_path, "wb") as output_file:
        writer.write(output_file)


def add_text_to_pdf(input_pdf_path, output_pdf_path, text_data, coordinates_json):
    """
    Add text to PDF using the specified coordinates
    """
    # Load coordinates from JSON
    coordinates = json.loads(coordinates_json)
    # print(coordinates , "line 1")
    coord_map = {item['page']: [{'x': item['x'], 'y': item['y']}] for item in coordinates}
    print(coord_map , "line 2")
    
    # coord_map = {}
    # for item in coordinates:
    #     if item['page'] not in coord_map:
    #         coord_map[item['page']] = []
    # coord_map[item['page']].append({'x': item['x'], 'y': item['y']})

    # print(coord_map)

    # Process PDF
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    # Group positions by page
    grouped_positions = {}
    for item in text_data:
        page_num = item['page']
        # print(page_num)
        if page_num <= len(reader.pages):  # Check if page exists in PDF
            if page_num not in grouped_positions:
                grouped_positions[page_num] = []

            if page_num in coord_map:
                # Add coordinates to the text data
                for coord in coord_map[page_num]:
                    # print(coord)
                    position_data = {
                        'x': coord['x'],
                        'y': coord['y'],
                        'content': item['content']
                    }
                    grouped_positions[page_num].append(position_data)

    # Create PDF with overlays
    with pdfplumber.open(input_pdf_path) as pdf:
        for page_number in range(len(reader.pages)):
            page = reader.pages[page_number]
            pdf_page = pdf.pages[page_number]

            page_width = pdf_page.width
            page_height = pdf_page.height

            if page_number + 1 in grouped_positions:  # Add 1 because pages are 1-indexed
                overlay_pdf_stream = create_overlay_pdf(
                    grouped_positions[page_number + 1],
                    page_width,
                    page_height
                )
                overlay_pdf = PdfReader(overlay_pdf_stream)
                overlay_page = overlay_pdf.pages[0]
                page.merge_page(overlay_page)

            writer.add_page(page)

    # Save the final PDF
    with open(output_pdf_path, "wb") as output_file:
        writer.write(output_file)

def process_all_rows(csv_file, template_pdf, coordinates_json, output_prefix="output"):
    """
    Process all rows in CSV and generate multiple PDFs
    """
    # Parse CSV content
    all_rows_data = parse_csv_content(csv_file)
    
    # Generate a PDF for each row
    for index, row_data in enumerate(all_rows_data):
        output_path = f"{output_prefix}_{index + 1}.pdf"
        add_text_to_pdf(template_pdf, output_path, row_data, coordinates_json)
        print(f"Generated {output_path}")

# Example usage
coordinates_json = '''
[
    {"page": 1, "x": 100, "y": 700},
    {"page": 1, "x": 200, "y": 900},
    {"page": 2, "x": 150, "y": 600},
    {"page": 3, "x": 200, "y": 500},
    {"page": 4, "x": 250, "y": 400},
    {"page": 5, "x": 300, "y": 300}
]
'''

# 1,1,2,3,4,5

# Use the functions
process_all_rows(
    csv_file="updated-content.csv",
    template_pdf="sample.pdf",
    coordinates_json=coordinates_json,
    output_prefix="output"
)