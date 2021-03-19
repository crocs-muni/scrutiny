from enum import Enum


class Contrast(object):

    def __init__(self, ref_name, prof_name):
        self.ref_name = ref_name
        self.prof_name = prof_name
        self.contrasts = []

    def add_contrasts(self, contrasts):
        self.contrasts.extend(contrasts)


class ContrastModule(object):

    def __init__(self, module_name):
        self.module_name = module_name

    def __str__(self):
        return self.module_name

    def get_state(self):
        pass

    def project_html(self, ref_name, prof_name):
        pass


class ContrastState(Enum):
    MATCH, WARN, SUSPICIOUS = range(3)
