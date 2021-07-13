from FileHandling import FileHandler
from music import MusicPlayer


def main() -> None:
    """Main function"""
    music_player = MusicPlayer()
    file_handler = FileHandler("./samples")

    file_handler.get_files()
    print(file_handler.files, file_handler.amt_of_files)

    music_player.load_file("test.mp3")
    music_player.play()
    music_player.set_volume(0.0)


if __name__ == '__main__':
    main()
