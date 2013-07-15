import logging
import requests
import json

from twisted.conch.checkers import SSHPublicKeyDatabase
from twisted.internet import (
    defer,
    reactor
)
from twisted.web.client import Agent
from twisted.conch.ssh.keys import Key

from hadoukngit.util import key_to_parts


logger = logging.getLogger(__name__)


class Checker(SSHPublicKeyDatabase):
    agent = Agent(reactor)

    def __init__(self, settings):
        self.settings = settings

    def checkKey(self, credentials):
        # dont bother checking until we've confirmed the key
        if not credentials.signature:
            return True

        key = Key.fromString(credentials.blob)
        key_type, key_key = key_to_parts(key.toString('OPENSSH'))

        payload = {
            'key_key': key_key
        }
        params = {
            'api_key': self.settings['hadoukngit']['api_key']
        }
        url = '%s/users/key' % self.settings['hadoukngit']['api_url']

        r = requests.get(url,
                         data=json.dumps(payload),
                         params=params)

        if r.ok:
            user = r.json()
            credentials.username = '%s:%s' % (user['username'], user['api_key'])
            return True
        else:
            error = r.json()
            logger.info(error['msg'])
            return defer.fail()
