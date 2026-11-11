"""Part 34's instruments: the file system and its crash checker, PebbleOS's disk, flash, LFS, RAID, LSM, COW."""
from __future__ import annotations

import random
import unittest
from fractions import Fraction

from explainer.cs.store import cow, disk, flash, lfs, lsm, raid
from explainer.cs.store.fs import FS, MAXFILE, Disk, FSError, crash_test, fsck

OLD, NEW = b"A" * 2000, b"B" * 3000


def _setup(f):
    f.create("/f")
    f.append("/f", OLD)


def _append(f):
    f.append("/f", NEW)


def _check(f):
    c = f.read("/f")
    if c in (OLD, OLD + NEW):
        return None
    return "garbage" if b"SECRET" in c else "torn"


class TestFS(unittest.TestCase):
    def test_operations(self):
        d = Disk(2048)
        fs = FS.mkfs(d, ninodes=128, mode="ordered")
        fs.mkdir("/a")
        fs.create("/a/x")
        rng = random.Random(0)
        big = bytes(rng.randrange(256) for _ in range(300_000))   # through the double-indirect block
        fs.append("/a/x", big)
        self.assertEqual(fs.read("/a/x"), big)
        fs.link("/a/x", "/y")
        self.assertEqual(fs.iget(fs.lookup("/y"))["nlink"], 2)
        fs.unlink("/a/x")
        self.assertEqual(fs.read("/y"), big)
        fs.create("/t")
        fs.append("/t", b"new")
        fs.rename("/t", "/y")
        self.assertEqual(fs.read("/y"), b"new")
        self.assertEqual(fsck(d), [])
        self.assertEqual(sorted(fs.listdir("/")), ["a", "y"])
        self.assertRaises(FSError, fs.lookup, "/a/x")
        self.assertEqual(MAXFILE, (10 + 256 + 65536) * 1024)

    def test_fsck_finds_and_repairs(self):
        d = Disk(512)
        fs = FS.mkfs(d, ninodes=64, mode="none")
        _setup(fs)
        ino = fs.iget(fs.lookup("/f"))
        # clear the data bitmap behind the file's back: its blocks look free
        sb = fs.sb
        d.write(sb["dbmap"], bytes(1024))
        kinds = {k for k, _ in fsck(d)}
        self.assertIn("free block in use", kinds)
        fsck(d, repair=True)
        self.assertEqual(fsck(d), [])
        self.assertEqual(FS(d, mode="none").read("/f"), OLD)
        self.assertTrue(ino["direct"][0])

    def test_crash_modes(self):
        r = {m: crash_test(_setup, _append, _check, mode=m) for m in ("none", "careful", "writeback", "ordered", "data")}
        self.assertGreater(r["none"]["corrupt"], 0)
        self.assertGreater(r["none"]["bad_data"], 0)
        self.assertEqual(r["careful"]["corrupt"], 0)               # only leaks
        self.assertEqual(r["writeback"]["corrupt"], 0)
        self.assertGreater(r["writeback"]["bad_data"], 0)          # garbage after a crash
        for m in ("ordered", "data"):
            self.assertEqual(r[m]["ok"], r[m]["states"], m)
        nb = crash_test(_setup, _append, _check, mode="ordered", barriers=False)
        self.assertGreater(nb["corrupt"] + nb["bad_data"], 0)      # the commit can land before the copies
        cs = crash_test(_setup, _append, _check, mode="ordered", barriers=False, jcsum=True)
        self.assertEqual(cs["ok"], cs["states"])

    def test_rename_needs_fsync_under_delayed_allocation(self):
        O, N = b"o" * 3000, b"n" * 3000

        def s(f):
            f.create("/cfg")
            f.append("/cfg", O)

        def chk(f):
            return None if f.read("/cfg") in (O, N) else "bad"

        def no_fsync(f):
            f.create("/tmp")
            f.append("/tmp", N)
            f.rename("/tmp", "/cfg")

        def with_fsync(f):
            f.create("/tmp")
            f.append("/tmp", N)
            f.fsync("/tmp")
            f.rename("/tmp", "/cfg")
        self.assertGreater(crash_test(s, no_fsync, chk, mode="ordered", delayed=True)["bad_data"], 0)
        r = crash_test(s, with_fsync, chk, mode="ordered", delayed=True)
        self.assertEqual(r["ok"], r["states"])


class TestPebbleOSDisk(unittest.TestCase):
    def test_open_and_read(self):
        from explainer.cs.os import fsos as F
        from explainer.cs.os import kernel as K
        d = Disk(1024)
        fs = FS.mkfs(d, ninodes=64, mode="none")
        fs.mkdir("/novels")
        rng = random.Random(1)
        text = bytes(rng.randrange(32, 127) for _ in range(20_000))
        fs.create("/novels/emma")
        fs.append("/novels/emma", text)
        path = "/novels/emma"
        cat = f"""
main:   li   a0, 0
        la   a1, path
        li   a2, {len(path)}
        li   a5, 5
        ecall
        li   t3, 3
        bne  a0, t3, fail
loop:   li   a0, 3
        la   a1, buf
        li   a2, 500
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
fail:   li   a5, 0
        li   a0, 9
        ecall
path:   .ascii "{path}"
        .align 4
buf:    .space 512
"""
        m = F.boot_fs([K.user_asm("cat", cat, 0)], d)
        m.run(50_000_000)
        self.assertEqual(bytes(m.output), text)
        self.assertEqual(K.pcbs(m)[0]["exit"], 0)
        self.assertEqual([b for _, b in m.io], F.predict_reads(fs, path))
        bad = cat.replace(f'"{path}"', '"/novels/zzzz"')
        m = F.boot_fs([K.user_asm("cat", bad, 0)], d)
        m.run(5_000_000)
        self.assertEqual(K.pcbs(m)[0]["exit"], 9)


