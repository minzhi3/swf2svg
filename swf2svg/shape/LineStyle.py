import struct
import swf2svg.basic_data_type as basic_type


class LineStyleArray:
    def __init__(self, content, shape_generation):
        self.content = content
        self.shape_generation = shape_generation
        self.data = []
        self.count = 0
        self.count_extend = 0
        self.read_data()
        self.size = self.read_data()

    def read_data(self):
        point = 0
        self.count = struct.unpack_from('B', self.content, point)[0]
        point += 1
        if self.count == 0xFF:
            count_extend = struct.unpack_from('H', self.content, point)
            point += 2
            self.count = count_extend

        if self.shape_generation <= 3:
            for i in range(1, self.count_extend):
                fill_style = LineStyle(self.content[point:], self.shape_generation)
                self.data.append(fill_style)
                point += fill_style.size
        else:
            raise Exception('not support shape 4')

        return point

    def __str__(self):
        if self.count > 0:
            return '[' + '  '.join(format(data_str, '') for data_str in self.data) + ']'
        else:
            return '_'


class LineStyle:
    def __init__(self, content, shape_generation):
        self.content = content
        self.shape_generation = shape_generation
        self.width = 0
        self.color = None
        self.size = self.read_data()

    def read_data(self):
        point = 0
        self.width = struct.unpack_from('H', self.content, point)[0]
        point += 2
        if self.shape_generation <= 2:
            self.color = basic_type.read_color(*(struct.unpack_from('BBB', self.content, point)), alpha=None)
            point += 3
        return point

    def __str__(self):
        return 'LineStyle: {0}'.format(self.color)
