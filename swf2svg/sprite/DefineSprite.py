import struct
import swf2svg.sprite.PlaceObject as PlaceObject
from swf2svg.TagData import TagData, ShowFrame


class DefineSprite(TagData):
    def __init__(self, content):
        super().__init__(content)
        (self.id, self.frame_count) = struct.unpack_from("HH", content)
        self.control_tags = list()
        self.read_data()
        self.tag_id = 39

    def read_data(self):
        self.read_tag()

    def read_tag(self):
        point = 4
        while True:
            tag_byte = struct.unpack_from('H', self.content, point)[0]
            point += 2
            tag = tag_byte >> 6
            length = tag_byte & 63
            if length == 63:
                length = struct.unpack_from('I', self.content, point)[0]
                point += 4

            sub_content = self.content[point:point + length]
            if tag in [9, 69, 77]:
                print(swf2svg.tag_name.get(tag))
            elif tag == 26:
                place_object2 = PlaceObject.PlaceObject2(sub_content, self.id)
                self.control_tags.append(place_object2)
            elif tag == 1:
                self.control_tags.append(ShowFrame())
            elif tag == 0:
                break
            else:
                raise Exception('unknown tag {0:02X}'.format(tag))
            point += length

    def to_xml(self, twink):
        use_nodes = list()
        for data in self.control_tags:
            if data.tag_id == 26:
                place_object = data  # type: PlaceObject.PlaceObject2
                use_node = place_object.to_xml(twink)
                if use_node is not None:
                    use_nodes.append(use_node)
        return use_nodes

    def __str__(self):
        ret = 'DefineSprite size:{0}, id:{1}, frame:{2}\n\t'.format(self.size, self.id, self.frame_count)
        ret += '\n\t'.join(str(n) for n in self.control_tags)
        return ret
