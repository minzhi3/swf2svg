import sys
import struct
import xml.etree.ElementTree as ET
import swf2svg.basic_data_type as basic_type
import swf2svg.bit_reader as bit_reader
from swf2svg.shape.DefineShape import DefineShape, DefineShape2, DefineShape3
from swf2svg.sprite.DefineSprite import DefineSprite
from swf2svg.sprite.PlaceObject import PlaceObject2

from swf2svg.util import tag_name


class SwfToSvg:
    def __init__(self, file):
        self.file = file
        self.version = 0
        self.size = 0
        self.display_rect = (0, 0, 0, 0)
        self.frame_rate = 0.0
        self.frame_count = 0
        self.twink = 20
        self.characters = dict()
        self.place_objects = list()

    def _read_head(self):
        head_str = self.file.read(3)
        if head_str != b'FWS':
            raise Exception("head string")
        self.version = struct.unpack('B', self.file.read(1))[0]
        self.size = struct.unpack('I', self.file.read(4))[0]
        reader = bit_reader.file_reader(self.file)
        self.display_rect = basic_type.read_rect(reader)
        self.frame_rate = struct.unpack('H', self.file.read(2))[0] / 256
        self.frame_count = struct.unpack('H', self.file.read(2))[0]

    def _read_tag(self):
        tag_byte = struct.unpack('H', self.file.read(2))[0]
        tag = tag_byte >> 6
        length = tag_byte & 63
        if length == 63:
            length = struct.unpack('I', self.file.read(4))[0]

        content = self.file.read(length)
        if tag in [0, 1, 9, 69, 77]:
            print(tag_name.get(tag))
        elif tag == 2:  # DefineShape
            define_shape = DefineShape(content)
            define_shape.read_data()
            self.characters[define_shape.id] = define_shape
            # print(define_shape)
        elif tag == 22:  # DefineShape2
            define_shape = DefineShape2(content)
            define_shape.read_data()
            self.characters[define_shape.id] = define_shape
            # print(define_shape)
        elif tag == 32:  # DefineShape3
            define_shape = DefineShape3(content)
            define_shape.read_data()
            self.characters[define_shape.id] = define_shape
            # print(define_shape)
        elif tag == 26:  # PlaceObject2
            place_object2 = PlaceObject2(content, parent_id=0)
            self.place_objects.append(place_object2)
            print(place_object2)
        elif tag == 39:  # DefineSprite
            define_sprite = DefineSprite(content)
            self.characters[define_sprite.id] = define_sprite
            print(define_sprite)
        else:
            raise Exception('Unknown tag {0}'.format(tag))

    def print_head(self):
        print(self.version, self.size)
        print(self.display_rect)
        print("offset", self.file.tell())
        print("frame_count", self.frame_count)
        print("frame_rate", self.frame_rate)

    def _is_end(self):
        current = self.file.tell()
        if current >= self.size:
            return True
        else:
            return False

    def _to_xml(self) -> ET.Element:

        root_attr = {'xmlns': 'http://www.w3.org/2000/svg',
                     'version': '1.1',
                     'xmlns:xlink': 'http://www.w3.org/1999/xlink'
                     }
        svg_root = ET.Element('svg', root_attr)
        svg_node_defs = ET.Element('defs')
        for (id, data) in self.characters.items():
            svg_node_symbol = ET.Element('symbol', {'id': 'symbol{:>02}'.format(data.id), 'overflow': 'visible'})
            if data.tag_id in [2, 22, 32]:  # DefineShape <defs>
                shape_xml_nodes = data.shape_with_style.to_xml(self.twink)
                for shape_xml in shape_xml_nodes:
                    svg_node_symbol.append(shape_xml)
            elif data.tag_id == 39:  # DefineSprite <defs> <use>
                sprite_xml_nodes = data.to_xml(self.twink)
                for sprite_xml in sprite_xml_nodes:
                    svg_node_symbol.append(sprite_xml)
            svg_node_defs.append(svg_node_symbol)

        svg_root.append(svg_node_defs)
        for place_object in self.place_objects:
            use_xml_node = place_object.to_xml(self.twink)
            if use_xml_node is not None:
                svg_root.append(use_xml_node)
        return svg_root

    def to_svg(self) -> ET.Element:
        self._read_head()
        while not self._is_end():
            self._read_tag()
        return self._to_xml()


def to_svg(swf_file) -> ET.Element:
    file = open(swf_file, "rb")
    swf = SwfToSvg(file)
    svg_xml = swf.to_svg()
    return svg_xml


def main():
    if len(sys.argv) != 3:
        print("Usage: python swf2svg.py <input file> <output file>")
        exit(2)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    svg_xml = to_svg(input_file)
    ET.ElementTree(svg_xml).write(output_file, encoding="UTF-8", xml_declaration=False, method="xml")


if __name__ == "__main__":
    main()
