from os import replace, remove
from shutil import copyfileobj, rmtree
import subprocess
import sys
from urllib.request import urlopen
from zipfile import ZipFile

from scrutiny.config import URL, Paths
from scrutiny.utils import errmsg


def download_file(tool_name, tool_url, tool_path):
    """
    Downloads file and saves it to tool_path
    :param tool_name:
    :param tool_url:
    :param tool_path:
    :return:
    """
    print("Downloading " + tool_name + "... ", end="")
    try:
        with urlopen(tool_url) as remote, open(tool_path, "wb") as file:
            copyfileobj(remote, file)
        print("Done.")
        return True
    except Exception as ex:
        return errmsg(tool_name, "downloading", ex)


def download_and_extract(tool_name, tool_url, file_translations):
    """
    Downloads zip archive and extracts it's contents
    :param tool_name:
    :param tool_url:
    :param file_translations:
    :return:
    """

    archive = tool_name + "_dist.zip"
    directory = tool_name + "_extracted"

    if not download_file(tool_name, tool_url, archive):
        return False

    print("Extracting " + tool_name + "... ", end="")
    try:
        with ZipFile(archive, "r") as zipped:
            zipped.extractall(directory)
        print("Done.")
    except Exception as ex:
        errmsg(tool_name, "extracting", ex)
        try:
            remove(archive)
        except Exception as ex:
            print(archive,
                  " could not be removed, please remove it manually.", ex)
        return False

    return_status = True

    print("Finishing " + tool_name + " set-up...", end="")
    try:
        for (original, destination) in file_translations:
            replace(directory + "/" + original, destination)
        print("Done.")
    except Exception as ex:
        errmsg(tool_name + " files", "moving", ex)
        return_status = False

    print("Cleaning up after " + tool_name + " set-up...", end="")
    try:
        remove(archive)
        rmtree(directory)
        print("Done.")
    except Exception as ex:
        errmsg(tool_name + " set-up", "cleaning after", ex)
        print("\tRemove", archive, "and", directory, "directory manually.")
        return_status = False

    return return_status


def pip_install(package):
    """
    Installs pip package
    :param package:
    :return:
    """
    try:
        print("Installing package", package, "with pip...")
        subprocess.check_call([sys.executable,
                               "-m", "pip", "install",
                               package])
        print("Done.")
        return True
    except Exception as ex:
        errmsg(package, "installing", ex)
        return False


def setup_jcalgtest():
    """
    Sets up JCAlgTest binaries and cap files
    :return:
    """
    jc_files = [Paths.JCALGTEST,
                Paths.JCALGTEST_305,
                Paths.JCALGTEST_304,
                Paths.JCALGTEST_222]

    jc_translations = [(dest.split("/")[-1], dest) for dest in jc_files]

    return download_and_extract("JCAlgTest", URL.JCALGTEST, jc_translations)


if __name__ == "__main__":

    return_value: bool = True

    print("Setting up Smart Card List:")
    return_value = return_value and \
        download_file("Smart Card List",
                      URL.SMARTCARD_LIST, Paths.SMARTCARD_LIST)

    print("Setting up GlobalPlatformPro:")
    return_value = return_value and \
        download_file("GlobalPlatformPro", URL.GPPRO, Paths.GPPRO)

    print()

    print("Setting up JCAlgTest:")
    return_value = return_value and setup_jcalgtest()

    print()

    print("Setting up jsonpickle:")
    return_value = return_value and pip_install("jsonpickle")

    print()

    print("Setting up dominate:")
    return_value = return_value and pip_install("dominate")

    print()
    if not return_value:
        print("Issues occured during set-up.",
              "Check the manual set-up section in README.md for assistance.")
        sys.exit(1)
    print("Set-up completed without issues.")
    sys.exit(0)
