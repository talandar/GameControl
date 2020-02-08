import sys
import os

# unsorted/The_Witcher_3_Wild_Hunt_-_Official_Soundtrack_(steam_edition)_mp3/'
rootDir = '/media/pi/New Volume/SkiesPlaylists/'
plFile = rootDir+'playlists.dat'

validFileTypes = ["flac", "mp3"]


def readPlFile():
    playlistData = {"playlistNames": [], "files": {}}
    try:
        with open(plFile, "r") as data:
            data = open(plFile, "r")
            lines = data.readlines()
            if len(lines) == 0:
                lines = ["All"]
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
            if pl != "":
                playlistData["files"][musicFile][pl] = True
        playlistData["files"][musicFile]["All"] = True
    print playlistData
    return playlistData


def writePlFile(playlistData):
    comma = ","
    lines = []
    lines.append(comma.join(playlistData["playlistNames"]))
    for musicFile in playlistData["files"]:
        lines.append("\n"+musicFile+":")
        playlists = []
        for plName in playlistData["files"][musicFile]:
            if playlistData["files"][musicFile][plName]:
                playlists.append(plName)
        lines.append(comma.join(playlists))
    with open(plFile, "w") as data:
        data.writelines(lines)


def traverseDirectory(playlistData):
    for root, d_names, f_names in os.walk(rootDir):
        for f in f_names:
            fullFilePath = os.path.join(root, f)
            fileType = fullFilePath[fullFilePath.rindex(".")+1:]
            if fileType in validFileTypes:
                playlistData["files"][fullFilePath] = {}
                for plName in playlistData["playlistNames"]:
                    playlistData["files"][fullFilePath][plName] = False
                playlistData["files"][fullFilePath]["All"] = True


if __name__ == "__main__":
    playlistData = readPlFile()
    writePlFile(playlistData)
