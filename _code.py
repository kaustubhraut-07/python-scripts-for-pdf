# # import pdfplumber
# # from reportlab.pdfgen import canvas
# # from reportlab.lib.pagesizes import letter
# # from pypdf import PdfWriter, PdfReader
# # import io
# # import json
# # from reportlab.lib.colors import white,black
# # from reportlab.lib.units import inch
# # from reportlab.lib.pagesizes import A4

# # from reportlab.pdfbase import pdfmetrics




# # def create_overlay_pdf(text_positions, page_width, page_height):
# #     """
# #     Create an overlay PDF with text at specified positions.
# #     :param text_positions: List of dictionaries with 'x', 'y', 'text'.
# #     :param page_width: Width of the page.
# #     :param page_height: Height of the page.
# #     :return: BytesIO object of the overlay PDF.
# #     """
# #     packet = io.BytesIO()
# #     can = canvas.Canvas(packet, pagesize=(A4)) # we can pass a4 size direclt here so that pdf will came propely
# #     can.setFillColor(white)

# #     for item in text_positions:
# #         x, y, text = item['x'], item['y'], item['text']

# #         # Invert y-coordinate to align with PDF coordinate system
# #         inverted_y = page_height - y

# #         # Calculate text width to handle overflow
# #         text_width = can.stringWidth(text, 'Helvetica', 12)

# #         # Adjust x if text overflows the right edge
# #         if x + text_width > A4[0]:
# #             print(f"Warning: Adjusting text '{text}' at ({x}, {y}) to fit page width.")
# #             x = A4[0] - text_width

# #         # Adjust y if text overflows the bottom edge
# #         if inverted_y < 0:
# #             print(f"Warning: Adjusting text '{text}' at ({x}, {y}) to fit page height.")
# #             inverted_y = 0

# #         # Draw the string on the canvas
# #         can.drawString(x, inverted_y -7 , text)
# #         print(f"Placing text '{text}' at ({x}, {inverted_y}) on page with dimensions ({A4[0]}, {A4[1]})")

# #     can.save()
# #     packet.seek(0)
# #     return packet





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
# #         page_number = item['page'] - 1  # Convert to 0-based index
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

# # # input_pdf_path = "sample.pdf"
# # # input_pdf_path = "dummy_10_pages.pdf"
# # input_pdf_path = "A4size_House-Warming-Invitation-Card.pdf"
# # # input_pdf_path = "House-Warming-Invitation-Card (1).pdf"

# # output_pdf_path = "1_test_output.pdf"

# # # JSON input from the frontend
# # json_input = '''
# # [
# #     {"page": 1, "x": 101, "y": 46, "text": "Test 1234"},

# #     {"page": 1, "x": 99, "y": 95, "text": "Test 1234"},
# #     {"page": 1, "x": 542.27, "y": 2, "text": "Test 1234"},
# #       {"page": 1, "x": 245.26999999999998, "y": 349, "text": "Test 1234"},
# #         {"page": 1, "x": 3, "y": 3, "text": "Test 1234"},
# #           {"page": 1, "x": 1, "y": 834.89, "text": "Test 1234"}, 
# #           {"page": 1, "x": 542.27, "y": 835, "text": "Test 1234"}
# # ]
# # '''

# # #   {"page": 1, "x": 1, "y": 834.89, "text": "Test 1234"},   for this added 20 as the height of input box in frontedn
# # #    {"page": 1, "x": 300, "y": 700, "text": "Test 6789"},
# # #     {"page": 2, "x": 150, "y": 600, "text": "Another Text"},
# # #     {"page": 8, "x": 200, "y": 500, "text": "Test 9999"}
# # text_positions = json.loads(json_input)

# # add_text_to_pdf(input_pdf_path, output_pdf_path, text_positions)









# # import pdfplumber
# # from reportlab.pdfgen import canvas
# # from reportlab.lib.pagesizes import letter, A4
# # from pypdf import PdfWriter, PdfReader
# # import io
# # import json
# # import csv
# # import os
# # from reportlab.lib.colors import white, black
# # from reportlab.lib.units import inch

