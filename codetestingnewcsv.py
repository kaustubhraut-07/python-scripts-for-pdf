import pdfplumber
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pypdf import PdfWriter, PdfReader
import io
import json
import csv
import os

def create_overlay_pdf(text_positions, page_width, page_height):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(page_width, page_height))
    for item in text_positions:
        # print(item['x'], item['y'], item['content'])
        x, y, text = item['x'], item['y'], item['content']
        can.drawString(x, y, text)
    can.save()
    packet.seek(0)
    return packet

def read_csv(file_path):
    text_positions_rows = []
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:  
            reader = csv.reader(csvfile)
            next(reader)  
            for row in reader:
                pages_str = row[0].strip()
                if not pages_str:  
                    text_positions_rows.append("FULL_PDF")  
                    continue

                pages = [int(p.strip()) for p in pages_str.split(',') if p.strip()] 
                content_index = 1
                row_positions = []
                for page in pages:
                    try:
                        content = row[content_index].strip() 
                        if content: 
                            row_positions.append({'page': page, 'text': content})
                        content_index += 1
                    except IndexError:  
                        continue
                text_positions_rows.append(row_positions)
    except FileNotFoundError:
        print(f"Error: CSV file '{file_path}' not found.")
        return None
    except Exception as e: 
        print(f"An error occurred while reading the CSV: {e}")
        return None
    return text_positions_rows

def combine_data(text_positions_rows, coordinates):
    if text_positions_rows is None:
        return None

    combined_data_rows = []
    for text_positions in text_positions_rows:
        if text_positions == "FULL_PDF":
            combined_data_rows.append("FULL_PDF")
            continue

        combined_data = []
        for text_item in text_positions: 
            for coord in coordinates: 
                # print(text_item['page'])
                if coord['pageNumber'] == text_item['page']:
                    combined_data.append({
                        'page': text_item['page'],
                        'x': coord['x'],
                        'y': coord['y'],
                        'content': text_item['text']
                    })
        combined_data_rows.append(combined_data)
    return combined_data_rows


def combine_data(text_positions_rows, coordinates):
    if text_positions_rows is None or coordinates is None:
        return None

    combined_data_rows = []
    for row in text_positions_rows:
        if row == "FULL_PDF":
            combined_data_rows.append("FULL_PDF")
            continue
        print(row)
        combined_row = []
        pages_in_row = sorted(list({item['page'] for item in row})) #get unique pages in a row and sort them
        # print(pages_in_row)
        for page in pages_in_row: 
            for coord in coordinates: 
                if coord['pageNumber'] == page: 
                    for text_item in row: 
                       
                        # if coord['text'] in text_item['content']:
                            print(coord['text'] ,  text_item )
                            combined_row.append({
                                'page': text_item['page'],
                                'x': coord['x'],
                                'y': coord['y'],
                                'content': text_item['text']
                                # 'content': text_item[coord['text']] 
                            })
        combined_data_rows.append(combined_row)
    return combined_data_rows

def add_text_to_pdf(input_pdf_path, output_base_path, combined_text_data):
    if combined_text_data is None:
        return

    try:
        reader = PdfReader(input_pdf_path)
        num_pages = len(reader.pages)
        with pdfplumber.open(input_pdf_path) as pdf:
            for row_index, text_positions in enumerate(combined_text_data):
                writer = PdfWriter()

                if text_positions == "FULL_PDF":
                    
                    for page_num in range(num_pages):
                        writer.add_page(reader.pages[page_num])
                    output_filename = f"{output_base_path}_row_{row_index + 1}_FULL.pdf"
                    with open(output_filename, "wb") as output_file:
                        writer.write(output_file)
                    continue

                # grouped_positions = {}
                page_positions = {}
                # for item in text_positions:
                #     page_number = int(item['page']) - 1
                #     if 0 <= page_number < num_pages: 
                #         if page_number not in grouped_positions:
                #             grouped_positions[page_number] = []
                #         grouped_positions[page_number].append(item)
                #     else:
                #         print(f"Warning: Page number {item['page']} is out of range. Skipping.")
                for item in text_positions:
                     page_number = item['page'] - 1
                     if 0 <= page_number < num_pages:
                        if page_number not in page_positions:
                            page_positions[page_number] = []
                        page_positions[page_number].append(item)
                else:
                    print(f"Warning: Page number {item['page']} is out of range. Skipping.")
                # print(grouped_positions , "grouped postions")

                pages_to_include = sorted(list(page_positions.keys())) 
                for page_number in pages_to_include:
                    # print(page_number , "page number")
                    page = reader.pages[page_number]
                    pdf_page = pdf.pages[page_number]
                    page_width = pdf_page.width
                    page_height = pdf_page.height

                    # if page_number in grouped_positions:
                    #     overlay_pdf_stream = create_overlay_pdf(
                    #         grouped_positions[page_number], page_width, page_height
                    #     )
                    #     overlay_pdf = PdfReader(overlay_pdf_stream)
                    #     overlay_page = overlay_pdf.pages[0]
                    #     page.merge_page(overlay_page)

                    # writer.add_page(page)
                    overlay_positions = page_positions.get(page_number, [])
                    if overlay_positions:
                        overlay_pdf_stream = create_overlay_pdf(
                            overlay_positions, page_width, page_height
                         )
                    if overlay_pdf_stream:
                        overlay_pdf = PdfReader(overlay_pdf_stream)
                        overlay_page = overlay_pdf.pages[0]
                        page.merge_page(overlay_page)

                writer.add_page(page)

                output_filename = f"{output_base_path}_row_{row_index + 1}.pdf"
                with open(output_filename, "wb") as output_file:
                    writer.write(output_file)
    except FileNotFoundError:
        print(f"Error: Input PDF file '{input_pdf_path}' not found.")
    except Exception as e:
        print(f"An error occurred during PDF processing: {e}")

