from lib2to3.pgen2.pgen import DFAState
import PyPDF2
from tabula import read_pdf
from tabulate import tabulate
import pandas as pd
import io


# Read the only the page n°1 of the file
file = r"C:\Users\araujo\Projects\BCA\Apoiadas AGO2021.pdf"
readpdf = PyPDF2.PdfFileReader(file)
page = readpdf.getPage(0)

#Extract Text of selected page
content = page.extractText()
print(type(content))
print(content)

# Transform the result into a string table format
# table = tabulate(content)

# Transform the table into dataframe
# df = pd.read_fwf(io.StringIO(table))

# Save the final result as excel file
# df.to_excel("test.xlsx")

# print (content)