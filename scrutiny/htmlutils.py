# MIT License
#
# Copyright (c) 2020-2024 SCRUTINY developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List, Optional, Callable, Tuple
import uuid
from dominate import tags

from scrutiny.interfaces import ContrastState

shown = []
hidden = []


def note(text: str) -> None:
    """Print note to HTML output"""
    tags.p(text)


def table(
        data: List[List[str]],
        header: Optional[List[str]] = None,
        green_value: Optional[str] = None,
        red_value: Optional[str] = None,
        red_predicate: Optional[Callable] = None
) -> None:
    """
    Print table to HTML output
    :param data: List of lines, each containing list of cell data
    :param header: optional list of header cells, no header if None or empty
    :param green_value: cell value content to highlight in green
    :param red_value: cell value content to highlight in red
    :param red_predicate: predicate on line to highlight in red
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
                    if red_predicate and red_predicate(line):
                        color = "var(--red-color)"
                    tags.td(cell, style="color:" + color)

def generate_piechart(percentages : List[float], rgb_colors : List[Tuple[int, int, int]]) -> str:
    """
    Generates specific pie chart into styles and returns class name for that pie chart
    """
    rgb_format = "rgb({r}, {g}, {b}) {percentage}%"
    pie_chart_format : str = "background: conic-gradient({color_percentages}); border-radius: 50%; position: relative; width: 35px; min-height: 35px; margin: 0; vertical-align: middle; display: inline-block;"
    colors = None
    last_value = 0
    for i in range(len(percentages)):
        if (percentages[i] == 0):
            continue
        last_value += percentages[i]
        if (i == (len(percentages) - 1)):
            last_value = 100;
        if (colors != None):
            colors += ", " + rgb_format.format(r = rgb_colors[i][0], g = rgb_colors[i][1], b = rgb_colors[i][2], percentage = 0)
            colors += ", " + rgb_format.format(r = rgb_colors[i][0], g = rgb_colors[i][1], b = rgb_colors[i][2], percentage = last_value)
        else:
            colors = rgb_format.format(r = rgb_colors[i][0], g = rgb_colors[i][1], b = rgb_colors[i][2], percentage = 0)
            colors += ", " + rgb_format.format(r = rgb_colors[i][0], g = rgb_colors[i][1], b = rgb_colors[i][2], percentage = last_value)
    return pie_chart_format.format(color_percentages = colors)

def generate_gallery(comparisons : List[Tuple[str, str]]):
    uid = str(uuid.uuid4())
    unique_id = "imageContainer-" + uid
    image_id = "imageText-" + uid
    div_wrapper = tags.div(cls="container-common")
    with div_wrapper:
        row = tags.div(cls="row container-common")
        with row:
            for comp in comparisons:
                column = tags.div(cls="column container-common", style="background-color: {color}".format(color = getStateStyle(comp[1])))
                with column:
                    tags.img(
                        src=comp[0],
                        alt=comp[0],
                        style="width: 100%; background-color: {color}".format(color = getStateStyle(comp[1])),
                        onclick="displayImage(this, '{img_id}', '{text_id}');".format(img_id=unique_id, text_id=image_id))
        div_container = tags.div(cls="container")
        with div_container:
            tags.span("X", onclick="this.parentElement.style.display='none'", cls="closebtn")
            tags.img(id=unique_id, style="width: 100%")
            tags.div(id=image_id, cls="container-common")
    return div_container

def getStateStyle(state : str) -> str:
    if (state == str(ContrastState.MATCH)):
        return "rgb(76,175,80,0.25)"
    elif (state == str(ContrastState.WARN)):
        return "rgb(211,208,62,0.25)"
    else:
        return "rgb(192,68,68,0.25)"

def show_hide_div(divname: str, hide=False):
    """
    Creates a show/hide button and matching div block
    :param divname: unique name of the div block
    :param hide: the div block is hidden by default if True
    :return: the div block
    """

    if hide:
        hidden.append(divname)
    else:
        shown.append(divname)

    tags.button("Show / Hide",
                onclick="hideButton('" + divname + "')")
    tags.br()

    if hide:
        return tags.div(id=divname, style="display:none")

    return tags.div(id=divname)

def show_hide_div_right(divname: str, hide=False):
    """
    Creates a show/hide button and matching div block
    :param divname: unique name of the div block
    :param hide: the div block is hidden by default if True
    :return: the div block
    """

    if hide:
        hidden.append(divname)
    else:
        shown.append(divname)

    tags.button("Show / Hide",
                onclick="hideButton('" + divname + "')",
                style="float: right center;")
    tags.br()

    if hide:
        return tags.div(id=divname, style="display:none")

    return tags.div(id=divname)


def show_all_button():
    """Creates a Show All button for every show/hide div block created"""

    tags.button("Show All",
                onclick="showAll(" + __get_js_array(__get_all_names()) + ")")


def hide_all_button():
    """Creates a Hide All button for every show/hide div block created"""

    tags.button("Hide All",
                onclick="hideAll(" + __get_js_array(__get_all_names()) + ")")


def default_button():
    """Creates a Hide All button for every show/hide div block created"""

    tags.button("Default",
                onclick="defaultAll(" + __get_js_array(shown) + ", " +
                        __get_js_array(hidden) + ")")


def __get_js_array(names):
    return "[" + ", ".join(["'" + entry + "'" for entry in names]) + "]"


def __get_all_names():
    div_names = []
    div_names.extend(hidden)
    div_names.extend(shown)
    return div_names
