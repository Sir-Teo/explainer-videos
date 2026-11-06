"""Part 36's network instruments: each against a formula, a reference or an invariant."""
from __future__ import annotations

import math
import random
import unittest
import zlib

import numpy as np

from explainer.cs.net import bgp, bridge, dataplane, ip, link, mac, phy, routing, wireless
from explainer.cs.net.sim import Internet


class Phy(unittest.TestCase):
    def test_qam_matches_formula(self):
        rng = np.random.default_rng(0)
        for M, snr in ((16, 14), (64, 22)):
            s = phy.qam_simulate(M, snr, 200_000, rng)
            self.assertAlmostEqual(s["ser"] / phy.qam_ser(M, snr), 1, delta=0.1)

    def test_shannon_gap(self):
        for M in (4, 16, 64, 256):
            gap = phy.snr_needed(M, 1e-6) - phy.db(phy.shannon_snr(math.log2(M)))
            self.assertTrue(7.5 < gap < 10, gap)


class Link(unittest.TestCase):
    def test_stuffing_roundtrip_and_no_flag(self):
        r = random.Random(1)
        for _ in range(200):
            b = [r.randrange(2) for _ in range(r.randrange(1, 300))]
            s = link.stuff(b)
            self.assertNotIn("111111", "".join(map(str, s)))
            self.assertEqual(link.unstuff(s), b)
            self.assertEqual(link.deframe(link.frame(b)), [b])

    def test_fcs_is_zlib_crc32(self):
        fr = link.ethernet("ff:ff:ff:ff:ff:ff", "02:00:00:00:00:01", 0x0800, b"call me ishmael")
        self.assertEqual(int.from_bytes(fr[-4:], "little"), zlib.crc32(fr[:-4]))
        self.assertTrue(link.fcs_ok(fr))

    def test_crc_catches_short_bursts(self):
        r = random.Random(2)
        for k in ("single", "double", "burst"):
            self.assertEqual(link.crc_trial(k, 3000, r)["missed"], 0)


class Mac(unittest.TestCase):
    def test_aloha_formulas(self):
        r = random.Random(3)
        self.assertAlmostEqual(mac.aloha(0.5, 60_000, r)["S"], 1 / (2 * math.e), delta=0.006)
        self.assertAlmostEqual(mac.slotted_aloha(1.0, 60_000, r)["S"], 1 / math.e, delta=0.006)

    def test_p_persistent_matches_metcalfe_boggs(self):
        r = random.Random(4)
        for n, a in ((5, 0.1), (50, 0.05)):
            x = mac.csma_cd(n, a, 30_000, r, policy="p")
            self.assertAlmostEqual(x["efficiency"], mac.metcalfe_boggs(n, a), delta=0.01)


class Bridges(unittest.TestCase):
    def test_storm_and_tree(self):
        topo = bridge.lan([(1, 2), (2, 3), (3, 1), (3, 4), (4, 2)], {"a": 1, "b": 4, "c": 3})
        storm = bridge.flood(topo, 1, limit=30)
        self.assertFalse(storm["ended"])
        st = bridge.spanning_tree(topo)
        f = bridge.flood(topo, 1, active=st["active"])
        self.assertTrue(f["ended"])
        self.assertEqual(f["delivered"], {"a": 1, "b": 1, "c": 1})
        active_links = sum(1 for b in topo for p, (k, _, _) in topo[b].items() if k == "bridge" and p in st["active"][b])
        self.assertEqual(active_links, 2 * (len(topo) - 1))          # a tree


class Ip(unittest.TestCase):
    def test_three_lpms_agree(self):
        r = random.Random(5)
        rows = ip.routing_table(5000, r)
        tabs = [ip.LinearTable(), ip.BinaryTrie(), ip.MultibitTrie(8), ip.MultibitTrie(4)]
        for p, h in rows:
            for t in tabs:
                t.insert(p, h)
        for _ in range(400):
            a = r.getrandbits(32)
            ans = {t.lookup(a) for t in tabs}
            self.assertEqual(len(ans), 1)

    def test_aggregate_and_fragment(self):
        P = ip.Prefix.parse
        ag = ip.aggregate([(P("10.0.0.0/24"), 1), (P("10.0.1.0/24"), 1), (P("10.0.2.0/23"), 1)])
        self.assertEqual([(repr(p), h) for p, h in ag], [("10.0.0.0/22", 1)])
        fr = ip.fragment(4000, 1500)
        self.assertEqual(sum(n for _, n, _ in fr), 4000)
        self.assertEqual([o for o, _, _ in fr], [0, 185, 370])


