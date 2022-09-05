import os
from posixpath import dirname
import re
from tika import parser
import pandas as pd
import shutil as sht
from unrar import rarfile
import zipfile
import py7zr
from Extracinfo import Extracinfo
from operator import is_not
from functools import partial
#import time

#path = "C:/Users/afernandez/Desktop/Prueba/Especial"
path = "C:/Users/afernandez/Documents/Procesos/CESEData/AzureBlobDownloads/2022-09-05_10-50-35"
#path = "C:/Zips/2022-09-02_15-33-57"
pathNoValidos = path + "/NoValidos"
#pdfFileObj = open('G:/Mi unidad/FORD_CE/Auditoria 2 - Gastos a Terceros/06 Primer Quincenal Junio/JUNIO 01/K042060-22/81016692006127 MIC.pdf', 'rb')  
flag = 1  
idDoc = ''
idCatOpe = ''
idTipDoc = '' 
lstRepse = []
lstNoValidos = []
lectura = list()
lstRepse.append(["DOC_ID", "CAT_OPE_TIP_DOC_ID", "TIP_DOC_ID", "INFORMACION"])

def unCompressZip(archivo):
    zf = zipfile.ZipFile(archivo)
    carpeta = archivo.replace('.zip', '')
    zf.extractall(carpeta)
    zf.close()

def unCompressRar(archivo):
    rf = rarfile.RarFile(archivo)
    carpeta = archivo.replace('.rar', '')
    rf.extractall(carpeta)

def unCompress7z(archivo):    
    sf = py7zr.SevenZipFile(archivo)
    carpeta = archivo.replace('.7z', '')
    sf.extractall(carpeta)

def getListOfFiles(dirName):
    global lista_pdf
    global lista_xml
    global idDoc
    global idCatOpe
    global idTipDoc
    global lectura

    listOfFile = os.listdir(dirName)
    allFiles = list()
    final = []
    val = ''
    #print(dirName)

    for entry in listOfFile: 
        if '.pdf' in entry.lower():
            lista_pdf.append(entry)
        elif '.xml' in entry.lower():
            lista_xml.append(entry)           
    
        fullPath = os.path.join(dirName, entry)

        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        # elif entry.endswith('.rar'):
        #     unCompressRar(fullPath)
        # elif entry.endswith('.zip'):
        #     unCompressZip(fullPath)
        # elif entry.endswith('.7z'):
        #     unCompress7z(fullPath)
        else:
            allFiles.append(fullPath)
            if entry.endswith('.xml') or entry.endswith('.XML'): 
                #print('Reading....'+ entry)
                xmldoc = open(fullPath,encoding="utf8")
                val = Extracinfo.xml_read(xmldoc)
                lectura.append([idDoc, idCatOpe, idTipDoc, val])

    # print(len(lista_pdf))
    # print(len(lista_xml))

    if len(lista_pdf) > 0 and len(lista_xml) == 0:
        final.append([idDoc, idCatOpe, idTipDoc, "SOLO PDF'S|"])
    # elif len(lista_pdf) == 0 and len(lista_xml) > 0:
    #     final.append([idDoc, idCatOpe, idTipDoc, "SOLO XML'S|"])
    elif len(lista_pdf) == 0 and len(lista_xml) == 0:
        final.append([idDoc, idCatOpe, idTipDoc, "Revisar a mano|"])
    else:
        final = lectura

    return final


