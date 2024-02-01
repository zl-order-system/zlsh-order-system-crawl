from function import *
import os

#---遠端爬取最新pdf---
latestData = getCompleteData(0)
print(latestData)

current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)
target_folder_path = os.path.join(current_directory, "API", "meals")
file_path = os.path.join(target_folder_path, "latest.json")
with open(file_path, 'w') as file:
    file.write(latestData)


