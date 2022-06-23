import requests

ss = 1

while ss < 9:
    url = f"http://127.0.0.1:5000/repos/{ss}"
    response = requests.get(url)
    if response.status_code == 200:
        response_data = response.json()

        for s in response_data:
            print(f"repo:{s.rsplit('/', 2)[1]}/{s.rsplit('/', 1)[-1]}")
        ss += 1
    else:
        print("request denied, retrying....")

