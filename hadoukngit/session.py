import os
import re
import json
import logging
import requests

from twisted.internet import reactor
from twisted.conch.ssh import session
from zope.interface import implementer


logger = logging.getLogger(__name__)

# accepts '/myapp.git' and retrieves 'myapp'
APP_NAME_RE = re.compile(r"^'/*(?P<app_name>[a-zA-Z0-9][a-zA-Z0-9@_-]*).git'$")


@implementer(session.ISession)
class GitSession(object):
    def __init__(self, user):
        self.settings = user.settings
        self.user = user
        self.app_name_regex = APP_NAME_RE

    def execCommand(self, proto, cmd):
        # will receive something like 'git-receive-pack'
        cmd_parts = cmd.split(' ')

        # git-receive-pack
        app_command = cmd_parts[0]
        # /myapp.git
        app_name_raw = cmd_parts[1]

        name_match = self.app_name_regex.match(app_name_raw)
        # myapp
        app_name = name_match.group('app_name')

        params = {
            'api_key': self.user.api_key
        }
        payload = {
            'command': app_command
        }
        url = '%s/internal/%s/gitaction' % (self.settings['hadoukngit']['api_url'],
                                            app_name)
        r = requests.post(url,
                          params=params,
                          data=json.dumps(payload))

        if r.ok:
            # see if the repo already exists
            home_directory = os.path.expanduser('~')
            git_template_path = self.settings['hadoukngit']['git_template_path']
            ssh_key_path = os.path.join(home_directory, '.hadoukn', 'repositories', '%s.git' % app_name)

            if not os.path.exists(ssh_key_path):
                os.makedirs(ssh_key_path)

                # initialize a git repo
                command = ('git', 'init', '--bare', '--template=%s' % git_template_path, ssh_key_path)
                reactor.spawnProcess(proto, 'git', command)

            command = ('git-shell', '-c', "%s '%s'" % (app_command, ssh_key_path))
            reactor.spawnProcess(proto, 'git-shell', command)
        else:
            error = r.json()
            logger.info(error['msg'])

    def eofReceived(self):
        pass

    def closed(self):
        pass
