class Contrast(object):

    def __init__(self, ref_name, prof_name):
        self.ref_name = ref_name
        self.prof_name = prof_name
        self.contrasts = []

    def add_contrasts(self, contrasts):
        self.contrasts.extend(contrasts)
