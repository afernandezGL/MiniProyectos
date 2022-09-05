from ast import Or
from asyncio.windows_events import NULL
from asyncore import read
from importlib.resources import path
from msilib.schema import Error
from operator import truediv
from pickle import FALSE
import pdfminer
import re
import os
import PyPDF2 as p2
import PyPDF2
import pandas as pd
import csv 
from pathlib import Path
import ntpath
import pandas as pd 
import logging
from logging import root
from pyexpat.model import XML_CTYPE_EMPTY
from xml.dom import XHTML_NAMESPACE, minidom
from xml.dom import minidom
import xml.etree.ElementTree
import asyncio


logging.basicConfig(level=logging.NOTSET, format='%(asctime)s :: %(levelname)s :: %(message)s')
class Extracinfo :
    WBLayout=[]
    Extraccion=[]
    Extraccion_xml=[]
    valores = ''

    

    # def convert(origin_file, destination_file):
    #     txt = ''
    #     try:
    #         # Get txt from PDF
    #         pdfFileObj = open(origin_file, 'rb')
    #         pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    #         pageObj = pdfReader.getPage(0)
    #         text = pageObj.extractText()
    #         pdfFileObj.close()

    #         # Write txt file
    #         os.makedirs(os.path.dirname(destination_file), exist_ok=True)
    #         with open(destination_file, 'w+', encoding='utf-8') as f:
    #             f.write(text)
    #         txt = open(destination_file, encoding='utf-8').read()
    #         print(txt)
    #         logging.info("File: " + destination_file + " saved successfully")
    #     except:
    #         logging.info("File: " + destination_file + " could not be read")
    #         txt = ''
    #         pass
    #     return txt
    
    # def convertidor(file,destinationfile):
    #     try:
    #         document = file.split('/').pop()
    #         output_filepath = destinationfile+document.replace('.pdf','.txt')
    #         pdf2txt.main(args=[file,'--outfile',output_filepath])
    #         #txt = open(os.path(output_filepath),encoding="utf8").read()
            
    #         #print(output_filepath+'saved successfully')
    #     except Exception:
    #         print('Hubo un error')
    #         #DECLARACION__IVA.append([str(file),str(),str(),str(),str(),str(),str("El documento no se pudo leer")])
    #         pass

    # def convertir(doc):
    #     try:
    #         #f = D:/Users/gpichardo/Documents/CESE/AzureBlobDownloads/82/2022-07-15/doc.pdf
    #         #output_filepath = D:/Users/gpichardo/Documents/CESE/AzureBlobDownloads/82/2022-07-15/doc.txt
    #         #output_filepath = D:/Users/gpichardo/Documents/CESE/AzureBlobDownloads/txt/doc.txt
    #         output_filepath = doc.replace('.pdf','.txt').replace()
    #         print('----------------------------------')
    #         pdf2txt.main(args=[doc,'--outfile',output_filepath])
    #         #cprint(output_filepath+'saved successfully')
    #     except:
    #         pass
    #     return open(output_filepath,encoding="utf8").read()
            
    #     #return  txt

    # # for file in os.listdir('D:/Users/gpichardo/Documents/CESE/AzureBlobDownloads/82/22-07-2022'):
    # #     if file.endswith('.pdf'):
    # #         #print('Reading....'+file)
    # #         txt = convertir(os.path.join('D:/Users/gpichardo/Documents/CESE/AzureBlobDownloads/82/22-07-2022',file))
    # #         #contenido(txt)
    # #         #print(convertir)

    # # def convertidor(file,destinationfile):
    # #     try:
    # #         document = file.split('/').pop()
    # #         output_filepath = destinationfile+document.replace('.pdf','.txt')
    # #         print(file)
    # #         print(output_filepath)
    # #         pdf2txt.main(args=[file,'--outfile',output_filepath])
    # #         print('------------------------------------------------------')
    # #         #print(output_filepath+'saved successfully')
    # #     except:
    # #         print('Hubo un error')
    # #         #DECLARACION__IVA.append([str(file),str(),str(),str(),str(),str(),str("El documento no se pudo leer")])
    # #         pass
            
    # #     return  open(os.path(output_filepath),encoding="utf8").read()

    # def convertir_prueba(doc,pathTxtFile):
    #     try:
    #         #f = D:/Users/gpichardo/Documents/CESE/AzureBlobDownloads/82/2022-07-15/doc.pdf
    #         #output_filepath = D:/Users/gpichardo/Documents/CESE/AzureBlobDownloads/82/2022-07-15/doc.txt
    #         #output_filepath = D:/Users/gpichardo/Documents/CESE/AzureBlobDownloads/txt/doc.txt
    #         output_filepath = doc.replace('.pdf','.txt').replace(doc,pathTxtFile)
    #         pdf2txt.main(args=[doc,'--outfile',output_filepath])
    #         #cprint(output_filepath+'saved successfully')
    #     except:
    #         pass
    #     #return open(output_filepath,encoding="utf8").read()










    # def convertidor(origin_file,destination_file,c_file):
    #     txt = ''
    #     try:
    #         output_filepath = origin_file.replace('.pdf','.txt').replace(origin_file,destination_file)
    #         pdf2txt.main(args=[origin_file,'--outfile',output_filepath])
    #         print(output_filepath+'saved successfully')
    #         logging.info("File: " + output_filepath + " saved successfully")
    #     except:
    #         logging.info("File: " + output_filepath + " could not be read")
    #         txt = ''
    #         Extracinfo.Extraccion.append([str(c_file),str(),str(),str(),str(),str(),str("El documento no se pudo leer")])
    #         pass
    #     return open(output_filepath,encoding="utf8").read() 



    def Repse(text,c_file):
        RFC = ''
        Nombre = ''
        Folio = ''
        RFC_Repse = ''
        Nombre_Repse = ''
        Folio_Repse = ''
        texto = text.split()
        B_Folio = False
        B_Nombre = False
        
        for palabra in texto:           
            RFC = re.findall('^[A-ZÑ&]{3,4}[0-9]{6}[A-ZÑ&0-9]{3},',palabra)
            if 'INGRESO:' in palabra and B_Folio==False:
                B_Folio= True
            if 'INGRESO:' not in palabra and B_Folio==True:
                Folio=palabra
                B_Folio= False
            
            if 'http://repse.stps.gob.mx' == palabra.strip() and B_Nombre == False and Nombre_Repse == '':
                B_Nombre=True
            if 'http://repse.stps.gob.mx' != palabra.strip() and B_Nombre == True:
                if 'por' != palabra and 'parte' != palabra and 'de' != palabra and 'CON' != palabra.upper() and 'Registro' != palabra and 'la' != palabra and 'persona:' != palabra and '(Física)' != palabra and '(Moral)' != palabra:
                    Nombre = Nombre + ' ' + palabra
                if 'CON' == palabra.upper() or 'Registro' == palabra:
                    if len(Nombre) > 0:
                        if 'documentación proporcionada a' in Nombre:
                            i = Nombre.find('documentación proporcionada a')
                            a = Nombre[-(len(Nombre)-i):]
                            Nombre = a.replace('documentación proporcionada a','').strip()
                        if 'través' in Nombre:
                            j = Nombre.find('través')
                            b = Nombre[-(len(Nombre)-j):]
                            Nombre = a.replace('través','').strip()
                        Nombre_Repse = Nombre.replace(',con','').strip()
                        Nombre = ''
                    B_Nombre = False
            
            if len(RFC) > 0:
                RFC_Repse = RFC[0].replace(',','').strip()
                RFC = ''
            if Folio != '':
                Folio_Repse = Folio.strip()
                Folio = ''
        if RFC_Repse != '' and Folio_Repse != '' and Nombre_Repse != '':
            Extracinfo.Extraccion.append([str(c_file),str() , str(RFC_Repse),str(Nombre_Repse),str(), str(),str()])
        else:
            Extracinfo.Extraccion.append([str(c_file),str(),str(),str(),str(),str(),str("No se pudo extraer la información")])

    def content_AcuseIVA(txt,c_file):
        RFC = ''
        RFC_Acuse = ''
        Nombre_Acuse = ''
        Nombre = ''
        Fecha = ''
        Fecha_Presentacion = ''
        texto = txt.split()
        Nombre_Documento = str(texto[0:10])
        Documento = Nombre_Documento.replace(',','').replace("'",'').replace('[','').replace(']','')
        print(Documento)
        Doc='ACUSE DE RECIBO DECLARACIÓN PROVISIONAL O DEFINITIVA DE IMPUESTOS FEDERALES'
        B_Nombre = False
        Periodo_Mes =' '
        PERIODO = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
        if len(texto)>50:
            if Documento== Doc:
            
                for palabra in texto:
                    RFC = re.findall('^[A-ZÑ&]{3,4}[0-9]{6}[A-ZÑ&0-9]{3}',palabra)
                    if len(RFC)>0 and RFC_Acuse=='':
                        RFC_Acuse=RFC[0].replace(',','').strip()
                        RFC=''
                        print(RFC_Acuse)
                    if palabra in PERIODO and Periodo_Mes==' ':
                        Periodo_Mes=palabra
                        print(Periodo_Mes)

                    Fecha = re.findall('[0-9]{2}/[0-9]{2}/[0-9]{4}',palabra)
                    if len(Fecha)>0 and Fecha_Presentacion=='':
                        Fecha_Presentacion=Fecha[0].strip()
                        Fecha=''
                        print(Fecha_Presentacion)

                    if 'social:' == palabra.strip() and B_Nombre == False and Nombre_Acuse == '':
                        B_Nombre = True
                    if 'social:' != palabra.strip()  and B_Nombre==True:
                        if 'Hoja' != palabra and 'Tipo' != palabra:
                            Nombre = Nombre + ' ' + palabra
                        if 'Hoja' == palabra or 'Tipo' == palabra:
                            if len(Nombre) > 0:
                                Nombre_Acuse= Nombre
                                Nombre=''
                                print(Nombre_Acuse)
                            B_Nombre =False
                if   Nombre_Acuse!='':

                    if RFC_Acuse!='' and Periodo_Mes!='' and Documento!='' or Nombre_Acuse!='':
                        Extracinfo.Extraccion.append([str(c_file),str(Documento),str(RFC_Acuse),str(Nombre_Acuse),str(Periodo_Mes),str(),str()])
                    else:
                        Extracinfo.Extraccion.append([str(c_file),str(),str(),str(),str(),str(),str('El documento no corresponde al Acuse IVA')])
                else:
                    Extracinfo.Extraccion.append([str(c_file),str(),str(),str(),str(),str(),str('El documento no se pudo leer')]) 
            else:
                Extracinfo.Extraccion.append([str(c_file),str(),str(),str(),str(),str(),str('El documento no corresponde al Acuse IVA')]) 
        else:
                Extracinfo.Extraccion.append([str(c_file),str(),str(),str(),str(),str(),str('El documento no se pudo leer')])
    
    def contenidoDeclaracion_IVA(txt,c_file):
        RFC = ''
        RFC_DECLARACION = ''
        Nombre_DECLARACION = ''
        Nombre = ''
        Fecha = ''
        Fecha_Presentacion = ''
        texto = txt.split()
        Nombre_Documento = str(texto[0:7])
        Documento = Nombre_Documento.replace(',','').replace("'",'').replace('[','').replace(']','')
        print(Documento)
        Doc='DECLARACIÓN PROVISIONAL O DEFINITIVA DE IMPUESTOS FEDERALES'
        B_Nombre = False
        Periodo_Mes =' '
        PERIODO = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
        if len(texto)>100:
            if Documento==Doc:
                for palabra in texto:
                    RFC = re.findall('^[A-ZÑ&]{3,4}[0-9]{6}[A-ZÑ&0-9]{3}',palabra)
                    if len(RFC)>0 and RFC_DECLARACION == '':
                        RFC_DECLARACION = RFC[0].replace(',','').strip()
                        RFC=''
                        print(RFC_DECLARACION)
                    if palabra in PERIODO and Periodo_Mes ==' ':
                        Periodo_Mes=palabra
                        print(Periodo_Mes)

                    Fecha = re.findall('[0-9]{2}/[0-9]{2}/[0-9]{4}',palabra)
                    if len(Fecha)>0 and Fecha_Presentacion=='':
                        Fecha_Presentacion=Fecha[0].strip()
                        Fecha=''
                        print(Fecha_Presentacion)

                    if 'SOCIAL' == palabra.strip() and B_Nombre == False and Nombre_DECLARACION == '':
                        B_Nombre = True
                    if 'SOCIAL' != palabra.strip()  and B_Nombre==True:
                        if 'DATOS' != palabra and 'GSC1603098R6' != palabra and 'TIPO'!= palabra and 'DE'!= palabra and 'DECLARACIÓN' != palabra and 'EJERCICIO' != palabra and 'FECHA' != palabra and 'Y' != palabra and 'HORA' != palabra and 'DE' != palabra and 'PRESENTACIÓN' != palabra and 'GPX161221IC7'  != palabra and 'Normal'  != palabra and '2022' != palabra and '16:27'!= palabra and '2021' != palabra and '15:40' != palabra and '21/02/2022' != palabra and '10:28'!= palabra and '20/06/2022' != palabra and '17:47'!= palabra and '17/06/2022'!= palabra and '18/01/2022'!= palabra : 
                            Nombre = Nombre + ' ' + palabra
                        if 'DATOS' == palabra or 'TIPO' == palabra:
                            if len(Nombre) > 0:
                                Nombre_DECLARACION= Nombre
                                Nombre=''
                                print(Nombre_DECLARACION)
                            B_Nombre =False
                if Nombre_DECLARACION!='':
                    if Documento !='' and  RFC_DECLARACION !='' and Nombre_DECLARACION!='' and Periodo_Mes!='' and Fecha_Presentacion!='':
                        Extracinfo.Extraccion.append([str(c_file),str(Documento) , str(RFC_DECLARACION),str(Nombre_DECLARACION),str(Periodo_Mes), str(Fecha_Presentacion),str()])
                    else:
                        Extracinfo.Extraccion.append([str(c_file),str(),str(),str(),str(),str(),str("El documento no corresponde a la Declaración de IVA")])
                else:
                    Extracinfo.Extraccion.append([str(c_file),str(),str(),str(),str(),str(),str("El documento no se pudo leer")])
            else:
                Extracinfo.Extraccion.append([str(c_file),str(),str(),str(),str(),str(),str('El documento no corresponde a la Declaración de IVA')]) 
        else:
            Extracinfo.Extraccion.append([str(c_file),str(),str(),str(),str(),str(),str("El documento no se pudo leer")])

    def contentAcuseIMSS(txt,c_file):
        RFC = ''
        RFC_IMSS = ''
        Periodo = False
        texto = txt.split()
        Nombre_Documento = str(texto[9:19])
        Documento = Nombre_Documento.replace(',','').replace("'",'').replace('[','').replace(']','')
        Doc='FORMATO PARA PAGO DE CUOTAS OBRERO PATRONALES APORTACIONES Y AMORTIZACIONES'
        if len(texto)>100:
            if Documento==Doc:
                Periodo_IMSS =''
                for palabra in texto:
                    RFC = re.findall('^[A-ZÑ&]{3,4}-[0-9]{6}-[A-ZÑ&0-9]{3}',palabra)
                    if len(RFC)>0 and RFC_IMSS=='':
                        RFC_IMSS=RFC[0].replace('-','').strip()
                        RFC=''
                        print(RFC_IMSS)
                    Periodo = re.findall('^[0-9]{2}-[0-9]{4}',palabra)
                    if len(Periodo)>0 and Periodo_IMSS=='':
                        Periodo_IMSS=Periodo[0].strip()
                        Periodo =''
                        print(Periodo_IMSS)
                
                if RFC_IMSS!='' and Periodo_IMSS!='' and Documento!='':
                    Extracinfo.Extraccion.append([str(c_file),str(Documento),str(RFC_IMSS),str(),str(Periodo_IMSS),str(),str()])
                else:
                    Extracinfo.Extraccion.append([str(c_file),str(),str(),str(),str(),str(),str('El documento no corresponde al Acuse IMSS')])
            else:
                    Extracinfo.Extraccion.append([str(c_file),str(),str(),str(),str(),str(),str('El documento no corresponde al Acuse IMSS')]) 
        else:
            Extracinfo.Extraccion.append([str(c_file),str(),str(),str(),str(),str(),str('El documento no se puede leer')])

    def contentAcuseINFO(txt,c_file):
        RFC = ''
        RFC_INFO = ''
        Periodo = False
        texto = txt.split()
        Nombre_Documento = str(texto[9:19])
        Documento = Nombre_Documento.replace(',','').replace("'",'').replace('[','').replace(']','')
        Doc= 'FORMATO PARA PAGO DE CUOTAS OBRERO PATRONALES APORTACIONES Y AMORTIZACIONES'
        if len(texto)>100:
            if Documento==Doc:

                Periodo_INFO =''
                for palabra in texto:
                    RFC = re.findall('^[A-ZÑ&]{3,4}-[0-9]{6}-[A-ZÑ&0-9]{3}',palabra)
                    if len(RFC)>0 and RFC_INFO=='':
                        RFC_INFO=RFC[0].replace('-','').strip()
                        RFC=''
                        print(RFC_INFO)
                    Periodo = re.findall('^[0-9]{2}-[0-9]{4}',palabra)
                    if len(Periodo)>0 and Periodo_INFO=='':
                        Periodo_INFO=Periodo[0].strip()
                        Periodo =''
                        print(Periodo_INFO)
                     
                if RFC_INFO!='' and Periodo_INFO!='' and Documento!='':
                    Extracinfo.Extraccion.append([str(c_file),str(Documento),str(RFC_INFO),str(),str(Periodo_INFO),str(),str()])
                else:
                    Extracinfo.Extraccion.append([str(c_file),str(),str(),str(),str(),str(),str('El documento no corresponde al Acuse INFONAVIT')])
            else:
                Extracinfo.Extraccion.append([str(c_file),str(),str(),str(),str(),str(),str('El documento no corresponde al Acuse INFONAVIT')])
        else:
         Extracinfo.Extraccion.append([str(c_file),str(),str(),str(),str(),str(),str('El documento no se puede leer')])  

    def contenomina(text,c_file):
        RFC = ''
        RFC_Nomina = ''
        Nombre_Nomina = ''
        Nombre = ''
        Fecha = ''
        Fecha_Nomina = ''
        BFec= False
        texto = text.split()
        DOC=''
        B_Nombre = False
        Periodo_Pago =' '
        for palabra in texto:
            RFC=re.findall('^[A-ZÑ&]{3,4}[0-9]{6}[A-ZÑ&0-9]{3}',palabra)
            if len(RFC)>0 and RFC_Nomina=='':
                RFC_Nomina=palabra.replace(',','').strip()
                print(RFC_Nomina)
            if palabra=='Fecha:' or palabra=='Pago' and BFec==False:
                BFec=True
            if palabra!='Fecha:' and BFec==True:
                Fecha = re.findall('^[0-9]{2}/[A-Z0-9a-z]{2,3}/[0-9]{4}',palabra) 
                if len(Fecha)>0 and Fecha_Nomina=='':
                    Fecha_Nomina=Fecha[0].strip()
                    Fecha=''
                    print(Fecha_Nomina)
                BFec=False
            if 'Internet' == palabra.strip() and B_Nombre == False and Nombre_Nomina == '':
                B_Nombre = True
            if 'Internet' != palabra.strip() and B_Nombre==True:
                if 'RFC:' != palabra and 'Folio' != palabra:
                    Nombre = Nombre + ' ' + palabra
                if 'RFC:' == palabra or 'Folio' == palabra:
                    if len(Nombre) > 0:
                        Nombre_Nomina= Nombre
                        Nombre=''
                        print(Nombre_Nomina)
                    B_Nombre =False
            if palabra=='CFDI' and DOC=='':
                DOC=palabra
                print(DOC)
        if RFC_Nomina!='' and DOC!='' and Fecha_Nomina!='' and Nombre_Nomina!='':
            Extracinfo.Extraccion.append([str(c_file),str(DOC),str(RFC_Nomina),str(Nombre_Nomina),str(),str(Fecha_Nomina),str()])
        else:
            Extracinfo.Extraccion.append([str(c_file),str(),str(),str(),str(),str(),str('No se pudo extraer el documento')])
    
    def xml_read(xmldoc):
        global valores

        try:
            doc = minidom.parse(xmldoc)
            comp = doc.getElementsByTagName("cfdi:Comprobante")[0]
            compFecha = comp.getAttribute("Fecha")
            nomi = doc.getElementsByTagName("nomina12:Nomina")[0]
            nomFechaPago = nomi.getAttribute("FechaPago")
            nomFechaInicial = nomi.getAttribute("FechaInicialPago")
            periodicidad=doc.getElementsByTagName("nomina12:Receptor")[0]
            peri = periodicidad.getAttribute("PeriodicidadPago")
            #print(peri)
            if peri == "02":
                Fecha=nomFechaInicial
                #print(Fecha)
            else:
                Fecha= nomFechaPago
                #print(Fecha)
            #print(nomFechaPago)
            emi=doc.getElementsByTagName("cfdi:Emisor")[0]
            emiRFC = emi.getAttribute("Rfc")
            emiRazon = emi.getAttribute("Nombre")
            recep=doc.getElementsByTagName("cfdi:Receptor")[0]
            recepRFC = recep.getAttribute("Rfc")
            recepRazon = recep.getAttribute("Nombre")
            # print(emi)
            # print(emiRFC)
            # print(emiRazon)
            # print(recep)
            # print(recepRFC)
            # print(recepRazon)
            if Fecha !='' or  emiRFC!='' or emiRazon!='' or recepRFC !='' or recepRazon!='':
                valores = str(Fecha) + "|" + str(emiRFC) + "|" + str(emiRazon) + "|" + str(recepRFC) + "|" + str(recepRazon)
            # else:
            #     Extracinfo.Extraccion_xml.append([str(id_d),str(cat_ope),str(nom_doc),str(),str(),str(),str(),str(),str("No se pudo extraer la información")])
        except:
            pass

        return valores

    def contenlist(f,l_file):
        df=pd.read_excel(f)
        colmun =df.head
        print(df.iloc[0,1])
        print(colmun)
        cl=df.columns
        Layout=(cl[0],cl[1],cl[2],cl[3],cl[4])
        print(Layout)
        for i in Layout:
            if i=='Año':
                lay1='ok'
                print(lay1)
            elif i =='Mes':
                lay2='ok'
                print(lay2)
                periodo=df.iloc[0,1]
                print(periodo)
            elif i=='RFC Empleado':
                lay3='ok'
                print(lay3)
            elif i=='Nombre':
                lay4='ok'
            elif i=='% de tiempo dedicado':
                lay5='ok'
                print(lay5)
        if lay1!='' and lay2!='' and lay3!='' and lay4!='' and lay5!='':
            Extracinfo.WBLayout.append([str(l_file),str(lay1),str(lay2),str(lay3),str(lay4),str(lay5),str(periodo)])
        else:
            Extracinfo.WBLayout.append([str(l_file),str(),str(),str(),str(),str(),str(),str(),'El archivo no es el layout correspondiente'])
        



                



