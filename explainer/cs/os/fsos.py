"""PebbleOS with a disk and a file system (Part 34).

    d = Disk(8192); fs = FS.mkfs(d, mode="none"); fs.mkdir("/novels"); ...    # build the disk (explainer.cs.store.fs)
    p = K.user("tok", TOK, 0, stdin="file", stdout="pipe"); p.fino = fs.lookup("/novels/emma")
    m = boot_fs([p, ...], d)                  # a DiskMachine: the kernel reads PebbleFS through the disk device
    m.run(); m.io                             # every block the kernel read, in order

**The device.**  Three registers in the I/O page: the block number, a physical memory address, and a command;
storing 1 to the command copies the 1 KiB block from the disk into memory (direct memory access).  Only the kernel
can reach them.  Every transfer is logged, so the access pattern can be timed on a model disk afterwards
(:mod:`explainer.cs.store.disk`).

**The kernel's part**, in Pebble assembly, about 170 instructions:

* at boot, read the superblock (block 0): where the inode table is;
* ``bread``: read a block into one of four one-block buffers (inode table, indirect, double-indirect, data), unless
  that buffer already holds it: a buffer cache of four blocks;
* ``iget``: find inode i in the inode table; ``bmap``: the disk block holding block k of a file, through the
  direct, single- and double-indirect pointers;
* ``open(path, length)`` (system call 5): walk the path from the root, one directory at a time, comparing names in
  32-byte entries; returns file descriptor 3, with the file's inode and offset 0 kept in the PCB;
* ``read`` on descriptor 3, or on descriptor 0 when standard input was redirected from a file (as a shell does with
  ``tok < /novels/emma``): copy from the file's blocks, at most to its end; 0 at the end.

Writing is left to the Python side (:class:`~explainer.cs.store.fs.FS`), which built the disk.
"""
from __future__ import annotations

from explainer.cs.os import kernel as K
from explainer.cs.os.machine import OSMachine
from explainer.cs.pebble.asm import assemble
from explainer.cs.pebble.isa import MASK
from explainer.cs.store.fs import BS, Disk

IO_DISK = 0xFFFF_0010          # +0 block, +4 address, +8 command (1 = read)
SYS_OPEN = 5

FS_BOOT = """        li   a3, 0              # read the superblock
        la   a4, sbuf
        la   a5, sbtag
        call bread"""
FS_DISPATCH = """        li   t2, 5
        beq  t1, t2, sys_open"""
FS_FD3 = """li   t2, 3
        beq  a0, t2, rd3"""
FS_STDIN = """        li   t2, 2
        beq  t1, t2, read_file  # standard input redirected from a file"""
