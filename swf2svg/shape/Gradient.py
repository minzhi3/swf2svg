import struct
import swf2svg.basic_data_type as basic_type


class Gradient:
    def __init__(self, content, shape_generation):
        flag_byte = struct.unpack_from('B', content, 0)[0]
        self.content = content
        self.shape_generation = shape_generation
        self.spread_mode = flag_byte >> 6
        self.interpolation_mode = (flag_byte >> 4) & 0x3
        self.num_gradients = flag_byte & 0xF
        self.grad_records = list()
        self.size_count = 0

        self.read_data()

    def read_data(self):
        point = 1
        for i in range(0, self.num_gradients):
            grad_record = GradRecord(self.content[point:], self.shape_generation)
            self.grad_records.append(grad_record)
            point += grad_record.size
        self.size_count = point

    @property
    def size(self):
        return self.size_count


class GradRecord:
    def __init__(self, content, shape_generation):
        self.content = content
        self.ratio = struct.unpack_from('B', content)
        if shape_generation <= 2:
            self.color = basic_type.read_color(*(struct.unpack_from('BBB', self.content, 1)), alpha=None)
        elif shape_generation == 3:
            self.color = basic_type.read_color(*(struct.unpack_from('BBB', self.content, 1)))

    @property
    def size(self):
        return self.color.size + 1
