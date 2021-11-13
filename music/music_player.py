"""Music file player"""
import random
import time
import threading
import pygame


class MusicPlayer(object):
    "play music playlists"

    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(1)
        self._file_paths = []
        self._queue_filler_thread = threading.Thread(
            target=self._keep_queue_full)
        self._queue_filler_thread.daemon = True
        self._queue_filler_thread.start()

    def play(self, file_paths):
        """play playlist in shuffled order, until stopped"""
        print(f'new list requested, has {len(file_paths)} files')
        self.stop()
        self._file_paths = list(file_paths)
        next_file = self._random_file()
        print(f'playing next file: {next_file}')
        if next_file:
            pygame.mixer.music.load(next_file)
            pygame.mixer.music.play()

    def play_single(self, file_path):
        """play a single file on loop until stopped"""
        self.stop()
        self._file_paths = [file_path]
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

    def stop(self):
        """stop playback"""
        self._file_paths = []
        pygame.mixer.music.stop()

    def _playback_end_callback(self):
        print('file ended or new list start requested')
        next_file = self._random_file()
        print(f'playing next file: {next_file}')
        if next_file:
            pygame.mixer.music.load(next_file)
            pygame.mixer.music.play()

    def _random_file(self):
        if not self._file_paths:
            return None
        index = random.randint(0, len(self._file_paths)-1)
        return self._file_paths[index]

    def _keep_queue_full(self):
        while True:
            if pygame.mixer.get_init() and not pygame.mixer.music.get_busy():
                queue_file = self._random_file()
                if queue_file:
                    print(f'queueing {queue_file}')
                    pygame.mixer.music.load(queue_file)
                    pygame.mixer.music.play()
            time.sleep(.1)
