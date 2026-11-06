"""Precompute everything numerical in Part 34 of *Computer Science, Built* ("Storage").

    python -m videos.cs.cs34.compute              # everything missing
    python -m videos.cs.cs34.compute --force crash

Results are cached in ``.cache/cs34/<name>.json``; scenes call ``load(name)``.  The instruments are
``explainer/cs/store/`` (fs.py: PebbleFS, its journal, fsck and crash injection; disk.py, flash.py, lfs.py, raid.py,
lsm.py, cow.py) and PebbleOS's disk (``explainer/cs/os/fsos.py``); tests in tests/test_cs34_storage.py.

Items:
    hook        one block appended to a one-block file with no journal: the three writes, and all eight subsets a
                crash can leave, each checked by fsck and by reading the file
    disk        the disk-time model: seek curve, rotation, transfer; random against sequential; FCFS, SSTF, SCAN and
                C-SCAN on the textbook queue and under load
    flash       the FTL: write amplification against over-provisioning (simulated, and the estimate), FIFO, skewed
                traffic and wear, TRIM, sequential writes
    fs          PebbleFS's layout on an 8 MiB disk, an inode, the largest file, and the blocks PebbleOS reads to open
                /novels/emma
    locality    a 4 MiB file laid out contiguously, interleaved with another, and on an aged disk: extents and read
                time on the model disk and on flash
    crash       every crash point of four operations under each commit mode, with and without barriers and journal
                checksums; fsck's reads against a journal replay's
    journal     one ordered-mode append, write by write, and what recovery does after a crash at each point
    apps        replacing a file's contents in place, by rename, and by fsync then rename, with delayed allocation
    lfs         the log-structured cleaner: write cost against utilization (greedy, hot-and-cold, cost-benefit) and
                the utilizations of the segments it cleans
    cow         a copy-on-write tree with checksums: blocks per write, a snapshot's sharing, bit rot caught and healed
    raid        layouts, small writes, throughput, RAID 6 recovering any two disks, rebuild risk, MTTDL
    lsm         leveled against tiered compaction, with and without Bloom filters, against a B-tree; a small tree's
                levels as it grows
    kv          a key-value store whose runs are files on PebbleFS: one novel's word counts, stored and read back
    pebble      PebbleOS reading the novels from its disk: the kernel's file-system code, a novel read through it,
                tok | job on passages read from files, the fit, the thirty novels; ledger row 12
    frontier    the LSM design space (Monkey's Bloom allocation), the explosion of crash states, zoned writes
"""

from __future__ import annotations

import itertools
import json
import math
import random

from explainer.ai.cache import Cache

CACHE = Cache("cs34")
load = CACHE.load

OLD1, NEW1 = b"o" * 1024, b"n" * 1024
STALE = b"PASSWORD=hunter2 "


def _roles(fs, blk: int) -> str:
    sb = fs.sb
    if blk == 0:
        return "superblock"
    if blk == sb["ibmap"]:
        return "inode bitmap"
    if sb["dbmap"] <= blk < sb["itable"]:
        return "data bitmap"
    if sb["itable"] <= blk < sb["journal"]:
        return "inode table"
    if sb["journal"] <= blk < sb["data"]:
        return "journal"
    return "data"


# ---- the hook --------------------------------------------------------------------------------------------------
def compute_hook() -> dict:
    from explainer.cs.store.fs import FS, Disk, fsck
    d = Disk(256)
    fs = FS.mkfs(d, ninodes=32, jlen=16, stale=STALE, mode="none")
    fs.create("/notes")
    fs.append("/notes", OLD1)
    base = d.copy()
    d.trace = []
    fs.append("/notes", NEW1)
    writes = [(e[1], e[2]) for e in d.trace if e[0] == "w"]
    d.trace = None
    roles = [_roles(fs, b) for b, _ in writes]
    out = []
    for r in range(len(writes) + 1):
        for sub in itertools.combinations(range(len(writes)), r):
            dsk = base.copy()
            for i in sub:
                dsk.b[writes[i][0]] = writes[i][1]
            probs = sorted({k for k, _ in fsck(dsk)})
            c = FS(dsk, mode="none", recover=False).read("/notes")
            content = ("old" if c == OLD1 else "new" if c == OLD1 + NEW1 else
                       "another file's bytes" if STALE[:8] in c else "other")
            out.append({"durable": [roles[i] for i in sub], "problems": probs, "content": content})
    return {"writes": roles, "blocks": [b for b, _ in writes], "states": out, "stale": STALE.decode().strip()}


