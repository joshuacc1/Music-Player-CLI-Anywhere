#!/usr/bin/env python

import signal

# local
import blessed.keyboard
from blessed import Terminal

from defaults import JsonConfigHandler
from FileHandling import FileHandler
from music import MusicPlayer

CODES = blessed.keyboard.get_keyboard_codes()

MUSIC_DIR = JsonConfigHandler('config.json').default_dir


class Option:
    """Single option for a select widget"""

    def __init__(self, graphic: list[str], choice: str):
        self.graphic = graphic
        self.choice = choice
        self.tl = len(graphic)

    def line(self, line: int) -> str:
        """Returns a line"""
        if line > len(self.graphic):
            return "" * len(self.graphic[0])
        return self.graphic[line]


class Widget:
    """Generic widget class"""

    def __init__(self, name: str = '', passive: bool = False):
        self.name = name
        self.passive = passive


class ProgessBarWidget(Widget):
    """Progress bar for showing progress"""

    def __init__(self, name: str = '', length: int = 5, terminal: Terminal = None):
        Widget.__init__(self, name, True)
        self.term = terminal if terminal else blessed.terminal
        self.length = length
        self.fillstyle = term.on_white
        self.progress = 4

    def render_lines(self) -> list:
        """Returns lines to be rendered"""
        lines = list()
        lines.append(chr(9556) + chr(9552) * self.length + chr(9559))
        lines.append(chr(9553) + f'{self.fillstyle}' + ' '*self.progress + f'{self.term.normal}' + ' '
                     * (self.length-self.progress) + chr(9553))
        lines.append(chr(9562) + chr(9552) * self.length + chr(9565))
        return lines

    def update(self, events: dict) -> None:
        """Update the progress bar with song progress"""
        print(events['progress'])
        self.progress = events['progress']


class SelectWidget(Widget):
    """Selection pane for selecting from a menu or control"""

    def __init__(self, options: list[Option] = None, initialchoice: int = None, selectformat: object = None,
                 layout: str = 'Verticle'):
        Widget.__init__(self, '')
        self.options = options if options else []
        self.choiceindex = initialchoice if initialchoice else 0
        self.selectformat = selectformat if selectformat else term.on_green
        self.layout = layout
        self.header = ''
        self.footer = ''
        self.optionlead = term.on_green
        self.optiontail = term.normal

    def render(self) -> str:
        """Renders the selection pane"""
        if self.layout == 'Horizontal':
            return self.render_horizontal()
        else:
            return self.render_verticle()

    def render_horizontal(self) -> str:
        """Renders a string horizontally"""
        phrase = ""
        maxlines = max([len(x.graphic) for x in self.options])
        for row in range(maxlines):
            for i in range(len(self.options)):
                if i == self.choiceindex:
                    phrase += f"{self.selectformat}{self.options[i].line(row)}{term.normal} "
                else:
                    phrase += f"{self.options[i].line(row)} "
            phrase += "\n"
        return phrase

    def render_verticle(self) -> str:
        """Renders a string vertically"""
        phrase = "" + self.header
        maxlines = max([len(x.graphic) for x in self.options])
        for i in range(len(self.options)):
            for row in range(maxlines):
                if i == self.choiceindex:
                    phrase += f"{self.optionlead}{self.options[i].line(row)}{self.optiontail}\n"
                else:
                    phrase += f"{self.options[i].line(row)}\n"
        return phrase + self.footer

    def render_lines(self) -> list[str]:
        """Renders an list of string lines"""
        if self.layout == 'Horizontal':
            return self.render_lines_horizontal()
        else:
            return self.render_lines_verticle()

    def render_lines_horizontal(self) -> list[str]:
        """Renders a list of string lines horizontally"""
        phrase = []
        maxlines = max([len(x.graphic) for x in self.options])
        for row in range(maxlines):
            line = '' + self.header
            for i in range(len(self.options)):
                if i == self.choiceindex:
                    line += f"{self.optionlead}{self.options[i].line(row)}{self.optiontail}"
                else:
                    line += f"{self.options[i].line(row)}"
            phrase.append(line)
        phrase[-1] = phrase[-1] + self.footer
        # phrase=phrase[0:-2]
        return phrase

    def render_lines_verticle(self) -> list[str]:
        """Renders a list of string lines vertically"""
        phrase = []
        maxlines = max([len(x.graphic) for x in self.options])
        for i in range(len(self.options)):
            for row in range(maxlines):
                if i == self.choiceindex:
                    phrase.append(f"{term.on_green}{self.options[i].line(row)}{term.normal}")
                else:
                    phrase.append(f"{self.options[i].line(row)}")
        return phrase

    def choice(self) -> str:
        """Returns the selection of a widget"""
        return self.options[self.choiceindex].choice

    def update(self, keystroke: blessed.keyboard.Keystroke) -> None:
        """Updates the widgets based upon key pressed"""
        if self.layout == 'Horizontal':
            if CODES[keystroke.code] == 'KEY_RIGHT':
                self.choiceindex = (self.choiceindex + 1) % len(self.options)
            elif CODES[keystroke.code] == 'KEY_LEFT':
                self.choiceindex = (self.choiceindex - 1) % len(self.options)
        else:
            if CODES[keystroke.code] == 'KEY_DOWN':
                self.choiceindex = (self.choiceindex + 1) % len(self.options)
            elif CODES[keystroke.code] == 'KEY_UP':
                self.choiceindex = (self.choiceindex - 1) % len(self.options)


