from function import *
import json

#---遠端爬取最新pdf---
pdfContent = getPdfContent(0)
text = pdfContentToText(pdfContent)
formatText = textFormat(text)
weekDate = checkWeek(formatText)
mealsData = weekDateToAllMealData(weekDate, formatText)
JsonStr = json.dumps(mealsData, ensure_ascii=False)
print(JsonStr)


#---讀取本地pdf---
# text = local_PdfFileToText("EX_PDF/112-12月.pdf")
# formatText = textFormat(text)
# print(formatText)