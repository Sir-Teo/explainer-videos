"""Part 55's security instruments (memory corruption and safety, authentication, access control).  Every computed
result is checked against an independent computation: the emulator's actual behaviour, the RFC test vectors, a direct
harmonic sum, the lattice rules, or a hand-traced leak."""
from __future__ import annotations

import math
import unittest

from explainer.cs.trust import access as AC
from explainer.cs.trust import auth as AU
from explainer.cs.trust import memory as MM


# ======================================================================================================================
# memory.py
# ======================================================================================================================

class DefenceMatrix(unittest.TestCase):
    def test_outcomes_match_the_emulator(self):
        cells = {(c["canary"], c["nx"], c["aslr"]): c for c in MM.defense_matrix()}
        self.assertEqual(cells[(False, False, False)]["outcome"], "pwned")
        self.assertEqual(cells[(False, True, False)]["outcome"], "fault")      # NX blocks the jump into the stack
        self.assertEqual(cells[(True, False, False)]["outcome"], "detected")   # the canary catches the overwrite
        self.assertEqual(cells[(True, True, False)]["outcome"], "detected")    # canary fires before the ret
        # ASLR: a single wrong guess does not pwn, and the success probability is modelled
        self.assertNotEqual(cells[(False, False, True)]["outcome"], "pwned")
        self.assertAlmostEqual(cells[(False, False, True)]["success_prob"], 2.0 ** -MM.ASLR_DEMO_BITS)


class AslrEntropy(unittest.TestCase):
    def test_arithmetic(self):
        for L in MM.aslr_entropy()["layouts"]:
            k = L["bits"]
            self.assertAlmostEqual(L["hit_prob"], 2.0 ** -k)
            self.assertEqual(L["expected_tries_rerandomised"], 2 ** k)
            self.assertEqual(L["expected_tries_sequential"], (2 ** k + 1) / 2)

    def test_experiment_hits_exactly_one_placement(self):
        r = MM.aslr_experiment(bits=4)
        self.assertEqual(r["placements"], 16)
        self.assertEqual(r["hit_count"], 1)
        self.assertAlmostEqual(r["measured_rate"], r["theoretical_rate"])
        self.assertAlmostEqual(r["measured_rate"], 1 / 16)


class Rop(unittest.TestCase):
    def test_every_gadget_ends_in_an_indirect_transfer_or_halt(self):
        exe = MM.build_rop()
        gs = MM.find_gadgets(exe)
        self.assertTrue(gs)
        for g in gs:
            last = g["instrs"][-1]
            self.assertTrue(last.startswith("jalr") or last == "halt", last)
            self.assertIn(g["terminator"], ("jalr", "halt"))

    def test_chain_pwns_with_nx_and_is_caught_by_a_canary(self):
        demo = MM.rop_demo("pwned")
        # with W^X on, no injected code can run, yet the gadget chain prints "pwned" and halts cleanly
        self.assertEqual(demo["nx"]["output"], "pwned")
        self.assertIsNone(demo["nx"]["fault"])
        self.assertTrue(demo["nx"]["halted"])
        # the canary catches the overwrite before control is hijacked
        self.assertIn("detected", demo["canary"]["output"])
        self.assertNotIn("pwned", demo["canary"]["output"])
        self.assertEqual(sorted(demo["chain"]["gadgets_used"]), ["halt", "restore3", "wb"])
        self.assertEqual(demo["chain"]["words"], 4 * len("pwned"))

    def test_chain_can_print_other_words(self):
        exe = MM.build_rop()
        gs = MM.find_gadgets(exe)
        tape, _ = MM.build_rop_chain(exe, gs, "root")
        self.assertEqual(MM.run_rop(exe, tape, nx=True)["output"], "root")


class BorrowChecker(unittest.TestCase):
    def test_examples_match_their_expected_verdicts(self):
        for row in MM.borrow_examples():
            self.assertEqual(row["accepted"], row["expected"],
                             f"{row['name']}: {row['program']!r} -> {row['reason']}")

    def test_specific_rules(self):
        self.assertFalse(MM.check_borrows("let x\ny = move x\nuse x")["ok"])           # use after move
        self.assertTrue(MM.check_borrows("let x\ny = move x\nuse y")["ok"])
        self.assertFalse(MM.check_borrows("let x\na = &mut x\nb = &mut x")["ok"])      # two &mut
        self.assertFalse(MM.check_borrows("let x\na = & x\nb = &mut x")["ok"])         # & and &mut
        self.assertFalse(MM.check_borrows("ref r\n{\nlet x\nr = &mut x\n}\nuse r")["ok"])  # dangling
        self.assertTrue(MM.check_borrows("let x\n{\nr = & x\nuse r\n}\nuse x")["ok"])


# ======================================================================================================================
# auth.py
# ======================================================================================================================

