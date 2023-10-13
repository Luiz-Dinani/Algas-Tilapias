import fitz
import io
from PIL import Image
from PIL import Image
import pytesseract
pdf_document = fitz.open('Biomassa.pdf')
page = pdf_document.load_page(6)
image_list = page.get_images(full=True)
for img_index, img in enumerate(image_list):
    xref = img[0]
    base_image = pdf_document.extract_image(xref)
    image_data = base_image["image"]
    image = Image.open(io.BytesIO(image_data))
    if img_index == 1:
        print(pytesseract.image_to_string(image))
pdf_document.close()
