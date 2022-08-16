import os 
from xml.dom import minidom

path = "G:/Mi unidad/FORD_CE/Auditoria 2 - Gastos a Terceros/06 Primer Quincenal Junio/JUNIO 01"

os.chdir(path)
flag = 0
lstFacturas = []


for dir in os.listdir():
    for file in os.scandir(dir):
        if '.xml' in file.name:
            xmlDoc = str(file.path)
            doc = minidom.parse(xmlDoc)
            factura = []
            
            comprobante = doc.getElementsByTagName("cfdi:Comprobante")[0]
            serie = comprobante.getAttribute("Serie")
            folio = comprobante.getAttribute("Folio")
            fechaComp = comprobante.getAttribute("Fecha")

            emisor = doc.getElementsByTagName("cfdi:Emisor")[0]
            nomEmi = emisor.getAttribute("Nombre")
            rfcEmi = emisor.getAttribute("Rfc")

            receptor = doc.getElementsByTagName("cfdi:Receptor")[0]
            nomRec = receptor.getAttribute("Nombre")
            rfcRec = receptor.getAttribute("Rfc")

            timbre = doc.getElementsByTagName("tfd:TimbreFiscalDigital")[0]
            uuidXML = timbre.getAttribute("UUID")

            for concepto in doc.getElementsByTagName("cfdi:Concepto"):
                descripcion = concepto.getAttribute("UUID")


print(flag)