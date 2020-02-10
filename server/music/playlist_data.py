"""Data container for playlist data.
Supports various methods for storage of playlist and file data"""
import os


class PlayList(object):
    """Container for playlist data"""

    VALID_FILE_TYPES = ["mp3", "flac"]
    DATA_FILE_NAME = "playlists.dat"

    def __init__(self, root_dir):
        self.root_dir = root_dir
        self._playlist_data_file = os.path.join(
            self.root_dir, self.DATA_FILE_NAME)
        self._read_playlist_file()

    def _read_playlist_file(self):
        playlist_data = {"list_names": [], "files": {}}
        try:
            with open(self._playlist_data_file, "r") as data:
                lines = data.readlines()
                if not lines:
                    lines = ["All"]
        except IOError:
            lines = ["All"]
        playlists = lines[0].replace("\n", "")
        playlist_names = playlists.split(',')
        playlist_data["list_names"] = playlist_names
        self._initial_directory_scan(playlist_data)
        line_num = 1
        while line_num < len(lines):
            file_line = lines[line_num].replace("\n", "")
            line_num += 1
            music_file_path = file_line[:file_line.index(":")]
            if music_file_path == "":
                continue
            file_playlists = file_line[file_line.index(":")+1:].split(",")
            for list_name in file_playlists:
                if list_name != "":
                    playlist_data["files"][music_file_path][list_name] = True
            playlist_data["files"][music_file_path]["All"] = True
        self._playlist_data = playlist_data

    def _scan_for_music_files(self):
        files = []
        for root, _, f_names in os.walk(self.root_dir):
            for f_name in f_names:
                file_path = os.path.join(root, f_name)
                file_type = file_path[file_path.rindex(".")+1:].lower()
                if file_type in self.VALID_FILE_TYPES:
                    files.append(file_path)
        return files

    def _initial_directory_scan(self, playlist_data):
        files = self._scan_for_music_files()
        for file_path in files:
            playlist_data["files"][file_path] = {}
            for list_name in playlist_data["list_names"]:
                playlist_data["files"][file_path][list_name] = False
            playlist_data["files"][file_path]["All"] = True

    def _persist(self):
        comma = ","
        lines = []
        lines.append(comma.join(self.lists()))
        for music_file in self.files():
            lines.append("\n"+music_file+":")
            playlists = []
            for list_name in self.lists():
                if self._playlist_data["files"][music_file][list_name]:
                    playlists.append(list_name)
            lines.append(comma.join(playlists))
        with open(self._playlist_data_file, "w") as data:
            data.writelines(lines)

    def lists(self):
        """get all playlists"""
        return sorted(self._playlist_data['list_names'])

    def files(self):
        """list all files"""
        return sorted(self._playlist_data["files"])

    def add_list(self, list_name):
        """add a new playlist, and persist the playlist file"""
        if list_name not in self.lists():
            self._playlist_data['list_names'].append(list_name)
            self._persist()

    def remove_list(self, list_name):
        """remove a list, if it exists.  Trying to remove a list
        that does not exist is not an error.
        the 'All' list may not be removed, and will fail silently.
        Persists the playlist file."""
        if list_name in self.lists() and list_name != "All":
            self._playlist_data['list_names'].remove(list_name)
            self._persist()

    def file_rescan(self):
        """rescan the directory to pick up any newly-added music files"""
        known_files = self.files()
        any_new_found = False
        for found_file in self._scan_for_music_files():
            if found_file not in known_files:
                any_new_found = True
                self._playlist_data["files"][found_file] = {}
                for list_name in self.lists():
                    self._playlist_data["files"][found_file][list_name] = False
                self._playlist_data["files"][found_file]["All"] = True
        if any_new_found:
            self._persist()

    def lists_for_file(self, file_path):
        """get the lists for a specific file"""
        lists = []
        if file_path in self.files():
            for playlist in self.lists():
                if self._playlist_data["files"][file_path][playlist]:
                    lists.append(playlist)
        return sorted(lists)


if __name__ == "__main__":
    DAT = PlayList("/media/pi/New Volume/SkiesPlaylists/")
    print DAT.lists()
    DAT.add_list("Battle")
    print DAT.lists()
    DAT.add_list("Other")
    print DAT.lists()
    DAT.remove_list("Other")
    print DAT.lists()
    DAT.remove_list("Other")
    print DAT.lists()
    DAT.remove_list("All")
    print DAT.lists()
