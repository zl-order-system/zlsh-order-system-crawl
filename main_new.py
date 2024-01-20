import requests
import bs4
import PyPDF2
import io

def getPdfContent(number): #number 為取得第n新的pdf(0為最新，1為第二新，以此類推)
    schoolWebURL = "https://www.zlsh.tp.edu.tw/category/office/div_300/section_lunch/lunch1_list/"
    schoolWebHTML = requests.get(schoolWebURL).text
    pdfURL = bs4.BeautifulSoup(schoolWebHTML, "html5lib").find_all("span", {"class":"modal_download"})[number].find("a").get("href")
    pdfContent = requests.get(pdfURL).content
    return pdfContent

def pdfContentToText(pdfContent):
    fakeFile = io.BytesIO(bytes(pdfContent))
    pdfReader = PyPDF2.PdfReader(fakeFile)
    text = ""
    for page_num in range(len(pdfReader.pages)):
        page = pdfReader.pages[page_num]
        text += page.extract_text()
    fakeFile.close()
    return text
    
def local_PdfFileToText(path):
    with open(path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

def textFormat(text):
    arrayText = text.split("\n")
    formatArray = []
    yi = arrayText[0].find("年")
    year = str(int(arrayText[0][yi-3:yi])+1911)
    mi = arrayText[0].find("月")
    month = ""
    for i in range(0, len(arrayText)):
        if "/" in arrayText[i]:
            startLineNum = i
            break
    for i in range(startLineNum, len(arrayText)):
        if "/" not in arrayText[i]:
            endLineNum = i-1
            break
    for i in range(2,0, -1):
        month += arrayText[0][mi - i] if arrayText[0][mi - i].isdigit() else  ""
    for i in range(startLineNum, endLineNum+1):
        formatArray.append(eachLineProcess(arrayText[i], year , month))
    return formatArray

def eachLineProcess(lineText, year , month):
    NotOwnBox = True if "無自備" in lineText else False
    returnData = {"date": f"{year}-{month}-", "name":"", "NotOwnBox":NotOwnBox}
    processData = lineText.split("/")
    date = ""
    for i in range(0, len(processData[1])):
        date += processData[1][i] if  processData[1][i].isdigit() and i < 3 else ""
    returnData["date"] += date
    name = ""
    nameStartLine = 0
    haveBeenChineseWeek = False
    for i in range(len(date), len(processData[1])):
        if isChineseWeekNumber(processData[1][i]) and haveBeenChineseWeek:
            nameStartLine = i
            break
        elif isChineseWeekNumber(processData[1][i]):
            haveBeenChineseWeek = True
            continue
        elif processData[1][i] == " ":
            continue
        else:
            nameStartLine = i
            break
    for i in range(nameStartLine, len(processData[1])):
        if processData[1][i] != " ":
            name += processData[1][i]
        else:
            break
    returnData["name"] += name
    return returnData

def isChineseWeekNumber(text):
    ChineseNumber = ("日","一","二","三","四","五","六")
    return True if text in ChineseNumber else False

#---遠端爬取最新pdf---
pdfContent = getPdfContent(0)
text = pdfContentToText(pdfContent)
print(text)
formatText = textFormat(text)
print(formatText)

#---讀取本地pdf---
# text = local_PdfFileToText("EX_PDF/112-12月.pdf")
# formatText = textFormat(text)
# print(formatText)