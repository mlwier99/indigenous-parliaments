import sys
import requests
import pandas as pd
import docx
import datetime

def get_docx(date):
    """
    date should be in following format: 180601
    """
    url = "http://www.assembly.gov.nt.ca/sites/default/files/hn"+date+".docx"
    r = requests.get(url)
    file = "./docs/"+date+".docx"
    with open(file, 'wb') as f:
        f.write(r.content)
    return file

def get_text(file):
    doc = docx.Document(file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return full_text

def process_doc(date):
    clean_df = pd.DataFrame(columns=["speaker","speech"])
    full_text = get_text(get_docx(date))
    for par in full_text:
        par = par.replace("[","").replace("]","")
        words = par.split(" ")
        if len(words[0]) > 1 and words[0].isupper() and ":" in par:
            par = par.split(":")
            df = pd.DataFrame(data={"speaker":par[0], "speech": par[1]}, index=[0])
            clean_df = clean_df.append(df, ignore_index=True)
    clean_df = clean_df[clean_df.speaker != "MR. SPEAKER"]
    print(clean_df)
    return clean_df


def main(date=sys.argv[1]):
    hansard_df = process_doc(date)
    hansard_df.to_csv("./clean_csvs/"+date+".csv",encoding='utf-8-sig')
    print("CSV daved for: " + date)
    

if __name__=='__main__':
    main()
