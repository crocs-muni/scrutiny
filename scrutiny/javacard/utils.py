from scrutiny.config import Paths


def get_smart_card(atr):

    with open(Paths.SMARTCARD_LIST, "r", encoding="utf8") as f:
        lines = f.readlines()

    info = []

    for i in range(len(lines)):
        if atr in lines[i].strip().replace(" ", ""):
            j = 1
            while lines[i+j].startswith("\t"):
                info.append(lines[i+j].strip())
                j += 1

    return info