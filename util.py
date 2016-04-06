from BitReader import BitReader

tag_name = {
    0: 'End',
    1: 'ShowFrame',
    2: 'DefineShape',
    9: 'SetBackgroundColor',
    22: 'DefineShape2',
    26: 'PlaceObject2',
    32: 'DefineShape3',
    39: 'DefineSprite',
    69: 'FileAttributes',
    77: 'Metadata'
}


def read_rect(buffer):
    bit_reader = BitReader(buffer)
    bits = bit_reader.read(5)
    xmin = bit_reader.read(bits)
    xmax = bit_reader.read(bits)
    ymin = bit_reader.read(bits)
    ymax = bit_reader.read(bits)
    return xmin, xmax, ymin, ymax
