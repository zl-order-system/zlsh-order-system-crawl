import requests
import bs4
import tabula
import pandas as pd
import io
from PyPDF2 import PdfReader

def getPdfContent():
    schoolWebURL = "https://www.zlsh.tp.edu.tw/category/office/div_300/section_lunch/lunch1_list/"
    schoolWebHTML = requests.get(schoolWebURL).text
    pdfURL = bs4.BeautifulSoup(schoolWebHTML, "html5lib").find("span", {"class":"modal_download"}).find("a").get("href")
    pdfContent = requests.get(pdfURL).content
    return pdfContent

def pdfToCsv(pdfContent):
    tables = tabula.read_pdf(pdfContent, pages="all", multiple_tables=True, stream=True)
    df = pd.concat(tables, ignore_index=True)
    csvContent = df.to_csv(index=False)
    return csvContent


def CsvToJson(csvContent):
    df = pd.read_csv(csvContent)
    json_content = df.to_json(orient='records')
    return json_content


print(getPdfContent())
# print(pdfToCsv(getPdfContent()))