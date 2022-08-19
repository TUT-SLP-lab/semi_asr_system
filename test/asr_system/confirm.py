""" FastAPI のAPIテストを書いていく"""
import requests
import pprint

baseurl = "http://127.0.0.1:5000/api/isrun"

r_post = requests.get(baseurl)

print(r_post.status_code)

pprint.pprint(r_post.json())
