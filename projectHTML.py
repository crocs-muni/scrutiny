import argparse
import dominate
from dominate.tags import *
import jsonpickle


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--contrast",
                        help="Contrast JSON profile to project",
                        action="store", metavar="file",
                        required=True)
    args = parser.parse_args()

    with open(args.contrast, "r") as f:
        modules = [jsonpickle.decode(f.read())]

    doc = dominate.document(title='Comparison of smart cards')

    with doc.head:
        link(rel="stylesheet", href="style.css")
        script(type="text/javascript", src="script.js")

    with doc:
        with div(id="intro"):
            p("This is the introductory section")

    with open("comparison.html", "w") as f:
        f.write(str(doc))
