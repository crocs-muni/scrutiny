import argparse
import configparser
import os
import sys

from scrutiny.device import Device, DeviceType
from scrutiny.javacard.toolwrappers.gppro import GPProInfo, GPProList
from scrutiny.javacard.toolwrappers.jcalgtest import JCAlgTestSupport, \
    JCAlgTestPerformance, JCAlgTestVariable
from scrutiny.utils import isdir, errmsg


CFG_FILE = "measure_javacard.ini"


def prepare_results(card_name):
    """
    Creates directory in results/
    :param card_name: card name
    :return: True on success
    """
    dirname = "results/" + card_name
    if isdir(dirname):
        print(dirname, "already exists, skipping the creation.")
        return True
    try:
        print("Creating", dirname + ".")
        os.mkdir(dirname)

        return True
    except FileExistsError as ex:
        return errmsg(dirname, "creating", ex)


def get_subtests(config, config_section):
    subtests = []
    for param in config[config_section]:
        if config[config_section][param].lower() == "yes":
            subtests.append(param)
    return subtests


def help_string(config, config_section):
    speed = {
        "instant":
            "    You can blink once in the meantime\n",
        "fast":
            "    Few minutes to fef hours.\n"
            "    You can go make a coffee.\n",
        "medium":
            "    Up to a few hours.\n"
            "    You can compile Firefox in the meantime.\n",
        "slow":
            "    Up to tens of hours.\n"
            "    You can compile Gentoo in the meantime.\n"
    }

    risk = {
        "low":
            "    The test uses standard JCAPI calls\n",
        "medium":
            "    The tests cause lot of API calls or allocations.\n"
            "    The tests may damage the card.\n",
        "high":
            "    The tests try to cause undefined behavior.\n"
            "    There is a high possibility of bricking the card.\n"
    }

    subtests = get_subtests(config, config_section)

    result = "Configuration: " + config_section + "\n"

    if "speed" in config[config_section]:
        result += "Speed: " + config[config_section]["speed"] + "\n" + \
                  speed.get(config[config_section]["speed"], "")

    if "risk" in config[config_section]:
        result += "Risk: " + config[config_section]["risk"] + "\n" + \
                  risk.get(config[config_section]["risk"], "")

    result += "Subtests:\n    " + "\n    ".join(subtests)

    return result


def get_wrapper(test):
    if test == "gppro_info":
        return GPProInfo(device_name)
    if test == "gppro_list":
        return GPProList(device_name),
    if test == "jcalgtest_support":
        return JCAlgTestSupport(device_name)
    if test == "jcalgtest_performance":
        return JCAlgTestPerformance(device_name)
    if test == "jcalgtest_variable":
        return JCAlgTestVariable(device_name)


if __name__ == "__main__":

    cf = configparser.ConfigParser()
    cf.read(CFG_FILE)

    configurations = []
    for section in cf:
        if section != "DEFAULT":
            configurations.append(section)

    parser = argparse.ArgumentParser()
    parser.add_argument("device_name",
                        help="the name of the device to be used")
    parser.add_argument("-c", "--use-configuration",
                        metavar="cfg",
                        help="Configurations currently defined in "
                             + CFG_FILE + ": " + " ".join(configurations)
                        )
    parser.add_argument("-i", "--info-configuration",
                        metavar="cfg",
                        help="Prints information about configuration")

    args = parser.parse_args()

    if args.info_configuration:
        if args.info_configuration in configurations:
            print(help_string(cf, args.info_configuration))
            exit(0)
        else:
            print("Configuration", args.info_configuration,
                  "not define in " + CFG_FILE)
            exit(1)

    if not args.use_configuration or \
            args.use_configuration not in configurations:
        print("Using default configuration.")
        args.use_configuration = "default"

    device_name = args.device_name.replace(" ", "_")
    device = Device(device_name, DeviceType.JAVA_CARD)
    prepare_results(device_name)

    tool_wrappers = [
        get_wrapper(test) for test in get_subtests(cf, args.use_configuration)
    ]

    for tool in tool_wrappers:
        tool.run()
        device.add_modules(tool.parse())

    with open("results/" + device_name + ".json", "w") as output:
        output.write(str(device))

    sys.exit(0)
