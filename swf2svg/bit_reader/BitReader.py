class Buffer:
    def __init__(self):
        self.buffer = None
        self.file = None
        self._offset = None

    def skip_bytes(self, size):
        raise NotImplementedError

    def next_byte(self):
        raise NotImplementedError

    def offset(self):
        raise NotImplementedError


class MemoryBuffer(Buffer):
    def __init__(self, buffer, _offset):
        super().__init__()
        self.buffer = buffer
        self._offset = _offset

    def skip_bytes(self, size):
        self.buffer = self.buffer[(self._offset+size):]
        self._offset = 0

    def next_byte(self):
        if self.offset < len(self.buffer):
            ret = self.buffer[self.offset]
            self._offset += 1
        else:
            ret = None
        return ret

    @property
    def offset(self):
        return self._offset


class FileBuffer(Buffer):
    def __init__(self, file):
        super().__init__()
        self.file = file

    def skip_bytes(self, size):
        raise Exception('cannot move file point')

    def next_byte(self):
        ret = self.file.read(1)
        if ret is not None:
            return ret[0]
        else:
            return None

    @property
    def offset(self):
        return self.file.tell()


class BitReader:
    def __init__(self, source: Buffer):
        self.source = source
        self.pool = 0
        self.pool_length = 0

    def read(self, count):
        if count == 0:
            return 0
        while self.pool_length < count:
            self.pool <<= 8
            self.pool += self.source.next_byte()
            self.pool_length += 8

        bit_diff = self.pool_length - count
        ret = self.pool >> bit_diff
        self.pool &= ((1 << bit_diff) - 1)
        self.pool_length = bit_diff

        return ret

    def read_signed(self, count):
        if count == 0:
            return 0
        ret = self.read(count)
        if ret > (1 << (count - 1)):
            ret -= (1 << count)
        return ret

    def skip_bytes(self, size):
        self.source.skip_bytes(size)
        self.pool = 0
        self.pool_length = 0

    @property
    def offset(self):
        return self.source.offset

    @property
    def remain_buffer(self):
        if self.source.offset is not None and self.source.buffer is not None:
            return self.source.buffer[self.source.offset:]
        else:
            return None
