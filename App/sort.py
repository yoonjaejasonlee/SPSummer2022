import os
import lizard
import requests
import time
import mariadb
import sys
from git.repo.base import Repo

# -----------------------------------------------------

# --------------DB 연결-----------------------------------
try:
    conn = mariadb.connect(
        user="root",
        password="a1234567!",
        host="sparrow-ml.fasoo.com",
        port=30198,
        database="Analyzer"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB platform: {e}")
    sys.exit(1)

cur = conn.cursor()


# ------------------------------------------------------------

# -------------------CLASS FOR QUEUE---------------------------------------
class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, data):
        self.queue.append(data)

    def dequeue(self):
        dequeue_object = None
        if self.isEmpty():
            print("Queue is Empty\n")
        else:
            dequeue_object = self.queue[0]
            self.queue = self.queue[1:]

        return dequeue_object

    def peek(self):
        peek_object = None
        if self.isEmpty():
            print("Queue is Empty")
        else:
            peek_object = self.queue[0]

        return peek_object

    def isEmpty(self):
        is_empty = False
        if len(self.queue) == 0:
            is_empty = True
        return is_empty


# --------------------------------------------------------------------

queue = Queue()
queue_size = 0
list_search = []
i = 0
py_count = 0
total_count = 0
CC_avg = 0
CC_min = 0
CC_max = 0
total_lines = 0
lines = 0
j = 1
queue_count = 0

start_time = time.time()

url = 1

while url is not None:

    api_url = f"https://api.github.com/search/repositories?q=language:python+stars:>=170+forks:>=20&page={j}&per_page" \
              f"=100 "

    response = requests.get(api_url)

    response_data = response.json()

    for s in response_data["items"]:
        url = s["url"]
        queue_size += 1
        queue.enqueue(url)
        j += 1

    print("Queue Size: ", queue_size)

    while not queue.isEmpty():
        url = queue.peek()
        queue.dequeue()

        api = url
        api_response = requests.get(api)
        api_response_data = api_response.json()

        user_name = api_response_data["owner"]["login"]
        repo_name = api_response_data["name"]

        hub = f"https://github.com/{user_name}/{repo_name}"
        temp_location = f"C:/Users/yoonj/Desktop/project-3-s22-yoonjaejasonlee-main/testing/{user_name}/{repo_name}"

        Repo.clone_from(hub, temp_location)


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
            py_count += 1
            total_count += 1
            CC = code.CCN
            CC_min = min(CC, CC_min)
            CC_max = max(CC, CC_max)
            lines += code.nloc
            CC_avg += CC
            total_lines += code.nloc
            i += 1

        if i == len(list_search):

            CC_avg = CC_avg / len(list_search)
            insert_query = "INSERT INTO analyze_results (user_name,repo_name, num_files, min_CCN, max_CCN, average_CCN, repo_LOC, cumulative_LOC) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

            try:
                cur.execute(insert_query, (user_name, repo_name, py_count, CC_min, CC_max, CC_avg, lines, total_lines))
            except mariadb.Error as e:
                print(f"Error: {e}")

            conn.commit()

            print(f"REPO: {user_name}/{repo_name} Successfully Added to the DB")

            CC_avg = 0
            py_count = 0
            CC_min = 0
            CC_max = 0
            lines = 0

        queue_size -= 1

end_time = time.time()

print(f"Total time cost: {end_time - start_time}")
print(f"Number of files: {total_count}")
print(f"time cost per file: {(end_time - start_time) / total_count}\n")
