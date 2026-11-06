"""PebbleFS (Part 34): a small Unix file system on a block device, with a journal, and crash injection.

    d = Disk(4096)
    fs = FS.mkfs(d, ninodes=256, mode="ordered")
    fs.mkdir("/novels"); fs.create("/novels/emma"); fs.append("/novels/emma", text)
    fs.read("/novels/emma") == text
    fsck(d) == []                          # every invariant holds

The layout, in 1 KiB blocks (the same bytes PebbleOS's kernel reads, :mod:`explainer.cs.os.fsos`):

    block 0          the superblock: where everything else is
    block 1          the inode bitmap (one bit per inode)
    blocks 2 ..      the data bitmap (one bit per data block)
    then             the inode table: 64-byte inodes, 16 to a block
    then             the journal
    then             the data blocks

An inode holds a type (1 file, 2 directory), a link count, a size, ten direct block pointers, one single-indirect
and one double-indirect pointer (a block of 256 pointers, and a block of 256 such blocks).  A directory is a file of
32-byte entries: an inode number (0 = unused) and a name of up to 28 bytes.  Inode 1 is the root.

**Transactions.**  Each operation (create, write, unlink, rename, ...) gathers the blocks it changes and commits them
together, by the file system's ``mode``:

* ``none``: write them all and flush.  The disk may reorder writes between flushes, so a crash can leave any subset.
* ``careful``: write them in dependency order with a flush between groups (data, then bitmaps, then inodes, then
  directories; the reverse when freeing), as FFS did with synchronous writes.  A crash leaves only leaks.
* ``writeback``: metadata goes to the journal first; data is written in place with no ordering.
* ``ordered``: data in place first, flushed; then the metadata through the journal (ext3/ext4's default).
* ``data``: data and metadata both through the journal (everything written twice).

A journal transaction is a descriptor block (which home blocks follow), the copies, and a commit block.  With
``barriers`` the commit is written only after the copies are flushed; without, they share one flush, and a disk that
reorders can make the commit durable before the copies: ``jcsum`` (a checksum of the copies in the commit block, as
ext4's journal_checksum) lets recovery tell.  Mounting replays a committed transaction and discards an uncommitted one.

**Crash injection.**  With ``disk.trace`` a list, every write and flush is recorded; :func:`crash_states` yields every
disk state a crash could leave (all writes before the last flush, plus any subset of those after it), and
:func:`fsck` checks every invariant of the file system.
"""
from __future__ import annotations

import itertools
import random
import struct
import zlib
from contextlib import contextmanager

BS = 1024
NDIRECT = 10
PER = BS // 4
ISIZE = 64
IPB = BS // ISIZE
DSIZE = 32
NAMELEN = 28
MAGIC = 0x50424653                  # "PBFS"
JDESC, JCOMMIT = 0x4A444553, 0x4A434D54
ROOT = 1
FREE_T, FILE, DIR = 0, 1, 2
MAXFILE = (NDIRECT + PER + PER * PER) * BS
MODES = ("none", "careful", "writeback", "ordered", "data")
SB_FIELDS = ("magic", "nblocks", "ninodes", "ibmap", "dbmap", "ndbmap", "itable", "nitable", "journal", "jlen",
             "data", "ndata")
# byte offsets inside an inode, for the kernel
I_TYPE, I_NLINK, I_SIZE, I_DIRECT, I_IND, I_DIND = 0, 4, 8, 12, 52, 56


class FSError(Exception):
    pass


class Disk:
    """A block device: ``nblocks`` blocks of 1 KiB.  ``trace`` (when a list) records ("w", n, bytes) and ("f",)."""

    def __init__(self, nblocks: int):
        self.b = [bytes(BS)] * nblocks
        self.trace: list | None = None
        self.reads = 0
        self.writes = 0
        self.log: list[tuple[str, int]] | None = None     # ("r" | "w", block): the access pattern, when a list

    def __len__(self):
        return len(self.b)

    def read(self, n: int) -> bytes:
        self.reads += 1
        if self.log is not None:
            self.log.append(("r", n))
        return self.b[n]

    def write(self, n: int, data) -> None:
        assert len(data) == BS and 0 <= n < len(self.b), (n, len(data))
        data = bytes(data)
        self.b[n] = data
        self.writes += 1
        if self.log is not None:
            self.log.append(("w", n))
        if self.trace is not None:
            self.trace.append(("w", n, data))

    def flush(self) -> None:
        if self.trace is not None:
            self.trace.append(("f",))

    def copy(self) -> Disk:
        d = Disk.__new__(Disk)
        d.b = list(self.b)
        d.trace, d.reads, d.writes, d.log = None, 0, 0, None
        return d


