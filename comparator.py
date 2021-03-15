import argparse
import jsonpickle

from jcpeg.card import Card, load_card


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
    args = parser.parse_args()

    reference = load_card(args.reference)
    profile = load_card(args.profile)

    contrasts = []

    for module in reference.modules.values():
        if module.id in profile.modules.keys():
            contrasts.extend(module.contrast(profile.modules[module.id]))

    with open("contrast.json", "w") as f:
        f.write(jsonpickle.encode(contrasts, indent=4))
