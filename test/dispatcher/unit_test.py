import requests
import pprint
import json

from create_dummy_data import create_dummy_data

baseurl = "http://127.0.0.1:5001/api/"

id = create_dummy_data()
print(id)
json_data = {"id": id}

r_post = requests.post(baseurl + "id", json=json_data)


print(json.dumps(json_data))
print(r_post.status_code)
