import argparse
import jsonpickle

from jcpeg.card import Card, load_card
from jcpeg.contrast import Contrast


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--reference",
                        help="Reference profile",
                        action="store", metavar="file",
                        required=True)
    parser.add_argument("-p", "--profile",
                        help="Profile to compare against reference",
                        action="store", metavar="file",
                        required=True)
    parser.add_argument("-o", "--output-file",
                        help="Name of output file",
                        action="store", metavar="outfile",
                        required=False, default="contrast.json")
    args = parser.parse_args()

    reference = load_card(args.reference)
    profile = load_card(args.profile)

    contrast = Contrast(reference.name, profile.name)
    
    for module in reference.modules.values():
        if module.id in profile.modules.keys():
            contrast.add_contrasts(module.contrast(profile.modules[module.id]))
    
    with open(args.output_file, "w") as f:
        f.write(jsonpickle.encode(contrast, indent=4))
