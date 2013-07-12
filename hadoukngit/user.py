from twisted.conch.avatar import ConchUser
from twisted.conch.ssh.session import SSHSession


class User(ConchUser):
    def __init__(self, username):
        ConchUser.__init__(self)
        self.username = username
        self.channelLookup['session'] = SSHSession

    def logout(self):
        pass
