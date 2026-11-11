from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs55.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, mono, tag_box


def cbox(text, color, w=None, h=0.46, size=17, fill=0.0, use_mono=False):
    """A labelled rounded box (Tex, or monospace with ``use_mono``)."""
    t = mono(text, size=size, color=WHITE) if use_mono else label(text, font_size=size, color=WHITE)
    w = w or t.width + 0.35
    r = RoundedRectangle(width=w, height=h, corner_radius=0.07, stroke_color=color, stroke_width=1.6,
                         fill_color=color if fill else BG, fill_opacity=fill if fill else 1)
    if t.width > w - 0.12:
        t.width = w - 0.12
    t.move_to(r)
    return VGroup(r, t)


def tree_node(text, color, use_mono=False, size=19, w=None):
    return cbox(text, color, w=w, size=size, use_mono=use_mono, h=0.5)


def edge(a, b):
    return Line(a.get_bottom(), b.get_top(), color=GREY_B, stroke_width=1.6, buff=0.04)


def lanes(names, xs, colors, top=2.35, bottom=-2.0, size=18):
    """The participants of a sequence diagram: a named box on top and a dashed lifeline down."""
    g = VGroup()
    for n, x, c in zip(names, xs, colors):
        b = cbox(n, c, w=2.4, h=0.5, size=size, use_mono=True).move_to([x, top, 0])
        life = DashedLine([x, top - 0.25, 0], [x, bottom, 0], color=GREY_D, stroke_width=1.5, dash_length=0.1)
        g.add(VGroup(b, life))
    return g


def message(x1, x2, y, text, color, size=16, use_mono=True):
    a = Arrow([x1, y, 0], [x2, y, 0], buff=0.06, stroke_width=2.6, color=color, max_tip_length_to_length_ratio=0.06,
              max_stroke_width_to_length_ratio=8)
    t = mono(text, size=size, color=color) if use_mono else label(text, font_size=size + 2, color=color)
    if t.width > abs(x2 - x1) - 0.1:
        t.width = abs(x2 - x1) - 0.1
    t.next_to(a, UP, buff=0.06)
    return VGroup(a, t)