# # def create_overlay_pdf(text_positions, page_width, page_height):
# #     """
# #     Create an overlay PDF with text at specified positions.
# #     :param text_positions: List of dictionaries with 'x', 'y', 'text'.
# #     :param page_width: Width of the page.
# #     :param page_height: Height of the page.
# #     :return: BytesIO object of the overlay PDF.
# #     """
# #     packet = io.BytesIO()
# #     can = canvas.Canvas(packet, pagesize=(A4)) # we can pass a4 size direclt here so that pdf will came propely
# #     can.setFillColor(white)

# #     for item in text_positions:
# #         x, y, text = item['x'], item['y'], item['text']

# #         # Invert y-coordinate to align with PDF coordinate system
# #         inverted_y = page_height - y

# #         # Calculate text width to handle overflow
# #         text_width = can.stringWidth(text, 'Helvetica', 12)

# #         # Adjust x if text overflows the right edge
# #         if x + text_width > A4[0]:
# #             print(f"Warning: Adjusting text '{text}' at ({x}, {y}) to fit page width.")
# #             x = A4[0] - text_width

# #         # Adjust y if text overflows the bottom edge
# #         if inverted_y < 0:
# #             print(f"Warning: Adjusting text '{text}' at ({x}, {y}) to fit page height.")
# #             inverted_y = 0

# #         # Draw the string on the canvas
# #         can.drawString(x, inverted_y -7 , text)
# #         print(f"Placing text '{text}' at ({x}, {inverted_y}) on page with dimensions ({A4[0]}, {A4[1]})")

# #     can.save()
# #     packet.seek(0)
# #     return packet

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
# #         page_number = item['page'] - 1  # Convert to 0-based index
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
# #             print(page_width, page_height)
            
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



# # def create_subset_pdf(input_pdf, pages_to_include):
# #     reader = PdfReader(input_pdf)
# #     writer = PdfWriter()
# #     for page_number in pages_to_include:
# #         if 1 <= page_number <= len(reader.pages):
# #             writer.add_page(reader.pages[page_number - 1])
# #     subset_pdf_path = io.BytesIO()
# #     writer.write(subset_pdf_path)
# #     subset_pdf_path.seek(0)
# #     return subset_pdf_path


# # def parse_page_numbers(pages_str):
# #     """Parse page numbers from string like "1,2,3" """
# #     if not pages_str or pages_str.strip() == '':
# #         return []
# #     return [int(p.strip()) for p in pages_str.split(',') if p.strip().isdigit()]

# # def main():
# #     # Configuration
# #     csv_file_path = "New Csv Format - Sheet1.csv"
# #     # pdf_input_path = ".pdf"
# #     # # input_pdf_path = "sample.pdf"
# # # # input_pdf_path = "dummy_10_pages.pdf"
# # # input_pdf_path = "A4size_House-Warming-Invitation-Card.pdf"
# #     # pdf_input_path = "House-Warming-Invitation-Card (1).pdf"
# #     pdf_input_path = "c"

# # # output_pdf_path = "1_test_output.pdf"
# #     output_directory = "output_files"

# #     # Ensure output directory exists
# #     os.makedirs(output_directory, exist_ok=True)

# #     # Read tag positions from JSON
# #     json_data = [
# #         {"pageNumber": 1, "x": 101, "y": 46, "text": "Tag 1"},
# #         # Add more tag positions as needed
# #     ]

# #     # Read the CSV file
# #     rows = []
# #     with open(csv_file_path, 'r') as csv_file:
# #         csv_reader = csv.DictReader(csv_file)
# #         for row in csv_reader:
# #             rows.append(row)


# #     for idx, row in enumerate(rows):
# #         cleaned_row = {key.strip(): value for key, value in row.items()}
# #         print(cleaned_row, "cleaned row")
# #         pages = cleaned_row.get('Pages', '')
# #         if pages:
# #             pages_to_include = [int(page.strip()) for page in pages.split(',') if page.strip().isdigit()]
# #         else:
# #             with pdfplumber.open(pdf_input_path) as pdf:
# #                 pages_to_include = list(range(1, len(pdf.pages) + 1))

