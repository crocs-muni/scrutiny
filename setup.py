from os import replace, remove
from shutil import copyfileobj, rmtree
from urllib.request import urlopen
from zipfile import ZipFile

from config import URL, Paths

PATH_PREFIX_LENGTH = 4

JC_DIST = "AlgTest_dist.zip"
JC_DIR = "AlgTest_dist"
JC_FILES = [Paths.JCALGTEST,
            Paths.JCALGTEST_305,
            Paths.JCALGTEST_304,
            Paths.JCALGTEST_222]


def download_file(tool_name, tool_url, tool_path):
    print("Downloading " + tool_name + "... ", end="")
    try:
        with urlopen(tool_url) as remote, open(tool_path, "wb") as file:
            copyfileobj(remote, file)
        print("Done.")
        return True
    except:
        print("Oops!\n"
              "\tSomething went wrong while downloading " + tool_name + ".\n"
              "\tPlease try again or check the set-up section in README.md")
        return False

def setup_jcalgtest():
    
    if not download_file("JCAlgTest", URL.JCALGTEST, JC_DIST):
        return False
    
    print("Extracting JCAlgTest... ", end="")
    try:
        with ZipFile(JC_DIST, "r") as zipped:
            zipped.extractall(JC_DIR)
        print("Done.")
    except:
        print("Oops!\n"
              "\tSomething went wrong while extracting JCAlgTest.\n"
              "\tPlease try again or check the set-up section in README.md")
        try:
            remove(JC_DIST)
        except:
            print(JC_DIST,
                  " could not be removed, please remove it manually.")
        return False

    retval = True
    
    print("Finishing JCAlgTest set-up...", end="")
    try:
        for file in JC_FILES:
            replace(JC_DIR + "/" + file[PATH_PREFIX_LENGTH:], file)
        print("Done.")
    except:
        print("Oops!\n"
              "\tSomething went wrong while moving JCAlgTest files.\n"              "\tPlease try again or check the set-up section in README.md")
        retval = False
    
    print("Cleaning up after JCAlgTest set-up...", end="")
    try:
        remove(JC_DIST)
        rmtree(JC_DIR)
        print("Done.")
    except:
        print("Oops!\n"
              "\tSomething went wrong while cleaning JCAlgTest files.\n"
              "\tRemove", JC_DIST, "and", JC_DIR, "manually.")
        retval = False

    return retval 
    
    
if __name__ == "__main__":

    print("Setting up GlobalPlatformPro:")
    download_file("GlobalPlatformPro", URL.GPPRO, Paths.GPPRO)

    print("\nSetting up JCAlgTest:")
    setup_jcalgtest()

