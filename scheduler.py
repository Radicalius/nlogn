import requests
import datetime
import time

jobs = [
    (lambda h,m: True, lambda: requests.get("http://www.nlogn.blog"))
]

while True:
    time.sleep(60)
    now = datetime.datetime.now()
    for job in jobs:
        if jobs[0](now.hour, now.minute):
            jobs[1]()
