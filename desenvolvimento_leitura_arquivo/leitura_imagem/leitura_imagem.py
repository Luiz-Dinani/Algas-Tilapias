# Importando o módulo Pillow (Manipulação de Imagens) para abrir a imagem no script
from PIL import Image
# Módulo para a utilização da tecnologia OCR
import pytesseract
# Extraindo o texto da imagem
print('A')
print( pytesseract.image_to_string( Image.open('teste-com-python-ocr.jpg')) )
print('F')