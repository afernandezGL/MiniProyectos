import os 
import shutil as sht
import time

path = "G:/Mi unidad/FORD_CE/Auditoria 2 - Gastos a Terceros/06 Primer Quincenal Junio/Junio 01"
destXml = "G:/Mi unidad/FORD_CE/Auditoria 2 - Gastos a Terceros/06 Primer Quincenal Junio/XMLAct/"
destZips = "G:/Mi unidad/FORD_CE/Auditoria 2 - Gastos a Terceros/06 Primer Quincenal Junio/Zips/"
destPedim = "G:/Mi unidad/FORD_CE/Auditoria 2 - Gastos a Terceros/06 Primer Quincenal Junio/Pedimentos/"

os.chdir(path)
flagXml = 0
flagZips = 0
flagPedim = 0

archivos = []

for emp in os.listdir():
    print(emp)
    for dir in os.listdir(emp):
        print(dir)

        if '.zip' in dir:
            sht.copy(path + "/" + emp + "/" + dir, destZips)
            time.sleep(5)
            flagZips+=1

        if '.zip' not in dir:
            for file in os.scandir(path + "/" + emp + "/" + dir):      

                if '.xml' in file.name:
                    sht.copyfile(file, destXml + file.name)
                    archivos.append(file.name)
                    flagXml+=1

                if '.zip' in file.name:
                    sht.copy(path + "/" + emp + "/" + dir, destZips)
                    time.sleep(5)
                    flagZips+=1

                if '.pdf' in file.name:
                    sht.copyfile(file, destPedim + file.name)
                    flagPedim+=1


for pdf in os.scandir(destPedim):
    if pdf.name.replace("pdf", "xml") in archivos:
        os.remove(pdf)
        flagPedim-=1
        

print("Total de Xml's: " + str(flagXml))
print("Total de Zip's: " + str(flagZips))
print("Total de Pedimentos: " + str(flagPedim))