# def combine_data(text_positions_rows, coordinates):
#     # if text_positions_rows is None or coordinates is None:
#     #     return None
#     print(text_positions_rows)
#     combined_data_rows = []
#     for row in text_positions_rows:
#         if row == "FULL_PDF":
#             combined_data_rows.append("FULL_PDF")
#             continue

#         print(row)

#         combined_row = []
#         print(row)
#         pages_in_row = sorted(list({int(item['page']) for item in row}))
#         for page in pages_in_row:
#             # print(page)
#             page_data = {'page': page, 'texts': []}  # Initialize data for the page
#             for coord in coordinates:
#                 if coord['pageNumber'] == page:
#                     for text_item in row:
#                         # print(text_item)
#                         if coord['text'] in text_item['text']:
#                             page_data['texts'].append({
#                                 'x': coord['x'],
#                                 'y': coord['y'],
#                                 'content': text_item['text']
#                             })
#             combined_row.append(page_data) #append the page to the combined row even if texts is empty
#         combined_data_rows.append(combined_row)
#     return combined_data_rows

# def add_text_to_pdf(input_pdf_path, output_base_path, combined_text_data):
#     if combined_text_data is None:
#         return

#     try:
#         reader = PdfReader(input_pdf_path)
#         num_pages = len(reader.pages)
#         with pdfplumber.open(input_pdf_path) as pdf:
#             for row_index, text_positions_data in enumerate(combined_text_data): #text_positions_data is now a list of dicts
#                 writer = PdfWriter()

#                 if text_positions_data == "FULL_PDF":
#                     for page_num in range(num_pages):
#                         writer.add_page(reader.pages[page_num])
#                     output_filename = f"{output_base_path}_row_{row_index + 1}_FULL.pdf"
#                     with open(output_filename, "wb") as output_file:
#                         writer.write(output_file)
#                     continue
                
#                 for page_data in text_positions_data: #Iterate through page_data
#                     page_number = page_data['page'] - 1
#                     if 0 <= page_number < num_pages:
#                         page = reader.pages[page_number]
#                         pdf_page = pdf.pages[page_number]
#                         page_width = pdf_page.width
#                         page_height = pdf_page.height

#                         overlay_positions = page_data.get('texts', []) #Get the list of texts or empty list
#                         if overlay_positions:
#                             overlay_pdf_stream = create_overlay_pdf(
#                                 overlay_positions, page_width, page_height
#                             )
#                             if overlay_pdf_stream:
#                                 overlay_pdf = PdfReader(overlay_pdf_stream)
#                                 overlay_page = overlay_pdf.pages[0]
#                                 page.merge_page(overlay_page)

#                         writer.add_page(page) #Add the page always
#                     else:
#                         print(f"Warning: Page number {page_data['page']} from CSV is out of range. Skipping this page.")

#                 output_filename = f"{output_base_path}_row_{row_index + 1}.pdf"
#                 with open(output_filename, "wb") as output_file:
#                     writer.write(output_file)
#     except FileNotFoundError:
#         print(f"Error: Input PDF file '{input_pdf_path}' not found.")
#     except Exception as e:
#         print(f"An error occurred during PDF processing: {e}")

# ... (rest of the code - same as before)
input_pdf_path = "sample.pdf"
csv_file_path = "New Csv Format - Sheet1.csv" 
output_base_path = "output"

# coordinates = [
#   {
#     "pageNumber": 1,
#     "x": 265,
#     "y": 176,
#     "text": "Tag 1",
#     "textSize": 16,
#     "textColor": {
#       "r": 0,
#       "g": 0,
#       "b": 0
#     }
#   },
#   {
#     "pageNumber": 2,
#     "x": 282,
#     "y": 306,
#     "text": "Tag 3",
#     "textSize": 16,
#     "textColor": {
#       "r": 0,
#       "g": 0,
#       "b": 0
#     }
#   },
#   {
#     "pageNumber": 2,
#     "x": 222,
#     "y": 195,
#     "text": "Tag 2",
#     "textSize": 16,
#     "textColor": {
#       "r": 0,
#       "g": 0,
#       "b": 0
#     }
#   },
#   {
#     "pageNumber": 10,
#     "x": 168,
#     "y": 364,
#     "text": "Tag 4",
#     "textSize": 16,
#     "textColor": {
#       "r": 0,
#       "g": 0,
#       "b": 0
#     }
#   }
# ]
try:
    with open("coordinates.json", "r") as f:
        coordinates = json.load(f)
except FileNotFoundError:
    print("Error: coordinates.json file not found.")
    exit()


# def read_csv_custom(csv_file_path):
#     text_positions_rows = []
#     with open(csv_file_path, mode='r', newline='') as csvfile:
#         csvreader = csv.reader(csvfile)
#         header = next(csvreader)  # Read the header
#         for row in csvreader:
#             pages = row[0].split(',') if row[0] else []
#             tags = row[1:]
#             for page in pages:
#                 if page:  # Ensure the page is not empty
#                     text_positions_rows.append({'page': (page), 'text': tags})
#     return text_positions_rows
# # print(coordinates)
# text_positions_rows = read_csv_custom(csv_file_path)
text_positions_rows = read_csv(csv_file_path)
# print(text_positions_rows , "csv file data")
combined_data_rows = combine_data(text_positions_rows, coordinates)
# print(combined_data_rows)
add_text_to_pdf(input_pdf_path, output_base_path, combined_data_rows)

# print("PDFs generated successfully!")