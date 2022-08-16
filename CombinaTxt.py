import os

root = 'G:/.shortcut-targets-by-id/1KVArC-ketnK0beNF5tl2JSQxR4e6bc76/Control Descargas/METADATA/READERS/DDE091203L54/2022/'
final = 'G:/.shortcut-targets-by-id/1KVArC-ketnK0beNF5tl2JSQxR4e6bc76/Control Descargas/METADATA/READERS/DDE091203L54/Finales/Rec_Combinado2022.txt'
data = ""

with os.scandir(root) as archivos:    
    for arch in archivos:
        if '.txt' in arch.name:
            with open(arch, encoding="utf8") as text:
                data += text.read()
                print(text.name)


with open(final, 'w', encoding="utf8") as fp:
    fp.write(data)