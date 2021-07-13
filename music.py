import pygame

pygame.init()
pygame.mixer.init()


def play(filename: str) -> bool:
    """Function to play music"""
    try:
        pygame.mixer.music.play(filename)
        pygame.mixer.music.play()
    except RuntimeError:
        print("Error playing music from file")
        return False
    return True


def pause() -> None:
    """Function to pause music"""
    pygame.mixer.music.pause()


def add_to_queue(filename: str) -> None:
    """Function to add to queue"""
    try:
        pygame.mixer.music.queue(filename)
    except RuntimeError:
        print("File not found or error encountered while loading file")
        return False
    return True


def get_position() -> int:
    """Function to return position in music"""
    return pygame.mixer.music.get_pos()
