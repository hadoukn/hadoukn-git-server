import sys

from twisted.internet import reactor
from twisted.python import components
from twisted.conch.ssh.session import ISession

from hadoukngit.server import SSHFactory
from hadoukngit.config import get_config
from hadoukngit.session import GitSession
from hadoukngit.user import User


def main(argv=sys.argv):
    config = get_config('hadoukngit.ini')
    settings = config.get_dict()

    factory = SSHFactory(settings)

    # adapting User to GitSession which implements ISession
    components.registerAdapter(GitSession, User, ISession)

    reactor.listenTCP(settings['hadoukngit']['post'], factory)
    reactor.run()
