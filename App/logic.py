from git.repo.base import Repo

url = "https://github.com/apache/airflow/"

temp_location = f"C:/Users/yoonj/Desktop/testing/apache/airflow"

Repo.clone_from(url, temp_location)
