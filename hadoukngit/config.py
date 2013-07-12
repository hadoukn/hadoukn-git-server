from ConfigParser import ConfigParser
import os


def get_config_file(path):
    return open(path, 'r+')


def get_config(path=None):
    if path is None:
        path = os.environ.get('HADOUKN_GIT_CONFIG')
    if path is None:
        if os.path.exists('.hadoukngitrc'):
            path = '.hadoukngitrc'
    if path is None:
        raise ValueError('Cannot find a configuration file.')

    # parse the the user settings file, and form a dict from it
    config = HadouknGitConfigParser()
    config.read(path)
    return config


class HadouknGitConfigParser(ConfigParser):
    def get_dict(self):
        sections = self.sections()

        # convert a INI file into a dict
        settings = {}
        for section in sections:
            items = self.items(section)

            settings[section] = {}
            for k, v in items:
                settings[section][k] = v

        return settings

    def set_dict(self, section, params):
        # if the section doesn't exist add it
        if not section in self.sections():
            self.add_section(section)

        # convert a dict into INI settings
        for k, v in params.items():
            self.set(section, k, v)
