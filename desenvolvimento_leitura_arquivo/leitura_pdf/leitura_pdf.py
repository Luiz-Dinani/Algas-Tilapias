import fitz
import io
from PIL import Image
import pytesseract
import pandas as pd

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
pdf_document = fitz.open('Biomassa.pdf')
page = pdf_document.load_page(6)
image_list = page.get_images(full=True)
for img_index, img in enumerate(image_list):
    xref = img[0]
    base_image = pdf_document.extract_image(xref)
    image_data = base_image["image"]
    image = Image.open(io.BytesIO(image_data))
    image.save(f'imagem{7}_{img_index}.png', 'PNG')
    if img_index == 1:
        texto_img = pytesseract.image_to_string(image)
        texto_img = texto_img.replace("(",'')
        texto_img = texto_img.replace(")",'')
        texto_img = texto_img.replace("_",'')
        texto_img = texto_img.replace(",",'.')
        texto_img = texto_img.replace("|",'')
        texto_img = texto_img.replace("/",'')
        texto_img = texto_img.replace("-",'')
        texto_img = texto_img.replace("{",'')
        texto_img = texto_img.replace("}",'')
        texto_img = texto_img.replace("]",'')
        texto_img = texto_img.replace("[",'')
        contador = 0
        texto_pd = ''
        for texto in texto_img.split('\n'):
            if texto!='':
                if contador>1:
                    if contador==2:
                        texto_pd+=f'{texto[0]}\t{texto[2:5]} a {texto[6:]}\t-\t-\n'
                    elif contador==3:
                        texto_pd+=f'{texto[0]}\t{texto[2:7]} a {texto[8:13]}\t{texto[13:16]} a {texto[18:23]}\t{texto[23:28]} a {texto[30:]}\n'
                    elif contador==4:
                        texto_pd+=f'3\t{texto[3:8]} a {texto[11:16]}\t{texto[17:21]} a {texto[24:29]}\t{texto[29:34]} a {texto[37:]}\n'
                    elif contador==5:
                        texto_pd+=f'{texto[0]}\t{texto[2:7]} a {texto[8:14]}\t{texto[15:20]} a {texto[23:28]}\t{texto[28:33]} a {texto[36:]}\n'
                    elif contador==6:
                        texto_pd+=f'{texto[1]}\t{texto[3:9]} a {texto[12:18]}\t{texto[19:24]} a {texto[27:33]}\t{texto[34:40]} a {texto[43:]}\n'
                    elif contador==7:
                        texto_pd+=f'{texto[0]}\t{texto[3:9]} a {texto[12:18]}\t{texto[20:26]} a {texto[29:35]}\t{texto[37:43]} a {texto[46:]}\n'
                    elif contador==8:
                        texto_pd+=f'{texto[1]}\t{texto[3:5]} a {texto[7:9]}kg/m³\t{texto[14:16]} a {texto[18:20]}kg/m³\t{texto[24:26]} a {texto[29:31]}kg/m³\n'
                    elif contador==9:
                        texto_pd+=f'8\t{texto[0:2]} a {texto[4:7]}kg/m³\t{texto[13:15]} a {texto[18:21]}kg/m³\t{texto[26:28]} a {texto[30:33]}kg/m³\n'
                    elif contador==10:
                        texto_pd+=f'9\t{texto[0:3]} a {texto[6:9]}kg/m³\t{texto[14:17]} a {texto[20:23]}kg/m³\t{texto[27:30]} a {texto[33:36]}kg/m³\n'
                contador+=1
        tabela_linha = ['Sistema de cultivo','Cap. de suporte (kg/ha)','Biom. Econômica (kg/ha/ciclo)', 'Densidade (px/ha)']
        tabela = pd.read_csv(io.StringIO(texto_pd), sep='\t', names=tabela_linha)
        pd_linha_nove = tabela.loc[8].values
        print('='*30)
        for i in range(len(tabela_linha)):
            print(tabela_linha[i])
            print(pd_linha_nove[i])
            print('='*30)
pdf_document.close()