from twisted.internet import reactor
from twisted.conch.ssh import session
from zope.interface import implementer


@implementer(session.ISession)
class GitSession(object):
    def __init__(self, user):
        self.user = user

    def execCommand(self, proto, cmd):
        command = ('git-shell', '-c', cmd)
        reactor.spawnProcess(proto, 'git-shell', command)

    def eofReceived(self):
        pass

    def closed(self):
        pass
