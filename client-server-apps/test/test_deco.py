import json


enable_tracing = True

def log(func):
    print("decorator working")
    try:
        with open('config.json') as f_n:
            print("reading config")
            conf = json.load(f_n)
            f_n.close()
    except: #EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
        conf = {"trace": False}
    enable_tracing = conf["trace"]
    print("enable_tracing = ", enable_tracing)
    if enable_tracing:
        def callf(*args,**kwargs):
            r = func(*args, **kwargs)
            print("%s вернула %s" % (func.__name__, r))
            return r
        return callf
    else:
        return func

@log
def sqr(x):
    return x*x

if __name__ == '__main__':
    print("main working")
    conf = {"trace": True}
    with open('config.json', 'w') as c_j:
        c_j.write(json.dumps(conf, indent=4))
        c_j.close()
    print(sqr(9))
    conf = {"trace": False}
    with open('config.json', 'w') as c_j:
        c_j.write(json.dumps(conf, indent=4))
        c_j.close()
    print(sqr(3))
