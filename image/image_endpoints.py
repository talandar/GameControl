"""flask blueprint that controls music/playlist rest endpoints (/music)"""

import os
from flask import Blueprint, jsonify, request
import music.playlist_data as PlayList
import music.music_player as Player

# setup components
PLAYLIST = PlayList.PlayList("/media/pi/New Volume/SkiesPlaylists/")
PLAYER = Player.MusicPlayer()
music_page = Blueprint('music_page', __name__,
                       template_folder='templates', url_prefix='/music')


@music_page.route('/filedata', methods=["GET"])
def list_file_data():
    """get json representation of file and playlist data for playlist editor"""
    f_data = PLAYLIST.get_file_data()
    f_data["totalRows"] = len(f_data["files"])
    page_num = int(request.args.get("currentPage")) - 1
    page_size = int(request.args.get("perPage"))
    start = page_num * page_size
    end = start + page_size
    new_file_data = {}
    for file_name in sorted(f_data["files"].keys())[start:end]:
        new_file_data[file_name] = f_data["files"][file_name]
    f_data["files"] = new_file_data
    return jsonify(f_data)


@music_page.route('/playlistdata', methods=["GET"])
def list_playlist_data():
    """get json representation of playlist data for music player"""
    return jsonify(PLAYLIST.get_list_data())


@music_page.route('/play/<playlist_name>', methods=["GET"])
def play_playlist(playlist_name):
    """play the specified playlist"""
    print 'request start playlist {0}'.format(playlist_name)
    list_files = PLAYLIST.files_in_list(playlist_name)
    print '{0} files in list'.format(len(list_files))
    PLAYER.play(list_files)
    return jsonify("success")


@music_page.route('/playfile', methods=["POST"])
def play_single():
    """play the file specified by the "file" element of the json body
    File path should not include the root directory of the playlist data"""
    req_body = request.json
    full_file_path = os.path.join(PLAYLIST.root_dir, req_body["file"])
    print 'file play {0}'.format(full_file_path)
    PLAYER.play_single(full_file_path)
    return jsonify("success")


@music_page.route("/playlist/<playlist_name>", methods=["PUT", "DELETE"])
def playlist_mod(playlist_name):
    """PUT: add a new playlist
    DELETE: remove a playlist"""
    if request.method == "PUT":
        PLAYLIST.add_list(playlist_name)
    else:  # DELETE
        PLAYLIST.remove_list(playlist_name)
    return jsonify("success")


@music_page.route('/stop', methods=["GET"])
def stop_music():
    """stop any playing music"""
    PLAYER.stop()
    return jsonify("success")


@music_page.route("/file", methods=["PUT", "DELETE"])
def file_playlist_mod():
    """Accepts a json document in the body with two parameters: "file", and "list"
    if PUT, add that file to that playlist (if both exist)
    if DELETE, remove that file from that playlist
    (if both exist).  Adding a file to a playlist that it is already in
    or removing a file from a playlist it is not in perform no operation
    and return success.  A playing playlist will not update until it is restarted."""
    if request.method == "PUT":
        req_body = request.json
        file_path = req_body["file"]
        list_name = req_body["list"]
        PLAYLIST.add_to_list(file_path, list_name)
    else:
        req_body = request.json['arg']
        file_path = req_body["file"]
        list_name = req_body["list"]
        PLAYLIST.remove_from_list(file_path, list_name)
    return jsonify("success")
