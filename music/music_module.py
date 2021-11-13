import music.playlist_data as playlist_data
import music.music_player as music_player
from message import split_message


class MusicModule(object):

    def __init__(self, root_dir):
        self.playlists = playlist_data.PlayList(root_dir)
        self.player = music_player.MusicPlayer()

    def action(self, args):
        print(args)
        verb, param = split_message(args)
        if verb == "PLAY":
            list_name = param
            files = self.playlists.files_in_list(list_name)
            self.player.play(files)
        if verb == "PLAYONE":
            self.player.play_single(param)
        elif verb == "STOP":
            self.player.stop()
        elif verb == "RESCAN":
            # look for new files
            self.playlists.file_rescan()
        elif verb == "DATA":
            # no-op, but this will trigger return of message
            pass
        elif verb == "ADD_TO_LIST":
            playlist = param[0]
            file = param[1]
            self.playlists.add_to_list(file, playlist)
        elif verb == "REMOVE_FROM_LIST":
            playlist = param[0]
            file = param[1]
            self.playlists.remove_from_list(file, playlist)
        elif verb == "ADD_LIST":
            self.playlists.add_list(param)
        elif verb == "REMOVE_LIST":
            self.playlists.remove_list(param)
        filedata = self.playlists.get_file_data()
        return filedata
