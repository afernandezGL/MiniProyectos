from ast import Import
from pickletools import pyunicode
import pyodbc
import pandas as pd


xlsx = 'G:/Mi unidad/ProcesosInternos/ELIMINA_CFDIs.xlsx'
df = pd.read_excel(xlsx, sheet_name='Hoja1')




try:
    connection = pyodbc.connect('DRIVER={SQL Server};SERVER=127.0.0.1,8282;DATABASE=PORTAL;UID=sa;PWD=Temporal01*')
    print("Conexión exitosa")

    cursor = connection.cursor()

    cursor.execute("SELECT @@version;")
    row = cursor.fetchone()
    print(row)

except Exception as ex:
    print(ex)