# ---- disks -----------------------------------------------------------------------------------------------------
def compute_disk() -> dict:
    from explainer.cs.store import disk as D
    h = D.HDD()
    curve = [{"d": d, "ms": h.seek(d)} for d in [0, 1, 100, 1000, 5000, 10_000, 25_000, 50_000, 75_000, 100_000]]
    rnd = h.random_io(4096)
    rand_mb = 4096 / (rnd / 1e3) / 1e6
    q = [98, 183, 37, 122, 14, 124, 65, 67]
    static = {p: {"order": D.order(p, 53, q), "distance": D.distance(53, D.order(p, 53, q))}
              for p in ("fcfs", "sstf", "scan", "cscan")}
    load = []
    for rate in (40, 60, 72):
        row = {"rate": rate}
        for p in ("fcfs", "sstf", "scan", "cscan"):
            row[p] = D.simulate(p, rate, n=20_000, seed=1)
        load.append(row)
    ssd = D.SSD
    return {"avg_seek": h.avg_seek(), "half_turn": h.rev_ms / 2, "rev": h.rev_ms, "mb_s": h.mb_s, "rpm": h.rpm,
            "t_min": h.t_min, "t_max": h.t_max, "cylinders": h.cylinders, "curve": curve,
            "random_4k_ms": rnd, "random_iops": 1000 / rnd, "random_mb_s": rand_mb, "ratio": h.mb_s / rand_mb,
            "transfer_4k_ms": h.transfer(4096), "static": static, "queue": q, "head": 53, "load": load,
            "ssd_read_us": ssd.read_us, "ssd_gb_s": ssd.gb_s}


def compute_flash() -> dict:
    from explainer.cs.store import flash as F
    ops = [0.07, 0.1, 0.15, 0.2, 0.28, 0.4, 0.55, 0.7, 1.0]
    greedy = [{"op": op, "wa": F.ftl(op=op, writes=6)["wa"], "estimate": F.wa_greedy_estimate(op)} for op in ops]
    fifo = [{"op": op, "wa": F.ftl(op=op, writes=6, policy="fifo")["wa"]} for op in ops]
    hot = F.ftl(op=0.28, writes=8, hot=(0.9, 0.1))
    uni = F.ftl(op=0.28, writes=8)
    trim = [{"trim": t, "wa": F.ftl(op=0.07, writes=6, trim=t)["wa"]} for t in (0.0, 0.1, 0.2, 0.3, 0.5)]
    seq = F.ftl(op=0.07, writes=6, pattern="sequential")
    return {"greedy": greedy, "fifo": fifo, "blocks": 256, "pages": 64,
            "hot": {"wa": hot["wa"], "erases": hot["erases"], "max": hot["erase_max"], "mean": hot["erase_mean"]},
            "uniform": {"wa": uni["wa"], "erases": uni["erases"], "max": uni["erase_max"], "mean": uni["erase_mean"]},
            "trim": trim, "sequential": seq["wa"]}


# ---- the file system ---------------------------------------------------------------------------------------------
def slug(title: str) -> str:
    """A file name for a novel: "The Count of Monte Cristo" -> "count-of-monte-cristo"."""
    w = [x for x in title.lower().replace("'", "").split() if x not in ("the", "a")]
    return "-".join(w)[:28]


def _novel_disk(nblocks=8192, alloc="next"):
    from explainer.cs.store.fs import FS, Disk
    from videos.cs.cs6.compute import novels
    import videos.ai.ai1.compute as A
    from explainer.cs.pebble import programs as PR
    d = Disk(nblocks)
    fs = FS.mkfs(d, ninodes=256, mode="none", alloc=alloc)
    fs.mkdir("/novels")
    books = novels()
    return d, fs, books, A.BOOKS, PR


