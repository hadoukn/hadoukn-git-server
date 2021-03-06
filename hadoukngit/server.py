from twisted.conch.ssh import factory
from twisted.cred.portal import Portal
from twisted.conch.ssh.keys import Key

from hadoukngit.realm import Realm
from hadoukngit.checker import Checker


class SSHFactory(factory.SSHFactory):
    def __init__(self, settings):
        self.settings = settings
        self.portal = Portal(Realm(settings))
        self.portal.registerChecker(Checker(settings))
        self.privateKeys = {
            'ssh-rsa': Key.fromFile(settings['hadoukngit']['private_key']),
        }
        self.publicKeys = {
            'ssh-rsa': Key.fromFile(settings['hadoukngit']['public_key']),
        }
