import random
import os
import json

"""Represents a server playlist."""

class ServerPlaylist(object):

    DATA_FILE_LOCATION = "./playlists/"
    
    def __init__(self, guild_id):
        self._currentPlaylist = None
        self._currentSong = None
        self._playlists = {}
        self.guild_id = guild_id
        self._load_data()

    def add_playlist(self, playlist_name):
        lower_name = playlist_name.lower()
        if lower_name not in self._playlists:
            self._playlists[lower_name] = {'songs': [], 'name': playlist_name}
            self._save_data()
            return True
        else:
            return False

    def remove_playlist(self, playlist_name):
        lower_name = playlist_name.lower()
        if lower_name in self._playlists:
            self._playlists.pop(lower_name)
            self._save_data()
            return True
        else:
            return False

    def list_playlists(self):
        playlists = []
        for entry in self._playlists.values():
            playlists.append(entry['name'])
        return sorted(playlists)

    def songs_in_list(self, playlist_name):
        lower_name = playlist_name.lower()
        if lower_name in self._playlists:
            songs = self._playlists[lower_name]['songs']
            return sorted(songs)
        return []

    def add_to_playlist(self, playlist_name, song_url):
        lower_name = playlist_name.lower()
        if lower_name in self._playlists:
            songs = self._playlists[lower_name]['songs']
            songs.append(song_url)
            self._save_data()
            return True
        else:
            return False

    def remove_from_playlist(self, playlist_name, song_url):
        lower_name = playlist_name.lower()
        if lower_name in self._playlists:
            songs = self._playlists[lower_name]['songs']
            if song_url in songs:
                songs.remove(song_url)
            self._save_data()
            return True
        else:
            return False

    def current_playlist(self):
        if self._currentPlaylist and self._currentPlaylist in self._playlists:
            return self._playlists[self._currentPlaylist]['name']
        return None

    def play(self, playlist_name):
        lower_name = playlist_name.lower()
        if lower_name in self._playlists:
            self._currentPlaylist = lower_name
            return self.get_next_song()
        else:
            return None

    def get_next_song(self):
        print(f"getting next song in playlist {self._currentPlaylist}.  Currently playing {self._currentSong}")
        if not self._currentPlaylist:
            return None
        if self._currentPlaylist in self._playlists:
            songs = self._playlists[self._currentPlaylist]['songs']
            if len(songs)==0:
                self._currentSong = None
                return None
            elif len(songs)==1:
                self._currentSong = songs[0]
                return songs[0]
            else:
                nextsong = random.choice(songs)
                while nextsong == self._currentSong:
                    print(f"tried to repick {nextsong}, trying again")
                    nextsong = random.choice(songs)
                self._currentSong = nextsong
                return nextsong
        return None

    def stop(self):
        self._currentPlaylist = None

    def _load_data(self):
        print(f"load data from {self._path()}")
        if os.path.exists(self._path()):
            with open(self._path()) as f:
                text = f.read()
                imported_data = json.loads(text)
                self._playlists = imported_data
        else:
            self._playlists = {}

    def _save_data(self):
        exported_data = json.dumps(self._playlists)
        print(exported_data)
        print(f"save data to {self._path()}")
        outputfile = self._path()
        tmpfile = f"{outputfile}.tmp"
        bakfile = f"{outputfile}.bak"
        with open(tmpfile, "w") as f:
            f.write(exported_data)
        if os.path.exists(outputfile):
            os.rename(outputfile,bakfile)
        os.rename(tmpfile,outputfile)
        os.remove(bakfile)

    def _path(self):
        return os.path.join(self.DATA_FILE_LOCATION, f"{self.guild_id}.json")