import fitz

file =fitz.open(r"C:\Users\araujo\Projects\BCA\Apoiadas AGO2021.pdf")

#----------------------------------------------------------------
#Extract Text
for pageNumber, page in enumerate(file.pages(), start = 1):
    
    text = page.getText()
    
    txt = open(f'repost_Page_{pageNumber}.txt', 'a')
    txt.writelines(text)
    txt.close()

#----------------------------------------------------------------    