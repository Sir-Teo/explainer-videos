"""Tests for Part 55's web and trusting-trust instruments (explainer/cs/trust: web, trojan).

Every claim is checked against an independent computation: the SQL results against a direct scan of the table and
against the wrong/right credential by hand; the trojan's backdoor against hand-written clean and backdoored login
semantics; the fixpoint and DDC against bit-for-bit byte comparison; XSS against an independent HTML parse.
"""

from __future__ import annotations

import json
import unittest

from explainer.cs.trust import trojan as T
from explainer.cs.trust import web as W


def _rows_set(rows):
    return {tuple(r) for r in rows}


class TestSQLInjection(unittest.TestCase):
    def setUp(self):
        self.db = W.demo_db()

    def test_honest_login_both_paths_agree_with_table(self):
        # independent oracle: the admin row is exactly the one matching (username, password) in USERS.
        admin = [u for u in W.USERS if u[1] == "admin" and u[2] == "hunter2-admin"][0]
        expect = [[admin[0], admin[1], admin[3]]]            # SELECT id, username, secret
        self.assertEqual(W.login_concat(self.db, "admin", "hunter2-admin")["rows"], expect)
        self.assertEqual(W.login_param(self.db, "admin", "hunter2-admin")["rows"], expect)

    def test_wrong_password_denied_both_paths(self):
        self.assertEqual(W.login_concat(self.db, "admin", "nope")["rows"], [])
        self.assertEqual(W.login_param(self.db, "admin", "nope")["rows"], [])

    def test_tautology_payload_breaks_concat_but_is_data_when_bound(self):
        payload = "' OR '1'='1"
        vuln = W.login_concat(self.db, payload, "x")
        # the input reached the parser as code -> the query does not parse.
        self.assertIsNone(vuln["rows"])
        self.assertIn("Error", vuln["error"])
        # bound, the same bytes are a literal username that matches nobody -> login denied, no error.
        self.assertEqual(W.login_param(self.db, payload, "x")["rows"], [])

    def test_unquoted_id_eq_id_leaks_whole_table(self):
        # the dangerous unquoted context: WHERE id = id dissolves the filter.
        leak = W.fetch_by_id_concat(self.db, "id")
        all_rows = [[u[0], u[1], u[3]] for u in W.USERS]
        self.assertEqual(_rows_set(leak["rows"]), _rows_set(all_rows))
        self.assertEqual(len(leak["rows"]), len(W.USERS))
        # one honest lookup returns exactly one row.
        self.assertEqual(len(W.fetch_by_id_concat(self.db, 2)["rows"]), 1)

    def test_param_id_value_does_not_leak(self):
        # binding the string "id" compares the column to the literal "id" -> no integer id equals it.
        safe = W._param_id_value(self.db)
        self.assertEqual(safe["rows"], [])

    def test_bind_never_reparses_arbitrary_injection(self):
        # a value that is itself a whole malicious query stays a single username literal.
        nasty = "x'; DROP TABLE users; SELECT * FROM users WHERE 'a'='a"
        res = W.login_param(self.db, nasty, "p")
        self.assertEqual(res["rows"], [])                    # matches no user; nothing executed
        # the table is untouched (still three rows reachable).
        self.assertEqual(len(self.db.query("SELECT id FROM users WHERE id = id")), len(W.USERS))

    def test_prepare_tree_shape_is_fixed(self):
        q = W.prepare(f"SELECT id FROM users WHERE username = '{W._STR_SENTINELS[0]}'")
        # binding wildly different values yields the same number of predicates (shape frozen).
        for val in ["admin", "' OR 1=1 --", ""]:
            bq = W.bind(q, [val])
            self.assertEqual(len(bq.where), len(q.where))

    def test_injection_report_json(self):
        rep = W.injection_report()
        json.dumps(rep)                                       # serialisable for the scene cache
        # concat leaks the whole table; the param value path leaks nothing.
        self.assertEqual(len(rep["id_leak"]["concat_id_eq_id"]["rows"]), len(W.USERS))
        self.assertEqual(rep["id_leak"]["param_value_id"]["rows"], [])


class TestXSS(unittest.TestCase):
    def test_escaping_changes_the_parse_tree(self):
        rep = W.xss_report("<script>steal()</script>")
        # unescaped: a real <script> element appears; escaped: it does not.
        self.assertTrue(rep["script_injected"]["raw"])
        self.assertFalse(rep["script_injected"]["safe"])
        self.assertIn("script", rep["raw"]["tags"])
        self.assertNotIn("script", rep["safe"]["tags"])
        # escaped output keeps the payload as visible text, not markup.
        self.assertIn("<script>", rep["safe"]["text"])
        json.dumps(rep)

    def test_escaped_render_has_no_new_tags(self):
        rep = W.xss_report("<img src=x onerror=alert(1)>")
        self.assertEqual(rep["safe"]["tags"], ["div"])        # only the template's own div
        self.assertIn("img", rep["raw"]["tags"])