for file in os.scandir(path):    
    try:
        idDoc = file.name.split('___')[0]
        idCatOpe = file.name.split('___')[1]
        idTipDoc = file.name.split('___')[2]
    except:
        continue

    if '.pdf' in file.name or '.PDF' in file.name:
        
        raw = parser.from_file(file.path, xmlContent=True)
        try:
            data = raw['content'].split('<div class="page">')[1].split('</div>')[0]
        except:
            lstNoValidos.append([idDoc, archValido])
            print(idDoc + " es " + str(archValido))
            lstRepse.append([idDoc, idCatOpe, idTipDoc, "Revisar archivo a mano|"])
            sht.copyfile(file.path, pathNoValidos + "//" + file.name)
            continue

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
            #print(data)
        
        lstNoValidos.append([idDoc, archValido])
        print(idDoc + " es " + str(archValido))

        if archValido == 1:
            rfcProv = ''
            anio = ''
            mes = ''
            nombre = ''
            bandera = 0
            band = 0

            if idTipDoc == '4':
                razonSocialProv = ''

                rfc = re.findall('[A-ZÑ&]{3,4}[0-9]{6}[A-ZÑ&0-9]{3}', data.replace('&amp;', '&'))
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

                try:
                    rfc = re.findall('[A-ZÑ&]{3,4}[0-9]{6}[A-ZÑ&0-9]{3}', data.replace('&amp;', '&'))
                    rfcProv = rfc[0]
                except:
                    lstRepse.append([idDoc, idCatOpe, idTipDoc, "Archivo No Valido|"])
                    continue

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

                    
                    elif 'EJERCICIO' in line and 'PERIODO' in line and len(line.split()) > 3:
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
                    elif 'NÚMERO DE' in line:
                        bandera = 2
                        band = 1
                    elif bandera == 2:
                        bandera -= 1
                    elif 'DENOMINACIÓN O' in line:
                        bandera = 1
                    elif bandera == 1 and band == 0:
                        nombre = line.replace('\n', ' ').replace('</p>', '')
                        bandera = 0
                    elif bandera == 1 and band == 1 and len(mes) == 0 and len(anio) == 0:
                        fila = line.split()
                        anio = fila[1]
                        mes = fila[0]
                        bandera = 0
                        band = 0

                razonSocial = nombre.strip() + ' ' + aPaterno.strip() + ' ' + aMaterno.strip() 

                lstRepse.append([idDoc, idCatOpe, idTipDoc, rfcProv + "|" + mes.upper().strip() + "|" + anio.strip() + "|" + razonSocial.upper().strip()])
                
            if idTipDoc == '12':
                try:
                    rfc = re.findall('[A-ZÑ&]{3,4}[0-9]{6}[A-ZÑ&0-9]{3}', data.replace('&amp;', '&'))
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
                except:
                    lstRepse.append([idDoc, idCatOpe, idTipDoc, "Revisar archivo a mano|"])
                    sht.copyfile(file.path, pathNoValidos + "//" + file.name)
                    continue

                lstRepse.append([idDoc, idCatOpe, idTipDoc, rfcProv + "|" + mes.upper().strip() + "|" + anio.strip() + "|" + nombre.upper().strip()])


                #print(data)
            # print(rfcProv)
            # print(nombre.strip())
            # print(mes.strip())
            # print(anio.strip())
                

        elif archValido == 0:
            if not os.path.exists(pathNoValidos):
                os.makedirs(pathNoValidos)
                                
            

            if formatoIncorrecto == 1:
                lstRepse.append([idDoc, idCatOpe, idTipDoc, "Archivo No Valido|"])
            else:
                lstRepse.append([idDoc, idCatOpe, idTipDoc, "Revisar archivo a mano|"])
                sht.copyfile(file.path, pathNoValidos + "//" + file.name)
    
    elif '.zip' in file.name or '.rar' in file.name or '.7z' in file.name:
        if idTipDoc == '8':
            archValido = 1
        else:            
            archValido = 0

        if archValido == 1:
            dirName = ''

            if '.zip' in file.name:
                unCompressZip(file.path)
                dirName = file.path.replace('.zip', '')
                #time.sleep(5)
            elif '.rar' in file.name:
                unCompressRar(file.path)
                dirName = file.path.replace('.rar', '')
                #time.sleep(5)
            elif '.7z' in file.name:
                unCompress7z(file.path)
                dirName = file.path.replace('.7z', '')
                #time.sleep(5)
            else:
                continue            

            lista_pdf = []
            lista_xml = []

            try:
                result = getListOfFiles(dirName)
            except:
                result = lectura.append([idDoc, idCatOpe, idTipDoc, "Revisar a mano|"])

            
            if result is None:
                lstRepse.append([idDoc, idCatOpe, idTipDoc, "Archivo Vacio|"])
            else:
                lstRepse += result

            print(result)
            

            lectura.clear()

    else:
        lstRepse.append([idDoc, idCatOpe, idTipDoc, "No es PDF|"])
        


dataNoValidos = pd.DataFrame(lstNoValidos)
dataNoValidos.to_csv(path + "//ArchivosNoValidos.csv", index=False, encoding='utf-8')   

dataRepse = pd.DataFrame(lstRepse)  
dataRepse.to_csv(path + "//InformacionCarga.csv", index=False, encoding='latin1')                   
