import swf2svg.bit_reader


class MatrixRecord:
    def __init__(self, content):
        bit_reader = swf2svg.bit_reader.memory_reader(content, offset=0)
        self.has_scale = bit_reader.read(1)
        if self.has_scale:
            self.scale_bits = bit_reader.read(5)
            self.scale_x = bit_reader.read_signed(self.scale_bits) / 65536
            self.scale_y = bit_reader.read_signed(self.scale_bits) / 65536
        else:
            self.scale_bits = 0
            self.scale_x = 1
            self.scale_y = 1
        self.has_rotate = bit_reader.read(1)
        if self.has_rotate:
            self.rotate_bits = bit_reader.read(5)
            self.rotate_skew0 = bit_reader.read_signed(self.rotate_bits) / 65536
            self.rotate_skew1 = bit_reader.read_signed(self.rotate_bits) / 65536
        else:
            self.rotate_bits = 0
            self.rotate_skew0 = 0
            self.rotate_skew1 = 0
        self.translate_bits = bit_reader.read(5)
        self.translate_x = bit_reader.read_signed(self.translate_bits)
        self.translate_y = bit_reader.read_signed(self.translate_bits)
        self.size = bit_reader.offset

    def to_matrix_tuple(self, twink):
        ret = (
            self.scale_x,
            self.rotate_skew0,
            self.rotate_skew1,
            self.scale_y,
            self.translate_x / twink,
            self.translate_y / twink
        )
        return ret

    def __str__(self):
        ret = 'Trans({0},{1})'.format(self.translate_x, self.translate_y)
        if self.has_scale:
            ret += ', Scale({0:.2f},{1:.2f})'.format(self.scale_x, self.scale_y)
        if self.has_rotate:
            ret += ', Rotate({0:.2f},{1:.2f})'.format(self.rotate_skew0, self.rotate_skew1)
        return ret
