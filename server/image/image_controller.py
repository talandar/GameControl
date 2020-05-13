"""This class maintains the image database for display to clients"""

import os


class ImageDatabase(object):
    """container for image data"""

    VALID_IMAGE_TYPES = ["png", "jpg"]

    CATEGORIES = set()

    FILE_DATA = {}

    def __init__(self, root_dir):
        self.root_dir = root_dir
        self._scan_for_images()

    def _scan_for_images(self):
        for root, category, f_names in os.walk(self.root_dir):
            self.CATEGORIES.add(category)
            FILE_DATA[category] = []
            for f_name in f_names:
                file_path = os.path.join(root, f_name)
                file_type = file_path[file_path.rindex(".")+1:].lower()
                if file_type in self.VALID_FILE_TYPES:
                    FILE_DATA[category].add(file_path)

    def categories(self):
        return self.CATEGORIES.copy()

    def files_in_category(self, category):