class MusicTerminal:
    """Main class for terminal rendering and control"""

    def __init__(self, terminal: Terminal):
        self.widgets = []
        self.passive_widgets = []
        self.small_window_widget = None
        self.term = terminal
        self.event_subscribers = []
        self.widgetfocus = 0
        self.min_win_size = (0, 0)
        self.miniwindow = False

        signal.signal(signal.SIGWINCH, self.on_resize)

    def on_resize(self, *args) -> None:
        """Executes when windows size changes"""
        if self.term.height > self.minimum_window_size()[0]:
            self.miniwindow = False
            self.render()
        else:
            self.miniwindow = True
            self.render()

    def run(self) -> None:
        """Runs the app"""
        self.min_win_size = self.minimum_window_size()
        self.render()
        with term.cbreak():
            # print(term.clear())
            val = ""
            while val.lower() != "q":
                val = term.inkey(timeout=3)
                if val:
                    if val.is_sequence:
                        self.notifywidget(val)
                        self.render()
                        if CODES[val.code] == 'KEY_ENTER':
                            if self.miniwindow:
                                events = {w['widget'].name: w['widget'].choice() for w in self.widgets}
                                events[self.small_window_widget.name] = self.small_window_widget.choice()
                                self.push_events(events)
                            else:
                                self.push_events({w['widget'].name: w['widget'].choice() for w in self.widgets})
                        if CODES[val.code] == 'KEY_TAB':
                            self.widgetfocus = (self.widgetfocus + 1) % len(self.widgets)
                    # if str(val) in [str(i) for i in range(10)]:
                    #     self.passive_widgets[0]['widget'].update({'progress': int(str(val))})
                    #     self.render()

    def render(self) -> None:
        """Renders the graphics to screen"""
        if self.miniwindow:
            print(self.term.clear + self.small_window_widget.render_lines()[0])
            return None
        all_widgets = [*self.widgets, *self.passive_widgets]
        all_widgets.sort(key=lambda x: x['pos'][0])
        screen = []
        for i in range(term.height):
            screen.append(' ' * term.width)
        screen[1] = '=' * term.width
        screen[-1] = '=' * term.width

        for w in all_widgets:
            x = w["pos"][0]
            y = w['pos'][1]
            widgetlines = w['widget'].render_lines()
            for row in range(len(widgetlines)):
                start = screen[x + row][0:y] if screen[x + row][0:y] else ''
                end = screen[x + row][y + self.term.length(widgetlines[row]):] if screen[x + row][y + self.term.length(
                    widgetlines[row]):] else ''
                screen[x + row] = start + widgetlines[row] + end
        print(self.term.clear + '\n'.join(screen))

    def add_widget(self, widget: Widget, position: tuple) -> None:
        """Adds a widget to the app"""
        if widget.passive:
            self.passive_widgets.append({'widget': widget, 'pos': position})
        else:
            self.widgets.append({'widget': widget, 'pos': position})

    def add_event_subscriber(self, subscriber: object) -> None:
        """Adds a subscriber to app events"""
        self.event_subscribers.append(subscriber)

    def notify(self, keystroke: blessed.keyboard.Keystroke) -> None:
        """Notify widgets of keyboard events"""
        for wp in self.widgets:
            w = wp['widget']
            w.update(keystroke)

    def notifywidget(self, keystroke: blessed.keyboard.Keystroke) -> None:
        """Notify a single widget"""
        if self.miniwindow:
            self.small_window_widget.update(keystroke)
        else:
            self.widgets[self.widgetfocus]['widget'].update(keystroke)

    def push_events(self, events: dict) -> None:
        """Updates all subscribers of app events"""
        for es in self.event_subscribers:
            es.update(events)

    def minimum_window_size(self) -> tuple:
        """Gets the minimum window size to fit all widgets"""
        allwidgets = [*self.widgets, *self.passive_widgets]
        maxypos = max([x['pos'][0] + len(x['widget'].render_lines()) for x in allwidgets])
        maxxpos = max([x['pos'][1] + max([len(line) for line in x['widget'].render_lines()]) for x in allwidgets])
        return maxypos, maxxpos


