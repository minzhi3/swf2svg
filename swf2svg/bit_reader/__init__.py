import swf2svg.bit_reader.BitReader


def file_reader(file):
    return BitReader.BitReader(BitReader.FileBuffer(file))


def memory_reader(buffer, offset):
    return BitReader.BitReader(BitReader.MemoryBuffer(buffer, offset))
