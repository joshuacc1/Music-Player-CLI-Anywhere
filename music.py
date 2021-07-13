import pygame

pygame.init()
pygame.mixer.init()


def play(song_file: str) -> bool:
    """Function to play music"""
    pygame.mixer.music.load(song_file)
    pygame.mixer.music.play()
    return True


def pause() -> None:
    """Function to pause music"""
    pygame.mixer.music.pause()


def get_position() -> int:
    """Function to return position in music"""
    return pygame.mixer.music.get_pos()
