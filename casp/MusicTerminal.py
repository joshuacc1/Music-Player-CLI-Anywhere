import os
import signal

import blessed
from blessed import Terminal, keyboard

from casp import render
from casp.Widgets import Widget

CODES = keyboard.get_keyboard_codes()


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
        if os.name != 'nt':
            signal.signal(signal.SIGWINCH, self.on_resize)
        self.dummypublishers = []
        self.styles = render.Render()
        self.skin_type = 'dark'

    def on_resize(self, *args) -> None:
        """Executes when windows size changes"""
        if self.term.height > self.minimum_window_size()[0]:
            self.miniwindow = False
            for subscribers in self.event_subscribers:
                subscribers.update({'width_window': self.term.width})
            self.render()
        else:
            self.miniwindow = True
            self.render()

    def run(self) -> None:
        """Runs the app"""
        self.min_win_size = self.minimum_window_size()
        self.render()
        with self.term.cbreak():
            # print(term.clear())
            val = ""
            while val.lower() != "q":
                for pub in self.dummypublishers:
                    if pub.run():
                        self.render()

                val = self.term.inkey(timeout=3)

                # check for pressed values
                if val:
                    if val.is_sequence:
                        self.notifywidget(val)
                        self.render()
                        if CODES[val.code] == 'KEY_ENTER':
                            if self.miniwindow:
                                events = {w.name: w.choice() for w in self.widgets}
                                events[self.small_window_widget.name] = self.small_window_widget.choice()
                                self.push_events(events)
                            else:
                                self.push_events({w.name: w.choice() for w in self.widgets})
                        if CODES[val.code] == 'KEY_TAB':
                            self.widgetfocus = (self.widgetfocus + 1) % len(self.widgets)

    def render(self) -> None:
        """Renders the graphics to screen"""
        if self.miniwindow:
            print(self.term.clear + self.small_window_widget.render_lines()[0])
            return None
        all_widgets = [*self.widgets, *self.passive_widgets]
        all_widgets.sort(key=lambda item: item.get_position()[0])

        screen = []
        for i in range(self.term.height):
            screen.append(' ' * self.term.width)
        screen[0] = screen[0]
        screen[1] = '=' * self.term.width
        screen[-1] = '=' * self.term.width

        for w in all_widgets:
            pos = w.get_position()
            x = pos[0]
            y = pos[1]
            widgetlines = w.render_lines()
            for row in range(len(widgetlines)):
                start = screen[x + row][0:y] if screen[x + row][0:y] else ''
                end = screen[x + row][y + self.term.length(widgetlines[row]):] \
                    if screen[x + row][y + self.term.length(widgetlines[row]):] else ''
                screen[x + row] = start + widgetlines[row] + end
        print(self.term.clear + '\n'.join(screen))

    def add_widget(self, widget: Widget) -> None:
        """Adds a widget to the app"""
        if widget.passive:
            self.passive_widgets.append(widget)
        else:
            self.widgets.append(widget)

    def add_event_subscriber(self, subscriber: object) -> None:
        """Adds a subscriber to app events"""
        self.event_subscribers.append(subscriber)

    def notify(self, keystroke: blessed.keyboard.Keystroke) -> None:
        """Notify widgets of keyboard events"""
        for wp in self.widgets:
            wp.update(keystroke)

    def notifywidget(self, keystroke: blessed.keyboard.Keystroke) -> None:
        """Notify a single widget"""
        if self.miniwindow:
            self.small_window_widget.update(keystroke)
        else:
            self.widgets[self.widgetfocus].update(keystroke)

    def push_events(self, events: dict) -> None:
        """Updates all subscribers of app events"""
        for es in self.event_subscribers:
            es.update(events)

    def minimum_window_size(self) -> tuple:
        """Gets the minimum window size to fit all widgets"""
        allwidgets = [*self.widgets, *self.passive_widgets]
        maxypos = max([x.position[0] + len(x.render_lines()) for x in allwidgets])
        maxxpos = max([x.position[1] + max([len(line) for line in x.render_lines()]) for x in allwidgets])
        return maxypos, maxxpos

    @property
    def skin(self) -> str:
        """Skin getter"""
        return self.skin_type

    @skin.setter
    def skin(self, skin: str = 'dark') -> None:
        """Skin setter"""
        if skin in self.styles.skins:
            self.skin_type = skin
