import struct
import xml.etree.ElementTree as ET
import swf2svg.basic_data_type as basic_type
from swf2svg.TagData import TagData


class PlaceObject2(TagData):
    def __init__(self, content):
        super().__init__(content)
        self.tag_id = 26
        flags = struct.unpack_from("B", content)[0]
        self.flag_clip_action = flags & 0x80 > 0
        self.flag_clip_depth = flags & 0x40 > 0
        self.flag_name = flags & 0x20 > 0
        self.flag_ratio = flags & 0x10 > 0
        self.flag_color_transform = flags & 0x08 > 0
        self.flag_matrix = flags & 0x04 > 0
        self.flag_character = flags & 0x02 > 0
        self.flag_move = flags & 0x01 > 0
        self.depth = struct.unpack_from("H", content, 1)[0]

        self.character_id = None
        self.matrix = None
        self.color_transform = None
        self.ratio = None
        self.name = None
        self.clip_depth = None
        self.clip_action = None
        self.read_data()

    def read_data(self):
        point = 3
        if self.flag_character:
            self.character_id = struct.unpack_from("H", self.content, point)[0]
            point += 2
        if self.flag_matrix:
            self.matrix = basic_type.read_matrix(self.content[point:])
            point += self.matrix.size
        if self.flag_color_transform:
            self.color_transform = basic_type.read_cx_form_with_alpha(self.content[point:])
            self.color_transform.read_data()
            point += self.color_transform.size
        if self.flag_ratio:
            self.ratio = struct.unpack_from("H", self.content, point)[0]
            point += 2
        if self.flag_name:
            string_end = point
            while self.content[string_end] != 0:
                string_end += 1
            self.name = self.content[point:string_end].decode()
            point = string_end
        if self.flag_clip_depth:
            raise Exception
        if self.flag_clip_action:
            raise Exception

    def to_xml(self, twink):
        if self.flag_character:
            # group_attr = {'id': 'parent{0:>02}_depth{1:>02}'.format(self.parent_id, self.depth)}
            use_attr = {'xlink:href': '#symbol{:>02}'.format(self.character_id)}
            # if self.flag_matrix:
            # group_attr['transform'] = 'matrix({0},{1},{2},{3},{4},{5})'.format(*(self.matrix.to_matrix_tuple(twink)))
            use_node = ET.Element('use', use_attr)
            # group_node = ET.Element('g', group_attr)
            # group_node.append(use_node)
            return use_node
        else:
            return None

    def to_dict(self, twink):
        if self.flag_matrix:
            animation = dict()
            animation['transform'] = 'matrix({0},{1},{2},{3},{4},{5})'.format(*(self.matrix.to_matrix_tuple(twink)))
            return animation
        else:
            return None

    def __str__(self):
        ret = 'PlaceObject2 size:{0}, name:{1}, character:{2}, move:{3}, depth:{4}'.format(self.size, self.name,
                                                                                           self.character_id,
                                                                                           self.flag_move,
                                                                                           self.depth)
        if self.flag_matrix:
            ret += '\n\t\tmatrix:{0}'.format(self.matrix)
        if self.flag_color_transform:
            ret += '\n\t\tCXForm:{0}'.format(self.color_transform)
        return ret


class RemoveObject2(TagData):
    def __init__(self, content):
        super(RemoveObject2, self).__init__(content)
        self.tag_id = 28
        self.depth = struct.unpack('H', content)[0]

    def __str__(self):
        return 'RemoveObject2 depth:{0}'.format(self.depth)
