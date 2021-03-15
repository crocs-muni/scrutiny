import argparse
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

    print(jsonpickle.encode(modules, indent=4))
