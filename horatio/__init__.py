import time
import fslog

unit = "s"
no_desc_default = "\033[0m\u2510"

def format(t):
    scale = {"s":1, "ms":1000, "us":1000000, "m":1/60, "h":1/3600}
    t *= scale[unit]
    return f"{t:.3f} {unit}"

class step():
    def __init__(self, desc=None):
        self.ts = []
        self.desc = desc

    def __enter__(self):
        if self.desc is None:
            self.desc = ""
        fslog.log(self.desc + " ... ", end="")
        self.ts.append(time.time())
        return self

    def __exit__(self, *args):
        t = self.ts.pop()
        t = time.time() - t
        fslog.plain("done in {}\n".format(format(t)), end="")

    def __call__(self, f):
        if self.desc is None:
            self.desc = f.__name__
        def wrapper(*args, **kwargs):
            self.__enter__()
            y = f(*args, **kwargs)
            self.__exit__()
            return y
        return wrapper

class flat():
    def __init__(self, desc=None, tail=None):
        self.ts = []
        self.desc = desc
        self.tail = tail

    def __enter__(self):
        if self.desc is None:
            fslog.log("[*]")
        else:
            fslog.log(f"[*] {self.desc}")
        self.ts.append(time.time())
        return self

    def __exit__(self, *args):
        t = self.ts.pop()
        t = time.time() - t
        tf = format(t)
        if self.tail is None:
            if self.desc is None:
                fslog.log("[*] {}".format(tf))
            else:
                fslog.log("[*] {}: {}".format(self.desc, tf))
        else:
            fslog.log("[*] {}".format(self.tail).format(self.desc, tf))

    def __call__(self, f):
        if self.desc is None:
            self.desc = f.__name__
        def wrapper(*args, **kwargs):
            self.__enter__()
            y = f(*args, **kwargs)
            self.__exit__()
            return y
        return wrapper

class section():
    def __init__(self, desc=None, tail=None):
        self.ts = []
        self.desc = desc
        self.tail = tail

    def __enter__(self):
        if self.desc is None:
            self.desc = no_desc_default
        fslog.open(self.desc)
        self.ts.append(time.time())
        return self

    def __exit__(self, *args):
        t = self.ts.pop()
        t = time.time() - t
        tf = format(t)
        if self.tail is None:
            if self.desc is None:
                fslog.close("{}".format(tf))
            else:
                fslog.close("{}: {}".format(self.desc, tf))
        else:
            fslog.close(self.tail.format(self.desc, tf))

    def __call__(self, f):
        if self.desc is None:
            self.desc = f.__name__

        def wrapper(*args, **kwargs):
            self.__enter__()
            y = f(*args, **kwargs)
            self.__exit__()
            return y
        return wrapper

fslog.param["indent.str"] += " "
fslog.param["open.style"] = fslog.style.BOLD
