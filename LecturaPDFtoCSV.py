import tabula
import pandas as pd
import os

rutaPDF = "C:/Users/afernandez/Desktop/FACTURA/FACTURA  GLAXO 11-20 MAYO 22.pdf"
rutaCSV = "C:/Users/afernandez/Desktop/FACTURA/FACTURA  GLAXO 11-20 MAYO 22.csv"
path = "C:/Users/afernandez/Desktop/Prueba"

data = []

for file in os.scandir(path):    
    if '.pdf' in file.name:
        df = tabula.read_pdf(file.path, pages='1', output_format="json", lattice=True)
        
        print(df)
        #df.to_csv(file.path.replace("pdf", "csv"), encoding='utf-8')
        #tabula.convert_into(file.path, file.path.replace("pdf", "csv"), output_format="csv", pages='all', stream = True)

#df = pd.read_csv(rutaCSV, header=None, encoding='latin-1', names=range(8))


#for i in df.index:
    #if df[i][0] in "DATE":
        #print(df[i][0])



print("Se completó proceso de transformación")
