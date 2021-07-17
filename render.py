import blessed


class Render:

    def __init__(self, width, height, skin):
        self.term = blessed.Terminal()
        self.width = width
        self.height = height
        self.skin = skin
        self.screen = []
        self.skins = {"classic":{"background": self.term.black_on_white, "bar": self.term.black_on_wheat, "time": self.term.fuchsia, "info": self.term.webpurple},
            "dark":{"background": self.term.white_on_gray22, "bar": self.term.white_on_darkslategray, "time": self.term.turquoise, "info": self.term.orchid1},
            "ocean":{"background": self.term.white_on_darkslategray, "bar": self.term.white_on_cadetblue, "time": self.term.darkgoldenrod4, "info": self.term.dodgerblue4},
            "cyberpunk":{"background": self.term.white_on_black, "bar": self.term.white_on_midnightblue, "time": self.term.aqua, "info": self.term.fuchsia},
            "onedark":{"background": self.term.on_color_rgb(40, 44, 52), "bar": self.term.on_color_rgb(33, 34, 43), "time": self.term.color_rgb(229, 192, 123), "info": self.term.color_rgb(198, 120, 221)},
            "vlc":{"background": self.term.on_color_rgb(255, 255, 255), "bar": self.term.on_color_rgb(239, 239, 239), "time": self.term.color_rgb(249, 181, 95), "info": self.term.color_rgb(118, 118, 118)}
        }

    def render_skin(self, album: str, time1: str, time2: str, progress_bar: str, play: bool, volume: str) -> None:
        '''
        album is n*n string separeted by '\n' with n given by gen_art_dim
        time1 is a 5 character string of the time passed
        time2 is a 5 character sting of the time left/total length of song
        progress_bar is an n character string with n given by gen_progress_dim
        play is a bool, set to True if the button should display "button" and False if "pause"
        volume is a 6 character string of the current volume e.g. --x--- or however it is formatted
        '''
        for i in range(self.height):
            self.screen.append(' ' * self.width)
        self.screen[0] = self.skins[self.skin]["background"] +  ' ' * self.width
        self.screen[-1] =  ' ' * self.width + self.term.normal

        # adding in album art
        album_height = self.gen_art_dim()[0]
        album = album.split("\n")
        for i in range(2, album_height+2):
            album_index = i-2
            self.screen[i] = album[album_index].center(self.width)
        
        # changing colour
        self.screen[-8] += (self.skins[self.skin]["bar"])
        
        # adding in progress bar
        self.screen[-6] = self.skins[self.skin]["info"] + "California Uber Alles".center(self.width) + self.skins[self.skin]["bar"]
        self.screen[-5] = "   " + self.skins[self.skin]["time"] + time1 + self.skins[self.skin]["bar"] + " " + progress_bar  + " " + self.skins[self.skin]["time"] + time2 + self.skins[self.skin]["bar"] + "   "

        # adding play/pause etc
        s = self.skins[self.skin]["info"] + ("play " if play else "pause") + self.skins[self.skin]["bar"]
        t = "    " + s + " " + self.skins[self.skin]["info"] + "|<<" + self.skins[self.skin]["bar"] + "   " + self.skins[self.skin]["info"] + ">>|" + self.skins[self.skin]["bar"]
        n = self.term.length(t)
        self.screen[-3] = t + " "*(self.width-18-n) + self.skins[self.skin]["info"] + "volume: " + volume + self.skins[self.skin]["bar"] + "    "
        


    def gen_art_dim(self) -> (int, int):
        '''generates the dimentions for the album art in the form (height, width)'''
        if (self.width-2)/2 >= self.height-11:
            return self.height-11, (self.height-11)*2
        else:
            return (self.width-2)//2, self.width-2
    
    def gen_progress_dim(self) -> int:
        '''generates the length of progress bar'''
        return self.width - 18

    def print_window(self):
        for i in self.screen:
            print(i)


def gen_album(render):
    # temporary
    height, width = render.gen_art_dim()
    string = "█" * width + "\n"
    string = string * height
    return string


r = Render(150, 40, "onedark")
string = gen_album(r)
length = r.gen_progress_dim()
progress_bar = "-" * length
r.render_skin(string, "00:46", "01:33", progress_bar, True, "--x---")
r.print_window()