# #         subset_pdf = create_subset_pdf(pdf_input_path, pages_to_include)
# #         filtered_tags = [tag.copy() for tag in json_data if tag["pageNumber"] in pages_to_include]
# #         # print(filtered_tags, "filtered tags")
# #         for tag in filtered_tags:
# #             tag_text = tag["text"]
# #             tag["text"] = cleaned_row.get(tag_text, "")

# #         print(filtered_tags, "filtered tags")
# #     # Process each row in the CSV
# #     for i, row in enumerate(rows, 1):
# #         # Get pages to include from the Pages column
# #         pages_to_include = parse_page_numbers(row.get('Pages', ''))
        
# #         # Create text positions for this row
# #         text_positions = []
# #         for pos in json_data:
# #             tag_name = pos['text']
# #             if tag_name in row and row[tag_name].strip():
# #                 text_positions.append({
# #                     'page': pos['pageNumber'],
# #                     'x': pos['x'],
# #                     'y': pos['y'],
# #                     'text': row[tag_name].strip()
# #                 })

# #         # Generate output filename
# #         output_pdf_path = os.path.join(output_directory, f'output_{i}.pdf')
        
# #         try:
# #             # Process the PDF with the current text positions
# #             add_text_to_pdf(subset_pdf, output_pdf_path, filtered_tags)
# #             print(f"Successfully processed PDF {i}: {output_pdf_path}")
# #         except Exception as e:
# #             print(f"Error processing PDF {i}: {str(e)}")

# # if __name__ == "__main__":
# #     main()








# import pdfplumber
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4
# from pypdf import PdfWriter, PdfReader
# import io
# import csv
# import os


# def create_overlay_pdf(text_positions, page_width, page_height):
#     """
#     Create an overlay PDF with text at specified positions.
#     :param text_positions: List of dictionaries with 'x', 'y', 'text'.
#     :param page_width: Width of the page.
#     :param page_height: Height of the page.
#     :return: BytesIO object of the overlay PDF.
#     """
#     packet = io.BytesIO()
#     can = canvas.Canvas(packet, pagesize=A4)

#     for item in text_positions:
#         x, y, text = item['x'], item['y'], item['text']

#         # Invert y-coordinate to align with PDF coordinate system
#         inverted_y = page_height - y

#         # Calculate text width to handle overflow
#         text_width = can.stringWidth(text, 'Helvetica', 12)

#         # Adjust x if text overflows the right edge
#         if x + text_width > A4[0]:
#             print(f"Warning: Adjusting text '{text}' at ({x}, {y}) to fit page width.")
#             x = A4[0] - text_width

#         # Adjust y if text overflows the bottom edge
#         if inverted_y < 0:
#             print(f"Warning: Adjusting text '{text}' at ({x}, {y}) to fit page height.")
#             inverted_y = 0

#         # Draw the string on the canvas
#         can.drawString(x, inverted_y - 7, text)
#         print(f"Placing text '{text}' at ({x}, {inverted_y}) on page with dimensions ({A4[0]}, {A4[1]})")

#     can.save()
#     packet.seek(0)
#     return packet


# def add_text_to_pdf(input_pdf_stream, output_pdf_path, text_positions):
#     """
#     Add text to specific positions in a PDF using pdfplumber, reportlab, and pypdf.
#     :param input_pdf_stream: Input PDF as a BytesIO stream.
#     :param output_pdf_path: Path to save the output PDF file.
#     :param text_positions: List of dictionaries with 'page', 'x', 'y', 'text'.
#     """
#     reader = PdfReader(input_pdf_stream)
#     writer = PdfWriter()

#     # Group positions by page for easy processing
#     grouped_positions = {}
#     for item in text_positions:
#         page_number = item['page'] - 1  # Convert to 0-based index
#         if page_number not in grouped_positions:
#             grouped_positions[page_number] = []
#         grouped_positions[page_number].append(item)

#     with pdfplumber.open(input_pdf_stream) as pdf:
#         for page_number in range(len(reader.pages)):
#             page = reader.pages[page_number]
#             pdf_page = pdf.pages[page_number]  # Get page size from pdfplumber

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


