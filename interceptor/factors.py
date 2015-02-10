parts = [
    r'(?P<host>\S+)',                   # host %h
    r'(?P<user>\S+)',                   # user %u
    r'\[(?P<day>\S{2})\/(?P<month>\S{3})\/(?P<year>\S{4}):(?P<time>.+)\s.+\]',                # time %t
    r'"(?P<request>.+)"',               # request "%r"
    r'(?P<protocol>.*)',               # protocol "%{Protocol}i"
    r'(?P<referer>.*)',               # referer "%{Referer}i"
    r'(?P<status>[0-9]+)',              # status %>s
    r'(?P<size>\S+)',                   # size %b (careful, can be '-')
    r'"(?P<agent>.*)"',                 # user agent "%{User-agent}i"
    r'(?P<hit>\S+)',               # hit "%{Hit}i"
    r'(?P<type>\S+)',               # type "%{Type}i"
    r'\S+',                             # indent %l (unused)
    r'(?P<unused1>.*)',               # unused1 "%{unused1}i"
    r'(?P<unused2>.*)',               # unused2 "%{Unused2}i"
]



res["http_ver"] = res["request"].split()[-1]
    res["method"] = res["request"].split()[0]
    res["request"] = res["request"].split()[-2]




    if res["size"] == "-":
        res["size"] = 0
    else:
        res["size"] = int(res["size"])

    #just to observe the illogically large sizes
    if (res["size"] >= UNREASANABLE_SIZE):
        print "unreasonably large payload ", line
        return None

    if res["referer"] == "-":
        res["referer"] = None

    res["time"] = res["year"]+'-'+months[res["month"]]+'-'+res["day"] + "T" + res["time"]+"Z"
