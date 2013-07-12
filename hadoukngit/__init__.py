from __future__ import print_function
import argparse
import os
import sys

from twisted.internet import reactor
from twisted.python import components
from twisted.conch.ssh.session import ISession

from hadoukngit.server import SSHFactory
from hadoukngit.config import get_config
from hadoukngit.session import GitSession
from hadoukngit.user import User


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c',
        '--config',
        help=(
            'Path to the configuration file. If not specified then the '
            'lookup order will check for a HADOUKN_GIT_CONFIG environ '
            'variable, then fallback to .hadoukngitrc in the CWD.'
        ),
    )
    args = parser.parse_args(args=argv)

    cfg_path = args.config
    if cfg_path is not None and not os.path.exists(cfg_path):
        print('Invalid path "{}" specified for the config file.'
              .format(cfg_path), file=sys.stderr)
        return 1

    config = get_config(cfg_path)
    settings = config.get_dict()

    factory = SSHFactory(settings)

    # adapting User to GitSession which implements ISession
    components.registerAdapter(GitSession, User, ISession)

    reactor.listenTCP(2022, factory)
    reactor.run()
