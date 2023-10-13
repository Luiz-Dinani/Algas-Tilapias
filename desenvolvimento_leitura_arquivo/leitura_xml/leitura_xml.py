from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import xml.etree.ElementTree as ET

# Converter o PDF em imagens
pages = convert_from_path('Analise de caso.pdf', 500)  # 500 DPI (ajuste conforme necessário)

xml_root = ET.Element("pdf_data")  # Crie o elemento raiz XML

for i, page in enumerate(pages):
    # Extrair texto da imagem usando pytesseract
    text = pytesseract.image_to_string(page, lang='pt-br')  # Use o idioma apropriado

    # Crie um elemento para a página atual
    page_element = ET.SubElement(xml_root, f"page_{i+1}")
    page_element.text = text

# Crie o arquivo XML a partir do elemento raiz
xml_tree = ET.ElementTree(xml_root)

# Salve o arquivo XML
xml_tree.write('output.xml')

print("PDF convertido para XML com sucesso!")
