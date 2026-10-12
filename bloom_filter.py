
import hashlib
import math

class BloomFilter:
    def __init__(self, n, p=0.01):
        self.size = math.ceil(
            -n * math.log(p) / (math.log(2) ** 2)
        )

        self.hash_count = max(
            1, round((self.size / n) * math.log(2))
        )

        self.bit_array = bytearray((self.size + 7) // 8)

    def _hashes(self, item):
        positions = []

        for i in range(self.hash_count):
            value = f"{item}-{i}".encode()
            digest = hashlib.sha256(value).digest()
            number = int.from_bytes(digest[:8], "big")
            positions.append(number % self.size)

        return positions

    def add(self, item):
        for position in self._hashes(item):
            byte_index = position // 8
            bit_offset = position % 8

            self.bit_array[byte_index] |= (1 << bit_offset)

    def contains(self, item):
        for position in self._hashes(item):
            byte_index = position // 8
            bit_offset = position % 8

            if not (self.bit_array[byte_index] & (1 << bit_offset)):
                return False

        return True
