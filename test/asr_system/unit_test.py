""" FastAPI のAPIテストを書いていく"""
import requests
import pprint

baseurl = "http://127.0.0.1:5000/api/"

item_data = {
    "attribute": "attribute",
    "audio_path": "/media/wav_data/2022-08-19_test_record_004.wav",
}

r_post = requests.get(baseurl + "inference", json=item_data)

print(r_post.status_code)

pprint.pprint(r_post.json())
