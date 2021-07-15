import blessed

CODES = blessed.keyboard.get_keyboard_codes()


class Widget:
    """Generic widget class"""

    def __init__(self, name: str = '', passive: bool = False):
        self.name = name
        self.passive = passive


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


class ProgressBarWidget(Widget):
    """Progress bar for showing progress"""

    def __init__(self, name: str = '', length: int = 5, terminal: blessed.Terminal = None):
        Widget.__init__(self, name, True)
        self.term = terminal if terminal else blessed.terminal
        self.length = length
        self.fillstyle = self.term.on_white
        self.progress = 4

    def render_lines(self) -> list:
        """Returns lines to be rendered"""
        lines = list()
        lines.append(chr(9556) + chr(9552) * self.length + chr(9559))
        lines.append(chr(9553) + f'{self.fillstyle}' + ' ' * self.progress + f'{self.term.normal}' + ' '
                     * (self.length - self.progress) + chr(9553))
        lines.append(chr(9562) + chr(9552) * self.length + chr(9565))
        return lines

    def update(self, events: dict) -> None:
        """Update the progress bar with song progress"""
        print(events['progress'])
        self.progress = events['progress']


class SelectWidget(Widget):
    """Selection pane for selecting from a menu or control"""

    def __init__(self, options: list[Option] = None, initialchoice: int = None, selectformat: object = None,
                 layout: str = 'Verticle', terminal: blessed.Terminal = None):
        Widget.__init__(self, '')
        self.term = terminal if terminal else blessed.terminal
        self.options = options if options else []
        self.choiceindex = initialchoice if initialchoice else 0
        self.selectformat = selectformat if selectformat else self.term.on_green
        self.layout = layout
        self.header = ''
        self.footer = ''
        self.optionlead = self.term.on_green
        self.optiontail = self.term.normal

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
                    phrase += f"{self.selectformat}{self.options[i].line(row)}{self.term.normal} "
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
                    phrase.append(f"{self.term.on_green}{self.options[i].line(row)}{self.term.normal}")
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
