import requests
import pprint
import json

baseurl = "http://127.0.0.1:5001/api/"

# json_data = {"id": "62ff681138a355785e453b8c"}
# r_post = requests.post(baseurl + "id", json=json_data)

json_data = {"text_path": "aaa"}
r_post = requests.put(baseurl + "update", json=json_data)


print(json.dumps(json_data))
print(r_post.status_code)
print(r_post.json())
