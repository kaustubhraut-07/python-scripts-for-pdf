import fitz  
from PIL import Image, ImageDraw, ImageFont
import io
import json

def add_text_to_pdf(input_pdf_path, output_pdf_path, text_positions):
    """
    Add text to specific positions in a PDF by rendering the page as an image, adding text, and saving back to PDF.
    :param input_pdf_path: Path to the input PDF file.
    :param output_pdf_path: Path to save the output PDF file.
    :param text_positions: List of dictionaries with 'page', 'x', 'y', 'text'.
    """
    pdf_document = fitz.open(input_pdf_path)
    output_pdf = fitz.open()

    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        pix = page.get_pixmap()  # Render page to image

        # Convert to PIL image
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Add overlay text
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", 40)  

        for item in text_positions:
            if item["page"] - 1 == page_number:  # Check if the text is for the current page
                draw.text((item["x"], item["y"]), item["text"], fill="white", font=font)

        # Convert back to PDF
        image_stream = io.BytesIO()
        image.save(image_stream, format="PDF")
        image_stream.seek(0)
        page_pdf = fitz.open(stream=image_stream, filetype="pdf")
        output_pdf.insert_pdf(page_pdf)

    output_pdf.save(output_pdf_path)
    pdf_document.close()
    output_pdf.close()

# Example usage
input_pdf_path = "House-Warming-Invitation-Card (1).pdf"
output_pdf_path = "outputhousewarming_fixed.pdf"

json_input = '''
[
    {"page": 1, "x": 241, "y": 125, "text": "Test 1234"}
]
'''
text_positions = json.loads(json_input)

add_text_to_pdf(input_pdf_path, output_pdf_path, text_positions)
print(f"PDF with text annotations saved as {output_pdf_path}")
