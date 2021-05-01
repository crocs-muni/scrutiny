class URL:
    """
    URL config strings
    """

    GPPRO = "https://github.com/martinpaljak/GlobalPlatformPro/releases/" \
            "download/v20.01.23/gp.jar"

    JCALGTEST = "https://github.com/crocs-muni/JCAlgTest/releases/" \
                "download/v1.8.0/AlgTest_dist_1.8.0.zip"

    SMARTCARD_LIST = "http://ludovic.rousseau.free.fr/softwares/pcsc-tools/" \
                     "smartcard_list.txt"


class Paths:
    """
    Path config strings
    """

    GPPRO = "data/bin/gp.jar"

    JCALGTEST = "data/bin/AlgTestJClient.jar"
    JCALGTEST_305 = "data/cap/AlgTest_v1.8.0_jc305.cap"
    JCALGTEST_304 = "data/cap/AlgTest_v1.8.0_jc304.cap"
    JCALGTEST_222 = "data/cap/AlgTest_v1.8.0_jc222.cap"
    JCALGTEST_CAPS = [JCALGTEST_305, JCALGTEST_304, JCALGTEST_222]

    SMARTCARD_LIST = "data/smartcard_list.txt"


class MeasureJavaCard:
    """
    Measure Java Card script config strings
    """

    CFG_FILE = "config/measure_javacard/configurations.json"

    SPEED = {
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

    RISK = {
        "low":
            "    The test uses standard JCAPI calls\n",
        "medium":
            "    The tests cause lot of API calls or allocations.\n"
            "    The tests may damage the card.\n",
        "high":
            "    The tests try to cause undefined behavior.\n"
            "    There is a high possibility of bricking the card.\n"
    }
