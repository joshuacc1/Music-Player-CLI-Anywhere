#!/usr/bin/env python
"""
Example event model for a selection of strings
"""

import types

# local
import blessed.keyboard
from blessed import Terminal

CODES=blessed.keyboard.get_keyboard_codes()

class Option:
    def __init__(self, graphic, choice):
        self.graphic = graphic
        self.choice = choice
        self.tl = len(graphic)

    def line(self, line):
        if line > len(self.graphic):
            return "" * len(self.graphic[0])
        return self.graphic[line]


class SelectWidget:
    def __init__(self, options:list[Option]=None, initialchoice:int=None, selectformat:object=None,layout='Verticle'):
        self.options=options if options else []
        self.choiceindex=initialchoice if initialchoice else 0
        self.selectformat=selectformat if selectformat else term.on_green
        self.layout=layout

    def render(self):
        if self.layout=='Horizontal':
            return self.render_horizontal()
        else:
            return self.render_verticle()

    def render_horizontal(self):
        phrase = ""
        maxlines = max([len(x.graphic) for x in self.options])
        for l in range(maxlines):
            for i in range(len(self.options)):
                if i == self.choiceindex:
                    phrase += f"{self.selectformat}{self.options[i].line(l)}{term.normal} "
                else:
                    phrase += f"{self.options[i].line(l)} "
            phrase += "\n"
        return phrase

    def render_verticle(self):
        phrase = ""
        maxlines = max([len(x.graphic) for x in self.options])
        for i in range(len(self.options)):
            for l in range(maxlines):
                if i == self.choiceindex:
                    phrase += f"{term.on_green}{self.options[i].line(l)}{term.normal}\n"
                else:
                    phrase += f"{self.options[i].line(l)}\n"
        return phrase

    def render_lines(self):
        if self.layout=='Horizontal':
            return self.render_lines_horizontal()
        else:
            return self.render_lines_verticle()

    def render_lines_horizontal(self):
        phrase = []
        maxlines = max([len(x.graphic) for x in self.options])
        for l in range(maxlines):
            line=''
            for i in range(len(self.options)):
                if i == self.choiceindex:
                    line+=f"{self.selectformat}{self.options[i].line(l)}{term.normal} "
                else:
                    line+=f"{self.options[i].line(l)} "
            phrase.append(line)
            # phrase=phrase[0:-2]
        return phrase

    def render_lines_verticle(self):
        phrase = []
        maxlines = max([len(x.graphic) for x in self.options])
        for i in range(len(self.options)):
            for l in range(maxlines):
                if i == self.choiceindex:
                    phrase.append(f"{term.on_green}{self.options[i].line(l)}{term.normal}")
                else:
                    phrase.append(f"{self.options[i].line(l)}")
        return phrase

    def choice(self):
        return self.options[self.choiceindex].choice

    def update(self,keystroke):
        if self.layout=='Horizontal':
            if CODES[keystroke.code] == 'KEY_RIGHT':
                self.choiceindex = (self.choiceindex + 1) % len(options)
            elif CODES[keystroke.code] == 'KEY_LEFT':
                self.choiceindex = (self.choiceindex - 1) % len(options)
        else:
            if CODES[keystroke.code] == 'KEY_DOWN':
                self.choiceindex = (self.choiceindex + 1) % (len(options)+1)
            elif CODES[keystroke.code] == 'KEY_UP':
                self.choiceindex = (self.choiceindex - 1) % (len(options)+1)


class MusicTerminal:
    def __init__(self,terminal):
        self.widgets=[]
        self.term=terminal
        self.event_subscribers=[]
        self.widgetfocus=0

    def run(self):
        self.render()
        with term.cbreak():
            # print(term.clear())
            val = ""
            phrase = ""
            while val.lower() != "q":
                val = term.inkey(timeout=3)
                if val:
                    self.notifywidget(val)
                    self.render()
                    if CODES[val.code]=='KEY_ENTER':
                        self.push_events([w['widget'].choice() for w in self.widgets])
                    if CODES[val.code]=='KEY_TAB':
                        self.widgetfocus=(self.widgetfocus + 1) % len(self.widgets)


    def render(self):
        self.widgets.sort(key=lambda x:x['pos'][0])
        screen=[]
        for i in range(10):
            screen.append(' '*term.width)

        for w in self.widgets:
            x=w["pos"][0]
            y=w['pos'][1]
            widgetlines=w['widget'].render_lines()
            for l in range(len(widgetlines)):
                start=screen[x+l][0:y] if screen[x+l][0:y] else ''
                end=screen[x+l][y+len(widgetlines[l]):] if screen[x+l][y+len(widgetlines[l]):] else ''
                screen[x+l]=start+widgetlines[l]+end
        print(self.term.clear+'\n'.join(screen))

    def add_widget(self,widget,position):
        self.widgets.append({'widget':widget,'pos':position})

    def add_event_subscriber(self,subscriber):
        self.event_subscribers.append(subscriber)

    def notify(self,keystroke):
        for wp in self.widgets:
            w=wp['widget']
            w.update(keystroke)

    def notifywidget(self,keystroke):
        self.widgets[self.widgetfocus]['widget'].update(keystroke)

    def push_events(self,events):
        for es in self.event_subscribers:
            es.update(events)

class EventSubscriber:
    def __init__(self):
        pass

    def update(self,event):
        print(event)

if __name__ == "__main__":
    term = Terminal()

    o1 = Option(["   ", "<<<", "   "], "previous")
    o2 = Option(["    ", "play", "    "], "play")
    o3 = Option(["     ", "Pause", "     "], "pause")
    o4 = Option(["   ", ">>>", "   "], "next")
    options = [o1, o2, o3, o4]

    o1 = Option(["abbas band"], "abbas band.mp3")
    o2 = Option(["the king"], "the king.mp3")
    o3 = Option(["flinstones"], "flinstones.mp3")
    o4 = Option(["superman"], "superman.mp3")
    o5 = Option(["Breath"], "Breath.mp3")
    options2 = [o1, o2, o3, o4, o5]

    volct=SelectWidget([Option(['='], "v5"),
                       Option(['='], "v4"),
                       Option(['='], "v3"),
                       Option(['='], "v2"),
                       Option(['='], "v1")])

    sw=SelectWidget(options2)
    sw2=SelectWidget(options,layout="Horizontal")
    printevent=EventSubscriber()
    m=MusicTerminal(term)
    m.add_widget(sw,  (1,0))
    m.add_widget(sw2, (7,0))
    #m.add_widget(volct, (1,30))
    #m.add_event_subscriber(printevent)
    m.run()
