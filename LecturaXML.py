from xml.dom import minidom

doc = minidom.parse("G:/Mi unidad/CFDIs Empresas/CORTEVA/PHI MEXICO/CFDIs/PHI931220AN5_Emi_2019_06/000a7d3d-d816-41e6-be5f-dae2f8cb6979.xml")
nombre = doc.getElementsByTagName("tfd:TimbreFiscalDigital")[0]

print(nombre.getAttribute("UUID"))
