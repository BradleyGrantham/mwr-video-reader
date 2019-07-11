def find_jaantr(s: str):
    if "jaantr" in s.lower():
        return "JaAnTr"
    else:
        return s


def find_jakeyy(s: str):
    if "lazyjakeyy" in s.lower():
        return "LazyJakeyy"
    elif "lazylakeyy" in s.lower():
        return "LazyJakeyy"
    elif "lazyakeyy" in s.lower():
        return "LazyJakeyy"
    else:
        return s


def find_bennettar95(s: str):
    if "bennettar95" in s.lower():
        return "bennettar95"
    elif "bennettar9s" in s.lower():
        return "bennettar95"
    else:
        return s


def find_ntsfbrad(s: str, include_bradlx888=True):
    if "ntsfbrad" in s.lower():
        return "ntsfbrad"
    elif "bradbx888" in s.lower() and include_bradlx888:
        return "ntsfbrad"
    elif "bradbx8:88" in s.lower() and include_bradlx888:
        return "nstbrad"
    else:
        return s


def find_jordanx267(s: str):
    if "jordanx267" in s.lower():
        return "Jordanx267"
    else:
        return s


def find_bradlx888(s: str):
    if "bradbx888" in s.lower():
        return "bradlx888"
    elif "bradbx8:88" in s.lower():
        return "bradlx888"
    else:
        return s


def convert_common_ocr_errors(l: list):
    l = [x if x not in ["s", "S"] else 5 for x in l]
    l = [x if x not in ["o", "O"] else 0 for x in l]
    l = [x if x not in ["o", "O"] else 0 for x in l]
    return l