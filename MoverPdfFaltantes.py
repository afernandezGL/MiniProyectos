import os 
import pandas as pd
import shutil as sht
import time

archivo = 'G:/Mi unidad/ProcesosInternos/OBTIENE_PEDIMENTOS_FALTANTES.xlsx'
path = "G:/Mi unidad/FORD_CE/Auditoria 1 - Honorarios/05 Prueba Exw Honorarios/Pedimentos/"
destPedim = "G:/Mi unidad/FORD_CE/Auditoria 1 - Honorarios/05 Prueba Exw Honorarios/Faltantes2/"

df = pd.read_excel(archivo, sheet_name='SIN PDF')
mylist = df['PEDIMENTO_COMPLETO'].to_list()
mylist2 = df['PEDIMENTO_COMPL_2'].to_list()

os.chdir(path)
flagPedim = 0

archivos = []

for emp in os.listdir():
    print(emp)
    for file in os.scandir(path + "/" + emp): 
        if '.pdf' in file.name:
            for ped in mylist:
                if file.name.lower() in ped.lower():
                    sht.copyfile(file.path, destPedim + file.name)
                    flagPedim+=1

            for ped in mylist2:
                if file.name.lower() in ped.lower():
                    sht.copyfile(file.path, destPedim + file.name)
                    flagPedim+=1
        
        elif '.csv' in file.name:
            continue
        else:
            for arch in os.scandir(path + "/" + emp + "/" + str(file.name)):  
                if '.pdf' in arch.name:
                    for ped in mylist:
                        if arch.name.lower() in ped.lower():
                            sht.copyfile(arch.path, destPedim + arch.name)
                            flagPedim+=1

                    for ped in mylist2:
                        if arch.name.lower() in ped.lower():
                            sht.copyfile(arch.path, destPedim + arch.name)
                            flagPedim+=1


        
print("Total de Pedimentos: " + str(flagPedim))