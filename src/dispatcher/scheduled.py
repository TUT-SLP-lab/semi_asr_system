import schedule
from time import sleep
import requests

url = "http://172.0.0.1:5001/api/delete"

def task():
    requests.delete(url)

# app.delete()を定期実行
schedule.every(1).hours.do(task)

while True:
    schedule.run_pending()
    sleep(1)