# def create_subset_pdf(input_pdf, pages_to_include):
#     """
#     Create a subset PDF containing only specified pages.
#     :param input_pdf: Path to the input PDF file.
#     :param pages_to_include: List of page numbers to include.
#     :return: BytesIO object of the subset PDF.
#     """
#     reader = PdfReader(input_pdf)
#     writer = PdfWriter()
#     for page_number in pages_to_include:
#         if 1 <= page_number <= len(reader.pages):
#             writer.add_page(reader.pages[page_number - 1])
#     subset_pdf_path = io.BytesIO()
#     writer.write(subset_pdf_path)
#     subset_pdf_path.seek(0)
#     return subset_pdf_path


# def parse_page_numbers(pages_str):
#     """
#     Parse page numbers from a string like "1,2,3".
#     :param pages_str: Comma-separated string of page numbers.
#     :return: List of integers.
#     """
#     if not pages_str or pages_str.strip() == '':
#         return []
#     return [int(p.strip()) for p in pages_str.split(',') if p.strip().isdigit()]


# def main():
#     # Configuration
#     csv_file_path = "New Csv Format - Sheet1.csv"
#     pdf_input_path = "A4size_House-Warming-Invitation-Card.pdf"
#     output_directory = "output_files"

#     # Ensure output directory exists
#     os.makedirs(output_directory, exist_ok=True)

#     # Read tag positions from JSON (hardcoded example for now)
#     json_data = [
#         {"pageNumber": 1, "x": 101, "y": 46, "text": "Tag 1"},
#         {"pageNumber": 2, "x": 50, "y": 100, "text": "Tag 2"},
#     ]

#     # Read the CSV file
#     rows = []
#     with open(csv_file_path, 'r') as csv_file:
#         csv_reader = csv.DictReader(csv_file)
#         for row in csv_reader:
#             rows.append(row)

#     # Process each row in the CSV
#     for i, row in enumerate(rows, 1):
#         # Get pages to include from the Pages column
#         pages_to_include = parse_page_numbers(row.get('Pages', ''))

#         # Create a subset PDF with selected pages
#         subset_pdf = create_subset_pdf(pdf_input_path, pages_to_include)

#         # Filter and map text positions for the current row
#         text_positions = []
#         for pos in json_data:
#             tag_name = pos['text']
#             if tag_name in row and row[tag_name].strip():
#                 text_positions.append({
#                     'page': pos['pageNumber'],
#                     'x': pos['x'],
#                     'y': pos['y'],
#                     'text': row[tag_name].strip()
#                 })

#         # Generate output filename
#         output_pdf_path = os.path.join(output_directory, f'output_{i}.pdf')

#         try:
#             # Add text to the PDF
#             add_text_to_pdf(subset_pdf, output_pdf_path, text_positions)
#             print(f"Successfully processed PDF {i}: {output_pdf_path}")
#         except Exception as e:
#             print(f"Error processing PDF {i}: {str(e)}")


# if __name__ == "__main__":
#     main()




# import pdfplumber
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter, A4
# from reportlab.lib.colors import white, black
# from reportlab.lib.units import inch
# from pypdf import PdfWriter, PdfReader
# import io
# import json
# import csv
# from typing import List, Dict

# def read_csv_config(csv_path: str) -> List[Dict]:
#     """
#     Read CSV file and convert it to a list of dictionaries with page numbers and tag values.
#     """
#     config_data = []
#     with open(csv_path, 'r') as file:
#         csv_reader = csv.DictReader(file)
#         for row in csv_reader:
#             print(row, "row")
#             # Handle the Pages column
#             pages = []
#             if row['Pages ']:
#                 pages = [int(p.strip()) for p in row['Pages '].strip('"').split(',')]
            
#             config_item = {
#                 'pages': pages,
#                 'tags': {}
#             }
            
#             # Add all non-empty tag values
#             for key, value in row.items():
#                 if key != 'Pages' and value:
#                     config_item['tags'][key] = value
            
#             config_data.append(config_item)
    
#     return config_data

# def create_overlay_pdf(text_positions, page_width, page_height):
#     """
#     Create an overlay PDF with text at specified positions.
#     """
#     packet = io.BytesIO()
#     can = canvas.Canvas(packet, pagesize=A4)
#     can.setFillColor(white)

