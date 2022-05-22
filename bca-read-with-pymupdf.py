import fitz
import re 

file =fitz.open(r"C:\Users\araujo\Projects\BCA\Apoiadas AGO2021.pdf")

#----------------------------------------------------------------
#Extract Text
for pageNumber, page in enumerate(file.pages(), start = 1):
    
    text = page.getText()
    
    txt = open(f'repost_Page_{pageNumber}.txt', 'a')
    #txt.writelines(text)
    txt.close()
#----------------------------------------------------------------
#Read PDF file
p=fitz.open(r"C:\Users\araujo\Projects\BCA\Apoiadas AGO2021.pdf")

#----------------------------------------------------------------    
#Search Pattern
NumPages =p.pageCount
patterns=[
    'GAP GL','PAMA GL','BAGL','CMRJ','1 CJM',
    'CEMAL','2/2 GT','CCA RJ','PAGL','1 GCC',
    'MTAB','DIRAP','DIRSA','CGABEG','BAGL_ANTIGA',
    'CBNB','SERIPA III','ESG','PAMB RJ','DTCEA-GL',
    '1/2 GT','BINFAE GL','1/1 GT','LAQFA','CTLA','GAP GL',
    'DT-INFRA RJ','ALA 11','CIMAER','CAE','COPE-S','GSD-GL',
    'MTAB-BOLIVIA','HFAG']

for i in range(0, NumPages):
    PageObj=p.loadPage(i)
    print("\nLooking through page" + str(i+1)+"\n")
    text=PageObj.getText()
    for pattern in patterns:
        print('Looking for (%s)\t'%pattern) 
    if re.search(pattern,text):
            print("FOUND a match!")
    else:
        print("not match")

