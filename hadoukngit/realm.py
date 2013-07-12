from twisted.conch.interfaces import IConchUser
from twisted.cred.portal import IRealm
from zope.interface import implementer

from hadoukngit.user import User


@implementer(IRealm)
class Realm(object):
    def __init__(self, settings):
        self.settings = settings

    def requestAvatar(self, auth_payload, mind, *interfaces):
        username, api_key = auth_payload.split(':', 1)
        return IConchUser, User(self.settings, username, api_key), lambda: None
