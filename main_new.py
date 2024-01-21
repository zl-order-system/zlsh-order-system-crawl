import requests
import bs4
import PyPDF2
import io
from datetime import datetime, timedelta

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

def checkWeek(dateArray): #將這個月的日期整理成一週一週的陣列（同週放在同一格陣列）
    weeks = ("一", "二", "三", "四", "五", "六", "日")
    allDate = [ datetime.strptime(date['date'],"%Y-%m-%d") for date in dateArray ]
    returnData = [[]]
    lastweek = 0
    everyWeekFirstDate = allDate[0] - timedelta(days=allDate[0].weekday())
    for i in allDate:
        if (i - everyWeekFirstDate).days < 7:
            returnData[lastweek].append(i.date().strftime("%Y-%m-%d"))
        else:
            returnData.append([]) 
            lastweek += 1
            returnData[lastweek].append(i.date().strftime("%Y-%m-%d"))
            everyWeekFirstDate = i - timedelta(days=i.weekday())
    return returnData
#---遠端爬取最新pdf---
pdfContent = getPdfContent(0)
text = pdfContentToText(pdfContent)
formatText = textFormat(text)
weekDate = checkWeek(formatText)
print(weekDate)

# checkWeek([{'date': '2024-1-2', 'name': '日式燒肉片', 'NotOwnBox': False}, {'date': '2024-1-3', 'name': '肉絲炒飯', 'NotOwnBox': False}, {'date': '2024-1-4', 'name': '香酥雞排', 'NotOwnBox': False}, {'date': '2024-1-5', 'name': '義式芝麻烤腿排', 'NotOwnBox': False}, {'date': '2024-1-8', 'name': '蒜香骰子豬', 'NotOwnBox': False}, {'date': '2024-1-9', 'name': '沙茶雞丁', 'NotOwnBox': False}, {'date': '2024-1-10', 'name': '椒鹽花枝排', 'NotOwnBox': False}, {'date': '2024-1-11', 'name': '清蒸多利魚', 'NotOwnBox': False}, {'date': '2024-1-12', 'name': '咖哩肉片燴飯', 'NotOwnBox': True}, {'date': '2024-1-15', 'name': '蔥爆肉絲', 'NotOwnBox': False}, {'date': '2024-1-16', 'name': '黑胡椒雞柳', 'NotOwnBox': False}, {'date': '2024-1-17', 'name': '紅燒肉', 'NotOwnBox': False}, {'date': '2024-1-18', 'name': '香滷棒腿', 'NotOwnBox': False}, {'date': '2024-1-23', 'name': '蠔油肉片', 'NotOwnBox': False}, {'date': '2024-1-24', 'name': '肉燥乾麵', 'NotOwnBox': True}, {'date': '2024-1-25', 'name': '咔啦雞排', 'NotOwnBox': False}, {'date': '2024-1-26', 'name': '椒鹽魚排', 'NotOwnBox': False}])

#---讀取本地pdf---
# text = local_PdfFileToText("EX_PDF/112-12月.pdf")
# formatText = textFormat(text)
# print(formatText)