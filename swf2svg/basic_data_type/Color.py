class RGBColorRecord:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    @property
    def size(self):
        return 3

    def __str__(self):
        return "RGB({0},{1},{2})".format(self.red, self.green, self.blue)


class RGBAColorRecord(RGBColorRecord):
    def __init__(self, red, green, blue, alpha):
        super().__init__(red, green, blue)
        self.alpha = alpha

    @property
    def size(self):
        return 4

    def __str__(self):
        return "RGBA({0},{1},{2},{3})".format(self.red, self.green, self.blue, self.alpha)
