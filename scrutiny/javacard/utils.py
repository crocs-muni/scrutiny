from typing import List

from scrutiny.config import Paths


def find_atr_in_database(atr: str) -> List[str]:
    """
    Searches atr in local copy of known smart card ATR list:
    http://ludovic.rousseau.free.fr/softwares/pcsc-tools/smartcard_list.txt

    :param atr: card's ATR
    :return: All the matching information pieces in a list,
             empty list if no matching ATR is found in the list
    """

    with open(Paths.SMARTCARD_LIST, "r", encoding="utf8") as f:
        lines = f.readlines()

    info = []

    for i, line in enumerate(lines):
        if atr in line.strip().replace(" ", ""):
            j = 1
            while lines[i+j].startswith("\t"):
                info.append(lines[i+j].strip())
                j += 1

    return info
