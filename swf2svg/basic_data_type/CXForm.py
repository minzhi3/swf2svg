import swf2svg.bit_reader.BitReader


class CXFormRecord:
    def __init__(self, content):
        self.red_mult_term = None
        self.green_mult_term = None
        self.blue_mult_term = None
        self.red_add_term = None
        self.green_add_term = None
        self.blue_add_term = None
        self.bit_reader = swf2svg.bit_reader.memory_reader(content, offset=0)
        self.has_add_terms = self.bit_reader.read(1)
        self.has_mult_terms = self.bit_reader.read(1)
        self.nbits = self.bit_reader.read(4)

    def read_data(self):
        if self.has_mult_terms:
            self.read_mult_term()
        if self.has_add_terms:
            self.read_add_term()

    def read_mult_term(self):
        self.red_mult_term = self.bit_reader.read_signed(self.nbits)
        self.green_mult_term = self.bit_reader.read_signed(self.nbits)
        self.blue_mult_term = self.bit_reader.read_signed(self.nbits)

    def read_add_term(self):
        self.red_add_term = self.bit_reader.read_signed(self.nbits)
        self.green_add_term = self.bit_reader.read_signed(self.nbits)
        self.blue_add_term = self.bit_reader.read_signed(self.nbits)

    @property
    def size(self):
        return self.bit_reader.offset

    def __str__(self):
        ret = ''
        if self.has_mult_terms:
            ret += 'CXForm  mult:{0},{1},{2}'.format(self.red_mult_term, self.green_mult_term, self.blue_mult_term)
        if self.has_add_terms:
            ret += ' ,add:{0},{1},{2}'.format(self.red_add_term, self.green_add_term, self.blue_add_term)
        return ret


class CXFormWithAlphaRecord(CXFormRecord):
    def __init__(self, content):
        super().__init__(content)
        self.alpha_add_term = None
        self.alpha_mult_term = None

    def read_data(self):
        if self.has_mult_terms:
            self.read_mult_term()
        if self.has_add_terms:
            self.read_add_term()

    def read_mult_term(self):
        super().read_mult_term()
        self.alpha_mult_term = self.bit_reader.read(self.nbits)

    def read_add_term(self):
        super().read_add_term()
        self.alpha_add_term = self.bit_reader.read(self.nbits)

    def __str__(self):
        ret = ''
        if self.has_mult_terms:
            ret += 'CXFormAlpha  mult:{0},{1},{2},{3}'.format(self.red_mult_term, self.green_mult_term,
                                                              self.blue_mult_term,
                                                              self.alpha_mult_term)
        if self.has_add_terms:
            ret += ', add:{0},{1},{2},{3}'.format(self.red_add_term, self.green_add_term, self.blue_add_term,
                                                  self.alpha_add_term)
        return ret
