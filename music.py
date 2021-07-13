import pygame

pygame.init()
pygame.mixer.init()


class MusicPlayer:
    """Music player class for handling music"""

    def __init__(self):
        self.current_song_file = ""
        self.current_length = 0
        self.playing = False
        self.total_length = 1
        self.volume = 1

    def load_file(self, filename: str) -> bool:
        """Function to load file"""
        try:
            current_song_obj = pygame.mixer.Sound(filename)
            self.current_song_file = filename
            pygame.mixer.music.load(filename)
            self.total_length = current_song_obj.get_length()
        except RuntimeError:
            print("Error loading file")
            return False
        return True

    def play(self) -> None:
        """Function to play music"""
        pygame.mixer.music.play()
        self.playing = True

    def pause(self) -> None:
        """Function to pause music"""
        pygame.mixer.music.pause()
        self.playing = False

    def set_volume(self, volume: float) -> None:
        """Sets volumes"""
        self.volume = volume
        pygame.mixer.music.set_volume(volume)

    def get_percent(self) -> int:
        """Gets percent of song passed"""
        self.current_length = pygame.mixer.music.get_pos()
        return int((self.current_length / (self.total_length*1000)) * 100)
