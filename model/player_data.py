from flask_login._compat import unicode
from mongoengine import *
from .map_data import Marker
from flask_login import UserMixin


class PlayerData(Document, UserMixin):

    name = StringField()
    map_data = EmbeddedDocumentListField(Marker)
    google_id = StringField(db_field="_id", required=True, primary_key=True)
    email = StringField()
    email_verified = BooleanField()
    profile_pic = StringField()

    meta = {
        'collection': 'users'
    }

    """ Methods required by flask_login.LoginManager """
    def get_id(self):
        return unicode(self.google_id)

    # self.is_authenticated = True
    # self is_anonymous = False
    # self is_active = True

    """ End flask_login.LoginManager requirements """

    def __repr__(self):
        return ";".join([f"{field}={getattr(self, field)}" for field in self._fields])

    @staticmethod
    def load_player(player_id):
        print(f"PlayerData.load_player called with {player_id}")
        player = PlayerData.objects.get(google_id=player_id)
        print(f"PlayerData.load_player: mongo returned {repr(player)}")
        return player

    @staticmethod
    def save_player(player):
        print('PlayerData.save_player called for ', player)

        if 'id' in player:
            print('PlayerData.save_player: Player already exists. Updating')
            player.save()
        else:
            print('PlayerData.save_player: Creating new player document')
            pd, _ = PlayerData.objects.create(player)
