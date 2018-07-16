import sys
import requests
import PyPDF2 as pypdf2
import pandas as pd

def get_pdf(date):
    # sometimes the files have a "_0" associated with them
    url = "http://www.assembly.nu.ca/sites/default/files/" + date + "-Blues-English.pdf" 
    r = requests.get(url)
    file = "./pdfs/" + date + ".pdf"
    with open(file, 'wb') as f:
        f.write(r.content)
    return file

def extract_speakers(pdf, first_page):
   titles = ["Hon.", "Mr.", "Ms.", "Speaker"]
   speaker_list = []
   clean_page = first_page[first_page.find("Members Present"):first_page.find(">>House")]
   clean_page = clean_page.replace(",","").replace("\n","").replace("Mr. Speaker", "mrspeaker").replace(">>Applause","")
   for t in titles:
       clean_page = clean_page.replace(t, "* " + t)
   clean_page = clean_page.split("*")
   for k, v in enumerate(clean_page):
       for t in titles:
           if t in v:
               speaker_list.append(v)
   return speaker_list

def process_pdf(pdf):
    pdf_obj = open(pdf, 'rb')
    pdf_reader = pypdf2.PdfFileReader(pdf_obj)
    print("Number of pages in Hansard: " + str(pdf_reader.numPages))
    clean_df = pd.DataFrame(columns=["speaker","speech"])
    titles = ["Hon.", "Mr.", "Ms.", "Speaker"]
    speaker_list = None
    for p in range(0, pdf_reader.numPages):
        page_obj = pdf_reader.getPage(p) 
        raw_page = page_obj.extractText()
        raw_page = raw_page.replace("\n", "")
        if "Members Present:" in raw_page:
            print(raw_page)
            speaker_list = extract_speakers(pdf, raw_page)
            print(speaker_list)
        elif speaker_list == None:
            print("Skipped cover page: " + str(p))
        else:
            clean_page = raw_page.replace(",","").replace("Mr. Speaker", "mrspeaker").replace(">>Applause","")
            clean_page = clean_page.replace(":",",")
            clean_page = clean_page.split(",")
            for k,v in enumerate(clean_page):
                for t in speaker_list:
                    if t in v:
                        try:
                            df = pd.DataFrame(data={"speaker":[t], "speech":[clean_page[k+1]]})
                            clean_df = clean_df.append(df, ignore_index=True)
                        except IndexError:
                            print(v)
    print(clean_df)
    return clean_df



def main(date=sys.argv[1]):
    # Add a loop for this to check and add for files automatically
    pdf_name = get_pdf(date)
    hansard_df = process_pdf(pdf_name)
    hansard_df.to_csv("./clean_csvs/"+date+".csv")
    print("CSV saved for: " + date)

if __name__=='__main__':
    main()    