def compute_fs() -> dict:
    from explainer.cs.os import fsos as F
    from explainer.cs.os import kernel as K
    from explainer.cs.store.fs import MAXFILE, fsck, superblock
    d, fs, books, names, PR = _novel_disk(8192)
    emma = PR.job_tape(books[158])[:200_000]             # the first 200 KB of Emma
    fs.create("/novels/emma")
    fs.append("/novels/emma", emma)
    fs.mkdir("/home")
    fs.create("/home/notes")
    fs.append("/home/notes", b"buy milk\n")
    sb = superblock(d)
    ino = fs.iget(fs.lookup("/novels/emma"))
    data, ind = fs.blocks_of(ino)
    path = "/novels/emma"
    reads = F.predict_reads(fs, path)
    cat = f"""
main:   li   a0, 0
        la   a1, path
        li   a2, {len(path)}
        li   a5, 5
        ecall
loop:   li   a0, 3
        la   a1, buf
        li   a2, 1024
        li   a5, 1
        ecall
        ble  a0, zero, done
        mv   a2, a0
        li   a0, 1
        la   a1, buf
        li   a5, 2
        ecall
        j    loop
done:   ret
path:   .ascii "{path}"
        .align 4
buf:    .space 1024
"""
    m = F.boot_fs([K.user_asm("cat", cat, 0)], d)
    m.run(100_000_000)
    io = [b for _, b in m.io]
    assert bytes(m.output) == emma and io == reads
    first = []
    for b in io[:12]:
        r = _roles(fs, b)
        if r == "data":
            r = "indirect" if b in ind else ("directory" if b not in data else "file data")
        first.append({"block": b, "role": r})
    dirs = {p: fs.listdir(p) for p in ("/", "/novels", "/home")}
    return {"sb": sb, "inode": {"type": ino["type"], "nlink": ino["nlink"], "size": ino["size"],
                                "direct": ino["direct"], "ind": ino["ind"], "dind": ino["dind"]},
            "maxfile": MAXFILE, "emma_bytes": len(emma), "data_blocks": len(data), "indirect_blocks": len(ind),
            "reads": len(io), "first_reads": first, "steps": m.steps, "kernel_fs_instructions": F.fs_instructions(),
            "dirs": dirs, "fsck": fsck(d), "nblocks": len(d)}


def compute_locality() -> dict:
    from explainer.cs.os import fsos as F
    from explainer.cs.store import disk as D
    from explainer.cs.store.fs import FS, Disk
    size = 4 << 20
    rng = random.Random(4)
    text = bytes(rng.randrange(32, 127) for _ in range(size))
    out = {}
    h, s = D.HDD(), D.SSD

    def runs(blocks):
        n = 1
        for a, b in zip(blocks, blocks[1:]):
            n += b != a + 1
        return n
    for name in ("contiguous", "interleaved", "aged"):
        d = Disk(16384)
        fs = FS.mkfs(d, ninodes=64, mode="none", alloc="random" if name == "aged" else "next", seed=3)
        fs.create("/big")
        if name == "interleaved":
            fs.create("/other")
            for k in range(0, size, 1024):
                fs.append("/big", text[k:k + 1024])
                fs.append("/other", text[k:k + 1024])
        else:
            fs.append("/big", text)
        inum = fs.lookup("/big")
        data, _ = fs.blocks_of(fs.iget(inum))
        reads = F.predict_reads(fs, inum=inum, boot=False)
        out[name] = {"extents": runs(data), "first": data[:24], "hdd_ms": h.trace_time(reads)["ms"],
                     "ssd_ms": s.trace_time(reads)["ms"], "reads": len(reads)}
    out["seq_limit_ms"] = size / (h.mb_s * 1e6) * 1e3
    return out


# ---- crash consistency -----------------------------------------------------------------------------------------
def _ops():
    OLD, NEW = b"A" * 2000, b"B" * 3000

    def s_file(f):
        f.mkdir("/d")
        f.create("/d/f")
        f.append("/d/f", OLD)

    def chk_append(f):
        c = f.read("/d/f")
        if c in (OLD, OLD + NEW):
            return None
        return "garbage" if STALE[:8] in c else "torn"

    def chk_create(f):
        if not f.exists("/d/g"):
            return None
        c = f.read("/d/g")
        return None if c in (b"", NEW) else ("garbage" if STALE[:8] in c else "torn")

    def chk_unlink(f):
        if not f.exists("/d/f"):
            return None
        return None if f.read("/d/f") == OLD else "torn"

    def chk_rename(f):
        a, b = f.exists("/d/f"), f.exists("/d/h")
        if a == b:
            return "lost" if not a else "both"
        c = f.read("/d/f" if a else "/d/h")
        return None if c == OLD else "torn"
    return {
        "append": (s_file, lambda f: f.append("/d/f", NEW), chk_append),
        "create": (s_file, lambda f: (f.create("/d/g"), f.append("/d/g", NEW)), chk_create),
        "unlink": (s_file, lambda f: f.unlink("/d/f"), chk_unlink),
        "rename": (s_file, lambda f: f.rename("/d/f", "/d/h"), chk_rename),
    }


