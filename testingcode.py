import pdfplumber
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pypdf import PdfWriter, PdfReader
import io
import json
import csv

def create_overlay_pdf(text_positions, page_width, page_height):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(page_width, page_height))

    for item in text_positions:
        x, y, text = item['x'], item['y'], item['content']
        can.drawString(x, y, text)

    can.save()
    packet.seek(0)
    return packet

def read_csv(file_path):
    text_positions = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            pages = row[0].split(',')
            content_index = 1
            row_positions = []  # List to store positions for current row
            for page in pages:
                try:
                    content = row[content_index]
                    row_positions.append({'page': int(page), 'text': content})
                    content_index += 1
                except (ValueError, IndexError):
                    continue
            text_positions.append(row_positions)  # Add row positions to main list
    return text_positions

def combine_data(text_positions_rows, coordinates):
    combined_data_rows = []
    for text_positions in text_positions_rows: #Iterate over each row of text positions
        combined_data = []
        coord_index = 0
        text_index = 0
        while text_index < len(text_positions):
            temp_list = []
            coord_index = 0
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
        combined_data_rows.append(combined_data)
    return combined_data_rows

def add_text_to_pdf(input_pdf_path, output_base_path, combined_text_data):
    reader = PdfReader(input_pdf_path)
    with pdfplumber.open(input_pdf_path) as pdf:
        for row_index, text_positions in enumerate(combined_text_data):
            writer = PdfWriter()  # Create a new writer for each row
            grouped_positions = {}
            for item in text_positions:
                page_number = int(item['page']) - 1
                if page_number not in grouped_positions:
                    grouped_positions[page_number] = []
                grouped_positions[page_number].append(item)

            for page_number in range(len(reader.pages)):
                page = reader.pages[page_number]
                pdf_page = pdf.pages[page_number]
                page_width = pdf_page.width
                page_height = pdf_page.height

                if page_number in grouped_positions:
                    overlay_pdf_stream = create_overlay_pdf(
                        grouped_positions[page_number], page_width, page_height
                    )
                    overlay_pdf = PdfReader(overlay_pdf_stream)
                    overlay_page = overlay_pdf.pages[0]
                    page.merge_page(overlay_page)

                writer.add_page(page)

            output_filename = f"{output_base_path}_row_{row_index + 1}.pdf"
            with open(output_filename, "wb") as output_file:
                writer.write(output_file)


input_pdf_path = "sample.pdf" 
csv_file_path = "updated-content.csv" 
output_base_path = "output-90"

# Create a dummy CSV file for testing
with open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Pages", "Content1", "Content2", "Content3", "Content4", "Content5", "Content6"])
    writer.writerow(["1,1,2,3,4,5", "Hi", "Hello", "Bye", "Thank you", "test", "34test"])
    writer.writerow(["1,1,2,3,4,5", "hello", "tesgasd", "adasd", "asdasd", "asdasd", "asdasd"])

# JSON input
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

text_positions_rows = read_csv(csv_file_path)
combined_data_rows = combine_data(text_positions_rows, coordinates)

add_text_to_pdf(input_pdf_path, output_base_path, combined_data_rows)

print("PDFs generated successfully!")