FS_HANDLER = """
# ---- the file system: PebbleFS, read through the disk device ------------------------------------
# bread: block a3 into the buffer at a4, unless the tag word at a5 says it is already there
bread:  lw   t1, 0(a5)
        beq  t1, a3, br_hit
        sw   a3, 0(a5)
        li   t1, {IO_DISK}
        sw   a3, 0(t1)          # which block
        sw   a4, 4(t1)          # where in memory
        li   t2, 1
        sw   t2, 8(t1)          # read it
        lw   t2, nbread(zero)
        addi t2, t2, 1
        sw   t2, nbread(zero)
br_hit: ret

# iget: s1 = the address of inode a0, in the inode-table buffer
iget:   addi sp, sp, -4
        sw   ra, 0(sp)
        la   t1, sbuf
        lw   a3, 24(t1)         # the superblock: the inode table's first block
        srli t2, a0, 4          # 16 inodes per block
        add  a3, a3, t2
        la   a4, ibuf
        la   a5, ibtag
        call bread
        andi t2, a0, 15
        slli t2, t2, 6          # 64 bytes each
        la   s1, ibuf
        add  s1, s1, t2
        lw   ra, 0(sp)
        addi sp, sp, 4
        ret

# bmap: a3 = the disk block holding block a0 of the file whose inode is at s1 (0 if none)
bmap:   addi sp, sp, -4
        sw   ra, 0(sp)
        li   t1, 10
        bge  a0, t1, bm1
        slli t2, a0, 2          # direct: inode word 3 + a0
        add  t2, s1, t2
        lw   a3, 12(t2)
        j    bmret
bm1:    addi a0, a0, -10
        li   t1, 256
        bge  a0, t1, bm2
        lw   a3, 52(s1)         # single indirect: a block of 256 pointers
        beqz a3, bmret
        la   a4, indbuf
        la   a5, indtag
        call bread
        slli t2, a0, 2
        la   a4, indbuf
        add  t2, a4, t2
        lw   a3, 0(t2)
        j    bmret
bm2:    addi a0, a0, -256
        lw   a3, 56(s1)         # double indirect: 256 blocks of 256
        beqz a3, bmret
        la   a4, dibuf
        la   a5, ditag
        call bread
        srli t2, a0, 8
        slli t2, t2, 2
        la   a4, dibuf
        add  t2, a4, t2
        lw   a3, 0(t2)
        beqz a3, bmret
        la   a4, indbuf
        la   a5, indtag
        call bread
        andi t2, a0, 255
        slli t2, t2, 2
        la   a4, indbuf
        add  t2, a4, t2
        lw   a3, 0(t2)
bmret:  lw   ra, 0(sp)
        addi sp, sp, 4
        ret

rd3:    call checkbuf           # read(3, buf, n): the opened file
        lw   t1, {FINO}(t0)
        beqz t1, bad
# read_file: copy min(n, size - offset) bytes of the PCB's file to a1, block by block
read_file: sw a1, rf_buf(zero)
        lw   a0, {FINO}(t0)
        call iget
        lw   t1, 8(s1)          # the size
        lw   t2, {FOFF}(t0)
        sub  t1, t1, t2         # bytes left
        bge  t1, a2, rf0
        mv   a2, t1
rf0:    sw   a2, rf_n(zero)
        sw   zero, rf_done(zero)
rf1:    lw   t1, rf_done(zero)
        lw   t2, rf_n(zero)
        bge  t1, t2, rf9
        lw   a0, {FOFF}(t0)
        srli a0, a0, 10         # which block of the file
        call bmap
        la   a4, dbuf
        la   a5, dbtag
        call bread
        lw   t1, {FOFF}(t0)
        andi t1, t1, 1023       # where in the block
        li   t2, 1024
        sub  t2, t2, t1         # room left in it
        lw   t3, rf_n(zero)
        lw   s0, rf_done(zero)
        sub  t3, t3, s0         # bytes still wanted
        bge  t3, t2, rf2
        mv   t2, t3
rf2:    la   s2, dbuf
        add  s2, s2, t1         # from
        lw   s0, rf_buf(zero)
        lw   t3, rf_done(zero)
        add  s0, s0, t3         # to
        add  t3, s2, t2         # end
rf3:    bge  s2, t3, rf4
        lbu  t1, 0(s2)
        sb   t1, 0(s0)
        addi s2, s2, 1
        addi s0, s0, 1
        j    rf3
rf4:    lw   t1, rf_done(zero)
        add  t1, t1, t2
        sw   t1, rf_done(zero)
        lw   t1, {FOFF}(t0)
        add  t1, t1, t2
        sw   t1, {FOFF}(t0)
        j    rf1
rf9:    lw   t1, rf_done(zero)
        sw   t1, 12(t0)
        j    resume

# open(path a1, length a2): walk the path from the root; fd 3
sys_open: call checkbuf
        add  t1, a1, a2
        sw   t1, lk_end(zero)
        sw   a1, lk_p(zero)
        li   t1, 1
        sw   t1, lk_cur(zero)   # start at the root, inode 1
op1:    lw   t1, lk_p(zero)
        lw   t2, lk_end(zero)
        bge  t1, t2, op_done
        lbu  t3, 0(t1)
        li   s0, 47
        bne  t3, s0, op2
        addi t1, t1, 1          # skip a '/'
        sw   t1, lk_p(zero)
        j    op1
op2:    mv   s0, t1             # the next name: [lk_p, s0)
op3:    bge  s0, t2, op4
        lbu  t3, 0(s0)
        li   s2, 47
        beq  t3, s2, op4
        addi s0, s0, 1
        j    op3
op4:    sub  t3, s0, t1
        sw   t3, lk_n(zero)
        li   s2, 28
        blt  s2, t3, bad        # longer than any name
        sw   s0, lk_next(zero)
        lw   a0, lk_cur(zero)
        call iget
        lw   t1, 0(s1)
        li   t2, 2
        bne  t1, t2, bad        # not a directory
        lw   t1, 8(s1)
        srli t1, t1, 10
        sw   t1, lk_nb(zero)    # its blocks
        sw   zero, lk_bi(zero)
op5:    lw   t1, lk_bi(zero)
        lw   t2, lk_nb(zero)
        bge  t1, t2, bad        # no such name
        lw   a0, lk_cur(zero)
        call iget
        lw   a0, lk_bi(zero)
        call bmap
        la   a4, dbuf
        la   a5, dbtag
        call bread
        la   s2, dbuf           # each 32-byte entry
op6:    la   t1, dbuf
        addi t1, t1, 1024
        bge  s2, t1, op8
        lw   t1, 0(s2)
        beqz t1, op7            # unused
        lw   t1, lk_p(zero)
        lw   t2, lk_n(zero)
        addi t3, s2, 4
        li   s0, 0
opc:    bge  s0, t2, opc2       # compare the name byte by byte
        add  a3, t1, s0
        lbu  a3, 0(a3)
        add  a4, t3, s0
        lbu  a4, 0(a4)
        bne  a3, a4, op7
        addi s0, s0, 1
        j    opc
opc2:   li   s0, 28
        beq  t2, s0, op_hit
        add  a4, t3, t2
        lbu  a4, 0(a4)
        bnez a4, op7            # the entry's name goes on
op_hit: lw   t1, 0(s2)
        sw   t1, lk_cur(zero)   # found: go down
        lw   t1, lk_next(zero)
        sw   t1, lk_p(zero)
        j    op1
op7:    addi s2, s2, 32
        j    op6
op8:    lw   t1, lk_bi(zero)
        addi t1, t1, 1
        sw   t1, lk_bi(zero)
        j    op5
op_done: lw  t1, lk_cur(zero)
        sw   t1, {FINO}(t0)
        sw   zero, {FOFF}(t0)
        li   t1, 3
        sw   t1, 12(t0)
        j    resume"""
