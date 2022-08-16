import os 
import pandas as pd
from xml.dom import minidom

archivo = 'G:/Mi unidad/ProcesosInternos/ELIMINA_CFDIs.xlsx'
ejemplo_dir = 'G:/Mi unidad/CFDIs Empresas/BPB/RECIBIDOS/BBI131009S36_Recibidos_2022_07_06-31/'

df = pd.read_excel(archivo, sheet_name='Hoja1')
mylist = df['UUID'].to_list()

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
        
            for uuid in mylist:
                if  uuid.lower() in uuidXML.lower():
                    #os.remove(fichero)
                    #print(uuid.lower())
                    flag = flag+1
            

print(flag)
print('Proceso terminado')

