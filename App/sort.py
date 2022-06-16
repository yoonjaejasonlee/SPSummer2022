from asyncio.windows_events import NULL
import os
import lizard

list_search = []
i = 0
CC_avg = 0


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


search("C:/Users/yoonj/Desktop/project-3-s22-yoonjaejasonlee-main")

while i < len(list_search):
    code = lizard.analyze_file(list_search[i])
    CC = code.CCN
    CC_avg = CC_avg + CC
    print("Cyclomatic Complexity:", CC)
    i += 1

    if i == len(list_search):
        print("Average Cyclomatic Complexity for the Repo: ", CC_avg / len(list_search))
