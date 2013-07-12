from twisted.conch.avatar import ConchUser
from twisted.conch.ssh.session import SSHSession


class User(ConchUser):
    def __init__(self, settings, username, api_key):
        ConchUser.__init__(self)
        self.settings = settings
        self.username = username
        self.api_key = api_key
        self.channelLookup['session'] = SSHSession

    def logout(self):
        pass
