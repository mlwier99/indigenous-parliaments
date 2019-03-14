import sys
import requests
import pandas as pd
import textract
import datetime
import PyPDF2
from tika import parser

def get_pdf(num):
    url = "http://www.legassembly.gov.yk.ca/hansard/33-legislature/"+num+".pdf" #EDIT THIS FOR EACH LEGISLATURE
    r = requests.get(url)
    file = "./pdfs/" + num + ".pdf"
    with open(file, 'wb') as f:
        f.write(r.content)
    return file

def process_pdf(pdf,date):
    pdf_file = parser.from_file(pdf)
    clean_page = pdf_file['content']
    clean_df = pd.DataFrame(columns=["speaker","speech"])
    clean_page = clean_page[clean_page.find("prayers"):]
    titles = ["Hon.", "Mr.", "Ms."]
    speakers = []
    clean_page = clean_page.replace("\n", "").replace(")","").replace("(","")
    pars = clean_page.replace(":","**")
    pars = pars.split("**")
    for par in pars:
        for t in titles:
            if t in par:
                speaker = par[par.find(t):]
                if len(speaker.split(" ")) < 4 and speaker not in speakers:
                    speakers.append(speaker)
    print(speakers)
    clean_page = clean_page.replace("\n"," ").replace("\xe2\x80\x94","")
    for s in speakers:
        clean_page = clean_page.replace(s, "**"+s+"**")
    clean_page = clean_page.split("**")
    clean_page = list(filter(None, clean_page))
    for k,v in enumerate(clean_page):
        if v in speakers:
            print(v)
            print(clean_page[k+1])
            row = pd.DataFrame(data={"speaker": v, "speech": clean_page[k+1].replace(":","")}, index=[0])
            clean_df = clean_df.append(row, ignore_index=True)
    print(clean_df)
    return clean_df
  
    


def main(date=sys.argv[1]):
    # LOOP APPLIES TO 32 and 33rd LEGISLATURE
    if len(date) == 1:
        date = "00" + date
    elif len(date) == 2:
        date = "0" + date
    pdf_name = get_pdf(date)
    hansard_df = process_pdf(pdf_name,date)
    hansard_df.to_csv("./clean_csvs/33_legislature/"+date+".csv", encoding='utf-8-sig') # MAKE NEW DIRECTORY FOR EACH LEGISLATURE
    print("CSV saved for: " + date)

if __name__=='__main__':
    main()    
