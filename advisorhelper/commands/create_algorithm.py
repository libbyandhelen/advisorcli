import os

from shutil import copy2

from advisorhelper import templates


class Command:
    def __init__(self, args, path):
        self.args = args
        self.path = path
        self.templates_base_dir = list(templates.__path__)[0]
        self.templates_algo_dir = os.path.join(self.templates_base_dir, "algorithm")
        self.algo_dir = os.path.join(path, args)

    def run(self):
        self._copydir(self.templates_base_dir, self.algo_dir)
        print("new algorithm created in: "+ self.algo_dir)

    def _copydir(self, src, dst):
        names = os.listdir(src)
        if not os.path.exists(dst):
            os.makedirs(dst)

        for name in names:
            srcname = os.path.join(src, name)
            dstname = os.path.join(dst, name)
            if os.path.isdir(srcname):
                self._copydir(srcname, dstname)
            else:
                copy2(srcname, dstname)