def compute_crash() -> dict:
    from explainer.cs.store.fs import FS, Disk, crash_test, fsck_reads
    configs = [("none", {}), ("careful", {}), ("writeback", {}), ("ordered", {}), ("data", {}),
               ("ordered", {"barriers": False}), ("ordered", {"barriers": False, "jcsum": True})]
    rows = []
    for mode, extra in configs:
        tot = {"mode": mode, **extra, "states": 0, "ok": 0, "leak_only": 0, "corrupt": 0, "bad_data": 0, "writes": 0,
               "flushes": 0, "ops": {}}
        for name, (s, o, c) in _ops().items():
            r = crash_test(s, o, c, mode=mode, stale=STALE, **extra)
            for k in ("states", "ok", "leak_only", "corrupt", "bad_data", "writes", "flushes"):
                tot[k] += r[k]
            tot["ops"][name] = {k: r[k] for k in ("states", "ok", "leak_only", "corrupt", "bad_data", "writes",
                                                  "flushes")}
            tot["ops"][name]["problems"] = r["problems"]
            tot["ops"][name]["examples"] = r["examples"][:2]
        rows.append(tot)
    # fsck reads the whole of the metadata; a journal replay reads the journal
    scan = []
    rng = random.Random(5)
    for nb in (2048, 8192, 32768):
        d = Disk(nb)
        fs = FS.mkfs(d, ninodes=nb // 16, mode="none")
        used = 0
        k = 0
        while used < nb * 0.5:
            n = rng.choice([2_000, 20_000, 300_000])
            fs.create(f"/f{k}")
            fs.append(f"/f{k}", bytes(n))
            used += n // 1024 + 2
            k += 1
        scan.append({"blocks": nb, "files": k, "fsck_reads": fsck_reads(d), "journal_blocks": fs.sb["jlen"]})
    return {"rows": rows, "scan": scan}


def compute_journal() -> dict:
    from explainer.cs.store.fs import FS, Disk, JCOMMIT, JDESC, fsck
    import struct
    d = Disk(256)
    fs = FS.mkfs(d, ninodes=32, jlen=16, stale=STALE, mode="ordered")
    fs.create("/notes")
    fs.append("/notes", OLD1)
    base = d.copy()
    d.trace = []
    fs.append("/notes", NEW1)
    trace = d.trace
    d.trace = None
    sb = fs.sb
    steps = []
    homes = []
    for e in trace:
        if e[0] == "f":
            steps.append({"kind": "flush"})
            continue
        b, blk = e[1], e[2]
        if sb["journal"] <= b < sb["data"]:
            magic = struct.unpack_from("<I", blk, 0)[0]
            if b == sb["journal"] and magic == JDESC:
                cnt = struct.unpack_from("<I", blk, 8)[0]
                homes = list(struct.unpack_from(f"<{cnt}I", blk, 16))
                kind, what = "descriptor", ", ".join(_roles(fs, h) for h in homes)
            elif magic == JCOMMIT:
                kind, what = "commit", ""
            elif b == sb["journal"]:
                kind, what = "clear", ""
            else:
                kind, what = "copy", _roles(fs, homes[b - sb["journal"] - 1])
        else:
            kind = "data" if _roles(fs, b) == "data" else "checkpoint"
            what = _roles(fs, b)
        steps.append({"kind": kind, "block": b, "what": what})
    # crash after each write (in order), and recover
    after = []
    cur = base.copy()
    nwrite = 0
    for e in trace:
        if e[0] == "f":
            continue
        cur.b[e[1]] = e[2]
        nwrite += 1
        dsk = cur.copy()
        f2 = FS(dsk, mode="ordered")
        c = FS(dsk, mode="none", recover=False).read("/notes")
        after.append({"writes": nwrite, "recovery": f2.recovery, "fsck": len(fsck(dsk)),
                      "content": "old" if c == OLD1 else "new" if c == OLD1 + NEW1 else "other"})
    return {"steps": steps, "after": after}


def compute_apps() -> dict:
    from explainer.cs.store.fs import crash_test
    O, N = b"o" * 3000, b"n" * 3000

    def s(f):
        f.create("/cfg")
        f.append("/cfg", O)

    def chk(f):
        c = f.read("/cfg")
        if c in (O, N):
            return None
        if c == b"":
            return "empty"
        return "garbage" if STALE[:8] in c else "torn"

    def inplace(f):
        f.write("/cfg", 0, N)

    def tmp_rename(f):
        f.create("/cfg.tmp")
        f.append("/cfg.tmp", N)
        f.rename("/cfg.tmp", "/cfg")

    def tmp_fsync_rename(f):
        f.create("/cfg.tmp")
        f.append("/cfg.tmp", N)
        f.fsync("/cfg.tmp")
        f.rename("/cfg.tmp", "/cfg")
    rows = []
    for name, op in (("in place", inplace), ("write, rename", tmp_rename), ("write, fsync, rename", tmp_fsync_rename)):
        for delayed in (False, True):
            r = crash_test(s, op, chk, mode="ordered", delayed=delayed, stale=STALE)
            rows.append({"pattern": name, "delayed": delayed, "states": r["states"], "ok": r["ok"],
                         "bad": r["bad_data"], "kinds": sorted({e["data"] for e in r["examples"] if e["data"]}),
                         "corrupt": r["corrupt"]})
    return {"rows": rows}


# ---- LFS, COW, RAID, LSM ---------------------------------------------------------------------------------------
def compute_lfs() -> dict:
    from explainer.cs.store import lfs as L
    us = [0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.85]
    curves = {"greedy, uniform": [], "greedy, hot and cold": [], "cost-benefit, hot and cold": []}
    for u in us:
        curves["greedy, uniform"].append(L.simulate(u, "greedy", writes=20)["write_cost"])
        curves["greedy, hot and cold"].append(L.simulate(u, "greedy", hot=(0.9, 0.1), writes=20)["write_cost"])
        curves["cost-benefit, hot and cold"].append(L.simulate(u, "cost-benefit", hot=(0.9, 0.1),
                                                               writes=20)["write_cost"])
    hist = {}
    for pol in ("greedy", "cost-benefit"):
        r = L.simulate(0.75, pol, hot=(0.9, 0.1), writes=20)
        h = [0] * 20
        for x in r["cleaned_u"]:
            h[min(19, int(x * 20))] += 1
        hist[pol] = {"bins": h, "mean": r["mean_cleaned_u"], "n": len(r["cleaned_u"])}
    return {"u": us, "curves": curves, "formula": [L.formula(u) for u in us], "hist": hist, "segments": 200,
            "seg_blocks": 64}


def compute_cow() -> dict:
    from explainer.cs.store.cow import CowTree
    t = CowTree(4, 3)
    built = t.writes
    snap = t.snapshot("monday")
    per = [t.write(i, f"v{i}".encode()) for i in (5, 6, 40)]
    for i in range(10):
        t.write((i * 7) % 64, b"x")
    now, old = t.reachable(t.root), t.reachable(snap)
    leaf_addr = next(iter(now - old))
    t.corrupt(leaf_addr)
    found = t.verify()
    t.verify(repair=True)
    after = t.verify()
    depth = {d: d + 1 for d in (2, 3, 4, 5)}
    return {"fanout": 4, "depth": 3, "blocks": t.nblocks, "built": built, "per_write": per, "live": t.live_blocks(),
            "now": len(now), "snapshot": len(old), "shared": len(now & old), "found": len(found), "after": len(after),
            "depth_cost": depth}


def compute_raid() -> dict:
    from explainer.cs.store import raid as R
    rng = random.Random(6)
    lay = {lv: R.layout(lv, 4 if lv == 1 else 5, 5) for lv in (0, 1, 4, 5, 6)}
    D = [bytes(rng.randrange(256) for _ in range(256)) for _ in range(6)]
    P, Q = R.pq(D)
    pairs = 0
    for x in range(6):
        for y in range(x + 1, 6):
            L = list(D)
            L[x] = L[y] = None
            assert R.rebuild_two(L, P, Q) == D
            pairs += 1
    assert R.rebuild_one(D[:3] + D[4:] + [P]) == D[3]
    thr = {lv: R.throughput(lv, 8) for lv in (0, 1, 4, 5, 6)}
    risk = []
    for afr, label in ((0.0087, "datasheet"), (0.03, "field")):
        for ure in (1e-14, 1e-15):
            r = R.rebuild_risk(8, 16, afr, 100, ure)
            risk.append({"afr": afr, "label": label, "ure": ure, **r})
    hours = R.rebuild_hours(16, 100)
    mt = []
    for mttf, label in ((1e6, "datasheet"), (8766 / 0.03, "field, 3%")):
        mt.append({"label": label, "mttf": mttf, "raid5_years": R.mttdl(8, mttf, hours) / 8766,
                   "raid6_years": R.mttdl(8, mttf, hours, 2) / 8766})
    check = {"ratio": 300, "raid5": {"formula": R.mttdl(8, 300, 1), "exact": R.mttdl_exact(8, 300, 1),
                                     "simulated": R.simulate_mttdl(8, 300, 1, trials=4000)},
             "raid6": {"formula": R.mttdl(8, 300, 1, 2), "exact": R.mttdl_exact(8, 300, 1, 2),
                       "simulated": R.simulate_mttdl(8, 300, 1, 2, trials=1500)}}
    return {"layouts": {str(k): v for k, v in lay.items()}, "pairs": pairs,
            "small": {str(lv): R.small_write_ios(lv) for lv in (0, 1, 4, 5, 6)},
            "throughput": {str(k): v for k, v in thr.items()}, "risk": risk, "rebuild_hours": hours, "mttdl": mt,
            "check": check}


def compute_lsm() -> dict:
    from explainer.cs.store import lsm as L
    rows = []
    for pol in ("leveled", "tiered"):
        for bits in (0, 5, 10):
            r = L.workload(pol, n=200_000, keys=100_000, memtable=1000, ratio=10, bloom_bits=bits, lookups=4000)
            rows.append({k: v for k, v in r.items()})
    bt = [L.btree_write_amp(n=200_000, keys=100_000, cache_pages=c) for c in (32, 256, 1024, 2048)]
    # a small tree, flush by flush, for drawing
    grow = {}
    for pol in ("leveled", "tiered"):
        t = L.LSM(memtable=4, ratio=3, policy=pol, bloom_bits=0)
        rng = random.Random(1)
        shapes = []
        for i in range(4 * 30):
            t.put(rng.randrange(10_000), i)
            if t.mem == {}:
                shapes.append(t.shape())
        grow[pol] = {"shapes": shapes, "written": t.written, "inserted": t.inserted}
    return {"rows": rows, "btree": bt, "grow": grow, "n": 200_000, "keys": 100_000, "memtable": 1000, "ratio": 10}


def compute_kv() -> dict:
    """The key-value store keeps each run as a file on PebbleFS: 8-byte entries (key, value), sorted."""
    import struct
    from explainer.cs.store import lsm as L
    from explainer.cs.store.fs import fsck
    d, fs, books, names, PR = _novel_disk(4096)
    first = next(iter(names))
    text = PR.job_tape(books[first])
    words = PR.job_words(text)
    vocab = {}
    t = L.LSM(memtable=512, ratio=4, policy="leveled", bloom_bits=10)
    counts = {}
    for w in words:
        k = vocab.setdefault(w, len(vocab))
        counts[k] = counts.get(k, 0) + 1
        t.put(k, counts[k])
    t.flush()
    fs.mkdir("/kv")
    files = []
    for li, lv in enumerate(t.levels):
        for ri, run in enumerate(lv):
            name = f"/kv/L{li}-{ri}"
            fs.create(name)
            fs.append(name, b"".join(struct.pack("<II", k, v) for k, v in run.data.items()))
            files.append({"name": name, "entries": len(run.data), "bytes": 8 * len(run.data)})
    # read back: look up the top words through the files
    top = sorted(counts.items(), key=lambda kv: -kv[1])[:5]
    inv = {v: k for k, v in vocab.items()}
    back = []
    for k, c in top:
        got = None
        for f in files:                      # newest level first, as a lookup goes
            raw = fs.read(f["name"])
            for i in range(0, len(raw), 8):
                kk, vv = struct.unpack_from("<II", raw, i)
                if kk == k:
                    got = vv
                    break
            if got is not None:
                break
        back.append({"word": inv[k].decode(errors="replace"), "count": c, "read": got})
        assert got == c
    return {"book": names[first], "words": len(words), "distinct": len(vocab), "files": files, "top": back,
            "fsck": fsck(d), "write_amp": t.written / t.inserted, "flushes": sum(1 for e in t.log if e[0] == "flush")}


# ---- PebbleOS on its disk: ledger row 12 --------------------------------------------------------------------------
def compute_pebble() -> dict:
    from explainer.cs.algo import job2 as J
    from explainer.cs.os import fsos as F
    from explainer.cs.os import kernel as K
    from explainer.cs.pebble import programs as PR
    from explainer.cs.store import disk as D
    from explainer.cs.store.fs import FS, Disk, fsck
    from videos.cs.cs17.compute import _passages
    from videos.cs.cs31.compute import TOK, _full_text, _tokstream
    tapes = _passages(n=32, lo=200, hi=90000, seed=31)
    d = Disk(8192)
    fs = FS.mkfs(d, ninodes=64, mode="none")
    fs.mkdir("/p")
    for i, t in enumerate(tapes):
        fs.create(f"/p/{i:02d}")
        fs.append(f"/p/{i:02d}", t)
    samples = []
    for i, t in enumerate(tapes):
        tok = K.user("tok", TOK, 0, stdin="file", stdout="pipe")
        tok.fino = fs.lookup(f"/p/{i:02d}")
        job = K.user("job", J.JOB_HASH, 1, stdin="pipe")
        m = F.boot_fs([tok, job], d)
        m.run(2_000_000_000)
        assert bytes(m.output) == PR.job_reference(t)
        io = [b for _, b in m.io]
        assert io == F.predict_reads(fs, inum=tok.fino)
        a = K.attribute(m)
        f = J.features(t)
        ts = _tokstream(t)
        samples.append({"bytes": len(t), "tok": a["user"]["tok"], "job": a["user"]["job"], "kernel": a["kernel"],
                        "traps": a["traps"], "reads": len(io), "out": len(ts),
                        "ftok": {k: f[k] for k in ("bytes", "letters", "capitals", "words")}, "fjob": J.features(ts)})
    held = [i for i in range(len(samples)) if i % 4 == 2]
    train = [s for i, s in enumerate(samples) if i not in held]

    def fit(key, feat):
        mdl = J.fit([(feat(s), s[key]) for s in train])
        err = max(abs(J.predict(mdl, feat(samples[i])) - samples[i][key]) / samples[i][key] for i in held)
        return mdl, err
    m_tok, e_tok = fit("tok", lambda s: s["ftok"])
    m_job, e_job = fit("job", lambda s: s["fjob"])
    m_ker, e_ker = fit("kernel", lambda s: {"bytes": s["bytes"], "out": s["out"]})
    m_trp, e_trp = fit("traps", lambda s: {"bytes": s["bytes"], "out": s["out"]})
    full = _full_text()
    ff, out = J.features_native(full)
    ts = _tokstream(full)
    fj, _ = J.features_native(ts)
    ins = {"tok": J.predict(m_tok, {k: ff[k] for k in ("bytes", "letters", "capitals", "words")}),
           "job": J.predict(m_job, fj), "kernel": J.predict(m_ker, {"bytes": len(full), "out": len(ts)})}
    traps = J.predict(m_trp, {"bytes": len(full), "out": len(ts)})
    # the thirty novels as files, laid out by our allocator, and on an aged disk
    from videos.cs.cs6.compute import novels
    import videos.ai.ai1.compute as A
    books = novels()
    lay = {}
    for alloc in ("next", "random"):
        dd = Disk(28 * 1024)
        f2 = FS.mkfs(dd, ninodes=64, mode="none", alloc=alloc, seed=7)
        f2.mkdir("/novels")
        total = 0
        reads = [0]
        sizes = []
        for n, title in A.BOOKS.items():
            t = PR.job_tape(books[n])
            f2.create(f"/novels/{slug(title)}")
            f2.append(f"/novels/{slug(title)}", t)
            total += len(t)
            sizes.append({"name": slug(title), "title": title, "bytes": len(t)})
        tagless = []
        for title in A.BOOKS.values():
            tagless += F.predict_reads(f2, f"/novels/{slug(title)}", boot=False)
        reads += tagless
        h, s = D.HDD().trace_time(reads), D.SSD.trace_time(reads)
        lay[alloc] = {"bytes": total, "reads": len(reads), "hdd_s": h["ms"] / 1e3, "hdd_jumps": h["jumps"],
                      "ssd_s": s["ms"] / 1e3, "fsck": len(fsck(dd)), "sizes": sizes}
    led = json.loads((Cache("cs31").dir / "ledger.json").read_text())
    led = [r for r in led if r["part"] != 34]
    row11 = next(r for r in led if r["part"] == 31)
    total_ins = sum(ins.values())
    trap_cycles = 35
    cycles = total_ins / row11["ipc"] + 2 * traps * trap_cycles + (row11["cycles"] - row11["instructions"] /
                                                                     row11["ipc"] - 2 * row11["traps"] * trap_cycles)
    cpu_s = cycles / (row11["clock_mhz"] * 1e6)
    disk_s = lay["next"]["hdd_s"]
    led.append({"part": 34, "label": r"from our file system, \ on a disk", "seconds": cpu_s + disk_s,
                "cpu_seconds": cpu_s, "disk_seconds": disk_s, "ssd_seconds": lay["next"]["ssd_s"],
                "aged_disk_seconds": lay["random"]["hdd_s"], "cycles": cycles, "clock_mhz": row11["clock_mhz"],
                "instructions": total_ins, "ipc": row11["ipc"], "kernel_instructions": ins["kernel"], "traps": traps})
    CACHE.dir.mkdir(parents=True, exist_ok=True)
    (CACHE.dir / "ledger.json").write_text(json.dumps(led, indent=1))
    return {"samples": samples, "errors": {"tok": e_tok, "job": e_job, "kernel": e_ker, "traps": e_trp},
            "n_train": len(train), "n_held": len(held), "bytes": len(full), "instructions": ins, "total": total_ins,
            "traps": traps, "cpu_seconds": cpu_s, "layouts": lay, "ledger": led, "row11": row11,
            "kernel_fs_instructions": F.fs_instructions(),
            "per_byte": {k: v / len(full) for k, v in ins.items()},
            "row11_kernel_per_byte": row11["kernel_instructions"] / len(full)}


# ---- frontier --------------------------------------------------------------------------------------------------
def compute_frontier() -> dict:
    from explainer.cs.store import flash as F
    from explainer.cs.store.fs import crash_test
    c = math.log(2) ** 2
    T, L = 10, 5
    N = [T ** i for i in range(1, L + 1)]
    tot = sum(N)

    def monkey(bits):
        B = bits * tot

        def spend(lam):        # p_i = min(1, lam * N_i); bits_i = -ln p_i / c
            return sum(max(0.0, -math.log(min(1.0, lam * n))) / c * n for n in N)
        lo, hi = 1e-30, 1.0
        for _ in range(200):
            mid = math.sqrt(lo * hi)
            if spend(mid) > B:
                lo = mid
            else:
                hi = mid
        return sum(min(1.0, hi * n) for n in N)
    rows = []
    for bits in (1, 2, 3, 4, 5, 6, 8, 10):
        rows.append({"bits": bits, "uniform": L * math.exp(-bits * c), "monkey": monkey(bits)})
    # crash states grow as 2^k in the writes between flushes
    grow = []
    for nblk in (1, 2, 4, 8):
        OLD, NEW = b"A" * 1024, b"B" * (1024 * nblk)

        def s(f):
            f.create("/f")
            f.append("/f", OLD)
        r = crash_test(s, lambda f: f.append("/f", NEW), None, mode="none", nblocks=1024, ninodes=32, jlen=16)
        grow.append({"blocks": nblk, "writes": r["writes"], "states": r["states"]})
    zns = {"random": F.ftl(op=0.07, writes=6)["wa"], "sequential": F.ftl(op=0.07, writes=6, pattern="sequential")["wa"]}
    return {"monkey": rows, "levels": L, "ratio": T, "grow": grow, "zns": zns}


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
