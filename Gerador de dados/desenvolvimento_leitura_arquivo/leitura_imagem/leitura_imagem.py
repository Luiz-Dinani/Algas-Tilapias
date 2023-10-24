from PIL import Image
import pytesseract
import pandas as pd
import io

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
image = Image.open('imagem3_0.png')
text = pytesseract.image_to_string(image)
vetor_texto = text.split('\n')
vetor_texto_sem_espaco = []
for texto in vetor_texto:
    if texto!='':
        vetor_texto_sem_espaco.append(texto)
for i in range(len(vetor_texto_sem_espaco)):
    if i==0 or i==11:
        vetor_texto_sem_espaco[i]='Morte'
    elif i==1:
        vetor_texto_sem_espaco[i]=f'Acima de {vetor_texto_sem_espaco[i]}C'
    elif i==2:
        vetor_texto_sem_espaco[i]=f'Redução de apetite e baixa resistência ao manejo e às doenças'
    elif i==3:
        vetor_texto_sem_espaco[i]=f''
    elif i==4:
        vetor_texto_sem_espaco[i]=f'Entre 32° a 38°C'
    elif i==5:
        vetor_texto_sem_espaco[i]=f'Conforto'
    elif i==6:
        vetor_texto_sem_espaco[i]=f'Entre 27° a 32°C'
    elif i==7:
        vetor_texto_sem_espaco[i]=f'Consumo de alimerto reduzido e crescimento lento'
    elif i==8:
        vetor_texto_sem_espaco[i]=f'Entre 20° a 27°C'
    elif i==9:
        vetor_texto_sem_espaco[i]=f'Crescimento lento, baixa tolerância ao manuseio e às doenças '
    elif i==10:
        vetor_texto_sem_espaco[i]=f'Entre 14° a 20°C'
        vetor_texto_sem_espaco.append(f'Abaixo de 14°C')
vetor_texto_final = []
for i in range(len(vetor_texto_sem_espaco)):
    texto = vetor_texto_sem_espaco[i]
    if texto != '':
        vetor_texto_final.append(texto)
txt_pd = ''
for i in range(len(vetor_texto_final)):
    if i%2==0:
        txt_pd+=f'{vetor_texto_final[i]}\t{vetor_texto_final[i+1]}\n'
txt_headers = ['Consequencia', 'Clima']
tabela = pd.read_csv(io.StringIO(txt_pd), sep='\t', names=txt_headers)
tabela.to_csv('tabela_temperatura.csv', index=False, encoding='UTF-8', sep=';')