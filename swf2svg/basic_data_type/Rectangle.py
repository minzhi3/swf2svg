import swf2svg.bit_reader.BitReader


def read_rect(bit_reader: swf2svg.bit_reader.BitReader.BitReader):
    bits = bit_reader.read(5)
    xmin = bit_reader.read(bits)
    xmax = bit_reader.read(bits)
    ymin = bit_reader.read(bits)
    ymax = bit_reader.read(bits)
    return xmin, xmax, ymin, ymax
