import sys
import os

# /media/pi/New Volume/SkiesPlaylists/'
rootDir = '/media/pi/New Volume/SkiesPlaylists/unsorted/The_Witcher_3_Wild_Hunt_-_Official_Soundtrack_(steam_edition)_mp3/'
plFile = rootDir+'playlists.dat'


def readPlFile():
    playlistData = {"playlistNames": [], "files": {}}
    try:
        data = open(plFile, "r")
        lines = data.readlines()
    except:
        lines = ["All"]
    playlists = lines[0].replace("\n", "")
    playlistNames = playlists.split(',')
    playlistData["playlistNames"] = playlistNames
    print(playlistNames)
    traverseDirectory(playlistData)
    lineNum = 1
    while lineNum < len(lines):
        fileLine = lines[lineNum].replace("\n", "")
        lineNum += 1
        musicFile = fileLine[:fileLine.index(":")]
        if musicFile == "":
            continue
        filePlaylists = fileLine[fileLine.index(":")+1:].split(",")
        for pl in filePlaylists:
            playlistData["files"][pl] = True
    print playlistData


def traverseDirectory(playlistData):
    for root, d_names, f_names in os.walk(rootDir):
        for f in f_names:
            fullFilePath = os.path.join(root, f)
            playlistData["files"][fullFilePath] = {}
            for plName in playlistData["playlistNames"]:
                playlistData["files"][fullFilePath][plName] = False


if __name__ == "__main__":
    readPlFile()
