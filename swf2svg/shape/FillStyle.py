import struct
import swf2svg.basic_data_type as basic_type
import swf2svg.shape


class FillStyleArray:
    def __init__(self, content, shape_generation):
        self.content = content
        self.shape_generation = shape_generation
        self.data = list()
        self.count = 0
        self.count_extend = 0
        self.size = self.read_data()

    def read_data(self):
        point = 0
        self.count = struct.unpack_from('B', self.content, point)[0]
        point += 1
        if self.count == 0xFF:
            count_extend = struct.unpack_from('H', self.content, point)[0]
            point += 2
            self.count = count_extend

        for i in range(0, self.count):
            fill_style = FillStyle(self.content[point:], self.shape_generation)
            self.data.append(fill_style)
            point += fill_style.size

        return point

    def __str__(self):
        if self.count > 0:
            return '[' + '  '.join(format(data_str, '') for data_str in self.data) + ']'
        else:
            return '_'


class FillStyle:
    def __init__(self, content, shape_generation):
        self.content = content
        self.shape_generation = shape_generation
        self.type = 0
        self.gradient_matrix = None
        self.gradient = None

        point = 0
        self.type = struct.unpack_from('B', self.content, point)[0]
        point += 1
        if self.type == 0x00:
            if self.shape_generation <= 2:
                self.color = basic_type.read_color(*(struct.unpack_from('BBB', self.content, point)), alpha=None)
                point += 3
            else:
                self.color = basic_type.read_color(*(struct.unpack_from('BBBB', self.content, point)))
                point += 4

        elif self.type in [0x10, 0x12, 0x13]:  # GradientMatrix
            self.gradient_matrix = basic_type.read_matrix(self.content[point:])
            point = self.gradient_matrix.size
            if self.type in [0x10, 0x12]:  # Gradient
                self.gradient = swf2svg.shape.read_gradient(self.content[point:], self.shape_generation)
            else:
                raise Exception('unknown gradient type {:#02x}'.format(self.type))
        else:
            raise Exception('unknown color type {:#02x}'.format(self.type))

        self.size = point

    def __str__(self):
        if self.type == 0x00:
            return 'FillStyle: {0}'.format(self.color)
        elif self.type in [0x10, 0x12, 0x13]:  # GradientMatrix
            return 'Gradient: {0}, {1}'.format(self.gradient_matrix, self.gradient)
