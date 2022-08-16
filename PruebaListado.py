import os 
import pandas as pd

archivo = 'G:/Mi unidad/ProcesosInternos/ELIMINA_CFDIs.xlsx'
ejemplo_dir = 'G:/Mi unidad/CFDIs Empresas/BPB/RECIBIDOS/BBI131009S36_Recibidos_2022_06_06-30/'

df = pd.read_excel(archivo, sheet_name='Hoja1')
mylist = df['UUID'].to_list()

flag = 0

with os.scandir(ejemplo_dir) as ficheros:
    for fichero in ficheros:
        for uuid in mylist:
            if  uuid.lower() in fichero.name.lower():
                os.remove(fichero)
                #print(uuid.lower())
                flag = flag+1
            

print(flag)
print('Proceso terminado')

