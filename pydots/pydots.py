# -*- coding: utf-8 -*-
import logging
import os
import yaml
import pprint
from pydots import __author__ as AUTHOR
from pydots import __email__ as EMAIL
from pydots import __version__ as VERSION

log = logging.getLogger()
console = logging.StreamHandler()
format_str = '%(asctime)s\t%(levelname)s:\t %(message)s'
console.setFormatter(logging.Formatter(format_str))
log.addHandler(console)
log.setLevel(logging.DEBUG)

class MissingPyDotsConfException(Exception): pass
class ValidationException(Exception): pass


class Task(object):
    def __init__(self, task, name=None, *args, **kwargs):
        try:
            self.name = name
            self.variation = task.get('variation')
            self.run = task.get('run')
            self.scripts = task.get('scripts')
            self.files = task.get('files')
        except:
            pass
        log.debug('Created task {}'.format(self))

    def __repr__(self):
        return '<Task name="{name}", variation="{variation}", run={_run}, scripts={_scripts}, files={_files}>'.format(
            _run=True if self.run is not None else False,
            _scripts=True if self.scripts is not None else False,
            _files=True if self.files is not None else False,
            **self.__dict__
            )

    def validate(self):
        log.debug('Validating task {}'.format(self))

        count = 0
        if self.name is None:
            log.error(ValidationException('--> "name" must not be empty'))
            count += 1
        if type(self.variation) is not str:
            log.error(ValidationException('--> "name" should be of type "str"'))
            count += 1
        if self.variation is None:
            log.error(ValidationException('--> "variation" must be specified'))
            count += 1
        if type(self.variation) is not str:
            log.error(ValidationException('--> "variation" should be of type "str"'))
            count += 1

        log.debug('--> {count} validation errors occured'.format(count=count))
        return count


class PyDots(object):
    def __init__(self, *args, **kwargs):
        self.config = None
        self.tasks = []

    def get_info(self):
        info = {
            "pydot": {
                "author": AUTHOR,
                "email": EMAIL,
                "version": VERSION
            },
            "runtime": {
                "cwd": os.getcwd(),
                "config": self.config,
                "tasks": self.tasks
            }
        }
        return info

    def print_info(self):
        info = self.get_info()
        sep = '{:=<80}'.format('')
        sep2 = '{:-<80}'.format('')
        print('PyDots')
        print(sep)
        for k1, v1 in info.items():
            print('{:>10}'.format(k1))
            print(sep2)
            for k2, v2 in v1.items():
                if k1 is 'runtime' and k2 is 'config':
                    print('{:>10}: ```python\n{}\n```'.format(k2, pprint.pformat(v2, indent=1, width=80)))
                else:
                    print('{:>10}: {}'.format(k2, v2))
            print(sep2)
        print(sep)

    def load_config(self):
        cwd = os.getcwd()
        conf = os.path.join(cwd, 'pydots.conf')
        if not os.path.isfile(conf):
            err = 'Could not locate file "pydots.conf" in directory: {}'.format(cwd)
            log.error(err)
            raise MissingPyDotsConfException(err)
        else:
            with open(conf, 'r') as config:
                self.config = yaml.load(config)

    def validate_config(self, config=None):
        config = self.config if config is None else config
        if config is None:
            err = 'Config has not been loaded'
            log.error(err)
            raise MissingPyDotsConfException(err)

        if 'tasks' not in config:
            err = '"tasks" dictionary not defined'
            log.error(err)
            raise ValidationException(err)
        else:
            for name in config.get('tasks'):
                task = config.get('tasks').get(name)
                t = Task(task, name=name)
                self.tasks.append(t)

        for task in self.tasks:
            task.validate()

    def main(self, *args, **kwargs):
        self.load_config()
        self.validate_config()

if __name__ == '__main__':
    pydots = PyDots()
    pydots.main()
