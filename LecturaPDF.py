import os
import re
from tika import parser
import pandas as pd
import shutil as sht

#path = "C:/Users/afernandez/Desktop/Prueba"
path = "C:/Users/afernandez/Documents/Procesos/CESEData/AzureBlobDownloads/2022-08-17_17-54-31"
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
        formatoIncorrecto = 0

        for line in data.split('<p>'):
            if idTipDoc == '4':
                if 'http://repse.stps.gob.mx' in line:
                    archValido = 1
                    break
            if idTipDoc == '12':
                if 'ACUSE DE RECIBO' in line.replace('\n</p>\n', '').upper():
                    archValido = 1
                    break
                elif 'DECLARACIÓN PROVISIONAL O DEFINITIVA DE IMPUESTOS FEDERALES' in line.replace('\n</p>\n', '').upper():
                    archValido = 0
                    formatoIncorrecto = 1
                    break
                elif 'RECIBO BANCARIO' in line.replace('\n</p>\n', '').upper():
                    archValido = 0
                    formatoIncorrecto = 1
                    break
            if idTipDoc == '82':
                if 'ACUSE DE RECIBO' in line.replace('\n</p>\n', '').upper():
                    archValido = 0
                    formatoIncorrecto = 1
                    break
                elif 'DECLARACIÓN PROVISIONAL O DEFINITIVA DE IMPUESTOS FEDERALES' in line.replace('\n</p>\n', '').upper():
                    archValido = 1
                    break
            
            # if idDoc == '187122':
            #     print(data)
        
        lstNoValidos.append([idDoc, archValido])
        print(idDoc + " es " + str(archValido))

        if archValido == 1:
            rfcProv = ''
            anio = ''
            mes = ''
            nombre = ''
            bandera = 0

            if idTipDoc == '4':
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
                aPaterno = ''
                aMaterno = ''

                rfc = re.findall('[A-ZÑ&]{3,4}[0-9]{6}[A-ZÑ&0-9]{3}', data)
                rfcProv = rfc[0]

                for line in data.split('<p>'):
                    
                    if 'Ejercicio:' in line:
                        ini = line.index("Ejercicio:")
                        ini += 10

                        fin = line.index("Fecha y hora de")

                        rango = slice(ini, fin)
                        anio = line.replace('\n', ' ')[rango]
                    
                    elif 'Periodicidad:' in line:
                        ini = line.replace('\n', ' ').index("declaración:")
                        ini += 12

                        fin = line.replace('\n', ' ').index("</")

                        rango = slice(ini, fin)
                        mes = line.replace('\n', ' ')[rango]

                    
                    elif 'EJERCICIO' in line and 'PERIODO' in line:
                        fila = line.split()
                        anio = fila[1]
                        mes = fila[3]

                    elif 'APELLIDO' in line:
                        fila = line.split()
                        if 'PATERNO' in line:
                            aPaterno = fila[2]
                        elif 'MATERNO' in line:
                            aMaterno = fila[2]
                    
                    elif 'NOMBRE(S)' in line:
                        ini = line.replace('\n', ' ').index("NOMBRE(S)")
                        ini += 9

                        fin = line.replace('\n', ' ').index("</")

                        rango = slice(ini, fin)
                        nombre = line.replace('\n', ' ')[rango]
                    
                    elif 'Denominación o razón' in line:
                        ini = line.replace('\n', ' ').index("social:")
                        ini += 7

                        fin = line.replace('\n', ' ').index("</")

                        rango = slice(ini, fin)
                        nombre = line.replace('\n', ' ')[rango]
                    
                    elif 'Nombre:' in line:
                        ini = line.replace('\n', ' ').index("Nombre:")
                        ini += 7

                        fin = line.replace('\n', ' ').index("</")

                        rango = slice(ini, fin)
                        nombre = line.replace('\n', ' ')[rango]

                    elif 'DENOMINACIÓN O' in line or bandera == 1:
                        if 'DENOMINACIÓN O' in line:
                            bandera = 1
                        elif bandera == 1:
                            nombre = line.replace('\n', ' ').replace('</p>', '')
                            bandera = 0

                razonSocial = nombre.strip() + ' ' + aPaterno.strip() + ' ' + aMaterno.strip() 

                lstRepse.append([idDoc, idCatOpe, idTipDoc, rfcProv + "|" + mes.upper().strip() + "|" + anio.strip() + "|" + razonSocial.upper().strip()])
                
            if idTipDoc == '12':
                rfc = re.findall('[A-ZÑ&]{3,4}[0-9]{6}[A-ZÑ&0-9]{3}', data)
                rfcProv = rfc[0]

                
                for line in data.split('<p>'):
                    if 'Denominación o razón' in line:
                        ini = line.replace('\n', ' ').index("social:")
                        ini += 7

                        fin = line.replace('\n', ' ').index("</")

                        rango = slice(ini, fin)
                        nombre = line.replace('\n', ' ')[rango]

                    elif 'Nombre:' in line:
                        ini = line.index(":")
                        ini += 1
 
                        fin = line.index("</")
 
                        rango = slice(ini, fin)
                        nombre = line.replace('\n', ' ')[rango]

                    elif  'Período de la declaración:' in line:
                        fila = line.split()
                        if 'Periodicidad:' in line:
                            mes = fila[6]
                        else:
                            mes = fila[4]

                    elif  'Tipo de declaraclón:' in line:
                        fila = line.replace('\n', ' ').split()
                        anio = fila[7]
                        anio = anio.replace('ü', '0')

                    elif  'Período de la declaracién:' in line:
                        fila = line.replace('\n', ' ').split()
                        mes = fila[4]

                    elif 'Sello díoital' in data or bandera == 1:
                        if rfcProv in line:
                            bandera = 1
                        elif bandera == 1:
                            nombre = line.replace('\n', ' ').replace('</p>', '')
                            bandera = 0

                    if 'Ejercicio:' in line:
                        ini = line.index("Ejercicio:")
                        ini += 10

                        if 'Fecha y hora de presentación:' in line:
                            fin = line.index("Fecha y hora de presentación:")
                        else:
                            fin = line.index("</")
                            
                        rango = slice(ini, fin)
                        anio = line.replace('\n', ' ')[rango]


                lstRepse.append([idDoc, idCatOpe, idTipDoc, rfcProv + "|" + mes.upper().strip() + "|" + anio.strip() + "|" + nombre.upper().strip()])


                #print(data)
                # print(rfcProv)
                # print(nombre.strip())
                # print(mes.strip())
                # print(anio.strip())
                

        elif archValido == 0:
            if not os.path.exists(pathNoValidos):
                os.makedirs(pathNoValidos)
                                
            sht.copyfile(file.path, pathNoValidos + "//" + file.name)

            if formatoIncorrecto == 1:
                lstRepse.append([idDoc, idCatOpe, idTipDoc, "Archivo No Valido|"])
            else:
                lstRepse.append([idDoc, idCatOpe, idTipDoc, "Revisar archivo a mano|"])
    
    else:
        lstRepse.append([idDoc, idCatOpe, idTipDoc, "No es PDF|"])
        


dataNoValidos = pd.DataFrame(lstNoValidos)
dataNoValidos.to_csv(path + "//ArchivosNoValidos.csv", index=False, encoding='utf-8')   

dataRepse = pd.DataFrame(lstRepse)  
dataRepse.to_csv(path + "//InformacionCarga.csv", index=False, encoding='latin1')                   
