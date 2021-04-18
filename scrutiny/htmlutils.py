from typing import List, Optional

from dominate import tags


def note(text: str) -> None:
    """Print note to HTML output"""
    tags.p(text)


def table(
        data: List[List[str]],
        header: Optional[List[str]] = None,
        green_value: Optional[str] = None,
        red_value: Optional[str] = None
) -> None:
    """
    Print table to HTML output
    :param data: List of lines, each containing list of cell data
    :param header: optional list of header cells, no header if None or empty
    :param green_value: cell value content to highlight in green
    :param red_value: cell value content to highlight in red
    """

    with tags.table():

        if header:
            with tags.tr():
                for cell in header:
                    tags.th(cell)

        for line in data:
            with tags.tr():
                for cell in line:
                    color = "var(--main-color)"
                    if green_value and green_value in cell:
                        color = "var(--green-color)"
                    if red_value and red_value in cell:
                        color = "var(--red-color)"
                    tags.td(cell, style="color:" + color)


def show_hide_div(divname: str, hide=False):
    """
    Creates a show/hide button and matching div block
    :param divname: unique name of the div block
    :param hide: the div block is hidden by default if True
    :return: the div block
    """

    tags.button("Show / Hide",
                onclick="hideButton('" + divname + "')")
    tags.br()

    if hide:
        return tags.div(id=divname, style="display:none")

    return tags.div(id=divname)
