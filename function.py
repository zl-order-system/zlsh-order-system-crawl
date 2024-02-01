import requests
import bs4
import PyPDF2
import io
from datetime import datetime, timedelta
import json

def getPdfContent(number): #number 為取得第n新的pdf(0為最新，1為第二新，以此類推)
    schoolWebURL = "https://www.zlsh.tp.edu.tw/category/office/div_300/section_lunch/lunch1_list/"
    schoolWebHTML = requests.get(schoolWebURL).text
    pdfURL = bs4.BeautifulSoup(schoolWebHTML, "html5lib").find_all("span", {"class":"modal_download"})[number].find("a").get("href")
    pdfContent = requests.get(pdfURL).content
    return pdfContent

def pdfContentToText(pdfContent): #爬取校網菜單pdf並輸出文字
    fakeFile = io.BytesIO(bytes(pdfContent))
    pdfReader = PyPDF2.PdfReader(fakeFile)
    text = ""
    for page_num in range(len(pdfReader.pages)):
        page = pdfReader.pages[page_num]
        text += page.extract_text()
    fakeFile.close()
    return text
    
def local_PdfFileToText(path): #讀取本地pdf並輸出文字
    with open(path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

def textFormat(text): #將每一天的日期以及餐像整理
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
    for i in range(len(formatArray)):
        formatArray[i]["date"] = datetime.strptime(formatArray[i]["date"], "%Y-%m-%d").strftime("%Y-%m-%d")
    return formatArray

def eachLineProcess(lineText, year , month): #在textFormat()中用到，用來處裡菜單每一行文字
    NotOwnBox = True if "無自備" in lineText else False
    processData = lineText.split("/")
    inLineMonth = ""
    for i in processData[0]:
        inLineMonth += i if i.isdigit() and len(inLineMonth) < 3 else ""
    date = ""
    for i in range(0, len(processData[1])):
        date += processData[1][i] if  processData[1][i].isdigit() and i < 3 else ""
    returnData = {"date": f"{year}-{inLineMonth}-", "name":"", "schoolOnly":NotOwnBox}
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

def isChineseWeekNumber(text): #檢查是否為中文的星期文字
    ChineseNumber = ("日","一","二","三","四","五","六")
    return True if text in ChineseNumber else False

def checkWeek(dateArray): #將這個月的日期整理成一週一週的陣列（同週放在同一格陣列）
    weeks = ("一", "二", "三", "四", "五", "六", "日")
    allDate = [ datetime.strptime(date['date'], "%Y-%m-%d") for date in dateArray ]
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

def weekDateToAllMealData(weekDate ,formatData): #將textFormat()回傳的陣列處理，並將同一週菜單合併，並以物件導出
    returnData = []
    for i in weekDate:
        mealOptions = []
        for date in i:
            num = searchNumByDate(date, formatData)
            mealOptions.append({
                "name":formatData[num]["name"],
                "schoolOnly":formatData[num]["schoolOnly"]
            })
        for date in i:
            num = searchNumByDate(date, formatData)
            returnData.append({
                "date":date,
                "mealOptions":mealOptions,
            })
    return returnData

def searchNumByDate(date, formatData): #利用日期來查找當天所在陣列第幾項
    num = 0
    for i in formatData:
        if i["date"] == date: return num
        else: num+=1 