class Passwords(unittest.TestCase):
    def test_entropy_and_guessing(self):
        self.assertAlmostEqual(AU.password_entropy(62, 10), 10 * math.log2(62))
        g = AU.guessing(40, 1e10)
        self.assertAlmostEqual(g["space"], 2.0 ** 40)
        self.assertAlmostEqual(g["seconds_full"], 2.0 ** 40 / 1e10)
        self.assertAlmostEqual(g["seconds_expected"], g["seconds_full"] / 2)

    def test_zipf_prefix_matches_direct_sum(self):
        r = AU.zipf_cracked(vocab=1000, exponent=1.0, ks=(1, 2, 3))
        H = sum(1.0 / x for x in range(1, 1001))
        for row in r["rows"]:
            n = min(row["guesses"], 1000)
            expect = sum(1.0 / x for x in range(1, n + 1)) / H
            self.assertAlmostEqual(row["share_cracked"], expect)
        shares = [row["share_cracked"] for row in r["rows"]]
        self.assertEqual(shares, sorted(shares))               # monotone non-decreasing


class Otp(unittest.TestCase):
    def test_totp_step_boundaries_and_contracts(self):
        key = b"12345678901234567890"
        for when, counter in ((0, 0), (29, 0), (30, 1), (59, 1), (60, 2)):
            self.assertEqual(AU.totp(key, when, digits=6), AU.hotp(key, counter))
        for kwargs in ({"counter": -1}, {"counter": 1 << 64}, {"counter": 0, "digits": 0},
                       {"counter": 0, "algorithm": "md5"}):
            with self.assertRaises(ValueError):
                AU.hotp(key, **kwargs)
        with self.assertRaises(ValueError):
            AU.totp(key, 0, step=0)

    RFC4226 = ["755224", "287082", "359152", "969429", "338314",
               "254676", "287922", "162583", "399871", "520489"]
    RFC6238 = {
        "sha1": ["94287082", "07081804", "14050471", "89005924", "69279037", "65353130"],
        "sha256": ["46119246", "68084774", "67062674", "91819424", "90698825", "77737706"],
        "sha512": ["90693936", "25091201", "99943326", "93441116", "38618901", "47863826"],
    }

    def test_hotp_rfc4226_vectors(self):
        self.assertEqual([v["hotp"] for v in AU.hotp_vectors()], self.RFC4226)

    def test_totp_rfc6238_vectors(self):
        got = {}
        for v in AU.totp_vectors():
            got.setdefault(v["algorithm"], []).append(v["totp"])
        for algo, expected in self.RFC6238.items():
            self.assertEqual(got[algo], expected, algo)


class NeedhamSchroeder(unittest.TestCase):
    def test_flawed_protocol_has_lowes_attack(self):
        r = AU.needham_schroeder(fixed=False)
        self.assertTrue(r["attack_found"])
        self.assertTrue(r["intruder_knows_Nb"])
        self.assertGreaterEqual(len(r["trace"]), 4)
        self.assertGreater(r["states_explored"], 0)
        joined = " | ".join(r["trace"])
        self.assertIn("A initiates with I", joined)
        self.assertIn("B receives M1", joined)
        self.assertIn("completes", joined)

    def test_lowes_fix_has_no_attack(self):
        r = AU.needham_schroeder(fixed=True)
        self.assertFalse(r["attack_found"])
        self.assertIsNone(r["trace"])
        self.assertGreater(r["states_explored"], 0)


# ======================================================================================================================
# access.py
# ======================================================================================================================

class AccessMatrix(unittest.TestCase):
    def test_acls_and_capabilities_are_the_same_matrix_sliced(self):
        am = AC.access_matrix()
        for key, rights in am["matrix"].items():
            s, o = key.split("->")
            self.assertEqual(am["acls_by_object"][o][s], rights)
            self.assertEqual(am["capabilities_by_subject"][s][o], rights)
        self.assertIn("own", am["acls_by_object"]["payroll.db"]["server"])
        self.assertIn("own", am["capabilities_by_subject"]["alice"]["report.txt"])

    def test_confused_deputy(self):
        d = AC.confused_deputy()
        self.assertTrue(d["ambient"]["write_happens"])         # ambient authority overwrites BILL
        self.assertFalse(d["capability"]["write_happens"])     # capability model denies it


class BellLaPadula(unittest.TestCase):
    def test_dominance(self):
        self.assertTrue(AC.dominates(("secret", {"ENG"}), ("confidential", {"ENG"})))
        self.assertFalse(AC.dominates(("secret", {"ENG"}), ("secret", {"OPS"})))

    def test_no_read_up_no_write_down(self):
        bl = AC.bell_lapadula()
        by = {c["what"]: c for c in bl["checks"]}
        self.assertTrue(by["secret/ENG reads unclassified doc"]["allowed"])           # read down: ok
        self.assertFalse(by["secret/ENG reads topsecret doc (read up)"]["allowed"])   # no read up
        self.assertFalse(by["secret/ENG writes unclassified doc (write down)"]["allowed"])  # no write down
        self.assertTrue(by["unclassified writes secret doc (write up, allowed)"]["allowed"])
        self.assertFalse(bl["forbidden_flow"]["allowed"])      # high -> low blocked


class Hru(unittest.TestCase):
    def test_leaking_system_leaks(self):
        r = AC.hru_safety(AC.leaking_system(), "read")
        self.assertTrue(r["leaks"])
        self.assertIsNotNone(r["trace"])
        self.assertIsNotNone(r["leaked_cell"])

    def test_safe_system_does_not_leak(self):
        r = AC.hru_safety(AC.safe_system(), "read")
        self.assertFalse(r["leaks"])
        self.assertIsNone(r["trace"])


if __name__ == "__main__":
    unittest.main()
