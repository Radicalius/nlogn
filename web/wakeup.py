import requests, time, logging, traceback as tb, sys

while True:
    try:
        requests.get("http://nlogn.blog")
    except:
        exc_type, exc_value, exc_tb = sys.exc_info()
        logging.error(tb.format_exception(exc_type, exc_value, exc_tb))
    time.sleep(300)
