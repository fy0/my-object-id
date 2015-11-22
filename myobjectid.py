# coding:utf-8

import os
import sys
import time
import socket
import struct
import hashlib
import binascii

py_ver = sys.version_info.major


class ObjectID(object):
    _index = 0
    _hostname_bytes = hashlib.md5(socket.gethostname().encode('utf-8')).digest()[0:3]

    def __init__(self, object_id=None):
        if object_id:
            self._parse_id(object_id)
        else:
            self._gen_id()

    def _gen_id(self):
        # 0|1|2|3 | 4|5|6 | 7|8 | 9|10|11
        # 时间戳 | 机器  | PID | 计数器
        ObjectID._index += 1
        self.time = int(time.time())
        object_id = struct.pack(">i", self.time)
        object_id += self._hostname_bytes
        # 在 celery 中，多个worker首次获取到的 os.getpid() 是同一个值！
        # 这会导致唯一性出现致命问题，所以保险起见生成一次取一次
        object_id += struct.pack(">H", os.getpid() % 0xFFFF)
        object_id += struct.pack(">I", ObjectID._index % 0xFFF)[1:]
        self.object_id = binascii.hexlify(object_id)

    def _parse_id(self, object_id):
        if not len(object_id) == 24:
            raise TypeError

        if py_ver == 3:
            if type(object_id) == str:
                object_id = bytes(object_id, 'utf-8')

            if type(object_id) == bytes:
                b = binascii.unhexlify(object_id)
                self.time = struct.unpack(">i", b[0:4])[0]
                self.object_id = object_id
            else:
                raise TypeError
        else:
            if type(object_id) == str:
                b = binascii.unhexlify(object_id)
                self.time = struct.unpack(">i", b[0:4])[0]
                self.object_id = object_id
            else:
                raise TypeError

    def to_bin(self):
        return binascii.unhexlify(self.object_id)

    def __str__(self):
        if py_ver == 3:
            return str(self.object_id, 'utf-8')
        else:
            return self.object_id

    def __repr__(self):
        return "ObjectID('%s')" % str(self)
        
    def __len__(self):
        return len(str(self))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.object_id == other.object_id
        raise TypeError

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return self.object_id != other.object_id
        raise TypeError

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.object_id < other.object_id
        raise TypeError

    def __le__(self, other):
        if isinstance(other, self.__class__):
            return self.object_id <= other.object_id
        raise TypeError

    def __gt__(self, other):
        if isinstance(other, self.__class__):
            return self.object_id > other.object_id
        raise TypeError

    def __ge__(self, other):
        if isinstance(other, self.__class__):
            return self.object_id >= other.object_id
        raise TypeError