# ---- encoding ---------------------------------------------------------------------------------------------------
def _words(b: bytes, n: int, off: int = 0) -> list[int]:
    return list(struct.unpack_from(f"<{n}I", b, off))


def superblock(d: Disk) -> dict:
    w = _words(d.b[0], len(SB_FIELDS))
    return dict(zip(SB_FIELDS, w))


def _inode(raw: bytes, off: int) -> dict:
    w = _words(raw, 16, off)
    return {"type": w[0], "nlink": w[1], "size": w[2], "direct": w[3:13], "ind": w[13], "dind": w[14]}


def _pack_inode(ino: dict) -> bytes:
    return struct.pack("<16I", ino["type"], ino["nlink"], ino["size"], *ino["direct"], ino["ind"], ino["dind"], 0)


def _empty_inode(kind: int) -> dict:
    return {"type": kind, "nlink": 0, "size": 0, "direct": [0] * NDIRECT, "ind": 0, "dind": 0}


def _dirents(raw: bytes):
    for k in range(BS // DSIZE):
        inum = struct.unpack_from("<I", raw, k * DSIZE)[0]
        name = raw[k * DSIZE + 4:k * DSIZE + DSIZE].rstrip(b"\0")
        yield k, inum, name


def _bit(raw, i):
    return raw[i >> 3] >> (i & 7) & 1


# ---- the file system ----------------------------------------------------------------------------------------------
class FS:
    def __init__(self, disk: Disk, mode: str = "ordered", barriers: bool = True, jcsum: bool = False,
                 alloc: str = "next", delayed: bool = False, seed: int = 0, recover: bool = True):
        assert mode in MODES, mode
        self.d = disk
        self.sb = superblock(disk)
        if self.sb["magic"] != MAGIC:
            raise FSError("no PebbleFS here")
        self.mode, self.barriers, self.jcsum, self.alloc, self.delayed = mode, barriers, jcsum, alloc, delayed
        self.rng = random.Random(seed)
        self.tx: dict[int, bytearray] | None = None
        self.kind: dict[int, str] = {}
        self.freeing = False
        self.pending: dict[int, list[tuple[int, bytes]]] = {}
        self.seq = 1
        self.cursor = 0
        self.recovery = self.recover() if recover else "skipped"

    # -- making one ---------------------------------------------------------------------------------------------
    @classmethod
    def mkfs(cls, disk: Disk, ninodes: int = 256, jlen: int = 64, stale: bytes = b"", **kw) -> FS:
        """Lay out an empty file system with a root directory.  ``stale``: what the free data blocks hold (a deleted
        file's bytes, say), so that a crash which exposes an unwritten block shows it."""
        n = len(disk)
        nitable = -(-ninodes // IPB)
        ndbmap = 1
        while True:
            data = 2 + ndbmap + nitable + jlen
            ndata = n - data
            if ndata <= ndbmap * BS * 8:
                break
            ndbmap += 1
        sb = dict(magic=MAGIC, nblocks=n, ninodes=ninodes, ibmap=1, dbmap=2, ndbmap=ndbmap, itable=2 + ndbmap,
                  nitable=nitable, journal=2 + ndbmap + nitable, jlen=jlen, data=data, ndata=ndata)
        trace, disk.trace = disk.trace, None
        disk.write(0, struct.pack(f"<{len(SB_FIELDS)}I", *[sb[k] for k in SB_FIELDS]).ljust(BS, b"\0"))
        for b in range(1, data):
            disk.write(b, bytes(BS))
        if stale:
            blk = (stale * (BS // len(stale) + 1))[:BS]
            for b in range(data, n):
                disk.b[b] = blk
        fs = cls(disk, mode="none", recover=False)
        with fs.op():
            ib = fs._get(sb["ibmap"])
            ib[0] |= 1 | 2                       # inode 0 is never used; 1 is the root
            root = _empty_inode(DIR)
            root["nlink"] = 2
            fs._iput(ROOT, root)
            fs._dir_add(ROOT, b".", ROOT)
            fs._dir_add(ROOT, b"..", ROOT)
        disk.flush()
        disk.trace = trace
        return cls(disk, **kw)

    # -- blocks, inside and outside a transaction ----------------------------------------------------------------
    def _rd(self, n: int) -> bytes:
        if self.tx is not None and n in self.tx:
            return bytes(self.tx[n])
        return self.d.read(n)

    def _get(self, n: int, kind: str = "meta", fresh: bool = False) -> bytearray:
        if n not in self.tx:
            self.tx[n] = bytearray(BS) if fresh else bytearray(self.d.read(n))
        if kind == "data":
            self.kind.setdefault(n, "data")
        elif self.kind.get(n) != "dir":
            self.kind[n] = kind
        return self.tx[n]

    @contextmanager
    def op(self, freeing: bool = False):
        assert self.tx is None, "operations do not nest"
        self.tx, self.kind, self.freeing = {}, {}, freeing
        try:
            yield
        except BaseException:
            self.tx = None
            raise
        tx, kind = self.tx, self.kind
        self.tx = None
        if tx:
            self._commit(tx, kind, freeing)

    # -- inodes --------------------------------------------------------------------------------------------------
    def _iloc(self, inum: int) -> tuple[int, int]:
        if not 0 < inum < self.sb["ninodes"]:
            raise FSError(f"bad inode {inum}")
        return self.sb["itable"] + inum // IPB, (inum % IPB) * ISIZE

    def iget(self, inum: int) -> dict:
        b, off = self._iloc(inum)
        return _inode(self._rd(b), off)

    def _iput(self, inum: int, ino: dict) -> None:
        b, off = self._iloc(inum)
        self._get(b)[off:off + ISIZE] = _pack_inode(ino)

    def _ialloc(self, kind: int) -> int:
        ib = self._get(self.sb["ibmap"])
        for i in range(2, self.sb["ninodes"]):
            if not _bit(ib, i):
                ib[i >> 3] |= 1 << (i & 7)
                self._iput(i, _empty_inode(kind))
                return i
        raise FSError("out of inodes")

    def _ifree(self, inum: int) -> None:
        ib = self._get(self.sb["ibmap"])
        ib[inum >> 3] &= ~(1 << (inum & 7))
        self._iput(inum, _empty_inode(FREE_T))

    # -- data blocks ---------------------------------------------------------------------------------------------
    def _bmap_block(self, i: int) -> tuple[int, int]:
        return self.sb["dbmap"] + i // (BS * 8), i % (BS * 8)

    def _balloc(self, goal: int | None = None) -> int:
        nd = self.sb["ndata"]
        if self.alloc == "random":
            order = self.rng.sample(range(nd), nd)
        else:
            g = self.cursor if goal is None else goal
            order = itertools.chain(range(g, nd), range(0, g))
        for i in order:
            bb, bit = self._bmap_block(i)
            raw = self._rd(bb)
            if not _bit(raw, bit):
                w = self._get(bb)
                w[bit >> 3] |= 1 << (bit & 7)
                self.cursor = i + 1 if i + 1 < nd else 0
                return self.sb["data"] + i
        raise FSError("disk full")

    def _bfree(self, blk: int) -> None:
        bb, bit = self._bmap_block(blk - self.sb["data"])
        w = self._get(bb)
        w[bit >> 3] &= ~(1 << (bit & 7))

    def _last_block(self, ino: dict) -> int | None:
        nb = -(-ino["size"] // BS)
        return self.bmap(ino, nb - 1) if nb else None

    def bmap(self, ino: dict, i: int, alloc: bool = False, goal: int | None = None) -> int:
        """The disk block holding block i of a file: 0 if there is none (and not ``alloc``)."""
        def slot(holder_blk, k):
            return struct.unpack_from("<I", self._rd(holder_blk), 4 * k)[0]

        def set_slot(holder_blk, k, v):
            struct.pack_into("<I", self._get(holder_blk), 4 * k, v)

        def new_block(zero, g):
            b = self._balloc(g)
            if zero:
                self._get(b, fresh=True)
            return b
        if i < NDIRECT:
            if not ino["direct"][i] and alloc:
                ino["direct"][i] = new_block(False, goal)
            return ino["direct"][i]
        i -= NDIRECT
        if i < PER:
            if not ino["ind"]:
                if not alloc:
                    return 0
                ino["ind"] = new_block(True, goal)
                goal = ino["ind"] + 1 - self.sb["data"]
            b = slot(ino["ind"], i)
            if not b and alloc:
                b = new_block(False, goal)
                set_slot(ino["ind"], i, b)
            return b
        i -= PER
        if i >= PER * PER:
            raise FSError("file too large")
        if not ino["dind"]:
            if not alloc:
                return 0
            ino["dind"] = new_block(True, goal)
            goal = ino["dind"] + 1 - self.sb["data"]
        mid = slot(ino["dind"], i // PER)
        if not mid:
            if not alloc:
                return 0
            mid = new_block(True, goal)
            set_slot(ino["dind"], i // PER, mid)
            goal = mid + 1 - self.sb["data"]
        b = slot(mid, i % PER)
        if not b and alloc:
            b = new_block(False, goal)
            set_slot(mid, i % PER, b)
        return b

    def blocks_of(self, ino: dict) -> tuple[list[int], list[int]]:
        """(data blocks in file order, indirect blocks): what a full read of the file touches."""
        data, ind = [], []
        nb = -(-ino["size"] // BS)
        for i in range(nb):
            data.append(self.bmap(ino, i))
        if ino["ind"]:
            ind.append(ino["ind"])
        if ino["dind"]:
            ind.append(ino["dind"])
            for k in range(PER):
                m = struct.unpack_from("<I", self._rd(ino["dind"]), 4 * k)[0]
                if m:
                    ind.append(m)
        return data, ind

    # -- directories ---------------------------------------------------------------------------------------------
    def _dir_blocks(self, inum: int):
        ino = self.iget(inum)
        for i in range(-(-ino["size"] // BS)):
            yield self.bmap(ino, i)

    def _dir_find(self, dinum: int, name: bytes) -> tuple[int, int, int] | None:
        for b in self._dir_blocks(dinum):
            for k, inum, nm in _dirents(self._rd(b)):
                if inum and nm == name:
                    return b, k, inum
        return None

    def _dir_add(self, dinum: int, name: bytes, inum: int) -> None:
        if not 0 < len(name) <= NAMELEN or b"/" in name:
            raise FSError(f"bad name {name!r}")
        for b in self._dir_blocks(dinum):
            for k, i, _ in _dirents(self._rd(b)):
                if not i:
                    self._get(b, "dir")[k * DSIZE:(k + 1) * DSIZE] = struct.pack("<I", inum) + name.ljust(NAMELEN, b"\0")
                    return
        d = self.iget(dinum)
        nb = d["size"] // BS
        b = self.bmap(d, nb, alloc=True)
        blk = self._get(b, "dir", fresh=True)
        blk[:DSIZE] = struct.pack("<I", inum) + name.ljust(NAMELEN, b"\0")
        d["size"] += BS
        self._iput(dinum, d)

    def _dir_remove(self, dinum: int, name: bytes) -> int:
        f = self._dir_find(dinum, name)
        if f is None:
            raise FSError(f"no such file {name!r}")
        b, k, inum = f
        self._get(b, "dir")[k * DSIZE:(k + 1) * DSIZE] = bytes(DSIZE)
        return inum

    def lookup(self, path: str) -> int:
        cur = ROOT
        for comp in [c for c in path.split("/") if c]:
            if self.iget(cur)["type"] != DIR:
                raise FSError(f"not a directory on the way to {path}")
            f = self._dir_find(cur, comp.encode())
            if f is None:
                raise FSError(f"no such file {path}")
            cur = f[2]
        return cur

    def exists(self, path: str) -> bool:
        try:
            self.lookup(path)
            return True
        except FSError:
            return False

    def _split(self, path: str) -> tuple[int, bytes]:
        parts = [c for c in path.split("/") if c]
        parent = self.lookup("/" + "/".join(parts[:-1]))
        return parent, parts[-1].encode()

    def listdir(self, path: str = "/") -> list[str]:
        out = []
        for b in self._dir_blocks(self.lookup(path)):
            out += [nm.decode() for _, i, nm in _dirents(self._rd(b)) if i and nm not in (b".", b"..")]
        return out

    # -- operations ----------------------------------------------------------------------------------------------
    def create(self, path: str, kind: int = FILE) -> int:
        with self.op():
            parent, name = self._split(path)
            if self._dir_find(parent, name):
                raise FSError(f"{path} exists")
            inum = self._ialloc(kind)
            ino = self.iget(inum)
            ino["nlink"] = 1
            self._iput(inum, ino)
            if kind == DIR:
                ino["nlink"] = 2
                self._iput(inum, ino)
                self._dir_add(inum, b".", inum)
                self._dir_add(inum, b"..", parent)
                p = self.iget(parent)
                p["nlink"] += 1
                self._iput(parent, p)
            self._dir_add(parent, name, inum)
        return inum

    def mkdir(self, path: str) -> int:
        return self.create(path, DIR)

    def _write(self, inum: int, off: int, data: bytes) -> None:
        ino = self.iget(inum)
        if off > ino["size"]:
            raise FSError("no holes")
        pos = 0
        while pos < len(data):
            i, bo = divmod(off + pos, BS)
            n = min(BS - bo, len(data) - pos)
            have = i < -(-ino["size"] // BS)
            goal = None
            if not have and self.alloc == "next":
                last = self._last_block(ino) if ino["size"] else None
                goal = last + 1 - self.sb["data"] if last else None
            b = self.bmap(ino, i, alloc=True, goal=goal)
            blk = self._get(b, "data", fresh=not have and bo == 0 and n == BS)
            if not have and not (bo == 0 and n == BS):
                blk[:] = bytes(BS)
            blk[bo:bo + n] = data[pos:pos + n]
            pos += n
            ino["size"] = max(ino["size"], off + pos)
        self._iput(inum, ino)

    def write(self, path: str | int, off: int, data: bytes) -> None:
        inum = path if isinstance(path, int) else self.lookup(path)
        if self.delayed:
            self.pending.setdefault(inum, []).append((off, bytes(data)))
            return
        with self.op():
            self._write(inum, off, data)

    def append(self, path: str | int, data: bytes) -> None:
        inum = path if isinstance(path, int) else self.lookup(path)
        size = self.iget(inum)["size"] + sum(len(d) for _, d in self.pending.get(inum, ()))
        self.write(inum, size, data)

    def fsync(self, path: str | int) -> None:
        inum = path if isinstance(path, int) else self.lookup(path)
        todo = self.pending.pop(inum, [])
        if todo:
            with self.op():
                for off, data in todo:
                    self._write(inum, off, data)
        self.d.flush()

    def sync(self) -> None:
        for inum in list(self.pending):
            self.fsync(inum)

    def read(self, path: str | int) -> bytes:
        inum = path if isinstance(path, int) else self.lookup(path)
        ino = self.iget(inum)
        out = bytearray()
        for i in range(-(-ino["size"] // BS)):
            b = self.bmap(ino, i)
            out += self._rd(b) if b else bytes(BS)
        return bytes(out[:ino["size"]])

    def _release(self, inum: int) -> None:
        ino = self.iget(inum)
        data, ind = self.blocks_of(ino)
        for b in data + ind:
            if b:
                self._bfree(b)
        self._ifree(inum)

    def unlink(self, path: str) -> None:
        with self.op(freeing=True):
            parent, name = self._split(path)
            inum = self._dir_remove(parent, name)
            ino = self.iget(inum)
            if ino["type"] == DIR:
                raise FSError("unlink of a directory")
            ino["nlink"] -= 1
            if ino["nlink"]:
                self._iput(inum, ino)
            else:
                self._release(inum)
        self.pending.pop(inum, None)

    def link(self, old: str, new: str) -> None:
        with self.op():
            inum = self.lookup(old)
            parent, name = self._split(new)
            ino = self.iget(inum)
            ino["nlink"] += 1
            self._iput(inum, ino)
            self._dir_add(parent, name, inum)

    def rename(self, old: str, new: str) -> None:
        """Atomic: ``new`` names the old file, and any file it named before is gone, in one transaction."""
        with self.op(freeing=True):
            op_, on = self._split(old)
            np_, nn = self._split(new)
            inum = self._dir_remove(op_, on)
            f = self._dir_find(np_, nn)
            if f:
                b, k, victim = f
                self._get(b, "dir")[k * DSIZE:(k + 1) * DSIZE] = struct.pack("<I", inum) + nn.ljust(NAMELEN, b"\0")
                v = self.iget(victim)
                v["nlink"] -= 1
                if v["nlink"]:
                    self._iput(victim, v)
                else:
                    self._release(victim)
            else:
                self._dir_add(np_, nn, inum)

    # -- commit ----------------------------------------------------------------------------------------------------
    def _jblocks(self, tx, homes) -> list[tuple[int, bytes]]:
        j = self.sb["journal"]
        if len(homes) > min(self.sb["jlen"] - 2, PER - 4):
            raise FSError(f"transaction of {len(homes)} blocks is larger than the journal")
        desc = struct.pack(f"<4I{len(homes)}I", JDESC, self.seq, len(homes), 0, *homes).ljust(BS, b"\0")
        copies = [bytes(tx[h]) for h in homes]
        crc = zlib.crc32(b"".join(copies)) if self.jcsum else 0
        commit = struct.pack("<4I", JCOMMIT, self.seq, crc, int(self.jcsum)).ljust(BS, b"\0")
        out = [(j, desc)] + [(j + 1 + k, c) for k, c in enumerate(copies)]
        return out, (j + 1 + len(homes), commit)

    def _commit(self, tx: dict, kind: dict, freeing: bool) -> None:
        d = self.d
        data = [b for b in tx if kind.get(b) == "data"]
        meta = [b for b in tx if kind.get(b) != "data"]
        if self.mode == "none":
            for b in tx:
                d.write(b, tx[b])
            d.flush()
            return
        if self.mode == "careful":
            sb = self.sb

            def group(b):
                k = kind.get(b)
                if k == "data":
                    return 0
                if k == "dir":
                    return 4
                if b < sb["itable"]:
                    return 1                                    # bitmaps
                if b < sb["journal"]:
                    return 3                                    # the inode table
                return 2                                        # indirect blocks
            groups: dict[int, list[int]] = {}
            for b in tx:
                groups.setdefault(group(b), []).append(b)
            # allocating: a block is written before anything points to it; freeing: pointers are cleared first
            order = [0, 1, 2, 3, 4] if not freeing else [4, 3, 2, 1, 0]
            for g in order:
                for b in groups.get(g, ()):
                    d.write(b, tx[b])
                if g in groups:
                    d.flush()
            return
        journaled = meta + (data if self.mode == "data" else [])
        if self.mode == "ordered":
            for b in data:
                d.write(b, tx[b])
            if data:
                d.flush()
        jb, (cn, commit) = self._jblocks(tx, journaled)
        for n, blk in jb:
            d.write(n, blk)
        if self.barriers:
            d.flush()
        d.write(cn, commit)
        d.flush()
        for b in journaled:                                     # checkpoint: the blocks to their homes
            d.write(b, tx[b])
        if self.mode == "writeback":                            # data whenever it gets there: here, after the commit
            for b in data:
                d.write(b, tx[b])
        d.flush()
        self.seq += 1
        d.write(self.sb["journal"], _jclear(self.seq))         # the journal is empty again
        d.flush()

    # -- recovery ----------------------------------------------------------------------------------------------------
    def recover(self) -> str:
        """Replay a committed transaction from the journal; discard an uncommitted one.  Returns what happened."""
        j = self.sb["journal"]
        desc = self.d.read(j)
        magic, seq, count, _ = _words(desc, 4)
        if magic != JDESC:
            self.seq = max(seq, 1)                             # a cleared journal keeps the next sequence number
            return "clean"
        if count > min(self.sb["jlen"] - 2, PER - 4):
            self.seq = seq + 1
            self.d.write(j, _jclear(self.seq))
            return "discarded"
        homes = _words(desc, count, 16)
        commit = self.d.read(j + 1 + count)
        cm, cseq, crc, has = _words(commit, 4)
        copies = [self.d.read(j + 1 + k) for k in range(count)]
        ok = cm == JCOMMIT and cseq == seq and (not has or zlib.crc32(b"".join(copies)) == crc)
        if ok:
            for h, c in zip(homes, copies):
                self.d.write(h, c)
            self.d.flush()
        self.seq = seq + 1
        self.d.write(j, _jclear(self.seq))
        self.d.flush()
        return "replayed" if ok else "discarded"


def _jclear(seq: int) -> bytes:
    return struct.pack("<2I", 0, seq).ljust(BS, b"\0")


# ---- checking ----------------------------------------------------------------------------------------------------
HARMLESS = ("leaked block", "leaked inode")


def fsck(d: Disk, repair: bool = False) -> list[tuple[str, str]]:
    """Every invariant of a PebbleFS image.  Returns (kind, detail) for each problem; kinds in ``HARMLESS`` lose only
    space.  ``repair`` rebuilds the bitmaps from what is reachable, drops entries naming free inodes, fixes link
    counts and trims sizes, as fsck -y would."""
    sb = superblock(d)
    if sb["magic"] != MAGIC:
        return [("bad superblock", "")]
    fs = FS(d, mode="none", recover=False)
    probs: list[tuple[str, str]] = []
    ib = d.read(sb["ibmap"])
    dbm = b"".join(d.read(sb["dbmap"] + k) for k in range(sb["ndbmap"]))
    owner: dict[int, int] = {}
    names: dict[int, int] = {}                              # directory entries naming each inode
    subdirs: dict[int, int] = {}                            # each directory's subdirectories
    seen: set[int] = set()
    dirs_fix: list[tuple[int, int]] = []
    size_fix: dict[int, int] = {}
    stack = [ROOT]
    while stack:
        inum = stack.pop()
        if inum in seen:
            continue
        seen.add(inum)
        ino = fs.iget(inum)
        if ino["type"] == FREE_T or not _bit(ib, inum):
            probs.append(("free inode in use", f"inode {inum}"))
            continue
        nb = -(-ino["size"] // BS)
        blocks = []
        for i in range(nb):
            try:
                b = fs.bmap(ino, i)
            except FSError:
                b = 0
            if not b:
                probs.append(("size beyond blocks", f"inode {inum}, block {i}"))
                size_fix[inum] = i * BS
                break
            blocks.append(b)
        _, ind = fs.blocks_of({**ino, "size": 0})
        for b in blocks + ind:
            if not sb["data"] <= b < sb["nblocks"]:
                probs.append(("bad pointer", f"inode {inum} -> {b}"))
                continue
            if b in owner and owner[b] != inum:
                probs.append(("doubly used block", f"block {b}: inodes {owner[b]} and {inum}"))
            owner[b] = inum
            if not _bit(dbm, b - sb["data"]):
                probs.append(("free block in use", f"block {b} (inode {inum})"))
        if ino["type"] == DIR:
            for b in blocks:
                if not sb["data"] <= b < sb["nblocks"]:
                    continue
                for k, c, nm in _dirents(d.read(b)):
                    if not c or nm in (b".", b".."):
                        continue
                    if not 0 < c < sb["ninodes"]:
                        probs.append(("bad entry", f"{nm!r} -> {c}"))
                        dirs_fix.append((b, k))
                        continue
                    ci = fs.iget(c)
                    if ci["type"] == FREE_T or not _bit(ib, c):
                        probs.append(("entry to a free inode", f"{nm.decode(errors='replace')} -> inode {c}"))
                        dirs_fix.append((b, k))
                        continue
                    names[c] = names.get(c, 0) + 1
                    if ci["type"] == DIR:
                        subdirs[inum] = subdirs.get(inum, 0) + 1
                    stack.append(c)
    # a file's links are its names; a directory's are its name (none for the root), its "." and its children's ".."
    for inum in seen:
        ino = fs.iget(inum)
        if ino["type"] == FREE_T or not _bit(ib, inum):
            continue
        want = names.get(inum, 0) if ino["type"] == FILE else 2 + subdirs.get(inum, 0)
        if ino["nlink"] != want:
            probs.append(("bad link count", f"inode {inum}: {ino['nlink']}, should be {want}"))
    for i in range(1, sb["ninodes"]):
        if _bit(ib, i) and i not in seen:
            probs.append(("leaked inode", f"inode {i}"))
    for i in range(sb["ndata"]):
        if _bit(dbm, i) and sb["data"] + i not in owner:
            probs.append(("leaked block", f"block {sb['data'] + i}"))
    if repair and probs:
        _repair(d, fs, sb, seen, owner, dirs_fix, size_fix)
    return probs


def _repair(d, fs, sb, seen, owner, dirs_fix, size_fix):
    with fs.op():
        for b, k in dirs_fix:
            fs._get(b)[k * DSIZE:(k + 1) * DSIZE] = bytes(DSIZE)
        for inum, size in size_fix.items():
            ino = fs.iget(inum)
            ino["size"] = size
            fs._iput(inum, ino)
        ib = bytearray(BS)
        ib[0] |= 1
        for i in seen:
            if fs.iget(i)["type"] != FREE_T:
                ib[i >> 3] |= 1 << (i & 7)
        fs._get(sb["ibmap"])[:] = ib
        for k in range(sb["ndbmap"]):
            fs._get(sb["dbmap"] + k)[:] = bytes(BS)
        for b in owner:
            bb, bit = fs._bmap_block(b - sb["data"])
            fs._get(bb)[bit >> 3] |= 1 << (bit & 7)
    # link counts last, from a fresh walk
    for kind, detail in fsck(d):
        if kind == "bad link count":
            inum = int(detail.split()[1].rstrip(":"))
            want = int(detail.rsplit(" ", 1)[1])
            with fs.op():
                ino = fs.iget(inum)
                ino["nlink"] = want
                fs._iput(inum, ino)


def fsck_reads(d: Disk) -> int:
    """How many blocks a full check reads: the cost that grows with the disk, not with what went wrong."""
    c = d.copy()
    fsck(c)
    return c.reads


# ---- crash injection ----------------------------------------------------------------------------------------------
def epochs(trace: list) -> list[list[tuple[int, bytes]]]:
    """The writes between flushes."""
    out, cur = [], []
    for e in trace:
        if e[0] == "f":
            out.append(cur)
            cur = []
        else:
            cur.append((e[1], e[2]))
    if cur:
        out.append(cur)
    return [e for e in out if e]


def crash_states(base: Disk, trace: list, reorder: bool = True, max_epoch: int = 12, rng=None):
    """Every disk a crash during ``trace`` could leave behind, starting from ``base``: (label, Disk).

    Without ``reorder`` the writes reach the disk in order, so a crash leaves a prefix.  With it, every write
    before the last flush is durable and any subset of the ones after it may be (an epoch with more than
    ``max_epoch`` writes is sampled: its prefixes and 4096 random subsets)."""
    if not reorder:
        flat = [(e[1], e[2]) for e in trace if e[0] == "w"]
        cur = base.copy()
        yield ("0 writes", cur.copy())
        for k, (n, blk) in enumerate(flat):
            cur.b[n] = blk
            yield (f"{k + 1} writes", cur.copy())
        return
    ep = epochs(trace)
    cur = base.copy()
    seen = set()
    rng = rng or random.Random(0)
    for e_i, writes in enumerate(ep):
        k = len(writes)
        if k <= max_epoch:
            subsets = itertools.chain.from_iterable(itertools.combinations(range(k), r) for r in range(k + 1))
        else:
            subsets = [tuple(range(r)) for r in range(k + 1)] + [
                tuple(sorted(rng.sample(range(k), rng.randint(1, k - 1)))) for _ in range(4096)]
        for sub in subsets:
            dsk = cur.copy()
            for i in sub:
                n, blk = writes[i]
                dsk.b[n] = blk
            key = hash(tuple(dsk.b[n] for n in sorted({w[0] for w in writes})))
            if (e_i, key) in seen:
                continue
            seen.add((e_i, key))
            yield (f"epoch {e_i + 1}: {len(sub)} of {k}", dsk)
        for n, blk in writes:
            cur.b[n] = blk
    yield ("all", cur.copy())


def crash_test(setup, operation, check=None, reorder: bool = True, **fskw) -> dict:
    """Run ``setup(fs)`` on a fresh file system, then record ``operation(fs)`` and crash it at every point.
    After each crash: mount (replaying the journal), fsck, and ``check(fs)`` (return None if the contents are
    acceptable, else a word for what is wrong).  Returns counts and a few examples."""
    d = Disk(fskw.pop("nblocks", 512))
    stale = fskw.pop("stale", b"OLD-SECRET ")
    fs = FS.mkfs(d, ninodes=fskw.pop("ninodes", 64), jlen=fskw.pop("jlen", 32), stale=stale, **fskw)
    setup(fs)
    fs.sync()
    base = d.copy()
    d.trace = []
    operation(fs)
    fs.sync()
    trace = d.trace
    d.trace = None
    res = {"states": 0, "consistent": 0, "leak_only": 0, "corrupt": 0, "bad_data": 0, "ok": 0, "examples": [],
           "writes": sum(1 for e in trace if e[0] == "w"), "flushes": sum(1 for e in trace if e[0] == "f"),
           "problems": {}, "recovery": {}}
    for lbl, dsk in crash_states(base, trace, reorder=reorder):
        res["states"] += 1
        try:
            f2 = FS(dsk, **{k: v for k, v in fskw.items() if k in ("mode", "barriers", "jcsum")})
            rec = f2.recovery
        except FSError:
            rec = "unmountable"
        res["recovery"][rec] = res["recovery"].get(rec, 0) + 1
        probs = fsck(dsk)
        kinds = sorted({p[0] for p in probs})
        for k in kinds:
            res["problems"][k] = res["problems"].get(k, 0) + 1
        bad = None
        if not probs:
            res["consistent"] += 1
        elif all(k in HARMLESS for k in kinds):
            res["leak_only"] += 1
        else:
            res["corrupt"] += 1
        if check and not [k for k in kinds if k not in HARMLESS]:
            try:
                bad = check(FS(dsk, mode="none", recover=False))
            except FSError as e:
                bad = f"error: {e}"
            if bad:
                res["bad_data"] += 1
        if not [k for k in kinds if k not in HARMLESS] and not bad:
            res["ok"] += 1
        if (probs and [k for k in kinds if k not in HARMLESS] or bad) and len(res["examples"]) < 6:
            res["examples"].append({"at": lbl, "problems": kinds, "data": bad})
    return res
