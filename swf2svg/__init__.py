import swf2svg.SwfToSvg


def to_svg(input_file, svg_path):
    return swf2svg.SwfToSvg.to_svg(input_file, svg_path)


def write_file(input_file_path, svg_file_path, json_file_path, petty_xml=False):
    swf2svg.SwfToSvg.write_file(input_file_path, svg_file_path, json_file_path, petty_xml)
