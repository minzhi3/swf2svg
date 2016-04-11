import struct
import swf2svg.shape
import swf2svg.bit_reader.BitReader as BitReader


class StyleChangeRecord:
    def __init__(self, content, shape_generation, bit_reader: BitReader.BitReader, end_flag, fill_bits, line_bits):
        self.content = content
        self.shape_generation = shape_generation
        self.bit_reader = bit_reader
        self.type_flag = 0
        self.end = 0
        self.state_new_styles = end_flag & 0x10 > 0
        self.state_line_style = end_flag & 0x8 > 0
        self.state_fill_style1 = end_flag & 0x4 > 0
        self.state_fill_style0 = end_flag & 0x2 > 0
        self.state_move_to = end_flag & 0x1 > 0

        self.fill_bits = fill_bits
        self.line_bits = line_bits
        self.state_move_bits = None
        self.move_delta_x = None
        self.move_delta_y = None
        self.fill_style0 = None
        self.fill_style1 = None
        self.line_style = None
        self.fill_styles = None
        self.line_styles = None
        self.size, self.new_style_size = self.read_data()

    def read_data(self):
        if self.state_move_to:
            self.state_move_bits = self.bit_reader.read(5)
            self.move_delta_x = self.bit_reader.read_signed(self.state_move_bits)
            self.move_delta_y = self.bit_reader.read_signed(self.state_move_bits)
        if self.state_fill_style0:
            self.fill_style0 = self.bit_reader.read(self.fill_bits)
        if self.state_fill_style1:
            self.fill_style1 = self.bit_reader.read(self.fill_bits)
        if self.state_line_style:
            self.line_style = self.bit_reader.read(self.line_bits)

        buffer = self.bit_reader.remain_buffer

        point = 0
        if self.state_new_styles:
            self.fill_styles = swf2svg.shape.read_fill_style_array(buffer, self.shape_generation)
            point += self.fill_styles.size
            self.line_styles = swf2svg.shape.read_line_style_array(buffer[point:], self.shape_generation)
            point += self.line_styles.size
            num_bits = struct.unpack_from("B", buffer, point)[0]
            point += 1
            self.fill_bits = num_bits >> 4
            self.line_bits = num_bits & 0xF

        return self.bit_reader.offset + point, point

    def __str__(self):
        ret = 'StyleChangeRecord size:{0}'.format(self.size, self.move_delta_x, self.move_delta_y)
        if self.state_move_to:
            ret += ', move: ({0},{1})'.format(self.move_delta_x, self.move_delta_y)
        if self.state_fill_style0:
            ret += ', fill_style0:{0}'.format(self.fill_style0)
        if self.state_fill_style1:
            ret += ', fill_style1:{0}'.format(self.fill_style1)
        if self.state_line_style:
            ret += ', line_style:{0}'.format(self.line_style)
        if self.state_new_styles:
            ret += ', new style:{0}, {1}'.format(self.fill_styles, self.line_styles)
        return ret


class CurvedEdgeRecord:
    def __init__(self, bit_reader):
        self.bit_reader = bit_reader
        self.type_flag = 1
        self.straight_flag = 0
        self.num_bits = None
        self.control_delta_x = None
        self.control_delta_y = None
        self.anchor_delta_x = None
        self.anchor_delta_y = None
        self.size = self.read_data()

    def read_data(self):
        point = self.bit_reader.offset
        self.num_bits = self.bit_reader.read(4)
        self.control_delta_x = self.bit_reader.read_signed(self.num_bits + 2)
        self.control_delta_y = self.bit_reader.read_signed(self.num_bits + 2)
        self.anchor_delta_x = self.bit_reader.read_signed(self.num_bits + 2)
        self.anchor_delta_y = self.bit_reader.read_signed(self.num_bits + 2)

        return self.bit_reader.offset - point

    def __str__(self):
        ret = 'CurvedEdgeRecord size:{0}'.format(self.size)
        ret += ', C ({0},{1})'.format(self.control_delta_x, self.control_delta_y)
        ret += ', A ({0},{1})'.format(self.anchor_delta_x, self.anchor_delta_y)
        return ret


class StraightEdgeRecord:
    def __init__(self, bit_reader):
        self.bit_reader = bit_reader
        self.type_flag = 1
        self.straight_flag = 1
        self.num_bits = None
        self.general_line_flag = None
        self.vert_line_flag = None
        self.delta_x = None
        self.delta_y = None
        self.size = self.read_data()

    def read_data(self):
        point = self.bit_reader.offset
        self.num_bits = self.bit_reader.read(4)
        self.general_line_flag = self.bit_reader.read(1)
        if self.general_line_flag == 0:
            self.vert_line_flag = self.bit_reader.read(1)
        if self.general_line_flag or self.vert_line_flag == 0:
            self.delta_x = self.bit_reader.read_signed(self.num_bits + 2)
        if self.general_line_flag or self.vert_line_flag == 1:
            self.delta_y = self.bit_reader.read_signed(self.num_bits + 2)

        return self.bit_reader.offset - point

    def __str__(self):
        ret = 'StraightEdgeRecord size:{0}'.format(self.size)
        ret += ', M ({0},{1})'.format(self.delta_x, self.delta_y)
        return ret


class EndRecord:
    def __init__(self):
        self.type_flag = 0
        self.end = 1

    def __str__(self):
        return 'EndRecord'
