import requests
import re

URL = "http://localhost:8000/"
patt = re.compile(r'Coffee')

s = requests.Session()
for i in range(1001):
    res = s.get(URL)
    # print(res.text)
    num = re.findall(patt, res.text)
    # print(len(num))
    is_correct = s.post(URL, data={"num": len(num) - 1})
    print(is_correct.text)
