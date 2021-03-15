import argparse


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
    print(args.reference, args.profile)
