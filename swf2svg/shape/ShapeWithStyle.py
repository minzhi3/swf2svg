import struct
import xml.etree.ElementTree as ET
import swf2svg.shape as shape
import swf2svg.bit_reader
import swf2svg.shape.ShapeRecord as ShapeRecord
import swf2svg.shape.FillStyle as Fill
import swf2svg.shape.LineStyle as Line


class ShapeWithStyle:
    def __init__(self, content, shape_generation):
        self.content = content
        self.shape_generation = shape_generation
        self.shape_records = []
        self.num_fill_bits = 0
        self.num_line_bits = 0

        point = 0
        self.fill_styles = shape.read_fill_style_array(self.content[point:], self.shape_generation)
        point += self.fill_styles.size
        self.line_styles = shape.read_line_style_array(self.content[point:], self.shape_generation)
        point += self.line_styles.size

        num_bits = struct.unpack_from('B', self.content, point)[0]
        self.num_fill_bits = num_bits >> 4
        self.num_line_bits = num_bits & 0xF
        point += 1

        reader = swf2svg.bit_reader.memory_reader(self.content, point)
        while True:
            type_flag = reader.read(1)
            if type_flag == 0:
                end_flag = reader.read(5)
                if end_flag == 0:
                    self.shape_records.append(ShapeRecord.EndRecord())
                    break
                else:
                    shape_record = ShapeRecord.StyleChangeRecord(self.content[point:], self.shape_generation, reader,
                                                                 end_flag,
                                                                 self.num_fill_bits, self.num_line_bits)
            else:
                straight = reader.read(1)
                if straight == 1:
                    shape_record = ShapeRecord.StraightEdgeRecord(reader)
                else:
                    shape_record = ShapeRecord.CurvedEdgeRecord(reader)
            self.shape_records.append(shape_record)
            point += shape_record.size

        point = reader.offset
        self.size = point

    def to_xml(self, twink):
        path_nodes = list()
        path_xml = PathXml(self.fill_styles, self.line_styles, twink)
        for record in self.shape_records:
            if record.type_flag == 1:
                if record.straight_flag == 1:
                    path_xml.add_straight(record)
                else:
                    path_xml.add_curve(record)
            else:
                if record.end == 0:
                    if not path_xml.is_empty:
                        path_nodes.append(path_xml.to_xml_node)
                    path_xml.reset_path()
                    path_xml.style_change(record)

        if not path_xml.is_empty:
            path_nodes.append(path_xml.to_xml_node)
        return path_nodes

    def __str__(self):
        ret = 'ShapeWithStyle size:{0}'.format(self.size)
        ret += ', StyleArray: {0}, {1}'.format(str(self.fill_styles), self.line_styles)
        for record in self.shape_records:
            ret += '\n\t\t' + str(record)
        return ret


class PathXml:
    def __init__(self, fill_styles: Fill.FillStyleArray, line_styles: Line.LineStyleArray, twink: int):
        self.path_data = ''
        self.twink = twink
        self.fill_array = fill_styles
        self.line_array = line_styles
        self.fill0 = None  # type: Fill.FillStyle
        self.fill1 = None  # type: Fill.FillStyle
        self.line = None  # type: Line.LineStyle

    def add_straight(self, record: ShapeRecord.StraightEdgeRecord):
        if record.general_line_flag == 1:
            self.path_data += 'l {0} {1}'.format(record.delta_x / self.twink, record.delta_y / self.twink)
        else:
            if record.vert_line_flag == 0:
                self.path_data += 'h {0}'.format(record.delta_x / self.twink)
            else:
                self.path_data += 'v {0}'.format(record.delta_y / self.twink)

    def add_curve(self, record: ShapeRecord.CurvedEdgeRecord):
        self.path_data += 'q {0} {1} {2} {3}'.format(record.control_delta_x / self.twink,
                                                     record.control_delta_y / self.twink,
                                                     (record.anchor_delta_x + record.control_delta_x) / self.twink,
                                                     (record.anchor_delta_y + record.control_delta_y) / self.twink)

    def style_change(self, record: ShapeRecord.StyleChangeRecord):
        if record.state_move_to:
            self.path_data += 'M {0} {1}'.format(record.move_delta_x / self.twink, record.move_delta_y / self.twink)
        if record.state_fill_style0 and record.fill_style0 > 0:
            self.fill0 = self.fill_array.data[record.fill_style0 - 1]
        else:
            self.fill0 = None
        if record.state_fill_style1 and record.fill_style1 > 0:
            self.fill1 = self.fill_array.data[record.fill_style1 - 1]
        else:
            self.fill1 = None
        if record.state_line_style and record.fill_style1 > 0:
            self.line = self.line_array.data[record.line_style - 1]
        else:
            self.line = None
        if record.state_new_styles == 1:
            self.fill_array = record.fill_styles
            self.line_array = record.line_styles

    def reset_path(self):
        self.path_data = ''

    @property
    def to_xml_node(self) -> ET.Element:
        path_attr = {'d': self.path_data + 'Z'}
        if self.fill0 is not None:
            fill = self.fill0
        elif self.fill1 is not None:
            fill = self.fill1
        else:
            fill = None
        if fill is not None:
            path_attr['fill'] = '#{0:02X}{1:02X}{2:02X}'.format(fill.color.red, fill.color.green, fill.color.blue)
        return ET.Element('path', path_attr)

    @property
    def is_empty(self):
        return len(self.path_data) == 0