FS_DATA = """nbread: .word 0
sbtag:  .word -1
ibtag:  .word -1
indtag: .word -1
ditag:  .word -1
dbtag:  .word -1
rf_buf: .word 0
rf_n:   .word 0
rf_done: .word 0
lk_p:   .word 0
lk_end: .word 0
lk_n:   .word 0
lk_next: .word 0
lk_cur: .word 0
lk_nb:  .word 0
lk_bi:  .word 0
        .align 4
sbuf:   .space 1024
ibuf:   .space 1024
indbuf: .space 1024
dibuf:  .space 1024
dbuf:   .space 1024"""


def fs_parts() -> dict:
    f = dict(IO_DISK=IO_DISK, FINO=K.FINO, FOFF=K.FOFF)
    return {"fs_boot": FS_BOOT, "fs_dispatch": FS_DISPATCH, "fs_fd3": FS_FD3, "fs_stdin": FS_STDIN,
            "fs_handler": FS_HANDLER.format(**f), "fs_data": FS_DATA}


class DiskMachine(OSMachine):
    """Part 31's machine with a disk on the I/O page."""

    def __post_init__(self):
        super().__post_init__()
        self.disk: Disk | None = None
        self.dreg = [0, 0]
        self.io: list[tuple[int, int]] = []          # (instruction count, block) for every block read

    def store(self, addr, size, value):
        a = addr & MASK
        if self.mode == 1 and IO_DISK <= a < IO_DISK + 12:
            r = (a - IO_DISK) // 4
            if r < 2:
                self.dreg[r] = value & MASK
                return
            if value == 1:
                blk, dst = self.dreg
                self.mem[dst:dst + BS] = self.disk.b[blk]
                for w in range(dst, dst + BS, 4):
                    self._dec.pop(w, None)
                self.io.append((self.steps, blk))
            return
        super().store(addr, size, value)


