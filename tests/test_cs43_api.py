import unittest

from explainer.cs.api import delivery, services, wire


class Wire(unittest.TestCase):
    def test_published_examples(self):
        r = wire.check_published()
        self.assertTrue(all(ok for *_, ok in r["encodings"]))
        self.assertTrue(all(ok for *_, ok in r["zigzag"]))

    def test_roundtrip(self):
        for n in (0, 1, 127, 128, 300, 2 ** 35, 2 ** 63):
            self.assertEqual(wire.read_varint(wire.varint(n))[0], n)
        for n in (-5, -1, 0, 7, -2 ** 31):
            self.assertEqual(wire.unzigzag(wire.zigzag(n)), n)
        self.assertEqual(wire.decode(bytes.fromhex("089601")), [(1, 0, 150)])

    def test_evolution(self):
        cases = {c["change"]: c for c in wire.evolution_cases()}
        self.assertTrue(cases["add an optional field"]["backward"] and cases["add an optional field"]["forward"])
        self.assertFalse(cases["add a required field"]["backward"])
        self.assertFalse(cases["change a field's type"]["forward"])


class Delivery(unittest.TestCase):
    def test_semantics(self):
        r = delivery.semantics(2000)["policies"]
        self.assertLess(r["at most once"]["error"], 0)
        self.assertGreater(r["at least once"]["error"], 0)
        self.assertEqual(r["exactly once"]["error"], 0)

    def test_job(self):
        text = "the whale the sea the ship a whale " * 400
        self.assertEqual(delivery.job_services(text, chunk=50)["wrong_counts"], 0)
        self.assertGreater(delivery.job_services(text, chunk=50, dup=0.2, dedup=False)["overcount"], 0)

    def test_pagination(self):
        r = delivery.pagination(500, 25, 2)
        self.assertEqual(r["cursor"]["duplicates"], 0)
        self.assertGreater(r["offset"]["duplicates"], 0)


class Services(unittest.TestCase):
    def test_outbox(self):
        m = services.dual_write(5000, 0.02)["modes"]
        self.assertGreater(m["commit then publish"]["lost_events"], 0)
        self.assertEqual(m["outbox"]["lost_events"], 0)

    def test_saga(self):
        self.assertEqual(services.saga_experiment(3000)["inconsistent"], 0)

    def test_jwt(self):
        rows = {r["token"]: r for r in services.jwt_demo()["rows"]}
        self.assertIsNotNone(rows["alg: none"]["naive"])
        self.assertIsNone(rows["alg: none"]["pinned"])
        self.assertIsNone(rows["payload edited"]["pinned"])


if __name__ == "__main__":
    unittest.main()
