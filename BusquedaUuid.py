import os 
import pandas as pd
from xml.dom import minidom

uuid = '3FC306CE-1F06-44D2-868E-1E18D0487A36'
ejemplo_dir = 'G:/Mi unidad/CFDIs Empresas/BPB/RECIBIDOS/BBI131009S36_Recibidos_2022_07_06-31/'

#df = pd.read_excel(archivo, sheet_name='Hoja1')
#mylist = df['UUID'].to_list()

flag = 0

with os.scandir(ejemplo_dir) as ficheros:
    for fichero in ficheros:
        xmlDoc = str(fichero.path)
        #print(xmlDoc)
        
        if xmlDoc.endswith('.xml'):
            doc = minidom.parse(xmlDoc)
            timbre = doc.getElementsByTagName("tfd:TimbreFiscalDigital")[0]
            uuidXML = timbre.getAttribute("UUID")

            #print(uuidXML)
        
            if  uuid.lower() in uuidXML.lower():
                #os.remove(fichero)
                print(fichero.name)
                flag = flag+1
            

print(flag)
print('Proceso terminado')

