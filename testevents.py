#!/usr/bin/env python
"""
Example event model for a selection of strings
"""

# local
from blessed import Terminal

class option:
    def __init__(self,graphic,choice):
        self.graphic = graphic
        self.choice = choice
        self.tl = len(graphic)

    def line(self,line):
        if line > len(self.graphic):
            return '' * len(self.graphic[0])
        return self.graphic[line]


def outputhorizontal(options,choice):
    phrase=''
    for i in range(len(options)):
        if i == choice:
            phrase+=f'{term.on_green}{options[i]}{term.normal} '
        else:
            phrase+=f'{options[i]} '
        #phrase=phrase[0:-2]
    return term.clear() + phrase

def multilineoutputhorizontal(options,choice):
    phrase=''
    maxlines=max([len(x.graphic) for x in options])
    for l in range(maxlines):
        for i in range(len(options)):
            if i == choice:
                phrase+=f'{term.on_green}{options[i].line(l)}{term.normal} '
            else:
                phrase+=f'{options[i].line(l)} '
        phrase+='\n'
        #phrase=phrase[0:-2]
    return term.clear() + phrase

def multilineoutputverticle(options,choice):
    phrase=''
    maxlines=max([len(x.graphic) for x in options])
    for i in range(len(options)):
        for l in range(maxlines):
            if i == choice:
                phrase+=f'{term.on_green}{options[i].line(l)}{term.normal}\n'
            else:
                phrase+=f'{options[i].line(l)}\n'
        #phrase=phrase[0:-2]
    return term.clear() + phrase


def renderverticleoptions(term,options,initialchoice):
    choice=initialchoice
    print(multilineoutputverticle(options, choice))
    with term.cbreak():
        #print(term.clear())
        val = ''
        phrase = ''
        while val.lower() != 'q':
            val=term.inkey(timeout=3)
            if val:
                if val.code == 258:
                    #left
                    choice = (choice + 1) % len(options)
                elif val.code == 259:
                    #right
                    choice = (choice - 1) % len(options)
                print(multilineoutputverticle(options,choice))
            if val.is_sequence:
                if val.code == 343:
                    print("You just chose: {0}".format(options[choice].choice))

def renderhorizontaloptions(term,options,initialchoice):
    choice=initialchoice
    print(multilineoutputhorizontal(options, choice))
    with term.cbreak():
        #print(term.clear())
        val = ''
        phrase = ''
        while val.lower() != 'q':
            val=term.inkey(timeout=3)
            if val:
                if val.code == 261:
                    #left
                    choice = (choice + 1) % len(options)
                elif val.code == 260:
                    #right
                    choice = (choice - 1) % len(options)
                print(multilineoutputhorizontal(options,choice))
            if val.is_sequence:
                if val.code == 343:
                    print("You just chose: {0}".format(options[choice].choice))


if __name__ == "__main__":
    term = Terminal()

    o1 = option(['   ', '<<<', '   '], 'previous')
    o2 = option(['    ', 'play', '    '], 'play')
    o3 = option(['     ', 'Pause', '     '], 'pause')
    o4 = option(['   ', '>>>', '   '], 'next')

    # options=['<<','play','pause','>>']
    options = [o1, o2, o3, o4]
    choice = 0

    o1 = option(['abbas band'], 'abbas band.mp3')
    o2 = option(['the king'], 'the king.mp3')
    o3 = option(['flinstones'], 'flinstones.mp3')
    o4 = option(['superman'], 'superman.mp3')

    options2 = [o1, o2, o3, o4]
    choice = 0

    renderverticleoptions(term,options2,1)

    renderhorizontaloptions(term,options,1)


##Example editor
# with term.cbreak():
#     print(term.clear())
#     val=''
#     phrase = ''
#     while val.lower() != 'q':
#         val=term.inkey(timeout=3)
#
#         if val:
#             phrase += val
#             print(term.clear() + str(phrase))
#         if val.is_sequence:
#             if val.code == 263:
#                 phrase=phrase[0:-2]
#                 print(term.clear() + str(phrase))
#         # elif val.is_sequence:
#         #     print("got sequence: {0}.".format((str(val),val.name,val.code)))
#         # elif val:
#         #     print("got {0}".format(val))