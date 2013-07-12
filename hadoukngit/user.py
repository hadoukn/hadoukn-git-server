from twisted.conch.avatar import ConchUser

from hadoukngit.session import Session


class User(ConchUser):
    def __inti__(self):
        self.channelLookup['session'] = Session
