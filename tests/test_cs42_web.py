import unittest

from explainer.cs.web import css, events, html, layout, platform, vdom


class Html(unittest.TestCase):
    def test_recovers(self):
        doc, errs, fixes = html.parse("<p>one<p>two</div><ul><li>a<li>b</ul>")
        tags = [n.tag for n in doc.walk() if not n.tag.startswith("#")]
        self.assertEqual(tags, ["p", "p", "ul", "li", "li"])
        self.assertIn("stray </div> ignored", fixes)

    def test_attributes_and_void(self):
        doc, errs, _ = html.parse('<img src=a.png alt="x y"><br/>t')
        img = doc.children[0]
        self.assertEqual(img.attrs, {"src": "a.png", "alt": "x y"})
        self.assertEqual(doc.children[2].text, "t")

    def test_stray_lt_is_text(self):
        doc, errs, _ = html.parse("<p>a < b</p>")
        self.assertEqual("".join(n.text for n in doc.walk() if n.tag == "#text"), "a < b")
        self.assertTrue(errs)


class Css(unittest.TestCase):
    def test_specificity(self):
        self.assertEqual(css.specificity("#main .note p"), (1, 1, 1))
        self.assertGreater(css.specificity(".a"), css.specificity("div p span"))

    def test_cascade(self):
        doc, _, _ = html.parse('<div id=main><div class=note><p class=lead>hi <b>x</b></p></div><p>y</p></div>')
        st = css.cascade(doc, css.parse_css("p {color: grey} #main .note p {color: green} .note p {color: red}"))
        ps = [n for n in doc.walk() if n.tag == "p"]
        b = [n for n in doc.walk() if n.tag == "b"][0]
        self.assertEqual(st[id(ps[0])]["color"], "green")
        self.assertEqual(st[id(ps[1])]["color"], "grey")
        self.assertEqual(st[id(b)]["color"], "green")          # inherited


class Layout(unittest.TestCase):
    def test_kp_never_worse(self):
        words = "a bb ccc dddd ee f gggggg hh iii j kkkk".split() * 4
        w = [10.0 * len(x) for x in words]
        g = layout.greedy(words, w, 5.0, 100.0)
        k = layout.knuth_plass(words, w, 5.0, 100.0)
        self.assertLessEqual(layout.line_stats(k, w, 5.0, 100.0)["badness"],
                             layout.line_stats(g, w, 5.0, 100.0)["badness"] + 1e-9)
        self.assertEqual(sum(len(x) for x in k), len(words))

    def test_flex(self):
        self.assertEqual(layout.flex(600, [(100, 1, 1), (200, 2, 1), (150, 0, 1)])["sizes"], [150.0, 300.0, 150.0])
        s = layout.flex(300, [(100, 1, 1), (200, 1, 1)])["sizes"]
        self.assertAlmostEqual(sum(s), 300)


class Loop(unittest.TestCase):
    def test_orderings(self):
        ex = events.ordering_examples()
        self.assertEqual(ex["basic"], ["A", "D", "C", "B"])
        self.assertEqual(ex["async"], ["before call", "f starts", "after call", "f resumes", "then"])

    def test_jank(self):
        self.assertGreater(events.jank(120)["dropped"], 5)
        self.assertEqual(events.chunked(120, 8)["dropped"], 0)


class Vdom(unittest.TestCase):
    def test_keys(self):
        r = vdom.list_experiment(50)
        self.assertLess(r["prepend"]["keyed"], 5)
        self.assertGreater(r["prepend"]["unkeyed"], 50)
        self.assertEqual(r["swap two"]["lis_moves"], 2)

    def test_ted(self):
        a = vdom.V("ul", kids=[vdom.V("li", text="a"), vdom.V("li", text="b")])
        b = vdom.V("ul", kids=[vdom.V("li", text="a"), vdom.V("li", text="c"), vdom.V("li", text="d")])
        self.assertEqual(vdom.tree_edit_distance(a, b), 2)

    def test_signals(self):
        r = vdom.signals_demo()
        self.assertEqual(r["reran"]["count"], ["badge", "header"])


class Platform(unittest.TestCase):
    def test_contrast(self):
        self.assertAlmostEqual(platform.contrast("#000000", "#ffffff"), 21.0)
        self.assertEqual(platform.grey_threshold(), "#767676")

    def test_origin(self):
        self.assertTrue(platform.same_origin("https://a.com/x", "https://a.com:443/y"))
        self.assertFalse(platform.same_origin("https://a.com", "http://a.com"))
        self.assertFalse(platform.same_origin("https://a.com:0", "https://a.com"))
        self.assertFalse(platform.same_origin("data:text/plain,a", "data:text/plain,b"))

    def test_cors_preserves_origin_port(self):
        args = ("https://a.com:8443", "https://b.com")
        self.assertTrue(platform.cors(*args, allow_origin="https://a.com:8443")["readable"])
        self.assertFalse(platform.cors(*args, allow_origin="https://a.com")["readable"])
        r = platform.cors(*args, method="PUT", allow_methods=("PUT",), allow_origin="*",
                          credentials=True, allow_credentials=True)
        self.assertTrue(r["preflight"])
        self.assertFalse(r["readable"])
        self.assertIn("never sent", r["why"])


if __name__ == "__main__":
    unittest.main()
