import argparse
import dominate
from dominate.tags import *
from dominate.util import raw
import jsonpickle

from scrutiny.contrast import Contrast
from scrutiny.interfaces import ContrastState


TOOLTIPTEXT = {
    ContrastState.MATCH : "The cards seem to match",
    ContrastState.WARN : "There seem to be some differencies worth checking",
    ContrastState.SUSPICIOUS : "The cards probably don't match"
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

    doc = dominate.document(title='Comparison of smart cards')

    with doc.head:
        link(rel="stylesheet", href="style.css")
        script(type="text/javascript", src="script.js")

    with doc:
        with div(id="intro"):
            p("This is the introductory section")

        with div(id="modules"):

            module_count = 0
            for m in contrast.contrasts:
                divname = m.module_name + str(module_count)
                h2("Module: " + str(m), style="display: inline-block;")
                contrast_class = m.get_state()
                with span(cls = "dot " + contrast_class.name.lower()):
                    span(TOOLTIPTEXT[contrast_class],
                            cls = "tooltiptext " + contrast_class.name.lower())
                button("Show / Hide", onclick="hideButton('" + divname + "')")
                with div(id=divname):
                    m.project_HTML(contrast.ref_name, contrast.prof_name)
                br()
                module_count += 1
                

    with open(args.output_file, "w") as f:
        f.write(str(doc))
