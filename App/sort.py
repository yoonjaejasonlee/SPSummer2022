import os
import lizard
import requests
import time
import mariadb
import sys

from git.repo.base import Repo

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
total_files = 0
j = 1

start_time = time.time()

user = 'yoonjaejasonlee'
token = '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'


# -----------------------------------------------------------------------
def queuing(page_num):
    if page_num <= 2:
        url = f"http://127.0.0.1:5000/repos/{page_num}"

        response = requests.get(url)

        response_data = response.json()

        for s in response_data:
            queue.enqueue(s)

        print("Queue Size: ", len(queue.queue))
    else:
        print("nothing to queue")


# -----------------------------------------------------------------------
def analyze(cc_avg, cc_min, cc_max, total_line, file_count, counter, page_num, line, total_file):
    queuing(page_num)
    if not queue.isEmpty():
        url = queue.peek()
        queue.dequeue()

        user_name = url.rsplit('/', 2)[1]
        repo_name = url.rsplit('/', 1)[-1]

        temp_location = f"C:/Users/yoonj/Desktop/project-3-s22-yoonjaejasonlee-main/testing/{user_name}/{repo_name}"

        Repo.clone_from(url, temp_location)

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

        page_num += 1
        while counter < len(list_search):
            code = lizard.analyze_file(list_search[counter])
            total_file += 1
            file_count += 1
            cc = code.CCN
            cc_min = min(cc, cc_min)
            cc_max = max(cc, cc_max)
            line += code.nloc
            cc_avg += cc
            total_line += code.nloc
            counter += 1

        if counter == len(list_search):

            cc_avg = cc_avg / len(list_search)
            insert_query = "INSERT INTO analyze_results (user_name,repo_name, num_files, min_CCN, max_CCN, average_CCN, repo_LOC, cumulative_LOC) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

            try:
                cur.execute(insert_query, (user_name, repo_name, file_count, cc_min, cc_max, cc_avg, line, total_line))
            except mariadb.Error as es:
                print(f"Error: {es}")

            conn.commit()

            print(f"REPO: {user_name}/{repo_name} Successfully Added to the DB")
            cc_avg = 0
            file_count = 0
            cc_min = 0
            cc_max = 0
            line = 0
        analyze(cc_avg, cc_min, cc_max, total_line, file_count, counter, page_num, line, total_file)


if __name__ == "__main__":
    analyze(CC_avg, CC_min, CC_max, total_lines, py_count, i, j, lines, total_files)

    end_time = time.time()
    print(f"Total time cost: {end_time - start_time}")
    print(f"total files: {total_files}")
    print(f"Average time cost per file: {total_files / (start_time - end_time)}")
