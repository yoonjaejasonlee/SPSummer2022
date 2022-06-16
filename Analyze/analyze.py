import os
import sys

import lizard
import json
from git.repo.base import Repo
import requests
import pygount
#crawler 한테 정보를 받아와서 클론 실행 
#crawler 한테 받아와야하는 정보
#Repo 주소, repo 이름, 크롤링 완료 타임스탬프, 
#Repo.clone_from("<repo 주소>", "<저장위치/repo 이름>") #새로운 파일로 저장 가능
#Repo.clone_from("https://github.com/public-apis/public-apis.git", "C:/Users/yoonj/Desktop/project-3-s22-yoonjaejasonlee-main/test")


list = []
def main():
    api_url = f"<put url here>"

    response = requests.get(api_url)

    data = response.json()

    url = data["<Repo URL>"]
    name = data["name"]

    temp_location = "저장소위치/{name}"

    Repo.clone_from("{url}","{temp_location}") #새로운 폴더 생성 그리고 그안에 리포 집어넣기


#Repo 안에 .py 파일만 추출
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
                    list.append(full_filename)
    except PermissionError:
        pass
search("{temp_location}")
     


    



#work queue 생성후 하나씩 lizard 이용해서 SLoC, CCN  발췌
i = lizard.analyze_file("C:/Users/yoonj/Desktop/project-3-s22-yoonjaejasonlee-main/server.c")

CC = i.function_list[0].__dict__['cyclomatic_complexity']
#nloc = i.function_list[0].__dict__['loc']


#print(CC)
#print(nloc)
print(i.function_list[0].__dict__)



#totalSLoC = 0 #파일 하나씩 진행할때마다 더해줌 .... 나중에 average 를 가져오기 위함. 
#totalCCN = 0
#minSLoC = 0 #나중에 다 db로 넘어갈 지표들임. 
#maxSLoC = 0 



