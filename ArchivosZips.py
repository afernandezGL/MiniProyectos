import os 
import shutil as sht
import time

path = "G:/Mi unidad/FORD_CE/Auditoria 2 - Gastos a Terceros/06 Primer Quincenal Junio/ZipsTrabajo"
destXml = "G:/Mi unidad/FORD_CE/Auditoria 2 - Gastos a Terceros/06 Primer Quincenal Junio/XML_Zips/"
destPedim = "G:/Mi unidad/FORD_CE/Auditoria 2 - Gastos a Terceros/06 Primer Quincenal Junio/Pedimentos_Zips/"

os.chdir(path)
flagXml = 0
flagPedim = 0

archivos = []

for dir in os.listdir():
    print(dir)

    if '.pdf' in dir:
        sht.copy(path + "/" + dir, destPedim)
        flagPedim+=1
        continue

    elif '.xml' in dir:
        sht.copy(path + "/" + dir, destXml)
        archivos.append(dir)
        flagXml+=1
        continue

    elif '.zip' in dir:
        continue

    else:
        for file in os.scandir(path + "/" + dir):      

            if '.xml' in file.name:
                sht.copyfile(file, destXml + file.name)
                archivos.append(file.name)
                flagXml+=1

            if '.pdf' in file.name:
                sht.copyfile(file, destPedim + file.name)
                flagPedim+=1


for pdf in os.scandir(destPedim):
    if pdf.name.replace("pdf", "xml") in archivos:
        os.remove(pdf)
        flagPedim-=1
        

print("Total de Xml's: " + str(flagXml))
print("Total de Pedimentos: " + str(flagPedim))