#     for item in text_positions:
#         x, y, text = item['x'], item['y'], item['text']
#         inverted_y = page_height - y

#         text_width = can.stringWidth(text, 'Helvetica', 12)

#         # Adjust positions if needed
#         if x + text_width > A4[0]:
#             x = A4[0] - text_width
#         if inverted_y < 0:
#             inverted_y = 0

#         can.drawString(x, inverted_y - 7, text)

#     can.save()
#     packet.seek(0)
#     return packet

# def process_pdf_with_tags(input_pdf_path: str, output_pdf_path: str, 
#                          tag_positions: List[Dict], csv_config: List[Dict]):
#     """
#     Process PDF with text placement based on CSV configuration and tag positions.
    
#     :param input_pdf_path: Path to input PDF
#     :param output_pdf_path: Path for output PDF
#     :param tag_positions: List of dictionaries containing position data for each tag
#     :param csv_config: List of dictionaries containing CSV configuration data
#     """
#     reader = PdfReader(input_pdf_path)
#     writer = PdfWriter()
#     total_pages = len(reader.pages)
    
#     # Create a mapping of tag names to their positions
#     tag_pos_map = {}
#     for pos in tag_positions:
#         # Assuming the 'text' field contains the tag name (e.g., "Tag 1")
#         tag_pos_map[pos['text']] = {'x': pos['x'], 'y': pos['y']}
    
#     # Process each page
#     with pdfplumber.open(input_pdf_path) as pdf:
#         for page_num in range(total_pages):
#             current_page = page_num + 1
#             page = reader.pages[page_num]
#             pdf_page = pdf.pages[page_num]
            
#             # Collect all text positions for this page
#             page_text_positions = []
            
#             # Go through each configuration item
#             for config in csv_config:
#                 # If pages list is empty or current page is in pages list
#                 if not config['pages'] or current_page in config['pages']:
#                     # Process each tag in the configuration
#                     for tag_name, tag_value in config['tags'].items():
#                         if tag_name in tag_pos_map:
#                             position = tag_pos_map[tag_name]
#                             page_text_positions.append({
#                                 'x': position['x'],
#                                 'y': position['y'],
#                                 'text': tag_value
#                             })
            
#             # If we have text to add to this page
#             if page_text_positions:
#                 # Create and merge overlay
#                 overlay_pdf_stream = create_overlay_pdf(
#                     page_text_positions,
#                     pdf_page.width,
#                     pdf_page.height
#                 )
#                 overlay_pdf = PdfReader(overlay_pdf_stream)
#                 overlay_page = overlay_pdf.pages[0]
#                 page.merge_page(overlay_page)
            
#             writer.add_page(page)
    
#     # Save the final PDF
#     with open(output_pdf_path, "wb") as output_file:
#         writer.write(output_file)

# # Example usage
# def main():
#     input_pdf_path = "A4size_House-Warming-Invitation-Card.pdf"
#     output_pdf_path = "2_test_output.pdf"
#     csv_path = "New Csv Format - Sheet1.csv"
    
#     # Tag positions (this would typically come from your JSON input)
#     tag_positions = [
#         {"page": 1, "x": 101, "y": 46, "text": "Tag 1"},
#         {"page": 1, "x": 99, "y": 95, "text": "Tag 2"},
#         {"page": 1, "x": 542.27, "y": 2, "text": "Tag 3"},
#         {"page": 1, "x": 245.27, "y": 349, "text": "Tag 1"},
#         {"page": 1, "x": 3, "y": 3, "text": "Tag 1"},
#          {"page": 1, "x": 1, "y": 834.89, "text": "Tag 1"},
#                   {"page": 1, "x": 542.27, "y": 835, "text": "Tag 1"},
#     ]
    
#     # Read CSV configuration
#     csv_config = read_csv_config(csv_path)
    
#     # Process the PDF
#     process_pdf_with_tags(input_pdf_path, output_pdf_path, tag_positions, csv_config)

# if __name__ == "__main__":
#     main()




















    

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
from reportlab.lib.pagesizes import A4

