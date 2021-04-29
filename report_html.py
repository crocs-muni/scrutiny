import argparse
from datetime import datetime
from dominate import document, tags
import jsonpickle

from scrutiny.htmlutils import show_hide_div, show_all_button,\
    hide_all_button, default_button
from scrutiny.interfaces import ContrastState


TOOLTIP_TEXT = {
    ContrastState.MATCH: "The cards seem to match",
    ContrastState.WARN: "There seem to be some differences worth checking",
    ContrastState.SUSPICIOUS: "The cards probably don't match"
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--contrast",
                        help="Contrast JSON profile to project",
                        action="store", metavar="file",
                        required=True)
    parser.add_argument("-o", "--output-file",
                        help="Name of output file",
                        action="store", metavar="outfile",
                        required=False, default="comparison.html")
    args = parser.parse_args()

    with open(args.contrast, "r") as f:
        contrast = jsonpickle.decode(f.read())

    doc = document(title='Comparison of smart cards')

    with doc.head:
        tags.link(rel="stylesheet", href="style.css")
        tags.script(type="text/javascript", src="script.js")

    with doc:
        intro_div = tags.div(id="intro")
        with intro_div:
            tags.p("This is the introductory section")
            tags.p("Generated on: " +
                   datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

        with tags.div(id="modules"):
            module_count: int = 0
            for m in contrast.contrasts:
                divname = m.module_name + str(module_count)
                contrast_class = m.get_state()
                with tags.span(cls="dot " + contrast_class.name.lower()):
                    tags.span(
                        TOOLTIP_TEXT[contrast_class],
                        cls="tooltiptext " + contrast_class.name.lower())
                tags.h2("Module: " + str(m), style="display: inline-block;")
                module_div = show_hide_div(divname)
                with module_div:
                    m.project_html(contrast.ref_name, contrast.prof_name)
                tags.br()
                module_count += 1

        with intro_div:
            show_all_button()
            hide_all_button()
            default_button()

    with open(args.output_file, "w") as f:
        f.write(str(doc))
