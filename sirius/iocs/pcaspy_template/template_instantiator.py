
import os
import shutil


TEMPLATE_DIR = 'template_files'


class TemplateInstatiator:
    
    def __init__(self, args):
        self.name = args.name
        if args.dest is not None:
            self.destination = os.path.realpath(args.dest)
        else:
            self.destination = os.path.realpath(os.curdir)
        s = os.path.dirname(os.path.realpath(__file__))
        self.source = os.path.join(s, TEMPLATE_DIR)
    
    def instantiate(self):
        self._check_destination_empty()
        self._create_directories()
        self._copy_files()
    
    def _check_destination_empty(self):
        contents = os.listdir(self.destination)
        if len(contents) > 0:
            raise Exception('destination directory not empty')
    
    def _create_directories(self):
        os.mkdir(os.path.join(self.destination, self.name))
        os.mkdir(os.path.join(self.destination, 'test'))
    
    def _copy_files(self):
        contents = os.listdir(self.source)
        filenames = [os.path.join(self.source, fn) for fn in contents]
        file_destination = os.path.join(self.destination, self.name)
        for fn in filenames:
            shutil.copy(fn, file_destination)
