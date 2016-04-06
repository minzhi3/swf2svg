from BitReader import BitReader, MemoryBuffer


class MatrixRecord:
    def __init__(self, content):
        bit_reader = BitReader(MemoryBuffer(content, 0))
        self.has_scale = bit_reader.read(1)
        if self.has_scale:
            self.scale_bits = bit_reader.read(5)
            self.scale_x = bit_reader.read_signed(self.scale_bits)/65536
            self.scale_y = bit_reader.read_signed(self.scale_bits)/65536
        else:
            self.scale_bits = None
            self.scale_x = None
            self.scale_y = None
        self.has_rotate = bit_reader.read(1)
        if self.has_rotate:
            self.rotate_bits = bit_reader.read(5)
            self.rotate_skew0 = bit_reader.read_signed(self.rotate_bits)/65536
            self.rotate_skew1 = bit_reader.read_signed(self.rotate_bits)/65536
        else:
            self.rotate_bits = None
            self.rotate_skew0 = None
            self.rotate_skew1 = None
        self.translate_bits = bit_reader.read(5)
        self.translate_x = bit_reader.read_signed(self.translate_bits)
        self.translate_y = bit_reader.read_signed(self.translate_bits)
        self.size = bit_reader.offset

    def __str__(self):
        ret = 'Trans({0},{1})'.format(self.translate_x, self.translate_y)
        if self.has_scale:
            ret += ', Scale({0:.2f},{1:.2f})'.format(self.scale_x, self.scale_y)
        return ret
