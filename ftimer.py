import time
import flog

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
        flog.log(self.desc + " ... ", end="")
        self.ts.append(time.time())
        return self

    def __exit__(self, *args):
        t = self.ts.pop()
        t = time.time() - t
        flog.plain("took {}\n".format(format(t)), end="")

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
            flog.log("[*]")
        else:
            flog.log(f"[*] {self.desc}")
        self.ts.append(time.time())
        return self

    def __exit__(self, *args):
        t = self.ts.pop()
        t = time.time() - t
        tf = format(t)
        if self.tail is None:
            if self.desc is None:
                flog.log("[*] {}".format(tf))
            else:
                flog.log("[*] {}: {}".format(self.desc, tf))
        else:
            flog.log("[*] {}".format(self.tail).format(self.desc, tf))

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
        flog.open(self.desc)
        self.ts.append(time.time())
        return self

    def __exit__(self, *args):
        t = self.ts.pop()
        t = time.time() - t
        flog.close(self.tail.format(format(t)))


    def __call__(self, f):
        if self.desc is None:
            self.desc = f.__name__
        if self.tail is None:
            self.tail = "{}: {}".format(self.desc, "{}")

        def wrapper(*args, **kwargs):
            self.__enter__()
            y = f(*args, **kwargs)
            self.__exit__()
            return y
        return wrapper

flog.param["indent.str"] += " "
flog.param["open.style"] = flog.style.BOLD
