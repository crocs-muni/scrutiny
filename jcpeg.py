import subprocess
from sys import argv

GP_PRO = "java -jar bin/gp.jar"

JCALGTEST = "java -jar bin/AlgTestJClient.jar"

CAPS = "cap/"
ALGTEST_305 = "AlgTest_v1.8.0_jc305.cap"
ALGTEST_304 = "AlgTest_v1.8.0_jc304.cap"
ALGTEST_222 = "AlgTest_v1.8.0_jc222.cap"

def prepare_results(card_name):
    cmd_line = "mkdir " + card_name
    process = subprocess.Popen(cmd_line, shell=True)
    out = process.communicate()[0]
    rc = process.returncode

def cleanup(card_name):
    cmd_line = "rm -rf " + card_name
    process = subprocess.Popen(cmd_line, shell=True)
    out = process.communicate()[0]
    rc = process.returncode

def run_gp_info(card_name):
    cmd_line = GP_PRO + " -info > " + card_name + "/gp_info.txt"
    process = subprocess.Popen(cmd_line, shell=True)
    out = process.communicate()[0]
    rc = process.returncode

def run_gp_list(card_name):
    cmd_line = GP_PRO + " -list > " + card_name + "/gp_list.txt"
    process = subprocess.Popen(cmd_line, shell=True)
    out = process.communicate()[0]
    rc = process.returncode

def install_jcalgtest():
    for applet in [ALGTEST_305, ALGTEST_304, ALGTEST_222]:
        cmd_line = GP_PRO + " -install " + CAPS + applet
        process = subprocess.Popen(cmd_line, shell=True)
        out = process.communicate()[0]
        if process.returncode == 0:
            break

def run_jcalgtest(card_name):
    
    install_jcalgtest()
    
    cmd_line = JCALGTEST
    process = subprocess.Popen(cmd_line, shell=True)
    out = process.communicate()[0]
    rc = process.returncode
    

def print_help():
    print("script.py [Card Name]")
    

if __name__ == "__main__":
    argc = len(argv)

    if argc < 2:
        print_help()
        exit(1)

    card_name = argv[1]

    prepare_results(card_name)

    run_gp_info(card_name)
    run_gp_list(card_name)

    run_jcalgtest(card_name)

    #cleanup(card_name)
    
    exit(0)
