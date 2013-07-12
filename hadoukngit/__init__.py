import sys

from twisted.internet import reactor

from hadoukngit.server import SSHFactory
from hadoukngit.config import get_config


def main(argv=sys.argv):
    config = get_config('hadoukngit.ini')
    settings = config.get_dict()

    factory = SSHFactory(settings)
    reactor.listenTCP(2022, factory)
    reactor.run()
