import pandas as pd
import fitz  # PyMuPDF
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

def add_text_to_pdf(input_pdf_path, output_pdf_path, text_data, coordinates_json):
    """
    Adds multiple texts to specific locations on pages of a PDF.

    Args:
        input_pdf_path (str): Path to the input PDF file.
        output_pdf_path (str): Path to save the modified PDF file.
        text_data (list): A list of dictionaries, where each dictionary
            specifies the text and page number for a text to be added.
        coordinates_json (str): JSON string specifying the coordinates for each page.
    """
    # Load coordinates from JSON
    coordinates = json.loads(coordinates_json)
    coord_map = {item['page']: [{'x': item['x'], 'y': item['y']}] for item in coordinates}

    # Process PDF
    pdf_document = fitz.open(input_pdf_path)

    for item in text_data:
        page_num = item['page'] - 1  # Page numbers are 0-based
        if 0 <= page_num < len(pdf_document):
            page = pdf_document[page_num]
            text = item['content']

            if page_num + 1 in coord_map:
                for coord in coord_map[page_num + 1]:
                    position = (coord['x'], coord['y'])
                    font_name = 'helv'  # Default font name
                    font_size = 12  # Default font size
                    color = (0, 0, 0)  # Default color (black)

                    text_params = {
                        "text": text,
                        "fontname": font_name,
                        "fontsize": font_size,
                        "rect": fitz.Rect(position[0], position[1], position[0] + 100, position[1] + 20),  # Adjust the rectangle size as needed
                        "fill_color": color,
                        "rotate": 0
                    }
                    page.insert_text(**text_params)
        else:
            print(f"Page number {item['page']} is out of range.")

    pdf_document.save(output_pdf_path)
    pdf_document.close()

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

# Use the functions
process_all_rows(
    csv_file="updated-content.csv",
    template_pdf="sample.pdf",
    coordinates_json=coordinates_json,
    output_prefix="output"
)
