"""Part 35's instruments: relational algebra and FDs, the SQL engine against sqlite3, joins, B+ trees,
serializability, isolation levels, and ARIES."""
from __future__ import annotations

import random
import sqlite3
import unittest

from explainer.cs.db import aries, joins, txn
from explainer.cs.db import rel as R
from explainer.cs.db.bptree import BPlusTree, levels_for
from explainer.cs.db.engine import Database, count_plans


def _db(seed=1):
    rng = random.Random(seed)
    books = [(i, f"book{i}", 1800 + (i * 7) % 120) for i in range(20)]
    vocab = ["the", "whale", "sea", "ship", "love"] + [f"w{i}" for i in range(200)]
    words = [(b, p, rng.choice(vocab[:5]) if rng.random() < 0.5 else rng.choice(vocab))
             for b in range(20) for p in range(300)]
    db = Database(page_rows=50, buffer_pages=20)
    db.create("books", ["book_id", "title", "year"], books)
    db.create("words", ["book_id", "pos", "word"], words)
    db.index("words", "word")
    con = sqlite3.connect(":memory:")
    con.execute("create table books(book_id, title, year)")
    con.execute("create table words(book_id, pos, word)")
    con.executemany("insert into books values (?,?,?)", books)
    con.executemany("insert into words values (?,?,?)", words)
    return db, con


class TestAlgebra(unittest.TestCase):
    def test_operators(self):
        A = R.table(["a", "b"], [(1, "x"), (2, "y"), (3, "x")])
        B = R.table(["b", "c"], [("x", 10), ("y", 20)])
        J = R.join(A, B)
        self.assertEqual(sorted(J.rows), [(1, "x", 10), (2, "y", 20), (3, "x", 10)])
        self.assertEqual(R.pi(A, ["b"]).rows, [("x",), ("y",)])
        self.assertEqual(len(R.sigma(A, lambda r: r["a"] > 1)), 2)
        self.assertEqual(sorted(R.group(A, ["b"], [("n", "count", None)]).rows), [("x", 2), ("y", 1)])
        self.assertEqual(len(R.minus(A, R.table(["a", "b"], [(1, "x")]))), 2)

    def test_fds(self):
        fds = [R.fd("A", "B"), R.fd("B", "C"), R.fd("CD", "E")]
        self.assertEqual(R.keys("ABCDE", fds), [frozenset("AD")])
        self.assertFalse(R.is_bcnf("ABCDE", fds))
        parts = R.bcnf_decompose("ABCDE", fds)
        self.assertTrue(all(R.is_bcnf(p, fds) for p in parts))
        self.assertTrue(R.lossless("ABCDE", parts, fds))
        three = R.synthesize_3nf("ABCDE", fds)
        self.assertTrue(R.lossless("ABCDE", three, fds))
        self.assertFalse(R.lossless("ABC", [frozenset("AB"), frozenset("AC")], [R.fd("B", "C")]))


class TestEngine(unittest.TestCase):
    def test_against_sqlite(self):
        db, con = _db()
        for sql in ["SELECT word, COUNT(*) FROM words GROUP BY word ORDER BY 2 DESC LIMIT 5",
                    "SELECT title, COUNT(*) FROM words JOIN books ON words.book_id = books.book_id "
                    "WHERE word = 'whale' GROUP BY title ORDER BY 2 DESC LIMIT 3",
                    "SELECT title, year FROM books WHERE year < 1850 ORDER BY year"]:
            ours = db.query(sql)
            ref = con.execute(sql).fetchall()
            self.assertEqual([r[-1] for r in ours], [r[-1] for r in ref], sql)
        for force in ({"join": "hash"}, {"join": "nested loops"}, {"join": "sort-merge"}, {"agg": "sort"}):
            sql = "SELECT title, COUNT(*) FROM words JOIN books ON words.book_id = books.book_id GROUP BY title"
            ours = sorted(db.run(db.plan(sql, force=force)))
            self.assertEqual(ours, sorted(con.execute(sql).fetchall()), force)

    def test_plan_counts(self):
        self.assertEqual(count_plans(4), {"n": 4, "left_deep": 24, "bushy": 120, "subsets": 16})


class TestJoinsAndTrees(unittest.TestCase):
    def test_join_io(self):
        r = joins.compare(n_r=4000, n_s=2000, page_rows=50, B=20, keys=1000)
        self.assertEqual(r["measured"]["block nested loops"], r["formula"]["block nested loops"])
        self.assertEqual(r["measured"]["sort-merge"], r["formula"]["sort-merge"])

    def test_bptree(self):
        t = BPlusTree(order=5)
        ks = list(range(500))
        random.Random(3).shuffle(ks)
        for k in ks:
            t.insert(k, -k)
        t.check()
        self.assertEqual(t.search(123), -123)
        self.assertEqual([k for k, _ in t.range(10, 15)], list(range(10, 16)))
        self.assertEqual(levels_for(10 ** 9, 400), 4)


class TestTransactions(unittest.TestCase):
    def test_serializability(self):
        s = [(1, "r", "A"), (2, "w", "A"), (1, "w", "A"), (3, "w", "A"), (1, "c", None), (2, "c", None),
             (3, "c", None)]
        self.assertFalse(txn.conflict_serializable(s)[0])
        self.assertTrue(txn.view_serializable(s)[0])          # blind writes
        ok, order = txn.conflict_serializable([(1, "r", "A"), (1, "w", "A"), (2, "r", "A"), (2, "w", "A")])
        self.assertTrue(ok)
        self.assertEqual(order, [1, 2])

    def test_2pl_is_serializable(self):
        rng = random.Random(5)
        for _ in range(60):
            ts = {t: [(rng.choice("rw"), rng.choice("ABC")) for _ in range(3)] for t in (1, 2, 3)}
            order = [rng.choice((1, 2, 3)) for _ in range(30)]
            r = txn.run_2pl(ts, order)
            self.assertTrue(txn.conflict_serializable(r["schedule"])[0])

    def test_isolation_table(self):
        t = txn.anomaly_table()
        self.assertEqual(t["read committed"]["dirty read"], "prevented")
        self.assertEqual(t["read committed"]["lost update"], "allowed")
        self.assertEqual(t["repeatable read"]["phantom"], "allowed")
        self.assertEqual(t["snapshot"]["write skew"], "allowed")
        self.assertEqual(t["snapshot + SSI"]["write skew"], "prevented")
        self.assertTrue(all(v == "prevented" for v in t["serializable"].values()))


class TestAries(unittest.TestCase):
    def test_recovery(self):
        for seed in range(120):
            self.assertTrue(aries.crash_and_recover(seed)["ok"], seed)
            self.assertTrue(aries.crash_and_recover(seed, crash_in_undo=True)["ok"], seed)


if __name__ == "__main__":
    unittest.main()