json_data = [
    # {"pageNumber": 1, "x": 244.17864999999995, "y": 349, "text": "Tag 1"},  
    {"pageNumber": 1, "x": 101, "y": 46, "text": "Tag 1"},
        {"pageNumber": 1, "x": 99, "y": 95, "text": "Tag 2"},
        {"pageNumber": 1, "x": 542.27, "y": 2, "text": "Tag 3"},
        {"pageNumber": 1, "x": 245.27, "y": 349, "text": "Tag 1"},
        {"pageNumber": 1, "x": 3, "y": 3, "text": "Tag 1"},
         {"pageNumber": 1, "x": 1, "y": 834.89, "text": "Tag 1"},
                  {"pageNumber": 1, "x": 542.27, "y": 835, "text": "Tag 1"},
]
csv_file_path = "New Csv Format - Sheet1.csv"
# pdf_input_path = "House-Warming-Invitation-Card (1).pdf" 
# pdf_input_path = "A4size_House-Warming-Invitation-Card.pdf" 
pdf_input_path = "sample.pdf"  
# pdf_input_path = "dummy_10_pages.pdf"
output_directory = "output_files"
os.makedirs(output_directory, exist_ok=True)

rows = []
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        rows.append(row)

# def normalize_coordinates(x_scaled, y_scaled, scaled_width, scaled_height, original_width, original_height, standard_width=800, standard_height=600):
#     x_standard = (x_scaled / scaled_width) * standard_width
#     y_standard = (y_scaled / scaled_height) * standard_height
#     x_original = (x_standard / standard_width) * original_width
#     y_original = (y_standard / standard_height) * original_height
#     return x_original, y_original

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
    """
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    can.setFillColor(black)

    for item in text_positions:
        x, y, text = item['x'], item['y'], item['text']
        inverted_y = page_height - y

        text_width = can.stringWidth(text, 'Helvetica', 12)

        # Adjust positions if needed
        if x + text_width > A4[0]:
            x = A4[0] - text_width
        if inverted_y < 0:
            inverted_y = 0

        can.drawString(x, inverted_y - 7, text)

    can.save()
    packet.seek(0)
    return packet

def add_text_to_pdf(input_pdf_stream, output_pdf_path, text_positions):
    """
    Add text to specific positions in a PDF using pdfplumber, reportlab, and pypdf.
    :param input_pdf_stream: Input PDF as a BytesIO stream.
    :param output_pdf_path: Path to save the output PDF file.
    :param text_positions: List of dictionaries with 'page', 'x', 'y', 'text'.
    """
    reader = PdfReader(input_pdf_stream)
    writer = PdfWriter()

    # Group positions by page for easy processing
    grouped_positions = {}
    for item in text_positions:
        page_number = item['pageNumber'] - 1  # Convert to 0-based index
        if page_number not in grouped_positions:
            grouped_positions[page_number] = []
        grouped_positions[page_number].append(item)

    with pdfplumber.open(input_pdf_stream) as pdf:
        for page_number in range(len(reader.pages)):
            page = reader.pages[page_number]
            pdf_page = pdf.pages[page_number]  # Get page size from pdfplumber

            page_width = pdf_page.width
            page_height = pdf_page.height
            # page_width = 595.2755905511812
            # page_height = 841.8897637795277

            if page_number in grouped_positions:
                # Create overlay with reportlab
                overlay_pdf_stream = create_overlay_pdf(
                    grouped_positions[page_number], page_width, page_height
                )
                overlay_pdf = PdfReader(overlay_pdf_stream)
                overlay_page = overlay_pdf.pages[0]

                # Merge overlay with original page
                page.merge_page(overlay_page)

            # Add the updated page to the writer
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

    scaled_width =   595.2755905511812
    scaled_height =  841.8897637795277
    print(filtered_tags, "filtered tags")
    output_pdf_path = os.path.join(output_directory, f"output_file_{idx + 1}.pdf")
    add_text_to_pdf(subset_pdf, output_pdf_path, filtered_tags)  # Pass scaled dimensions

print(f"Tagged PDFs saved in directory: {output_directory}")