import argparse
from datetime import datetime
from dominate import document, tags
from dominate.util import raw
import jsonpickle

from scrutiny.htmlutils import show_hide_div, show_all_button, hide_all_button, default_button
from scrutiny.interfaces import ContrastState

TOOLTIP_TEXT = {
    ContrastState.MATCH: "Devices seem to match",
    ContrastState.WARN: "There seem to be some differences worth checking",
    ContrastState.SUSPICIOUS: "Devices probably don't match"
}

RESULT_TEXT = {
    ContrastState.MATCH: lambda x:
    "None of the modules raised suspicion during the verification process.",
    ContrastState.WARN: lambda x:
    "There seem to be some differences worth checking. " + str(x) +
    " module(s) report inconsistencies.",
    ContrastState.SUSPICIOUS: lambda x:
    str(x) + " module(s) report suspicious differences between profiled and "
    "reference devices. The verification process may have  been unsuccessful "
    "and compared devices are different."
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verification-profile",
                        help="Input verification JSON profile",
                        action="store", metavar="file",
                        required=True)
    parser.add_argument("-o", "--output-file",
                        help="Name of output file",
                        action="store", metavar="outfile",
                        required=False, default="comparison.html")
    parser.add_argument("-e", "--exclude-style-and-scripts",
                        help="Link CSS and JavaScript from report instead of "
                             "inlining",
                        action="store_true")
    args = parser.parse_args()

    with open("data/script.js", "r", encoding="utf-8") as js, \
            open("data/style.css", "r", encoding="utf-8") as css:
        script = "\n" + js.read() + "\n"
        style = "\n" + css.read() + "\n"

    with open(args.verification_profile, "r") as f:
        contrast = jsonpickle.decode(f.read())

    doc = document(title='Comparison of smart cards')

    with doc.head:
        if args.exclude_style_and_scripts:
            tags.link(rel="stylesheet", href="style.css")
            tags.script(type="text/javascript", src="script.js")
        else:
            tags.style(raw(style))
            tags.script(raw(script), type="text/javascript")

    with doc:

        tags.button("Back to Top", onclick="backToTop()",
                    id="topButton", cls="floatingbutton")
        intro_div = tags.div(id="intro")
        with intro_div:
            tags.h1(
                "Verification of " + contrast.prof_name +
                " against " + contrast.ref_name
            )
            tags.p("Generated on: " +
                   datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            tags.p("Generated from: " + args.verification_profile)
            tags.h2("Verification results")
            tags.h4("Ordered results from tested modules:")

        worst_contrast_state = ContrastState.MATCH
        suspicions = 0

        with tags.div(id="modules"):
            module_count: int = 0
            for m in contrast.contrasts:

                divname = m.module_name + str(module_count)

                contrast_class = m.get_state()
                if contrast_class.value > worst_contrast_state.value:
                    worst_contrast_state = contrast_class

                if contrast_class.value >= ContrastState.WARN.value:
                    suspicions += 1

                with intro_div:
                    with tags.span(cls="dot " + contrast_class.name.lower()):
                        tags.span(
                            TOOLTIP_TEXT[contrast_class],
                            cls="tooltiptext " + contrast_class.name.lower())

                m.project_html_intro()
                module_div = show_hide_div(divname, hide=True)
                with module_div:
                    m.project_html(contrast.ref_name, contrast.prof_name)

                tags.br()
                module_count += 1

        with intro_div:
            tags.br()
            tags.p(RESULT_TEXT[worst_contrast_state](suspicions))

            tags.h3("Quick visibility settings")
            show_all_button()
            hide_all_button()
            default_button()

    with open(args.output_file, "w", encoding="utf-8") as f:
        f.write(str(doc))
