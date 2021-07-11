#!/usr/bin/env python
"""
Example event model for a selection of strings
"""

# local
from blessed import Terminal


term = Terminal()

phrase=f'{term.on_blue}X{term.normal} Y Z'
options=['<<','play','pause','>>']
choice=0


def output(options,choice):
    phrase=''
    for i in range(len(options)):
        if i == choice:
            phrase+=f'{term.on_blue}{options[i]}{term.normal} '
        else:
            phrase+=f'{options[i]} '
        #phrase=phrase[0:-2]
    return term.clear() + phrase

print(output(options,choice))
with term.cbreak():
    #print(term.clear())
    val=''
    phrase = ''
    while val.lower() != 'q':
        val=term.inkey(timeout=3)
        if val:
            if val.code == 261:
                #left
                choice=(choice+1)%len(options)
            elif val.code == 260:
                #right
                choice =(choice - 1) % len(options)
            print(output(options,choice))
        if val.is_sequence:
            if val.code == 343:
                print("You just chose: {0}".format(options[choice]))


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