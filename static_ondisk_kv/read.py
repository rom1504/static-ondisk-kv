"""read"""


import bisect
import os
import mmap
from struct import unpack, Struct


class OnDiskKVByIndex:
    def __init__(self, ondiskkv):
        self.ondiskkv = ondiskkv

    def __getitem__(self, i):
        return self.ondiskkv.get_key(i)


class OnDiskKV:
    """on disk kv provides a fast and simple kv store"""

    def __init__(self, file, key_format="q", value_format="ee"):
        self.key_format = key_format
        self.value_format = value_format
        self.key_size = Struct(key_format).size
        self.value_size = Struct(value_format).size
        self.entry_size = self.key_size + self.value_size
        size = os.path.getsize(file)
        self.length = int(size / self.entry_size)
        self.f = open(file, "rb")  # pylint: disable=consider-using-with
        self.mm = mmap.mmap(self.f.fileno(), 0, prot=mmap.PROT_READ)
        self.filename = file
        self.ondiskkv_by_index = OnDiskKVByIndex(self)

    def __getstate__(self):
        return {
            "filename": self.filename,
            "key_format": self.key_format,
            "value_format": self.value_format,
        }

    def __setstate__(self, state):
        self.__init__(state["filename"], state["key_format"], state["value_format"])

    def get_key(self, i):
        return unpack(self.key_format, self.mm[self.entry_size * i : self.entry_size * i + self.key_size])[0]

    def get_value(self, i):
        return unpack(
            self.value_format, self.mm[self.entry_size * i + self.key_size : self.entry_size * i + self.entry_size]
        )

    def __getitem__(self, k):
        i = bisect.bisect_left(self.ondiskkv_by_index, k, lo=0, hi=self.length)
        k2 = self.get_key(i)
        if k != k2:
            raise ValueError(str(k) + "not Found")
        return self.get_value(i)