class Routing(unittest.TestCase):
    def test_count_to_infinity_and_fixes(self):
        net = {"A": {"B": 1}, "B": {"A": 1, "C": 1}, "C": {"B": 1}}
        plain = routing.dv_fail(net, "B", "C")["after"]
        self.assertGreater(plain["converged"], 10)
        self.assertEqual(plain["table"]["A"]["C"][0], 16)
        for mode in ("split", "poison"):
            self.assertLessEqual(routing.dv_fail(net, "B", "C", mode=mode)["after"]["converged"], 2)
        tri = {"A": {"B": 1, "C": 1}, "B": {"A": 1, "C": 1}, "C": {"A": 1, "B": 1, "D": 1}, "D": {"C": 1}}
        self.assertGreater(routing.dv_fail(tri, "C", "D", mode="split")["after"]["converged"], 10)

    def test_dv_equals_dijkstra(self):
        r = random.Random(6)
        nodes = list(range(12))
        net = {x: {} for x in nodes}
        for x in nodes:
            for y in r.sample(nodes, 3):
                if x != y:
                    c = r.randint(1, 5)
                    net[x][y] = net[y][x] = c
        dv = routing.dv_run(net, infinity=10 ** 6)["table"]
        for x in nodes:
            sp = routing.spf(net, x)
            for y in nodes:
                self.assertEqual(dv[x][y][0], sp[y][0])


class Bgp(unittest.TestCase):
    def test_valley_free_and_hijack(self):
        r = random.Random(8)
        rel, T = bgp.tiered(r)
        v, att = T["stubs"][0], T["stubs"][57]
        P22, P24 = ip.Prefix.parse("208.65.152.0/22"), ip.Prefix.parse("208.65.153.0/24")
        res = bgp.propagate(rel, [(v, P22)])
        for a, table in res["routes"].items():
            path = table[P22]
            kinds = [rel[path[i]][path[i + 1]] for i in range(len(path) - 1)]
            # valley-free: some provider hops (towards the origin, i.e. "the next AS is my provider"), at most one
            # peer, then customer hops
            seq = "".join({"provider": "u", "peer": "p", "customer": "d"}[k] for k in kinds)
            self.assertRegex(seq, r"^u*p?d*$")
        rc = bgp.reach(bgp.propagate(rel, [(v, P22), (att, P24)])["routes"], ip.ip("208.65.153.10"))
        self.assertEqual(sum(1 for x in rc.values() if x == att), len(rel))
        rov = set(rel)
        rc = bgp.reach(bgp.propagate(rel, [(v, P22), (att, P24)], rov=rov, roa={P22: (v, 22)})["routes"],
                       ip.ip("208.65.153.10"))
        self.assertEqual(sum(1 for x in rc.values() if x == att), 1)

    def test_gadgets(self):
        self.assertFalse(bgp.spp(bgp.BAD_GADGET)["stable"])
        self.assertTrue(bgp.spp(bgp.GOOD_GADGET)["stable"])


class Sim(unittest.TestCase):
    def test_ping_traceroute(self):
        n = Internet(1)
        for x in ("a", "b", "c"):
            n.router(x)
        n.link("a", "b", 1000, 1000)
        n.link("b", "c", 1000, 1000)
        n.host("h1", "10.1.0.2/24", "a")
        n.host("h2", "10.2.0.2/24", "c")
        n.converge()
        rtt = n.ping("h1", "h2")[0]["rtt"]
        self.assertAlmostEqual(rtt, 4 * 1000e3 / phy.C_FIBRE, delta=1e-4)
        hops = [h["by"] for h in n.traceroute("h1", "h2")]
        self.assertEqual(hops, ["a", "b", "c", "h2"])


class Frontier(unittest.TestCase):
    def test_verifier_and_wireless(self):
        P = ip.Prefix.parse
        fib = {"a": [(P("10.0.0.0/8"), "b")], "b": [(P("10.0.0.0/8"), "a"), (P("10.1.0.0/16"), "c")],
               "c": [(P("10.1.0.0/16"), "h")]}
        v = dataplane.verify(fib, {P("10.1.0.0/16"): "c", P("10.2.0.0/16"): "d"})
        self.assertEqual(len(v["loops"]), 1)
        rng = np.random.default_rng(0)
        c = [wireless.mimo_capacity(n, n, 20, 200, rng) for n in (1, 4)]
        self.assertGreater(c[1] / c[0], 3.3)


if __name__ == "__main__":
    unittest.main()
