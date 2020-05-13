"""Data container for image data.
Supports various methods for storage of image categorization and file data"""
import os
import json


class Images(object):
    """Container for image data"""

    VALID_FILE_TYPES = ["jpg", "png"]
    DATA_FILE_NAME = "images.dat"

    def __init__(self, root_dir):
        self.root_dir = root_dir
        self._image_data_file = os.path.join(
            self.root_dir, self.DATA_FILE_NAME)
        self._read_data_file()

    def _read_data_file(self):
        image_data = {"categories": [], "files": {}}
        try:
            with open(self._image_data_file, "r") as data:
                lines = data.readlines()
                if not lines:
                    lines = ["Uncategorized"]
        except IOError:
            lines = ["Uncategorized"]
        categories = lines[0].replace("\n", "")
        category_names = categories.split(',')
        image_data["categories"] = category_names
        self._initial_directory_scan(image_data)
        line_num = 1
        while line_num < len(lines):
            file_line = lines[line_num].replace("\n", "")
            line_num += 1
            image_path = file_line[:file_line.index(":")]
            image_metadata = file_line[file_line.index(":")+1:]
            if image_path == "":
                continue
            image_name = image_metadata[:image_metadata.index(":")]
            image_category = image_metadata[image_metadata.index(":")+1:]
            image_data["files"][image_path] = {
                image_name, image_category, image_path}
        self._image_data = image_data

    def _scan_for_image_files(self):
        files = []
        for root, _, f_names in os.walk(self.root_dir):
            for f_name in f_names:
                file_path = os.path.join(root, f_name)
                file_type = file_path[file_path.rindex(".")+1:].lower()
                if file_type in self.VALID_FILE_TYPES:
                    files.append(file_path)
        return files

    def _initial_directory_scan(self, image_data):
        files = self._scan_for_image_files()
        for file_path in files:
            image_data["files"][file_path] = {'image_name': file_path, 'image_category': "Uncategorized", 'image_path': file_path}

    def _persist(self):
        comma = ","
        lines = []
        lines.append(comma.join(self.categories()))
        for image_file in self.files():
            lines.append("\n"+image_file+":"+self.file_name(image_file)+":"+self.file_category(image_file))
        with open(self._image_data_file, "w") as data:
            data.writelines(lines)

    def categories(self):
        """get all categories"""
        return sorted(self._image_data['categories'])

    def files(self):
        """list all files"""
        return sorted(self._image_data["files"])

    def file_category(self, file_path):
        """get the category for a specific file"""
        return self._image_data["files"][file_path].get("image_category","Uncategorized")

    def file_name(self, file_path):
        """get the friendly name for a specific file"""
        return self._image_data["files"][file_path].get("image_name", file_path)

    def files_in_category(self, category_name):
        """get the list of files in a category"""
        files = []
        for file_path in self.files():
            if self.file_category(file_path)==category_name:
                files.append(file_path)
        return files

    def add_category(self, category_name):
        """add a new category, and persist the data file"""
        if category_name not in self.categories():
            self._image_data['categories'].append(category_name)
            self._persist()

    def remove_category(self, category_name):
        """remove a category, if it exists.  Trying to remove a category
        that does not exist is not an error.
        the 'Uncategorized' category may not be removed, and will fail silently.
        Persists the data file."""
        if category_name in self.categories() and category_name != "Uncategorized":
            self._image_data['categories'].remove(category_name)
            for file_path in self.files_in_category(category_name):
                self.set_category(file_path,"Uncategorized")
            self._persist()

    def set_category(self, file_path, category_name):
        """Add a file to a playlist.  Persist after change."""
        if category_name in self.categories() and file_path in self.files():
            self._image_data["files"][file_path]['image_category'] = category_name
            self._persist()


    def file_rescan(self):
        """rescan the directory to pick up any newly-added music files"""
        known_files = self.files()
        any_new_found = False
        for found_file in self._scan_for_image_files():
            if found_file not in known_files:
                any_new_found = True
                self._image_data["files"][found_file] = {
                    'image_name': found_file, 'image_category': "Uncategorized", 'image_path': found_file}
        if any_new_found:
            self._persist()

    # def get_file_data(self):
    #     """file data for use by ui.  Object with three fields;
    #     root: the root directory of all files.  For improving display of filesname.
    #     files: an object that has details of which files are in which playlists
    #     lists: a list of the active playlists"""
    #     data = {}
    #     data["files"] = self._image_data["files"].copy()
    #     data["root"] = self.root_dir
    #     data["categories"] = self.categories()
    #     return data

    # def get_category_data(self):
    #     """playlist data used by the player ui.  Array of objects:
    #     each one has 'name' and 'numfiles'"""
    #     data = []
    #     for list_name in self.lists():
    #         list_dat = {
    #             'name': list_name,
    #             'numfiles': len(self.files_in_list(list_name))
    #         }
    #         data.append(list_dat)
    #     return data


if __name__ == "__main__":
    DAT = Images("/media/pi/New Volume/SkiesImages/")
    print DAT.categories()
    print DAT.files()
    DAT.add_category("Party")
    DAT.add_category("Maps")
    DAT.add_category("NPCs")
    DAT.add_category("Scenery")
    DAT.add_category("Monsters")
