from pydub import AudioSegment
from pydub.playback import play

sound = AudioSegment.from_file(
    "/media/pi/New Volume/SkiesPlaylists/unsorted/The_Witcher_3_Wild_Hunt_-_Official_Soundtrack_(steam_edition)_mp3/33 Ladies of the Woods.mp3", format="mp3")
play(sound)
