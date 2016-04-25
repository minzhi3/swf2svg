import struct
import swf2svg.sprite.PlaceObject as PlaceObject
from swf2svg.TagData import TagData, ShowFrame
import xml.etree.ElementTree as ET


class DefineSprite(TagData):
    def __init__(self, content):
        super().__init__(content)
        (self.id, self.frame_count) = struct.unpack_from("HH", content)
        self.control_tags = list()
        self.tag_id = 39
        self.display_list = dict()
        self.animate_list = dict()
        self.read_data()

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
            elif tag == 28:
                print('RemoveObject2')
            elif tag == 26:
                place_object2 = PlaceObject.PlaceObject2(sub_content)
                self.control_tags.append(place_object2)
            elif tag == 12:
                print('DoAction')
            elif tag == 1:
                self.control_tags.append(ShowFrame())
            elif tag == 0:
                break
            else:
                raise Exception('unknown tag {0:02X}'.format(tag))
            point += length

    def to_xml_list(self, twink):
        if len(self.display_list) == 0:
            self._convert(twink)
        ret = list()
        depth_keys = sorted(self.display_list.keys())
        for depth in depth_keys:
            group_attr = {'id': 'sprite{0:>02}_depth{1:>02}'.format(self.id, depth)}
            if len(self.animate_list.get(depth, list())) == 1:
                animation = self.animate_list.get(depth)[0]
                group_attr.update(animation['animation'])
            group_node = ET.Element('g', group_attr)
            for use_node in self.display_list[depth]:
                group_node.append(use_node)
            ret.append(group_node)
        return ret

    def to_json_list(self, twink):
        if len(self.animate_list) == 0:
            self._convert(twink)
        ret = list()
        for (depth, animation_list) in self.animate_list.items():
            animation = dict()
            animation['elementID'] = 'sprite{0:>02}_depth{1:>02}'.format(self.id, depth)
            animation['frameData'] = animation_list
            if len(animation_list) > 1:
                ret.append(animation)
        return ret

    def _convert(self, twink):
        display_list = dict()
        animate_list = dict()
        frame = 0
        for data in self.control_tags:
            if data.tag_id == 26:  # PlaceObject2
                place_object = data  # type: PlaceObject.PlaceObject2
                if place_object.flag_character:
                    if place_object.depth not in display_list.keys():
                        display_list[place_object.depth] = list()
                    use_node = place_object.to_xml(twink)
                    display_list[place_object.depth].append(use_node)
                if place_object.flag_matrix:
                    if place_object.depth not in animate_list.keys():
                        animate_list[place_object.depth] = list()
                    animation = dict()
                    animation['frame'] = frame
                    animation['animation'] = place_object.to_dict(twink)
                    animate_list[place_object.depth].append(animation)
            if data.tag_id == 1:  # ShowFrame
                frame += 1
        self.display_list = display_list
        self.animate_list = animate_list

    def __str__(self):
        ret = 'DefineSprite size:{0}, id:{1}, frame:{2}\n\t'.format(self.size, self.id, self.frame_count)
        ret += '\n\t'.join(str(n) for n in self.control_tags)
        return ret
