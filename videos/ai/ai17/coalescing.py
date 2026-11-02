"""Address arithmetic for the explicitly illustrative coalescing diagram.

For compute capability 6.0+, a warp's global accesses are serviced in 32-byte
sectors (CUDA C++ Best Practices, coalesced access). This is not a benchmark.
"""

import operator


def _integer(value):
    if isinstance(value, bool):
        raise ValueError("sizes and byte addresses must be integers, not booleans")
    try:
        return operator.index(value)
    except TypeError as exc:
        raise ValueError("sizes and byte addresses must be integers") from exc


def sectors_touched(addresses, word_bytes=4, sector_bytes=32):
    """Distinct sectors covering all requested words, including boundary crossings."""
    word_bytes, sector_bytes = _integer(word_bytes), _integer(sector_bytes)
    if word_bytes <= 0 or sector_bytes <= 0:
        raise ValueError("word and sector sizes must be positive")
    sectors = set()
    for address in addresses:
        address = _integer(address)
        if address < 0:
            raise ValueError("byte addresses must be nonnegative integers")
        first = address // sector_bytes
        last = (address + word_bytes - 1) // sector_bytes
        sectors.update(range(first, last + 1))
    return sorted(sectors)
