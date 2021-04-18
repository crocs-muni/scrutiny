from typing import List, Optional

from dominate import tags


def note(text: str) -> None:
    """Print note to HTML output"""
    tags.p(text)


def table(data: List[List[str]], header: Optional[List[str]]) -> None:
    """
    Print table to HTML output
    :param data: List of lines, each containing list of cell data
    :param header: optional list of header cells, no header if None or empty
    """

    with tags.table():

        if header:
            with tags.tr():
                for cell in header:
                    tags.th(cell)

        for line in data:
            with tags.tr():
                for cell in line:
                    tags.td(cell)
