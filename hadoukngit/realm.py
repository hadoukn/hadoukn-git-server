from twisted.conch.interfaces import IConchUser
from twisted.cred.portal import IRealm
from zope.interface import implementer

from hadoukngit.user import User


@implementer(IRealm)
class Realm(object):
    def __init__(self, settings):
        self.settings = settings

    def requestAvatar(self, username, mind, *interfaces):
        return IConchUser, User(username), lambda: None
