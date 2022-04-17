"""read"""


import bisect
import os
import mmap
from struct import unpack, Struct


class OrderedFile:
    """OrderedFile provides an ordered file for fast search"""

    def __init__(self, file, key_format, value_format):
        key_size = Struct(key_format).size
        value_size = Struct(value_format).size
        self.key_format = key_format
        self.value_format = value_format
        size = os.path.getsize(file)
        self.entry_size = key_size + value_size
        self.key_size = key_size
        self.value_size = value_size
        self.length = int(size / self.entry_size)
        self.f = open(file, "rb")  # pylint: disable=consider-using-with
        self.mm = mmap.mmap(self.f.fileno(), 0, prot=mmap.PROT_READ)

    def get_key(self, i):
        return unpack(self.key_format, self.mm[self.entry_size * i : self.entry_size * i + self.key_size])[0]

    def get_value(self, i):
        return unpack(
            self.value_format, self.mm[self.entry_size * i + self.key_size : self.entry_size * i + self.entry_size]
        )

    def __getitem__(self, i):
        z = self.get_key(i)
        return z


class OnDiskKV:
    """on disk kv provides a fast and simple kv store"""

    def __init__(self, file, key_format="q", value_format="ee"):
        self.ordered_file = OrderedFile(file, key_format, value_format)
        self.length = self.ordered_file.length

    def get_key(self, i):
        return self.ordered_file.get_key(i)

    def get_value(self, i):
        return self.ordered_file.get_value(i)

    def __getitem__(self, k):
        i = bisect.bisect_left(self.ordered_file, k, lo=0, hi=self.length)
        k2 = self.ordered_file.get_key(i)
        if k != k2:
            raise ValueError(str(k) + "not Found")
        return self.ordered_file.get_value(i)
