from PIL import Image

class Color(object):
    """The class that contains a color code and its name"""
    def __init__(self, name, code, rgb = (0,0,0)):
        """Set the name of the color and code"""
        self._name = name
        self._code = code
        self._rgb  = rgb

    def get_name(self):
        return self._name
    def get_code(self):
        return self._code
    def get_rgb(self):
        return self._rgb
    name = property(get_name)
    code = property(get_code)
    rgb  = property(get_rgb)

class Palette(object):
    def __init__(self, color_list=[]):
        self._color_list = {}
        for i in color_list:
            self.add(i)
    
    def add(self, color):
        """Add a color to the color list."""
        self._color_list[color.name] = color

    def get_code(self, name):
        """Get the corresponding code of given color name."""
        return self._color_list[name].code

    def get_rgb(self, name):
        """Get the corresponding rgb values of give name"""
        return self._color_list[name].rgb

    def get_color_class(self):
        return self._color_list.values()

    def get_color_list(self):
        """Get the list of colors in user-friendly syntax."""
        return list(self._color_list.keys())

    def color_class():
        """The color_class property."""
        def fget(self):
            return self._color_list.values()
        return locals()
    color_class = property(**color_class())

    def color_list():
        """The color_list property."""
        def fget(self):
            return self.get_color_list()
        def fset(self, values):
            """Add colors from a list of 'Color' class."""
            for i in values:
                self.add(i)
        return locals()
    color_list = property(**color_list())

class ColText(object):
    """The class that contains colored text."""
    def __init__(self, text, color = "", end = ""):
        self._text = text
        self._color = color
        self.end = end

    def colored_text():
        """The colored_text."""
        def fget(self):
            return self._color + self._text + self.end
        return locals()
    colored_text = property(**colored_text())

class Motd(object):
    def __init__(self, palette):
        self.s = []
        self.p = palette

    def append(self, string, color_name, end = " "):
        self.s.append(ColText(string + end, self.p.get_code(color_name)))

    def append_line(self, string, color_name):
        self.append(string, color_name)
        self.new_line()

    def new_line(self):
        self.s.append(ColText("\n", "\033[39;49m"))

    def colored_text():
        """Get colored text."""
        def fget(self):
            out = ""
            for i in self.s:
                out += i.colored_text
            return out
        return locals()
    colored_text = property(**colored_text())

    def color_list():
        """The list of colors."""
        def fget(self):
            return self.p.color_list
        return locals()
    color_list = property(**color_list())

class ImageMotd(Motd):
    def __init__(self, palette, file_name="", text="  "):
        Motd.__init__(self, palette)
        self._t = text
        if file_name != "":
            self.open(file_name)

    def open(self, file_name):
        self.img = Image.open(file_name, "r")
        px = self.img.load()

        for y in range(self.img.size[1]):
            for x in range(self.img.size[0]):
                p = px[x, y]
                p_bef = (-1, -1, -1)

                for c in self.p.color_class:
                    if p == c.rgb:
                        if p == p_bef:
                            self.s.append(ColText(self._t, ""))
                        else:
                            p_bef = p
                            self.s.append(ColText(self._t, c.code))
            self.new_line()

    def text():
        """Fill character(s)"""
        def fget(self):
            return self._t
        def fset(self, value):
            self._t = value
        return locals()
    text = property(**text())

def main():
    p = Palette(
        [
            Color("BLACK",   "\033[100m", (0,0,0)),
            Color("RED",     "\033[101m", (255,0,0)),
            Color("GREEN",   "\033[102m", (0,255,0)),
            Color("YELLOW",  "\033[103m", (255,255,0)),
            Color("BLUE",    "\033[104m", (0,0,255)),
            Color("MAGENTA", "\033[105m", (255,0,255)),
            Color("CYAN",    "\033[106m", (0,255,255)),
            Color("WHITE",   "\033[107m", (255,255,255)),

            Color("D_RED",     "\033[0;41m", (127,0,0)),
            Color("D_GREEN",   "\033[0;42m", (0,127,0)),
            Color("D_YELLOW",  "\033[0;43m", (127,127,0)),
            Color("D_BLUE",    "\033[0;44m", (0,0,127)),
            Color("D_MAGENTA", "\033[0;45m", (127,0,127)),
            Color("D_CYAN",    "\033[0;46m", (0,127,127)),

            Color("GRAY",      "\033[0;47m", (127,127,127)),

            #Color("RESET",   "\033[1;37m", (-1,-1,-1))
        ]
    )

    m = Motd(p)
    im = ImageMotd(p, file_name = "wooser_s.bmp", text="  ")
    
    s = "Quick brown fox jumps over the lazy dog."
    l = im.color_list
    for i in range(len(l)):
      m.append_line(l[i % len(l)] + " = " + s, l[i % len(l)])
    
    #m.append("Hello", "WHITE")
    #m.append("red", "RED")
    #m.append_line("world!", "WHITE")
    
    print(m.colored_text)

    imstr = im.colored_text
    motd = open("motd", "wb")

    imstr = [ord(x) for x in imstr]
    motd.write(bytes(imstr))
    motd.close()

if __name__ == "__main__":
    main()
