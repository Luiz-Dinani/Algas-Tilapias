import PyPDF2

# Abra o arquivo PDF em modo de leitura binária
pdf_file = open('Analise de caso.pdf', 'rb')

# Crie um objeto PyPDF2.PdfReader para ler o arquivo PDF
pdf_reader = PyPDF2.PdfReader(pdf_file)

# Obtenha o número de páginas no arquivo PDF
num_pages = len(pdf_reader.pages)

# Loop através de todas as páginas e imprima o conteúdo de cada página
for page_num in range(num_pages):
    page = pdf_reader.pages[page_num]
    page_text = page.extract_text()
    print(page_text)

# Feche o arquivo PDF após a leitura
pdf_file.close()
