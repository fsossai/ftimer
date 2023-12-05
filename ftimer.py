import time
import flog

unit = "s"
no_text_default = "\033[0m\u2510"

def format(t):
    scale = {"s":1, "ms":1000, "us":1000000, "m":1/60, "h":1/3600}
    t *= scale[unit]
    return f"{t:.3f} {unit}"

class step():
    def __init__(self, text=None):
        self.ts = []
        self.text = text

    def __enter__(self):
        if self.text is None:
            self.text = ""
        flog.log(self.text + " ... ", end="")
        self.ts.append(time.time())
        return self

    def __exit__(self, *args):
        t = self.ts.pop()
        t = time.time() - t
        flog.plain("took {}\n".format(format(t)), end="")

    def __call__(self, f):
        if self.text is None:
            self.text = f.__name__
        def wrapper(*args, **kwargs):
            self.__enter__()
            y = f(*args, **kwargs)
            self.__exit__()
            return y
        return wrapper

class flat():
    def __init__(self, text=None):
        self.ts = []
        self.text = text

    def __enter__(self):
        if self.text is None:
            self.text = "?"
        flog.log(f"[*] Running: {self.text}")
        self.ts.append(time.time())
        return self

    def __exit__(self, *args):
        t = self.ts.pop()
        t = time.time() - t
        tf = format(t)
        flog.log(f"[*] {self.text}: took {tf}")

    def __call__(self, f):
        if self.text is None:
            self.text = f.__name__
        def wrapper(*args, **kwargs):
            self.__enter__()
            y = f(*args, **kwargs)
            self.__exit__()
            return y
        return wrapper

class section():
    def __init__(self, text=None):
        self.ts = []
        self.text = text

    def __enter__(self):
        if self.text is None:
            self.text = no_text_default
        flog.open(self.text)
        self.ts.append(time.time())
        return self

    def __exit__(self, *args):
        t = self.ts.pop()
        t = time.time() - t
        flog.close("Elapsed: {}".format(format(t)))

    def __call__(self, f):
        if self.text is None:
            self.text = f.__name__
        def wrapper(*args, **kwargs):
            self.__enter__()
            y = f(*args, **kwargs)
            self.__exit__()
            return y
        return wrapper

flog.param["open.style"] = flog.style.BOLD
