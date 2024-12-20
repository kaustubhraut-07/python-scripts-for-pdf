import pdfplumber
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pypdf import PdfWriter, PdfReader
import io
import json
import csv


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
        x, y, text = item['x'], item['y'], item['content']
        print(x, y, text)
        can.drawString(x, y, text)
    
    can.save()
    packet.seek(0)
    return packet



def read_csv(file_path):
    text_positions = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            pages = row[0].split(',')
            #print(pages) 
            content_index = 1  
            for page in pages: 
                try:
                    content = row[content_index]
                    #print(content) 
                    text_positions.append({'page': int(page), 'text': content})
                    content_index += 1 
                except (ValueError, IndexError):
                    continue
    return text_positions

csv_content = read_csv('updated-content.csv')
print(csv_content, "csv file data")

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
        # print(item["page"])
        page_number = int(item['page']) - 1  # Convert to 0-based index
        if page_number not in grouped_positions:
            grouped_positions[page_number] = []
        grouped_positions[page_number].append(item)
    
    # Open pdfplumber to read page dimensions
    with pdfplumber.open(input_pdf_path) as pdf:
        for page_number in range(len(reader.pages)):
            page = reader.pages[page_number]
            pdf_page = pdf.pages[page_number]  
            
            # Extract page dimensions
            page_width = pdf_page.width
            page_height = pdf_page.height
            # print(page_width , page_height , "page number")
            
            if page_number in grouped_positions:
                # Create overlay with reportlab
                print(grouped_positions[page_number], page_width, page_height , "contn")
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
output_pdf_path = "output.pdf"

# JSON input from the frontend
json_input = '''
[
  {"page": 1, "x": 100, "y": 200},
  {"page": 1, "x": 150, "y": 400},
  {"page": 1, "x": 150, "y": 500},
  {"page": 2, "x": 150, "y": 600},
  {"page": 2, "x": 200, "y": 800},
  {"page": 3, "x": 200, "y": 500},
  {"page": 4, "x": 250, "y": 400},
  {"page": 5, "x": 300, "y": 300}
]
'''


# def combine_data(text_positions, coordinates):
 

#     combined_data = []
#     coord_index = 0  # To track the current coordinate

#     for text_item in text_positions:
#         text_page = text_item['page']
#         text_content = text_item['text']

#         # Find a matching coordinate on the same page
#         while coord_index < len(coordinates) and coordinates[coord_index]['page'] < text_page:
#             coord_index += 1  # Move to the next coordinate if it's on a previous page

#         if coord_index < len(coordinates) and coordinates[coord_index]['page'] == text_page:
#             combined_data.append({
#                 'page': text_page,  # Convert to string for consistency
#                 'x': str(coordinates[coord_index]['x']),  # Convert to string
#                 'y': str(coordinates[coord_index]['y']),  # Convert to string
#                 'content': text_content
#             })
#             coord_index+=1
#         else:
#             print(f"No matching coordinates found for page {text_page}")
#             continue


#     return combined_data

def combine_data(text_positions, coordinates):
    combined_data = []

    text_index = 0
    while text_index < len(text_positions):
        coord_index = 0 
        temp_list = []
        while coord_index < len(coordinates) and text_index < len(text_positions):
            text_item = text_positions[text_index]
            text_page = text_item['page']
            text_content = text_item['text']
            if coordinates[coord_index]['page'] == text_page:
                temp_list.append({
                    'page': text_page,
                    'x': coordinates[coord_index]['x'],
                    'y': coordinates[coord_index]['y'],
                    'content': text_content
                })
                text_index+=1
                coord_index+=1
            elif coordinates[coord_index]['page'] < text_page:
                coord_index+=1
            else:
                text_index+=1

        combined_data.extend(temp_list)

    return combined_data


# text_positions = [
#     {'page': 1, 'text': 'Hi'}, {'page': 1, 'text': 'Hello'}, {'page': 2, 'text': 'Bye'},
#     {'page': 3, 'text': 'Thank you'},{'page': 4, 'text': 'test'},{'page': 5, 'text': '34test'}
# ]

json_input = '''
[
    {"page": 1, "x": 100, "y": 200},
    {"page": 1, "x": 150, "y": 400},
    {"page": 2, "x": 150, "y": 600},
    {"page": 3, "x": 200, "y": 500},
    {"page": 4, "x": 250, "y": 400},
    {"page": 5, "x": 300, "y": 300}

]
'''
coordinates = json.loads(json_input)

combined_json = combine_data(csv_content, coordinates)
print(json.dumps(combined_json, indent=4))


# text_positions_missing = [{'page': 1, 'text': 'Text1'}, {'page': 6, 'text': 'Text2'}]
# combined_missing = combine_data(text_positions_missing, coordinates)
# print("\nExample with missing coordinates:")
# print(json.dumps(combined_missing, indent=4))
# combineddata = json.dumps(combined_json, indent=4)




text_positions = json.loads(json_input)

add_text_to_pdf(input_pdf_path, output_pdf_path, combined_json)