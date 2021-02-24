import argparse
import os
import subprocess

from jcpeg.card import Card
from jcpeg.gppro import GPPro
from jcpeg.jcalgtest import JCAlgTest
from jcpeg.utils import isdir, errmsg

def prepare_results(card_name):
    dirname = "results/" + card_name
    if isdir(dirname):
       print(dirname, "already exists, skipping the creation.")
       return True
    try:
        print("Creating", dirname + ".")
        os.mkdir(dirname)
        return True
    except Exception as e:
        return errmsg(dirname, "creating", e)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("card_name",
                        help="the name of the card to be used")
    parser.add_argument("-a", "--atr",
                        help="check card's ART",
                        action="store_true")
    parser.add_argument("-i", "--info",
                        help="check card's basic information",
                        action="store_true")
    parser.add_argument("-l", "--list-applets", dest="list",
                        help="list card's installed applets",
                        action="store_true")
    parser.add_argument("-e", "--essentials",
                        help="perform essential checks: "
                        "ATR, basic information and list installed applets "
                        "(same as -acl)",
                        action="store_true")
    parser.add_argument("-s", "--support",
                        help="check supported JCAPI methods",
                        nargs="?", const=None, metavar="file_in")
    parser.add_argument("-p", "--performance",
                        help="test performance (SLOW)",
                        nargs="?", const=None, metavar="file_in")
    parser.add_argument("-v", "--variable-performance",
                        help="test variable data-langth performance "
                        "(VERY SLOW)",
                        nargs="?", const=None, metavar="file_in")
    parser.add_argument("-j", "--jcalgtest",
                        help="run JCAlgTest in interactive mode",
                        nargs="?", const=None, metavar="file_in")

    args = parser.parse_args()
    if args.essentials:
        args.atr = True
        args.info = True
        args.list = True

    card_name = args.card_name.replace(" ", "_")
    
    prepare_results(card_name)
    
    gppro = GPPro(card_name)
    jcalgtest = JCAlgTest(card_name)

    card = Card(card_name)

    #if args.info:
    #    gppro.run_info()

    gppro.run()
    card.add_modules(gppro.parse())

    #jcalgtest.run_support()

    #print(card)
    
    exit(0)
