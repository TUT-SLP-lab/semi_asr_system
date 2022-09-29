import requests
import pprint
import json
import os
from dotenv import load_dotenv

load_dotenv()

baseurl = f"http://{os.getenv('DISPATCHER_IP')}:{os.getenv('DISPATCHER_PORT')}/api/"

# json_data = {"id": "62ff681138a355785e453b8c"}
# r_post = requests.post(baseurl + "id", json=json_data)

json_data = {"text_path": "aaa"}
r_post = requests.put(baseurl + "update", json=json_data)


print(json.dumps(json_data))
print(r_post.status_code)
print(r_post.json())
