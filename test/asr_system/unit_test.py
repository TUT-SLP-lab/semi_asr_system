""" FastAPI のAPIテストを書いていく"""
import requests
import pprint

baseurl = "http://0.0.0.0:5000/api/"

item_data = {
    "attribute": "attribute",
    "audio_path": "/mnt/wav_data/K006_003a_IC0A.wav",
}

r_post = requests.post(baseurl + "inference", json=item_data)

print(r_post.status_code)

pprint.pprint(r_post.json())
