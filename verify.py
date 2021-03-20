import argparse
import jsonpickle

from scrutiny.device import load_device
from scrutiny.interfaces import Contrast

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

    reference = load_device(args.reference)
    profile = load_device(args.profile)

    contrast = Contrast(reference.name, profile.name)

    for module in reference.modules.values():
        if module.module_name in profile.modules.keys():
            contrast.add_contrasts(
                module.contrast(profile.modules[module.module_name]))

    with open(args.output_file, "w") as f:
        f.write(jsonpickle.encode(contrast, indent=4))
