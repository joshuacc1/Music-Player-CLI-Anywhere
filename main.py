#!/usr/bin/env python

from blessed import Terminal
import os

from FileHandling import FileHandler
from music import MusicEventHandler
from MusicTerminal import MusicTerminal
from Widgets import Option, ProgressBarWidget, SelectWidget

if __name__ == "__main__":
    term = Terminal()
    m = MusicTerminal(term)
    MUSIC_DIR = os.curdir

    controls = SelectWidget([Option([" play "], "play"),
                             Option([" |<< "], "previous"),
                             Option([" pause "], "pause"),
                             Option([" >>| "], "next")], layout="Horizontal", terminal=term)

    fh = FileHandler(MUSIC_DIR)
    files = fh.files
    filenames = []

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

    progressbar = ProgressBarWidget('progressbar', term.width - 12, terminal=term)

    music_event = MusicEventHandler(MUSIC_DIR, progress_bar=progressbar)
    music_menu.position = (4, 2)
    music_menu.get_position = lambda: (4, int(m.term.width/2 - music_menu.get_dimensions()[1]/2))
    music_event.position = (len(music_menu.options) + 4, 2)
    volct.get_position = lambda: (m.term.height - 2, m.term.width - volct.get_dimensions()[0] - 5)
    progressbar.get_position = lambda: (m.term.height - 6, 2)
    controls.get_position = lambda: (m.term.height - 2, 2)
    m.add_widget(music_menu)
    m.add_widget(music_event.progress_bar)
    m.add_widget(volct)
    m.add_widget(controls)
    m.small_window_widget = mini_controls

    m.add_event_subscriber(music_event)
    m.add_event_subscriber(fh)
    m.add_event_subscriber(progressbar)
    m.dummypublishers.append(music_event)
    music_event.add_publisher(progressbar)
    m.run()