class MusicEventHandler:
    """Example subscriber of app events"""

    def __init__(self):
        self.currentsong = ''
        self.musicplayer = MusicPlayer()
        self.queue = []
        self.queue_pointer = 0

    def update(self, event: dict) -> None:
        """Called when app subscribed to has an event"""

        songfile = event['filename']
        event_type = event['controls']
        if event_type == "play":
            self.queue = FileHandler(MUSIC_DIR).files
            if not songfile == self.currentsong:  # If a song hasn't been selected already
                self.currentsong = songfile
                self.musicplayer.load_file(MUSIC_DIR + songfile)
                self.musicplayer.play()
            else:
                self.musicplayer.unpause()

        elif event_type == "pause":
            self.musicplayer.pause()

        elif event_type == "next" and len(self.queue) != 0:
            self.queue_pointer += (self.queue.index(songfile)+1)
            self.queue_pointer = self.queue_pointer % len(self.queue)
            self.musicplayer.load_file(MUSIC_DIR+self.queue[self.queue_pointer])
            self.musicplayer.play()

        elif event_type == "previous" and len(self.queue) != 0:
            self.queue_pointer += self.queue.index(songfile)-1
            self.queue_pointer = self.queue_pointer % len(self.queue)
            self.musicplayer.load_file(MUSIC_DIR+self.queue[self.queue_pointer])
            self.musicplayer.play()


if __name__ == "__main__":
    term = Terminal()

    # o1 = Option(["abbas band"], "abbas band.mp3")
    # o2 = Option(["the king"], "the king.mp3")
    # o3 = Option(["flinstones"], "flinstones.mp3")
    # o4 = Option(["superman"], "superman.mp3")
    # o5 = Option(["Breath"], "Breath.mp3")
    # options2 = [o1, o2, o3, o4, o5]

    controls = SelectWidget([Option(["     ", " <<< ", "     "], "previous"),
                             Option(["      ", " play ", "      "], "play"),
                             Option(["       ", " Pause ", "       "], "pause"),
                             Option(["     ", " >>> ", "     "], "next")], layout="Horizontal")

    fh = FileHandler(MUSIC_DIR)
    files = fh.files
    filenames = []
    for file in files:
        filenames.append(Option([file], file))
    music_menu = SelectWidget(filenames)
    music_menu.name = 'filename'

    mini_controls = SelectWidget([Option([" <<< "], "previous"),
                                  Option([" play "], "play"),
                                  Option([" Pause "], "pause"),
                                  Option([" >>> "], "next")], layout="Horizontal")
    controls.name = 'controls'

    volct = SelectWidget([Option(['x'], "0"),
                          Option(['='], "0.2"),
                          Option(['='], "0.4"),
                          Option(['='], "0.6"),
                          Option(['='], "0.8"),
                          Option(['='], "1")], layout="Horizontal")
    volct.header = 'Volume: ' + term.on_green
    volct.name = 'volume'

    progressbar = ProgessBarWidget('progressbar', 10, term)
    progressbar.length = 10

    printevent = MusicEventHandler()

    m = MusicTerminal(term)
    m.add_widget(music_menu, (2, 2))
    m.add_widget(progressbar, (len(music_menu.options) + 4, 2))
    m.add_widget(volct, (len(music_menu.options) + 7, 2))
    m.add_widget(controls, (len(music_menu.options) + 8, 2))
    m.small_window_widget = mini_controls

    m.add_event_subscriber(printevent)
    m.run()
