import os
import lizard
import requests
from git.repo.base import Repo

list_search = []
i = 0
CC_avg = 0
total_lines = 0

api_url = f"https://api.github.com/search/repositories?q=language:python+stars:%3E=30+forks:%3E=30&page=1&per_page=1"

response = requests.get(api_url)

data = response.json()

for s in data["items"]:
    #urls = i["html_url"]
    name = s["full_name"]

hub = f"https://github.com/{name}"
temp_location = f"C:/Users/yoonj/Desktop/project-3-s22-yoonjaejasonlee-main/{name}"

Repo.clone_from(hub, temp_location)  # 새로운 폴더 생성 그리고 그안에 리포 집어넣기


def search(directory):
    try:
        filenames = os.listdir(directory)
        for filename in filenames:
            full_filename = os.path.join(directory, filename)
            if os.path.isdir(full_filename):
                search(full_filename)
            else:
                ext = os.path.splitext(full_filename)[-1]
                if ext == '.py':
                    list_search.append(full_filename)
    except PermissionError:
        pass


search(temp_location)

while i < len(list_search):
    code = lizard.analyze_file(list_search[i])
    CC = code.CCN
    lines = code.nloc
    CC_avg = CC_avg + CC
    total_lines += lines
    print("File:", code.filename)
    print("Cyclomatic Complexity:", CC)
    print("Lines of Code:", lines)
    print("Cumulative number of LOC:", total_lines)
    print("\n")
    i += 1

    if i == len(list_search):
        print("Average Cyclomatic Complexity for the Repo: ", CC_avg / len(list_search))