class TestDevices(unittest.TestCase):
    def test_disk_model(self):
        h = disk.HDD()
        self.assertAlmostEqual(h.avg_seek(), 0.5 + 15.5 * 8 / 15)
        self.assertGreater(h.mb_s / (4096 / h.random_io(4096) / 1e3), 300)   # sequential beats random 4 KiB 300x
        q = [98, 183, 37, 122, 14, 124, 65, 67]
        self.assertEqual(disk.distance(53, disk.order("fcfs", 53, q)), 640)
        self.assertEqual(disk.distance(53, disk.order("sstf", 53, q)), 236)

    def test_flash(self):
        r = flash.ftl(blocks=64, op=0.28, writes=3)
        self.assertGreater(r["wa"], 1.5)
        self.assertLess(abs(r["wa"] - flash.wa_greedy_estimate(0.28)) / r["wa"], 0.15)
        self.assertLess(flash.ftl(blocks=64, op=0.28, writes=3, trim=0.3)["wa"], r["wa"])

    def test_lfs(self):
        g = lfs.simulate(0.75, "greedy", hot=(0.9, 0.1), segments=200, writes=4)
        c = lfs.simulate(0.75, "cost-benefit", hot=(0.9, 0.1), segments=200, writes=4)
        self.assertLess(c["write_cost"], g["write_cost"])
        self.assertTrue(all(0 <= u <= 1 for u in c["final_u"]))

    def test_raid(self):
        self.assertEqual(raid.layout(1, 4, 2), [["D0", "M0", "D1", "M1"], ["D2", "M2", "D3", "M3"]])
        with self.assertRaises(ValueError):
            raid.layout(1, 3, 1)
        rng = random.Random(2)
        D = [bytes(rng.randrange(256) for _ in range(32)) for _ in range(5)]
        P, Q = raid.pq(D)
        self.assertEqual(raid.rebuild_one([D[0], D[1], D[3], D[4], P]), D[2])
        for x in range(5):
            for y in range(x + 1, 5):
                L = list(D)
                L[x] = L[y] = None
                self.assertEqual(raid.rebuild_two(L, P, Q), D)
        ex = raid.mttdl_exact(8, 300, 1)
        self.assertLess(abs(raid.simulate_mttdl(8, 300, 1, trials=1500) - ex) / ex, 0.1)

    def test_rare_failure_reliability(self):
        # Closed-form backward-equation solutions, evaluated as exact rationals.
        for lifetime in (300, 10**12):
            a, b, c = (Fraction(k, lifetime) for k in (8, 7, 6))
            expected5 = 1 / a + 1 / b + 1 / (a * b)
            expected6 = expected5 + 1 / c + 1 / (b * c) + 1 / (a * b * c)
            for parity, expected in ((1, expected5), (2, expected6)):
                self.assertAlmostEqual(raid.mttdl_exact(8, lifetime, 1, parity) / float(expected), 1)
        for fn in (raid.mttdl, raid.mttdl_exact, raid.simulate_mttdl):
            for args in ((2, 300, 1, 2), (8, 0, 1, 1), (8, 300, -1, 1), (8, 300, 1, 3)):
                with self.assertRaises(ValueError):
                    fn(*args)

    def test_small_rebuild_probabilities(self):
        r = raid.rebuild_risk(2, 1e-12, 1e-20, ure=1e-30)
        self.assertGreater(r["p_second_failure"], 0)
        self.assertAlmostEqual(r["p_ure"] / 8e-30, 1)
        self.assertGreaterEqual(r["p_loss"], r["p_ure"])
        self.assertEqual(raid.rebuild_risk(2, 0, 0)["p_loss"], 0)
        for kwargs in ({"afr": 1}, {"tb": -1}, {"rebuild_mb_s": 0}, {"ure": -1}):
            with self.assertRaises(ValueError):
                raid.rebuild_risk(**({"n": 8, "tb": 16, "afr": .03} | kwargs))

    def test_lsm(self):
        lv = lsm.workload("leveled", n=20_000, keys=10_000, memtable=200, lookups=500)
        ti = lsm.workload("tiered", n=20_000, keys=10_000, memtable=200, lookups=500)
        self.assertLess(ti["write_amp"], lv["write_amp"])
        self.assertLess(lv["runs"], ti["runs"])
        t = lsm.LSM(memtable=50, ratio=4)
        for i in range(2000):
            t.put(i % 700, i)
        self.assertEqual(t.get(5), 1405)

    def test_cow(self):
        t = cow.CowTree(4, 3)
        s = t.snapshot()
        self.assertEqual(t.write(5, b"x"), 4)
        self.assertEqual(t.read(5, s), bytes(64))
        leaf = t.read(5)
        self.assertEqual(leaf[:1], b"x")
        a = next(iter(t.reachable(t.root) - t.reachable(s)))
        t.corrupt(a)
        self.assertEqual(t.verify(), [a])
        t.verify(repair=True)
        self.assertEqual(t.verify(), [])


if __name__ == "__main__":
    unittest.main()
