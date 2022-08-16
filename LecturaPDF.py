import os
import re
from tika import parser
import pandas as pd
import shutil as sht

#path = "C:/Users/afernandez/Desktop/Prueba"
path = "C:/Users/afernandez/Documents/Procesos/CESEData/AzureBlobDownloads/2022-08-16_10-48-53"
pathNoValidos = path + "/NoValidos"
#pdfFileObj = open('G:/Mi unidad/FORD_CE/Auditoria 2 - Gastos a Terceros/06 Primer Quincenal Junio/JUNIO 01/K042060-22/81016692006127 MIC.pdf', 'rb')  
flag = 1  
idDoc = ''
idCatOpe = ''
idTipDoc = '' 
lstRepse = []
lstNoValidos = []
lstRepse.append(["DOC_ID", "CAT_OPE_TIP_DOC_ID", "TIP_DOC_ID", "INFORMACION"])

for file in os.scandir(path):    
    try:
        idDoc = file.name.split('___')[0]
        idCatOpe = file.name.split('___')[1]
        idTipDoc = file.name.split('___')[2]
    except:
        continue

    if '.pdf' in file.name or '.PDF' in file.name:
        
        raw = parser.from_file(file.path, xmlContent=True)
        data = raw['content'].split('<div class="page">')[1].split('</div>')[0]
        archValido = 0

        for line in data.split('<p>'):
            if idTipDoc == '4':
                if 'AVISO DE REGISTRO' in line.replace('\n</p>\n', '').upper():
                    archValido = 1
                    break
                elif 'http://repse.stps.gob.mx' in line:
                    archValido = 1
                    break
            if idTipDoc == '12':
                if 'ACUSE DE RECIBO' in line.replace('\n</p>\n', '').upper():
                    archValido = 1
                    break
            if idTipDoc == '82':
                if 'ACUSE DE RECIBO' in line.replace('\n</p>\n', '').upper():
                    archValido = 0
                    break
                elif 'DECLARACIÓN PROVISIONAL O DEFINITIVA DE IMPUESTOS FEDERALES' in line.replace('\n</p>\n', '').upper():
                    archValido = 1
                    break
        
        lstNoValidos.append([idDoc, archValido])
        print(idDoc + " es " + str(archValido))

        if archValido == 1:
            if idTipDoc == '4':
                rfcProv = ''
                razonSocialProv = ''

                rfc = re.findall('[A-ZÑ&]{3,4}[0-9]{6}[A-ZÑ&0-9]{3}', data)
                rfcProv = rfc[0]

                if '(Moral)' in data:
                    persona = data.index("(Moral)")
                    persona += 7
                elif '(Física)' in data:
                    persona = data.index("(Física)")
                    persona += 8
                else:
                    persona = data.index("por parte de")
                    persona += 12

                if 'Con CURP' in data:
                    con = data.replace('\n', ' ').index("Con CURP")
                else:
                    con = data.replace('\n', ' ').index("con Registro Federal")
                
                rango = slice(persona, con)

                razonSocialProv = data[rango]
                razonSocialProv = razonSocialProv.replace('\n', ' ').replace(',', '').strip()

                lstRepse.append([idDoc, idCatOpe, idTipDoc, rfcProv + "|" + razonSocialProv])

        
            if idTipDoc == '82':
                rfcProv = ''

                rfc = re.findall('[A-ZÑ&]{3,4}[0-9]{6}[A-ZÑ&0-9]{3}', data)
                rfcProv = rfc[0]
                

        elif archValido == 0:
            if not os.path.exists(pathNoValidos):
                os.makedirs(pathNoValidos)
                                
            sht.copyfile(file.path, pathNoValidos + "//" + file.name)
    
    else:
        lstRepse.append([idDoc, idCatOpe, idTipDoc, "No es PDF|"])
        


dataNoValidos = pd.DataFrame(lstNoValidos)
dataNoValidos.to_csv(path + "//RepseMarzoNoValidos.csv", index=False, encoding='utf-8')   

dataRepse = pd.DataFrame(lstRepse)  
dataRepse.to_csv(path + "//RepseMarzo.csv", index=False, encoding='latin1')                   

            
        # raw = parser.from_file(file.path, xmlContent=True)
        # data = raw['content'].split('<div class="page">')[1].split('</div>')[0]
        # #print(data)

        # for line in data.split('<p>'):

        #     if 'ACUSE DE RECIBO' in line:
        #         print("DOC: ACUSE DE IVA")
        #         continue

        #     if 'Período de' in line:
        #         for char in line.replace('\n</p>\n', '').split(' '):
        #             if flag == 5:
        #                 print(char)
        #             elif flag == 7:
        #                 print(char)                    
        #             flag+=1

        #         flag=1                 
        #         continue
            
        #     if 'RFC:' in line:
        #         for char in line.replace('\n</p>\n', '').split(' '):
        #             if flag == 2:
        #                 print(char)
                    
        #             flag+=1

        #         flag=1
        #         continue
            
        #     if 'Nombre:' in line:
        #         print(line.replace('\n</p>\n', '').replace('Nombre: ', ''))
        #         continue


        
        #print(raw['metadata'])
        # pdfFileObj = open(file.path, 'rb') 
        # pdfReader = PyPDF2.PdfFileReader(pdfFileObj, stream=True)      
        # pageObj = pdfReader.getPage(0)  
        # extracted_text = sl.PDF(pdfReader)
        # print(extracted_text)      
        #pdfFileObj.close()  