from jcpeg.interfaces import Module


class JCSupport(Module):
    def __init__(self, moduleid="jcsupport"):
        super().__init__(moduleid)
        self.test_info = {}
        self.jcsystem = {}
        self.cplc = {}
        self.support = {}
