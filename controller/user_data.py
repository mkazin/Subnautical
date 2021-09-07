class UserDataController:

    @staticmethod
    def update_marker_type(current_user, old_type_name, new_type_name, color):
        markers_to_update = UserDataController.find_existing_markers_of_type_name(current_user, old_type_name)
        for marker in markers_to_update:
            marker.marker_type_name = new_type_name
            marker.color = color
        current_user.save()

    @staticmethod
    def find_existing_markers_of_type_name(current_user, name):
        return list(filter(lambda marker: marker.marker_type_name is name, current_user.map_data))

    @staticmethod
    def find_existing_marker_with_name(current_user, marker_name):
        for marker in current_user.map_data:
            if marker.name is marker_name:
                return marker
        return None
