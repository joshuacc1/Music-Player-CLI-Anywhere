import os

import pygame

from FileHandling import FileHandler
from Widgets import Widget

pygame.init()
pygame.mixer.init()


class MusicPlayer:
    """Music player class for handling music"""

    def __init__(self):
        self.current_song_file = ""
        self.current_song_name = ""
        self.current_length = 0
        self.playing = False
        self.total_length = 1
        self.volume = 1
        self.paused = pygame.mixer.music.get_busy()
        self.dummypublishers = []

    def load_file(self, filename: str) -> bool:
        """Function to load file"""
        try:
            current_song_obj = pygame.mixer.Sound(filename)
            self.current_song_file = filename
            pygame.mixer.music.load(filename)
            self.total_length = current_song_obj.get_length() * 1000
            pygame.mixer.music.play()
        except FileNotFoundError as err:
            print("File Not Found Error: {0}".format(err))
            print(filename + " not found!")
            return False
        return True

    def pause(self) -> None:
        """Function to pause music"""
        pygame.mixer.music.pause()
        self.playing = False

    def unpause(self) -> None:
        """Function to unpause music"""
        pygame.mixer.music.unpause()
        self.playing = True

    # TODO: next song and other controls
    # TODO: clean song data

    def update(self) -> None:
        """Communicates with the controls (all of the widgets selections) [file selected, play/pause, set volume]"""
        return

    def set_volume(self, volume: float) -> None:
        """Sets volumes (0.0 to 1.0)"""
        self.volume = volume
        pygame.mixer.music.set_volume(volume)
        return

    def get_percent(self) -> int:
        """Gets percent of song passed"""
        self.current_length = pygame.mixer.music.get_pos()
        return int((self.current_length / self.total_length) * 100)


class MusicEventHandler:
    """Music Event subscriber of app events"""

    def __init__(self, music_dir: str, progress_bar: Widget):
        self.currentsong = ''
        self.musicplayer = MusicPlayer()
        self.queue = []
        self.queue_pointer = 0
        self.percent = 0
        self.dir = music_dir
        self.progress_bar = progress_bar
        self.progress = 0
        self.event_publishers = []

    def get_dir(self, file):
        return os.path.isdir(os.path.join(self.dir, '/'+file))

    def update(self, event: dict) -> None:
        """Called when app subscribed to has an event"""
        if not any([x in ['filename', 'controls'] for x in event.keys()]):
            return None

        songfile = event['filename']
        event_type = event['controls']
        try:
            if event_type == "play" and not self.get_dir(songfile):
                self.queue = FileHandler(self.dir).files
                if not songfile == self.currentsong:  # If a song hasn't been selected already
                    self.currentsong = songfile
                    self.musicplayer.load_file(self.dir + os.path.sep + songfile)
                else:
                    self.musicplayer.unpause()

            elif event_type == "pause":
                self.musicplayer.pause()

            elif event_type == "next" and len(self.queue) != 0:
                self.queue_pointer += (self.queue.index(songfile) + 1)
                self.queue_pointer = self.queue_pointer % len(self.queue)
                self.musicplayer.load_file(self.dir + os.path.sep + self.queue[self.queue_pointer])

            elif event_type == "previous" and len(self.queue) != 0:
                self.queue_pointer += self.queue.index(songfile) - 1
                self.queue_pointer = self.queue_pointer % len(self.queue)
                self.musicplayer.load_file(self.dir + os.path.sep + self.queue[self.queue_pointer])
        except pygame.error:
            pass  # The intention is to change enter the folder here

    def run(self) -> bool:
        """Updates progress bar"""
        progress = self.musicplayer.get_percent()
        if not self.progress == progress:
            events = {'progress': progress}
            for event_publisher in self.event_publishers:
                event_publisher.update(events)
            return True
        return False

    def add_publisher(self, publisher: Widget) -> None:
        """Publishes events for the event"""
        self.event_publishers.append(publisher)