def kernel_source(procs, quantum: int = K.QUANTUM) -> str:
    return K.kernel_source(procs, quantum, fs=fs_parts())


def boot_fs(procs: list[K.Proc], disk: Disk, quantum: int = K.QUANTUM, tape: bytes = b"") -> DiskMachine:
    k = assemble(kernel_source(procs, quantum))
    m = DiskMachine(image=k.image, tape=tape, mem_size=K.MEM)
    m.disk = disk
    for p in procs:
        m.mem[p.lo:p.lo + len(p.image)] = p.image
    m.kernel = k
    m.procs = procs
    return m


def fs_instructions() -> int:
    """How many instructions the file-system part adds to the kernel."""
    return (assemble(kernel_source([])).labels["kend"] - assemble(K.kernel_source([])).labels["kend"]) // 4


def predict_reads(fs, path: str | None = None, inum: int | None = None, boot: bool = True) -> list[int]:
    """The blocks PebbleOS's kernel reads, in order, to open ``path`` (or, with ``inum``, a file handed over as
    standard input) and read it to the end: the kernel's algorithm and its four tagged buffers, in Python.  The
    tests check it against the device's log; the ledger uses it for files too long to run through the emulator."""
    import struct
    from explainer.cs.store.fs import IPB, NDIRECT, PER
    disk = fs.d
    tags = {"sb": -1, "ib": -1, "ind": -1, "di": -1, "db": -1}
    out = []

    def bread(blk, buf):
        if tags[buf] != blk:
            tags[buf] = blk
            out.append(blk)
        return disk.b[blk]

    def word(raw, k):
        return struct.unpack_from("<I", raw, 4 * k)[0]
    if boot:
        bread(0, "sb")
    sb = fs.sb

    def iget(i):
        raw = bread(sb["itable"] + i // IPB, "ib")
        off = (i % IPB) * 64
        return [word(raw[off:off + 64], k) for k in range(16)]

    def bmap(ino, k):
        if k < NDIRECT:
            return ino[3 + k]
        k -= NDIRECT
        if k < PER:
            if not ino[13]:
                return 0
            return word(bread(ino[13], "ind"), k)
        k -= PER
        if not ino[14]:
            return 0
        mid = word(bread(ino[14], "di"), k // PER)
        if not mid:
            return 0
        return word(bread(mid, "ind"), k % PER)
    if path is not None:
        cur = 1
        for comp in [c for c in path.split("/") if c]:
            ino = iget(cur)
            nb = ino[2] // 1024
            found = None
            for bi in range(nb):
                ino = iget(cur)
                raw = bread(bmap(ino, bi), "db")
                for e in range(32):
                    n = word(raw, 8 * e)
                    name = raw[32 * e + 4:32 * e + 32].rstrip(b"\0")
                    if n and name == comp.encode():
                        found = n
                        break
                if found:
                    break
            cur = found
        inum = cur
    ino = iget(inum)
    size = ino[2]
    for k in range(-(-size // 1024)):
        ino = iget(inum)
        bread(bmap(ino, k), "db")
    return out
