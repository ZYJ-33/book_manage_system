import time
from json import loads, dumps

def log(*args, **kwargs):
    print(time.strftime("%Y-%m-%d  %H:%M:%S --- ", time.localtime(time.time())), args, kwargs)

def get_date(howlong):
    start = time.time()
    end = start + 86400*howlong
    start = time.strftime("%Y-%m-%d", time.localtime(start))
    end = time.strftime("%Y-%m-%d", time.localtime(end))
    return start, end

    # return time.strftime("%Y-%m-%d", time.localtime(time.time()))

def date_2_str(data):
    keys = []
    if len(data) > 0:
        for key, val in data[0].items():
            if type(val) != str:
                keys.append(key)
        for d in data:
            for key in keys:
                d[key] = str(d[key])
        return data
    return []

def get_current_date():
    return time.localtime(time.time())

def jsonlify(data):
    return dumps(data, ensure_ascii=False)

def str2date(date_str):
    return time.strptime(date_str, "%Y-%m-%d")

import Model.order
def check_due_thread():
    log("check due thread begin")
    while True:
        Model.order.pending_Orders.check_for_due_order()
        time.sleep(86400)

if __name__ == "__main__":
    ...