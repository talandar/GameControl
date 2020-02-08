from pydub import AudioSegment
from pydub.playback import play

sound = AudioSegment.from_file(
    "/media/pi/New Volume/SkiesPlaylists/Battle-HighEnergy/02 They Who Govern Reason.flac", format="flac")
play(sound)
