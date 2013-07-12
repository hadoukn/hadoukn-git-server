from ConfigParser import ConfigParser


def get_config_file(path):
    return open(path, 'r+')


def get_config(path):
    config_file = get_config_file(path)

    # parse the the user settings file, and form a dict from it
    config = HadoukncliGitConfigParser()
    config.readfp(config_file)

    # close file
    config_file.close()
    return config


class HadoukncliGitConfigParser(ConfigParser):
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