# independent oracles for login semantics
def _clean_login(pw):
    return pw == T.CORRECT


def _backdoored_login(pw):
    return pw == T.MAGIC or pw == T.CORRECT


class TestTrojan(unittest.TestCase):
    def test_clean_binary_has_no_backdoor(self):
        login = T.run_compiler_binary(T.clean_compile(T.CLEAN_COMPILER), T.CLEAN_LOGIN)
        for pw in [T.CORRECT, T.MAGIC, "guess", ""]:
            self.assertEqual(T.run_login(login, pw), _clean_login(pw))

    def test_trojaned_binary_backdoors_login(self):
        login = T.run_compiler_binary(T.clean_compile(T.trojaned_compiler_source()), T.CLEAN_LOGIN)
        for pw in [T.CORRECT, T.MAGIC, "guess", ""]:
            self.assertEqual(T.run_login(login, pw), _backdoored_login(pw))
        # the two logins genuinely differ only on the magic password.
        self.assertTrue(_backdoored_login(T.MAGIC) and not _clean_login(T.MAGIC))

    def test_fixpoint_clean_source_trojaned_binary(self):
        troj = T.clean_compile(T.trojaned_compiler_source())
        reproduced = T.run_compiler_binary(troj, T.CLEAN_COMPILER)  # compile CLEAN source with trojaned binary
        self.assertEqual(reproduced, troj)                          # bit-for-bit identical
        # and the reproduced binary still backdoors login.
        login = T.run_compiler_binary(reproduced, T.CLEAN_LOGIN)
        self.assertEqual(T.run_login(login, T.MAGIC), True)

    def test_trojan_absent_from_every_source(self):
        self.assertNotIn(T.MAGIC, T.CLEAN_COMPILER)
        self.assertNotIn(T.MAGIC, T.CLEAN_LOGIN)
        # but present in the trojaned binary's source, as expected.
        self.assertIn(T.MAGIC, T.trojaned_compiler_source())

    def test_clean_compile_is_deterministic(self):
        self.assertEqual(T.clean_compile(T.CLEAN_COMPILER), T.clean_compile(T.CLEAN_COMPILER))
        self.assertEqual(T.clean_compile(T.trojaned_compiler_source()),
                         T.clean_compile(T.trojaned_compiler_source()))

    def test_thompson_report(self):
        rep = T.thompson_report()
        json.dumps(rep)
        self.assertTrue(rep["fixpoint"]["reproduced_equals_trojaned"])
        self.assertFalse(rep["source_is_clean"]["magic_in_clean_compiler"])
        self.assertTrue(rep["backdoor"]["trojaned_binary"]["accepts_magic"])
        self.assertFalse(rep["backdoor"]["clean_binary"]["accepts_magic"])
        self.assertTrue(rep["backdoor"]["trojaned_binary"]["accepts_correct"])
        self.assertFalse(rep["backdoor"]["trojaned_binary"]["accepts_wrong"])

    def test_ddc_detects_trojan_and_clears_clean(self):
        clean_bin = T.clean_compile(T.CLEAN_COMPILER)
        troj_bin = T.clean_compile(T.trojaned_compiler_source())
        clean = T.ddc(clean_bin)
        trojaned = T.ddc(troj_bin)
        # clean: the two stage-2 binaries agree bit for bit.
        self.assertTrue(clean["match"])
        self.assertEqual(clean["stage2_suspect"]["sha256"], clean["stage2_trusted"]["sha256"])
        # trojaned: they differ -> caught.
        self.assertFalse(trojaned["match"])
        self.assertNotEqual(trojaned["stage2_suspect"]["sha256"], trojaned["stage2_trusted"]["sha256"])
        self.assertEqual(trojaned["verdict"], "TROJAN DETECTED")

    def test_ddc_report_json(self):
        rep = T.ddc_report()
        json.dumps(rep)
        self.assertTrue(rep["clean"]["match"])
        self.assertFalse(rep["trojaned"]["match"])

    def test_reproducible_builds(self):
        rep = T.reproducible_report()
        json.dumps(rep)
        self.assertFalse(rep["unnormalized"]["identical"])   # timestamps/paths leak in
        self.assertTrue(rep["normalized"]["identical"])      # normalised -> identical bytes


if __name__ == "__main__":
    unittest.main()
