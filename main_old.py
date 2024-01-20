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

p = getPdfContent()
data = {
    "file" : p,
    "targetformat" : "csv",
    "filelocation" : "local",
    "legal" : "Our PHP programs can only be used in aconvert.com. We DO NOT allow using our PHP programs in any third-party websites, software or apps. We will report abuse to your cloud provider, Google Play and App store if illegal usage found!"
}
headers = {
":authority":'s6.aconvert.com',
':method':'POST',
':path':'/convert/convert9.php',
':scheme':'https',
'Accept':'*/*',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
'Cache-Control':'no-cache',
'Content-Length':'107707',
'Content-Type':'multipart/form-data; boundary=----WebKitFormBoundaryAwq8IkXW3YV7VBA7',
'Origin':'https://www.aconvert.com',
'Pragma':'no-cache',
'Referer':'https://www.aconvert.com/',
'Sec-Ch-Ua':'"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
'Sec-Ch-Ua-Mobile':'?0',
'Sec-Ch-Ua-Platform':"macOS",
'Sec-Fetch-Dest':'empty',
'Sec-Fetch-Mode':'cors',
'Sec-Fetch-Site':"same-site",
'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
response = requests.post("https://s6.aconvert.com/convert/convert9.php", data=data, headers=headers)
print(response.text)
# print(getPdfContent())
# print(pdfToCsv(getPdfContent()))


