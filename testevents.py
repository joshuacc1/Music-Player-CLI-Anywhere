#!/usr/bin/env python


from blessed import Terminal

from defaults import JsonConfigHandler
from FileHandling import FileHandler
from music import MusicEventHandler
from MusicTerminal import MusicTerminal
from Widgets import Option, ProgressBarWidget, SelectWidget

if __name__ == "__main__":
    term = Terminal()
    m = MusicTerminal(term)
    MUSIC_DIR = JsonConfigHandler('config.json').default_dir

    # o1 = Option(["abbas band"], "abbas band.mp3")
    # o2 = Option(["the king"], "the king.mp3")
    # o3 = Option(["flinstones"], "flinstones.mp3")
    # o4 = Option(["superman"], "superman.mp3")
    # o5 = Option(["Breath"], "Breath.mp3")
    # options2 = [o1, o2, o3, o4, o5]

    controls = SelectWidget([Option(["     ", " <<< ", "     "], "previous"),
                             Option(["      ", " play ", "      "], "play"),
                             Option(["       ", " Pause ", "       "], "pause"),
                             Option(["     ", " >>> ", "     "], "next")], layout="Horizontal", terminal=term)

    fh = FileHandler(MUSIC_DIR)
    files = fh.files
    filenames = []

    for folder in fh.folders:
        filenames.append(Option([term.blue(folder)], folder))
    for file in files:
        filenames.append(Option([file], file))
    music_menu = SelectWidget(filenames, terminal=term)
    music_menu.name = 'filename'

    mini_controls = SelectWidget([Option([" <<< "], "previous"),
                                  Option([" Play "], "play"),
                                  Option([" Pause "], "pause"),
                                  Option([" >>> "], "next")], layout="Horizontal", terminal=term)
    controls.name = 'controls'

    volct = SelectWidget([Option(['x'], "0"),
                          Option(['='], "0.2"),
                          Option(['='], "0.4"),
                          Option(['='], "0.6"),
                          Option(['='], "0.8"),
                          Option(['='], "1")], layout="Horizontal", terminal=term)
    volct.header = 'Volume: ' + term.on_green
    volct.name = 'volume'

    progressbar = ProgressBarWidget('progressbar', 10, terminal=term)

    music_event = MusicEventHandler(MUSIC_DIR, progress_bar=progressbar)
    music_event.run()

    m.add_widget(music_menu, (2, 2))
    m.add_widget(music_event.progress_bar, (len(music_menu.options) + 4, 2))
    m.add_widget(volct, (len(music_menu.options) + 7, 2))
    m.add_widget(controls, (len(music_menu.options) + 8, 2))
    m.small_window_widget = mini_controls

    m.add_event_subscriber(music_event)
    music_event.add_publisher(progressbar)
    m.run()
