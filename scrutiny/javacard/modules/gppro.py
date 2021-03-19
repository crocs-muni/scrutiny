from scrutiny.interfaces import Module


class GPInfo(Module):
    """
    SCRUTINY GlobalPlatformPro Basin Info module
    """

    def __init__(self, module_name="GPPro Basic Info"):
        super().__init__(module_name)
        self.iin = None
        self.cin = None
        self.supports = []
        self.versions = []
        self.other = []


class GPList(Module):
    """
        SCRUTINY GlobalPlatformPro Applet List module
    """

    def __init__(self, module_name="GPPro Applet List"):
        super().__init__(module_name)
        self.isd = None
        self.app = []
        self.pkg = []
