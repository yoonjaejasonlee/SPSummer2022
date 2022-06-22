import threading
import requests
from git.repo.base import Repo



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


# --------------------------------------------
j = 1
queueIT = Queue()
queueWho = Queue()
user = 'yoonjaejasonlee'
token = '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'


def queuing(ss):
    if ss < 2:
        api_url = f"https://api.github.com/search/repositories?q=language:python+stars:%3E=150+forks:%3E=20&page={ss}&per_page=1"

        response = requests.get(api_url, auth=(user, token))

        response_data = response.json()

        for s in response_data["items"]:
            urls = s["url"]
            user_name = s["owner"]["login"]
            repo_name = s["name"]
            queueIT.enqueue(urls)
            print("Queue Size: ", len(queueIT.queue))
            ss += 1
            hub = f"https://github.com/{user_name}/{repo_name}"
            temp_location = f"C:/Users/yoonj/Desktop/project-3-s22-yoonjaejasonlee-main/testing/{repo_name}/{user_name}"
            Repo.clone_from(hub, temp_location)

# def printed(ss):
#     if not queueIT.isEmpty():
#         url = queueIT.peek()
#         queueIT.dequeue()
#
#         api = url
#         api_response = requests.get(api, auth=(user, token))
#         api_response_data = api_response.json()
#
#         user_name = api_response_data["owner"]["login"]
#         repo_name = api_response_data["name"]
#
#         print(f"{user_name}/{repo_name}\n")
#
#     queuing(ss)
#     printed(ss)



if __name__ == "__main__":
    # thread1 = threading.Thread(target=queuing(j))
    # thread2 = threading.Thread(target=printed(j))
    # thread1.start()
    # thread2.start()

    queuing(j)
