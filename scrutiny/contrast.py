from enum import Enum


class Contrast:
    """
    Contrast in-memory representation
    """

    def __init__(self, ref_name, prof_name):
        self.ref_name = ref_name
        self.prof_name = prof_name
        self.contrasts = []

    def add_contrasts(self, contrasts):
        """
        Add contrasts to the list
        :param contrasts:
        :return:
        """
        self.contrasts.extend(contrasts)


class ContrastModule:
    """
    SCRUTINY Contrast module
    """

    def __init__(self, module_name):
        self.module_name = module_name

    def __str__(self):
        return self.module_name

    def get_state(self):
        """
        Get ContrastState according to the module-specific internal state
        :return:
        """

    def project_html(self, ref_name: str, prof_name: str) -> None:
        """
        Represent contrast using dominate tags
            happens within dominate div tag

        :param ref_name: Reference device name
        :param prof_name: Profile device name
        """


class ContrastState(Enum):
    """
    Contrast State representation
    """
    MATCH, WARN, SUSPICIOUS = range(3)
