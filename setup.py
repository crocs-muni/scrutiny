from os import replace, remove
from shutil import copyfileobj, rmtree
from urllib.request import urlopen
from zipfile import ZipFile

from config import URL, Paths


def errmsg(tool_name, action, e):
    print("Oops!\n"
          "\tSomething went wrong while", action, tool_name + ":\n",
          str(e),
          "\tPlease try again or check the manual set-up section in README.md")
    return False


def download_file(tool_name, tool_url, tool_path):
    print("Downloading " + tool_name + "... ", end="")
    try:
        with urlopen(tool_url) as remote, open(tool_path, "wb") as file:
            copyfileobj(remote, file)
        print("Done.")
        return True
    except Exception as e:
        return errmsg(tool_name, "downloading", e)


def download_and_extract(tool_name, tool_url, file_translations):

    archive = tool_name + "_dist.zip"
    directory = tool_name + "_extracted"

    if not download_file(tool_name, tool_url, archive):
        return False

    print("Extracting " + tool_name + "... ", end="")
    try:
        with ZipFile(archive, "r") as zipped:
            zipped.extractall(directory)
        print("Done.")
    except Exception as e:
        errmsg(tool_name, "extracting", e)
        try:
            remove(archive)
        except Exception as e:
            print(archive,
                  " could not be removed, please remove it manually.", e)
        return False

    retval = True

    print("Finishing " + tool_name + " set-up...", end="")
    try:
        for (original, destination) in file_translations:
            replace(directory + "/" + original, destination)
        print("Done.")
    except Exception as e:
        errmsg(tool_name + " files", "moving", e)
        retval = False

    print("Cleaning up after " + tool_name + " set-up...", end="")
    try:
        remove(archive)
        rmtree(directory)
        print("Done.")
    except Exception as e:
        errmsg(tool_name + " set-up", "cleaning after", e)
        print("\tRemove", archive, "and", directory, "directory manually.")
        retval = False

    return retval


def setup_jcalgtest():

    jc_files = [Paths.JCALGTEST,
                Paths.JCALGTEST_305,
                Paths.JCALGTEST_304,
                Paths.JCALGTEST_222]

    jc_translations = [(dest.split("/")[-1], dest) for dest in jc_files]

    download_and_extract("JCAlgTest", URL.JCALGTEST, jc_translations)


if __name__ == "__main__":

    retval = True

    print("Setting up GlobalPlatformPro:")
    retval = retval and \
        download_file("GlobalPlatformPro", URL.GPPRO, Paths.GPPRO)

    print()

    print("Setting up JCAlgTest:")
    retval = retval and \
        setup_jcalgtest()

    print()
    if not retval:
        print("Issues occured during set-up.",
              "Check the manual set-up section in README.md for assistance.")
        exit(1)
    print("Set-up completed without issues.")
    exit(0)
