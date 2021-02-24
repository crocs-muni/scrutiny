import os

from jcpeg.config import Paths
from jcpeg.interfaces import Module, ToolWrapper
from jcpeg.utils import execute_cmd, isfile

class JCAlgTest(ToolWrapper):

    BIN = "java -jar " + Paths.JCALGTEST
    CAPS = Paths.JCALGTEST_CAPS

    def __init__(self, card_name, force_mode=False):
        super().__init__(card_name, force_mode)
        self.install()
        self.support_file = None
        self.performance_file = None
        self.variable_file = None

    def install(self):
        for applet in Paths.JCALGTEST_CAPS:
            cmd_line = "java -jar bin/gp.jar -install " + applet
            if execute_cmd(cmd_line) == 0:
                break

    def is_support_file(self):
        if self.support_file:
            return self.support_file
        for file in os.listdir("results/" + self.card_name):
            if "ALGSUPPORT" in file:
                self.support_file = file
        return self.support_file
    
    def run_support(self):
        if self.is_support_file():
            print("Skipping JCAlgTest Algorithm Support")
            return 0
        
        cmd_line = self.BIN
        retcode = execute_cmd(cmd_line)

        for file in os.listdir("./"):
            if "ALGSUPPORT" in file and self.card_name in file:
                dest = "results/" + self.card_name + "/" + file
                os.replace(file, dest)
                self.support_file = file
                break

        return retcode

    def parse_support(self):
        pass

    def parse_performance(self):
        pass

    def run(self):
        self.run_support()
