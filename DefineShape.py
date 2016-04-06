import struct
from BitReader import MemoryBuffer
from ShapeWithStyle import ShapeWithStyle
from TagData import TagData
from util import read_rect


class DefineShape(TagData):
    def __init__(self, content):
        super().__init__(content)
        self.shape_with_style = None  # type: ShapeWithStyle
        self.shape_rect = None
        self.id = struct.unpack_from("H", content)[0]
        self.shape_generation = 1
        self.tag_id = 2

    def _read_head(self):
        memory_buffer = MemoryBuffer(self.content, 2)
        self.shape_rect = read_rect(memory_buffer)
        return memory_buffer.offset

    def read_data(self):
        point = self._read_head()
        self.shape_with_style = ShapeWithStyle(self.content[point:], self.shape_generation)

    def __str__(self):
        ret = 'DefineShape{0} id:{1}, rect:{2}'.format(self.shape_generation, self.id, self.shape_rect)
        ret += '\n\t{0}'.format(self.shape_with_style)
        return ret


class DefineShape2(DefineShape):
    def __init__(self, content):
        super().__init__(content)
        self.shape_generation = 2
        self.tag_id = 22


class DefineShape3(DefineShape):
    def __init__(self, content):
        super().__init__(content)
        self.shape_generation = 3
        self.tag_id = 32

