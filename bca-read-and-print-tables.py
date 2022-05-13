import tabula
from tabula import read_pdf

#----------------------------------------------------------------
#list tables
list_tables = tabula.read_pdf("Apoiadas AGO2021.pdf", pages="all")
print(len(list_tables))
#------------------------------
for table in list_tables:
    print(table)