class Web(VoiceoverScene):
    def construct(self):
        self.card()
        self.origin()
        self.xss()
        self.csrf()
        self.injection()
        self.binding()
        self.pki()

    def card(self):
        card = chapter_card(8, r"The web", r"When does a string become code?", lit=(1998, 2011),
                            extra=((1998, r"SQL injection described"), (2011, r"DigiNotar")), part=PART)
        with self.voiceover("Chapter eight. The web."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def origin(self):
        head = label(r"The same-origin policy \ (Part 42)", font_size=36).to_edge(UP, buff=0.3)
        ref = ("https", "bank.example", "443")
        rows = [("https", "bank.example", "443", "/account"), ("http", "bank.example", "80", "/"),
                ("https", "bank.example", "8443", "/"), ("https", "api.bank.example", "443", "/"),
                ("https", "evil.example", "443", "/")]
        hdr = VGroup(*[label(t, font_size=19, color=GREY_B) for t in (r"scheme", r"host", r"port")])
        widths = [1.5, 3.2, 1.3]
        xs = [-2.4, 0.15, 2.55]
        for h, x in zip(hdr, xs):
            h.move_to([x, 2.35, 0])
        reft = VGroup(*[cbox(v, HEAD, w=w, size=18, use_mono=True).move_to([x, 1.8, 0])
                        for v, w, x in zip(ref, widths, xs)])
        refl = label(r"this page's origin", font_size=18, color=HEAD).next_to(reft, LEFT, buff=0.3)
        lines = VGroup()
        for k, (sch, host, port, path) in enumerate(rows):
            y = 0.95 - k * 0.62
            parts = VGroup()
            for v, rv, w, x in zip((sch, host, port), ref, widths, xs):
                parts.add(cbox(v, YES if v == rv else NO, w=w, size=17, use_mono=True).move_to([x, y, 0]))
            same = (sch, host, port) == ref
            url = mono(f"{sch}://{host}" + ("" if port in ("443", "80") else f":{port}") + path, size=16,
                       color=GREY_A)
            url.move_to([-5.0, y, 0]).align_to([-6.7, 0, 0], LEFT)
            if url.width > 3.3:
                url.width = 3.3
                url.align_to([-6.7, 0, 0], LEFT)
            v = label(r"same origin" if same else r"different origin", font_size=18,
                      color=YES if same else NO).move_to([4.5, y, 0]).align_to([3.55, 0, 0], LEFT)
            lines.add(VGroup(url, parts, v))
        refl.next_to(reft, LEFT, buff=0.25)
        notes = wrapped_label(r"script from one origin may not \textit{read} another's pages, \ cookies or storage; "
                              r"\ but it may still \textit{send} requests anywhere", 12.4, font_size=21,
                              color=WHITE).to_edge(DOWN, buff=0.45)
        ill = label(r"illustrative addresses", font_size=16, color=GREY_B).next_to(notes, UP, buff=0.2).to_edge(
            RIGHT, buff=0.4)
        with self.voiceover(
            "A web page runs code from whoever sent it, so the browser needs a rule about whose data that code may "
            "touch. <bookmark mark='a'/> It is the same-origin policy, and an origin is three things: scheme, host "
            "and port. <bookmark mark='b'/> A script may read only what comes from its own origin. Change the scheme "
            "or the port, or add a subdomain, and it is a stranger. <bookmark mark='c'/> But a page may still send "
            "requests to origins it cannot read, and most web attacks live in that gap, or in code that slips inside "
            "an origin."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hdr), FadeIn(reft), FadeIn(refl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(L, shift=UP * 0.1) for L in lines], lag_ratio=0.35), FadeIn(ill),
                      run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(notes))
        self.wait(0.4)
        self.clear_scene()

    def xss(self):
        x = load("xss")
        head = label(r"Cross-site scripting: \ data parsed as code", font_size=36).to_edge(UP, buff=0.3)
        tmpl = VGroup(label(r"template:", font_size=19, color=GREY_A),
                      mono("<div class=comment>{value}</div>", 18, color=WHITE)).arrange(RIGHT, buff=0.25)
        pay = VGroup(label(r"a comment:", font_size=19, color=GREY_A),
                     mono(x["payload"], 18, color=NO)).arrange(RIGHT, buff=0.25)
        top = VGroup(tmpl, pay).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(head, DOWN, buff=0.35)
        top.to_edge(LEFT, buff=0.5)
        raw = VGroup(label(r"pasted:", font_size=18, color=NO), mono(x["raw"]["html"], 16, color=GREY_A)).arrange(
            RIGHT, buff=0.2)
        safe = VGroup(label(r"escaped:", font_size=18, color=YES), mono(x["safe"]["html"], 16, color=GREY_A)).arrange(
            RIGHT, buff=0.2)
        outs = VGroup(raw, safe).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(top, DOWN, buff=0.35)
        outs.align_to(top, LEFT)
        for o in outs:
            if o.width > 12.8:
                o.width = 12.8

        def dom(tags, text, cx, col, live):
            nodes = [tree_node(f"<{t}>", NO if t == "script" else DATA, use_mono=True) for t in tags]
            leaf = tree_node(text, col, use_mono=True, size=16)
            g = VGroup(*nodes, leaf).arrange(DOWN, buff=0.4).move_to([cx, -1.2, 0])
            es = VGroup(*[edge(a, b) for a, b in zip(list(nodes) + [], list(nodes[1:]) + [leaf])])
            cap = label(live, font_size=18, color=col).next_to(g, DOWN, buff=0.2)
            return VGroup(g, es, cap)
        t1 = dom(x["raw"]["tags"], x["raw"]["text"], -3.4, NO,
                 r"tags parsed: \ " + r", \ ".join(x["raw"]["tags"]) + r" \ --- \ the script runs")
        t2 = dom(x["safe"]["tags"], x["safe"]["text"], 3.4, YES,
                 r"tags parsed: \ " + r", \ ".join(x["safe"]["tags"]) + r" \ --- \ just text")
        ill = label(r"our toy templater; \ \texttt{steal} is a stand-in", font_size=16,
                    color=GREY_B).to_corner(DR, buff=0.35)
        defs = wrapped_label(r"defences: \ escape for the context; \ a Content-Security-Policy such as "
                             r"\texttt{script-src 'self'} refuses inline scripts; \ \texttt{HttpOnly} cookies are "
                             r"hidden from scripts", 9.8, font_size=19, color=HEAD).to_corner(DL, buff=0.35)
        with self.voiceover(
            "The first way in is to slip inside. <bookmark mark='a'/> A site shows comments through a template, and "
            "someone posts a comment that is a script. <bookmark mark='b'/> Pasted in raw, its bytes reach the "
            "browser's HTML parser, Part 42's state machine, as markup. <bookmark mark='c'/> Parsing our output finds "
            "a live script element, which would run with the site's own authority and read its users' cookies: "
            "cross-site scripting. <bookmark mark='d'/> Escape the same bytes and the parser finds only text. "
            "<bookmark mark='e'/> The defences stack: escape for the context, a Content Security Policy that refuses "
            "inline scripts, and HTTP-only cookies that scripts cannot see."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(top))
            vo.wait_until("b")
            self.play(FadeIn(raw))
            vo.wait_until("c")
            self.play(FadeIn(t1[0]), Create(t1[1]), FadeIn(t1[2]), FadeIn(ill))
            vo.wait_until("d")
            self.play(FadeIn(safe))
            self.play(FadeIn(t2[0]), Create(t2[1]), FadeIn(t2[2]))
            vo.wait_until("e")
            self.play(FadeIn(defs))
        self.wait(0.4)
        self.clear_scene()

    def csrf(self):
        head = label(r"Cross-site request forgery", font_size=36).to_edge(UP, buff=0.3)
        xs = [-5.2, -1.9, 1.4]
        ln = lanes([r"evil.example", r"your browser", r"bank.example"], xs, [NO, DATA, YES], top=2.3, bottom=-1.9)
        m1 = message(xs[0], xs[1], 1.45, "page with a hidden form", NO)
        m2 = message(xs[1], xs[2], 0.55, "POST /transfer", DATA)
        ck = mono("Cookie: session=...", 16, color=HEAD).next_to(m2[0], DOWN, buff=0.08)
        auto = label(r"attached automatically", font_size=16, color=HEAD).next_to(ck, DOWN, buff=0.05)
        done = label(r"valid session: \ done", font_size=18, color=NO).next_to([xs[2], -0.75, 0], LEFT, buff=0.15)
        ill = label(r"schematic", font_size=16, color=GREY_B).move_to([xs[1], -2.25, 0])
        notes = VGroup(
            wrapped_label(r"the browser is Chapter 6's \textbf{confused deputy}: \ it lends its ambient authority, "
                          r"\ the cookie, \ to any page that names the bank", 3.8, font_size=19, color=NO),
            wrapped_label(r"\texttt{SameSite} cookies: \ not attached to cross-site requests such as this one", 3.8,
                          font_size=19, color=YES),
            wrapped_label(r"a secret token in each form: \ a capability the evil page cannot read, \ thanks to the "
                          r"same-origin policy", 3.8, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.8, 0.0, 0])
        with self.voiceover(
            "The second way in uses the gap. <bookmark mark='a'/> You visit an evil page while logged in to your "
            "bank, and it submits a hidden form aimed at the bank. <bookmark mark='b'/> Your browser sends the "
            "request and, as for every request to the bank, attaches your session cookie. <bookmark mark='c'/> The "
            "bank sees a valid session, and obeys. <bookmark mark='d'/> The browser is Chapter six's confused deputy, "
            "lending its ambient authority to anyone who names the bank. <bookmark mark='e'/> The fixes are that "
            "chapter's too: same-site cookies stay off cross-site requests like this one, and a secret token in each "
            "genuine form is a capability the evil page cannot read."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ln), FadeIn(ill))
            vo.wait_until("a")
            self.play(GrowArrow(m1[0]), FadeIn(m1[1]))
            vo.wait_until("b")
            self.play(GrowArrow(m2[0]), FadeIn(m2[1]), FadeIn(ck), FadeIn(auto))
            vo.wait_until("c")
            self.play(FadeIn(done), Indicate(ln[2][0], color=NO))
            vo.wait_until("d")
            self.play(FadeIn(notes[0]))
            vo.wait_until("e")
            self.play(FadeIn(notes[1]))
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def injection(self):
        q = load("sql")["id_leak"]
        good, bad = q["concat_id_2"], q["concat_id_eq_id"]
        head = label(r"SQL injection, \ on our own database \ (Part 35)", font_size=36).to_edge(UP, buff=0.3)
        code = mono('sql = "SELECT id, username, secret FROM users WHERE id = " + uid', 17, color=WHITE)
        code.next_to(head, DOWN, buff=0.35)

        def case(sql, uid, right_text, right_col, rows, cx, col):
            pre, inp = sql[: sql.rindex("= ") + 2], sql[sql.rindex("= ") + 2:]
            s = VGroup(mono(pre.replace("SELECT id, username, secret FROM users ", "... "), 16, color=GREY_A),
                       mono(inp, 16, color=col)).arrange(RIGHT, buff=0.08)
            s.move_to([cx, 1.6, 0])
            ul = label(rf"\texttt{{uid}} = \texttt{{{uid}}}", font_size=19, color=col).next_to(s, UP, buff=0.12)
            eq = tree_node(r"=", GREY_B)
            lft = tree_node(r"column \texttt{id}", DATA)
            rgt = tree_node(right_text, right_col)
            kids = VGroup(lft, rgt).arrange(RIGHT, buff=0.35)
            tr = VGroup(eq, kids).arrange(DOWN, buff=0.45).move_to([cx, 0.45, 0])
            es = VGroup(Line(eq.get_bottom(), lft.get_top(), color=GREY_B, stroke_width=1.6),
                        Line(eq.get_bottom(), rgt.get_top(), color=GREY_B, stroke_width=1.6))
            tab = grid_table([r"id", r"username", r"secret"], [[str(r[0]), r[1], r[2]] for r in rows],
                             widths=[0.6, 1.5, 2.3], row_h=0.4, font_size=19, mono_cols=(1, 2))
            tab.next_to(tr, DOWN, buff=0.4).set_x(cx)
            for r in range(1, len(rows) + 1):
                tab.cells[r][2].set_color(col)
            return VGroup(ul, s, VGroup(tr, es), tab)
        c1 = case(good["sql"], "2", r"literal \texttt{2}", YES, good["rows"], -3.4, YES)
        c2 = case(bad["sql"], "id", r"column \texttt{id}", NO, bad["rows"], 3.4, NO)
        n1 = label(rf"{len(good['rows'])} row, \ as intended", font_size=18, color=YES).next_to(c1[3], DOWN, buff=0.2)
        n2 = label(rf"$\text{{id}} = \text{{id}}$ holds for every row: \ all {len(bad['rows'])} secrets",
                   font_size=18, color=NO).next_to(c2[3], DOWN, buff=0.2)
        foot = label(r"first described publicly in 1998; \ still in the OWASP Top 10 \ (2021)",
                     font_size=18, color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Now the same confusion on a server, with Part 35's database engine. <bookmark mark='a'/> A lookup builds "
            "its query by pasting the user's input into the SQL text. <bookmark mark='b'/> Given two, the parser "
            "compares the column id with the literal two, and one row comes back. <bookmark mark='c'/> Given the "
            "letters i, d, the parser reads a second column name. Id equals id holds for every row, the filter "
            "dissolves, and our engine returns all three secrets. <bookmark mark='d'/> Nothing overflowed and nothing "
            "was guessed: the input reached the parser and changed the program's shape. Injection was described "
            "publicly in 1998, and is still among the commonest web flaws."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code))
            vo.wait_until("a")
            self.play(Indicate(code, color=HEAD, scale_factor=1.03))
            vo.wait_until("b")
            self.play(FadeIn(c1[0]), FadeIn(c1[1]))
            self.play(FadeIn(c1[2]))
            self.play(FadeIn(c1[3]), FadeIn(n1))
            vo.wait_until("c")
            self.play(FadeIn(c2[0]), FadeIn(c2[1]))
            self.play(FadeIn(c2[2]))
            self.play(FadeIn(c2[3]), FadeIn(n2))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def binding(self):
        s = load("sql")
        head = label(r"The fix is a parsing fix \ (Part 12)", font_size=36).to_edge(UP, buff=0.3)
        steps = VGroup(
            cbox(r"template, \ parsed once", DATA, w=3.0, size=18),
            cbox(r"a fixed tree, \ with a hole", HEAD, w=3.0, size=18),
            cbox(r"values bound as leaves", YES, w=3.0, size=18),
        ).arrange(RIGHT, buff=0.7).next_to(head, DOWN, buff=0.4)
        arr = VGroup(*[Arrow(steps[i].get_right(), steps[i + 1].get_left(), buff=0.05, stroke_width=2.5,
                             color=GREY_B, max_tip_length_to_length_ratio=0.25) for i in range(2)])
        eq = tree_node(r"=", GREY_B)
        lft = tree_node(r"column \texttt{id}", DATA)
        bound = tree_node(r"string \texttt{'id'}", YES)
        hole = tree_node(r"?", HEAD, w=bound.width)
        kids = VGroup(lft, hole).arrange(RIGHT, buff=0.35)
        tr = VGroup(eq, kids).arrange(DOWN, buff=0.4).move_to([-4.6, 0.45, 0])
        es = VGroup(Line(eq.get_bottom(), lft.get_top(), color=GREY_B, stroke_width=1.6),
                    Line(eq.get_bottom(), hole.get_top(), color=GREY_B, stroke_width=1.6))
        bound.move_to(hole)
        trl = label(rf"bound value \texttt{{id}}: \ {len(s['id_leak']['param_value_id']['rows'])} rows",
                    font_size=18, color=YES).next_to(tr, DOWN, buff=0.25)

        def res(rows, err):
            if err:
                return r"parse error"
            n = len(rows)
            return rf"{n} row" + ("" if n == 1 else "s")
        rows = []
        for t in s["login"]:
            rows.append([t["username"], res(t["concat_rows"], t["concat_error"]), res(t["param_rows"], None)])
        leak = s["id_leak"]
        rows.append(["id", res(leak["concat_id_eq_id"]["rows"], None), res(leak["param_value_id"]["rows"], None)])
        tab = grid_table([r"user input", r"pasted in", r"bound"], rows, widths=[2.6, 2.0, 1.4], row_h=0.44,
                         font_size=19, mono_cols=(0,))
        tab.move_to([1.0, -0.5, 0])
        for r, t in enumerate(s["login"], start=1):
            bad = t["concat_error"] or (t["concat_rows"] and t["label"].startswith(("taut", "comm")))
            tab.cells[r][1].set_color(NO if bad else WHITE)
            tab.cells[r][2].set_color(YES)
        tab.cells[len(rows)][1].set_color(NO)
        tab.cells[len(rows)][2].set_color(YES)
        lab = VGroup(*[label(t["label"], font_size=16, color=GREY_B) for t in s["login"]] +
                     [label(r"the id lookup", font_size=16, color=GREY_B)])
        for k, L in enumerate(lab):
            L.next_to(tab.cells[k + 1][2], RIGHT, buff=0.45).align_to([4.25, 0, 0], LEFT)
        note = wrapped_label(r"our engine knows no \texttt{OR} and no comments, \ so the classic payloads stop it with "
                             r"a parse error \ --- \ which is itself the symptom: \ the input reached the parser", 12.4,
                             font_size=19, color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The cure is not to hunt for dangerous characters. It is Part 12's lesson about parsing. <bookmark "
            "mark='a'/> Parse the template once, with a hole for each value, so the tree's shape is fixed before any "
            "input arrives; then drop values in as finished leaves, never as text. <bookmark mark='b'/> Bound this "
            "way, i, d is just a string, and no user has that name. <bookmark mark='c'/> Run the classic login "
            "payloads both ways. Pasted in, they reach our parser, which stops on syntax it lacks; a full database "
            "would have obeyed. Bound, each is merely a strange username."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(st) for st in steps], lag_ratio=0.4), *[GrowArrow(a) for a in arr])
            self.play(FadeIn(eq), FadeIn(kids), Create(es))
            vo.wait_until("b")
            self.play(ReplacementTransform(hole, bound), FadeIn(trl))
            vo.wait_until("c")
            self.play(FadeIn(tab), FadeIn(lab))
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    def pki(self):
        head = label(r"When a trust anchor fails: \ DigiNotar \ (2011)", font_size=36).to_edge(UP, buff=0.3)
        store = cbox(r"your browser's root store", KERN, w=4.0, h=0.5, size=19, fill=0.12).move_to([-3.3, 2.2, 0])
        cas = VGroup(*[cbox(n, NO if n == "DigiNotar" else GREY_B, w=1.6 if n == "DigiNotar" else 1.25, h=0.46,
                            size=16) for n in (r"CA", r"DigiNotar", r"CA", r"CA")]).arrange(RIGHT, buff=0.12)
        cas.move_to([-3.3, 1.05, 0])
        dots = label(r"\dots", font_size=24, color=GREY_B).next_to(cas, RIGHT, buff=0.12)
        le = VGroup(*[Line(store.get_bottom(), c.get_top(), color=GREY_C, stroke_width=1.3) for c in cas])
        real = cbox(r"google.com", YES, w=2.3, h=0.46, size=17, use_mono=True).move_to([-5.0, -0.35, 0])
        fake = cbox(r"*.google.com", NO, w=2.3, h=0.46, size=17, use_mono=True).move_to([-1.6, -0.35, 0])
        e1 = Arrow(cas[0].get_bottom(), real.get_top(), buff=0.05, stroke_width=2.2, color=YES,
                   max_tip_length_to_length_ratio=0.12)
        e2 = Arrow(cas[1].get_bottom(), fake.get_top(), buff=0.05, stroke_width=2.2, color=NO,
                   max_tip_length_to_length_ratio=0.12)
        both = label(r"both accepted: \ any trusted CA may vouch for any name", font_size=18,
                     color=HEAD).next_to(VGroup(real, fake), DOWN, buff=0.3).set_x(-3.3)
        ill = label(r"schematic", font_size=16, color=GREY_B).next_to(both, DOWN, buff=0.12).set_x(-3.3)
        notes = VGroup(
            wrapped_label(r"2011: \ DigiNotar was broken into; \ a rogue certificate for \texttt{*.google.com} was "
                          r"used to intercept users in Iran", 5.4, font_size=19, color=NO),
            wrapped_label(r"Chrome, \ which pinned Google's keys, \ flagged it; \ every browser then removed "
                          r"DigiNotar, \ and the company went bankrupt that year", 5.4, font_size=19, color=WHITE),
            wrapped_label(r"\textbf{Certificate Transparency} \ (RFC 6962, \ 2013): \ certificates go into public, "
                          r"append-only Merkle logs \ (Part 29), \ so a rogue one cannot stay hidden", 5.4,
                          font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.7, 0.2, 0])
        foot = wrapped_label(r"a chain of trust is as strong as its weakest anchor", 12.4, font_size=21,
                             color=HEAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Beneath it all sits Part 30's public-key infrastructure, and it can fail too. <bookmark mark='a'/> Your "
            "browser trusts a store of root authorities, and any of them may vouch for any name. <bookmark mark='b'/> "
            "In 2011 the Dutch authority DigiNotar was broken into, and a certificate for every google dot com "
            "address was issued and used to intercept users in Iran. <bookmark mark='c'/> Chrome, which pinned "
            "Google's keys, noticed; the browsers removed DigiNotar, and it was bankrupt within the year. <bookmark "
            "mark='d'/> The structural fix, Certificate Transparency, from 2013, puts every certificate in public, "
            "append-only Merkle logs, so a rogue one cannot hide."
        ) as vo:
            self.play(FadeIn(head), FadeIn(store))
            vo.wait_until("a")
            self.play(Create(le), FadeIn(cas), FadeIn(dots))
            self.play(GrowArrow(e1), FadeIn(real))
            vo.wait_until("b")
            self.play(GrowArrow(e2), FadeIn(fake), FadeIn(notes[0]))
            self.play(FadeIn(both), FadeIn(ill))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES, PART, mono, tag_box)
