import unittest
from mongoengine import connect
from controller.user_data import UserDataController
from model.map_data import Marker
from model.player_data import PlayerData


class UserDataControllerTestCase(unittest.TestCase):

    db = None
    player_singleton = None

    @classmethod
    def setUpClass(cls):
        UserDataControllerTestCase.db = connect('testdb', host="mongomock://localhost", port=27017)
        UserDataControllerTestCase.db.drop_database('testdb')
        UserDataControllerTestCase._create_player()

    @classmethod
    def tearDownClass(cls):
        UserDataControllerTestCase.db.drop_database('testdb')
        UserDataControllerTestCase.db.close()

    def setUp(self):
        self.player = UserDataControllerTestCase.player_singleton
        self.player.map_data = []
        self.player.save()

    def test_update_marker_type_when_marker_existed(self):
        old_type_name = 'Old Type Name'
        self._create_marker(bearing=100, distance=456, depth=123, x=5, y=5,
                            name='Test Marker', marker_type_name=old_type_name, color='Old Color')

        new_type_name = 'New Type Name'
        new_color = 'New Color'
        UserDataController.update_marker_type(self.player, old_type_name, new_type_name, new_color)

        self._force_db_map_data_reload()
        self.assertEqual(1, len(self.player.map_data))
        self.assertEqual(new_type_name, self.player.map_data[0].marker_type_name)
        self.assertEqual(new_color, self.player.map_data[0].color)

    def test_update_marker_type_when_multiple_markers_exist(self):
        old_type_name = 'Old Type Name'
        self._create_marker(bearing=100, distance=456, depth=123, x=5, y=5,
                            name='First Marker', marker_type_name=old_type_name, color='Old Color')
        old_type_name = 'Old Type Name'
        self._create_marker(bearing=100, distance=456, depth=123, x=5, y=5,
                            name='Second Marker', marker_type_name=old_type_name, color='Old Color')

        new_type_name = 'New Type Name'
        new_color = 'New Color'
        UserDataController.update_marker_type(self.player, old_type_name, new_type_name, new_color)

        self._force_db_map_data_reload()
        self.assertEqual(2, len(self.player.map_data))

        for marker in self.player.map_data:
            self.assertEqual(new_type_name, marker.marker_type_name)
            self.assertEqual(new_color, marker.color)

    def test_update_marker_type_when_other_marker_types_should_be_ignored(self):
        type_name_to_replace = 'Old Type Name'
        type_name_which_should_not_be_changed = 'Very different from the old type name'
        self._create_marker(bearing=100, distance=456, depth=123, x=5, y=5,
                            name='Test Marker',
                            marker_type_name=type_name_which_should_not_be_changed,
                            color='A Completely Different Color')

        new_type_name = 'New Type Name'
        new_color = 'New Color'
        UserDataController.update_marker_type(self.player, type_name_to_replace, new_type_name, new_color)

        # Force a reload from the database, should find our one marker
        self._force_db_map_data_reload()
        self.assertEqual(1, len(self.player.map_data))
        self.assertEqual(type_name_which_should_not_be_changed, self.player.map_data[0].marker_type_name)

    def _create_marker(self, bearing, distance, depth, x, y, name, marker_type_name, color):
        new_marker = Marker(
            bearing=bearing, distance=distance, depth=depth, x=x, y=y,
            name=name, marker_type_name=marker_type_name, color=color)
        if not hasattr(self.player, 'map_data'):
            self.player.map_data = []

        self.player.map_data.append(new_marker)
        self.player.save(cascade=True)

    # def test_find_existing_markers_of_type_name(self):
    #     self.fail('Not implemented')

    def test_find_existing_marker_with_name_happy_path(self):
        marker_name_to_find = 'Hello Marker'
        self._create_marker(bearing=100, distance=456, depth=123, x=5, y=5,
                            name=marker_name_to_find,
                            marker_type_name='Marker Type',
                            color='Marker Color')

        found_marker = UserDataController.find_existing_marker_with_name(self.player, marker_name_to_find)
        self.assertEqual(marker_name_to_find, found_marker.name)

    def test_find_existing_marker_with_name_when_missing(self):
        self.assertEqual(0, len(self.player.map_data))
        marker_name_to_find = 'No such marker'
        found_marker = UserDataController.find_existing_marker_with_name(self.player, marker_name_to_find)
        self.assertIsNone(found_marker)

    @staticmethod
    def _create_player():
        player = PlayerData(
            id='test_id',
            name='Test Player',
            email='test@example.com',
            profile_pic='/static/test_user.svg',
            email_verified=True,
            map_data=[],
        )
        player.map_data = []
        player.validate()
        PlayerData.save_player(player)
        player.save(cascade=True)

        UserDataControllerTestCase.player_singleton = player

    def _force_db_map_data_reload(self):
        self.player.map_data = []
        self.assertEqual(0, len(self.player.map_data))
        self.player.reload()


if __name__ == '__main__':
    unittest.main()
