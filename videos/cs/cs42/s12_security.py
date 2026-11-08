from __future__ import annotations

from urllib.parse import urlsplit

from explainer.cs import *  # noqa: F403
from videos.cs.cs42.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, grid_table, load,
                                   module_box, mono, tag_box)

# the six requests of compute_cors, as the screen names them (the data's own names, checked below)
CASES = {"same origin": r"GET, \ same origin",
         "another origin, no CORS header": r"GET, \ no CORS header",
         "another origin that allows us": r"GET, \ server allows shop.example",
         "a PUT with a JSON header": r"PUT with an X-Token header, \ both allowed",
         "a PUT the server did not allow": r"PUT, \ not allowed",
         "cookies to an origin allowing *": r"GET with cookies, \ server allows *"}
WHY = {"same origin": r"same origin",
       "allowed": r"the server opted in",
       "sent, but the response is withheld from the script": r"sent; \ response withheld",
       "preflight refused; the request is never sent": r"preflight refused; \ never sent"}


def _origin(url):
    u = urlsplit(url)
    return u.scheme, u.hostname, u.port or {"http": 80, "https": 443}[u.scheme]


class Security(VoiceoverScene):
    def construct(self):
        self.card()
        self.origins()
        self.cors()
        self.xss()
        self.csp()
        self.csrf()
        self.isolation()
        self.wasm()

    def card(self):
        card = chapter_card(11, r"The security model", r"How can one program safely run code from strangers?",
                            lit=(1995, 2017, 2018), extra=((1995, r"JavaScript; \ the same-origin policy"),
                                                           (2017, r"WebAssembly"),
                                                           (2018, r"Spectre; \ site isolation")), part=PART)
        with self.voiceover("Chapter eleven. The security model."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def origins(self):
        d = load("cors")
        head = label(r"The same-origin policy", font_size=36).to_edge(UP, buff=0.3)
        url = Text("https://a.example:443/cart?id=7", font="DejaVu Sans Mono", font_size=30,
                   t2c={"https": DATA, "a.example": LAM, ":443": KERN, "/cart?id=7": GREY_C}).move_to([0, 1.95, 0])
        parts = [(url[0:5], DATA, r"URL scheme", DOWN), (url[8:17], LAM, r"host", DOWN),
                 (url[18:21], KERN, r"port\\(443 if omitted)", DOWN), (url[21:], GREY_C, r"path: \ not part of "
                                                                                       r"the origin", UP)]
        braces = VGroup()
        for mob, col, txt, side in parts:
            b = Brace(mob, side, color=col, buff=0.08)
            t = (wrapped_label(txt, 3.0, font_size=18, color=col) if r"\\" in txt else
                 label(txt, font_size=18, color=col))
            t.next_to(b, side, buff=0.08)
            braces.add(VGroup(b, t))
        rows, colors = [], []
        for a, b, same in d["origins"]:
            oa, ob = _origin(a), _origin(b)
            assert (oa == ob) == same
            diff = [n for n, x, y in zip(("scheme", "host", "port"), oa, ob) if x != y]
            rows.append([a, b, r"yes: \ only the path differs" if same else rf"no: \ the {diff[0]} differs"])
            colors.append([WHITE, WHITE, YES if same else NO])
        tab = grid_table([r"this page", r"the other URL", r"same origin?"], rows, widths=[4.1, 4.5, 3.8],
                         row_h=0.46, font_size=19, colors=colors, mono_cols=(0, 1))
        tab.move_to([0, -0.75, 0])
        rule = wrapped_label(r"a page may \textbf{embed} images, \ scripts and frames from anywhere, \ and "
                             r"\textbf{send} requests anywhere; \ its scripts may \textbf{read} only what their own "
                             r"origin serves", 12.6, font_size=20, color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "A browser runs code from every site you visit, so its first rule is about who may read what. <bookmark "
            "mark='a'/> An origin is three things: the scheme, the host and the port. The path does not count. "
            "<bookmark mark='b'/> Two pages share an origin only if all three match. Change https to http, add a port,"
            " or move to a subdomain, and they are strangers. <bookmark mark='c'/> A page may embed images, scripts "
            "and frames from anywhere, and send requests anywhere, but its scripts may read only what their own origin"
            " serves."
        ) as vo:
            self.play(FadeIn(head), Write(url))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in braces], lag_ratio=0.3), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[0])), Create(tab.rule))
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.4), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()

    def cors(self):
        d = load("cors")
        assert [r["case"] for r in d["rows"]] == list(CASES)
        head = label(r"CORS: \ the server opts in", font_size=36).to_edge(UP, buff=0.3)
        browser = RoundedRectangle(width=4.4, height=1.3, corner_radius=0.12, stroke_color=KERN,
                                   stroke_width=2).move_to([-4.4, 2.05, 0])
        btitle = label(r"browser", font_size=17, color=KERN).next_to(browser.get_corner(UL), DR, buff=0.1)
        script = tag_box("script on shop.example", color=DATA, size=16).move_to(browser).shift(LEFT * 0.3 +
                                                                                            DOWN * 0.15)
        server = RoundedRectangle(width=3.2, height=1.3, corner_radius=0.12, stroke_color=LAM,
                                  stroke_width=2).move_to([5.0, 2.05, 0])
        sname = mono("api.other.example", size=17, color=LAM).move_to(server)
        xl, xr = browser.get_right()[0], server.get_left()[0]
        req = Arrow([xl, 2.35, 0], [xr, 2.35, 0], buff=0.05, color=DATA, stroke_width=3)
        reqt = mono("GET /data", size=16, color=DATA).next_to(req, UP, buff=0.06)
        resp = Arrow([xr, 1.75, 0], [xl, 1.75, 0], buff=0.05, color=GREY_B, stroke_width=3)
        respt = mono("200 OK, with a body", size=16, color=GREY_B).next_to(resp, DOWN, buff=0.06)
        wall = Line([xl - 0.2, 1.45, 0], [xl - 0.2, 2.0, 0], color=NO, stroke_width=7)
        held = label(r"withheld from the script", font_size=18, color=NO).move_to(respt)
        hdr = mono("Access-Control-Allow-Origin: https://shop.example", size=16, color=YES)
        hdr.next_to(VGroup(browser, server), DOWN, buff=0.15)
        ok = label(r"readable: \ the header names our origin", font_size=18, color=YES).move_to(respt)
        rows, colors = [], []
        for r in d["rows"]:
            rows.append([CASES[r["case"]], r"yes" if r["preflight"] else r"no", r"yes" if r["readable"] else r"no",
                         WHY[r["why"]]])
            colors.append([WHITE, HEAD if r["preflight"] else GREY_B, YES if r["readable"] else NO,
                           GREY_A])
        tab = grid_table([r"request from shop.example", r"preflight", r"script reads it", r"why"], rows,
                         widths=[5.0, 1.6, 2.2, 3.8], row_h=0.4, font_size=18, colors=colors, mono_cols=())
        tab.next_to(hdr, DOWN, buff=0.3).set_x(0)
        lines = wrapped_label(r"a \textbf{preflight} is an \texttt{OPTIONS} request asking permission first; \ CORS "
                              r"guards reading, \ not sending: \ a simple request reaches the server either way",
                              12.6, font_size=19, color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Reading across origins needs the server to opt in. <bookmark mark='a'/> The browser sends the request, "
            "but when the response returns, it looks for a header naming the page's origin. Without one, the script "
            "never sees it. <bookmark mark='b'/> Here are six requests from a shop's page, decided by our model of the"
            " rules. A plain GET is always sent, but readable only if the server allows us. <bookmark mark='c'/> A PUT"
            " or a custom header could do things an old server never expected, so the browser first asks permission "
            "with a preflight, and if refused, never sends the request. And a request with cookies must be allowed by "
            "name, not by a wildcard."
        ) as vo:
            self.play(FadeIn(head), Create(browser), FadeIn(btitle), FadeIn(script), Create(server), FadeIn(sname))
            vo.wait_until("a")
            self.play(GrowArrow(req), FadeIn(reqt))
            self.play(GrowArrow(resp), FadeIn(respt))
            self.play(Create(wall), Transform(respt, held), resp.animate.set_color(NO))
            self.wait(1.0)
            self.play(FadeIn(hdr), FadeOut(wall), Transform(respt, ok), resp.animate.set_color(YES))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[0])), Create(tab.rule))
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:4]], lag_ratio=0.4), run_time=1.8)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[4:]], lag_ratio=0.4), run_time=1.8)
            self.play(FadeIn(lines))
        self.wait(0.4)
        self.clear_scene()

    @staticmethod
    def _tree(outline, x0, y0):
        """Draw an outline from our parser (two spaces per level) as an indented tree; returns nodes and lines."""
        nodes, links, stack, y = VGroup(), VGroup(), [], y0
        for ln in outline:
            depth = (len(ln) - len(ln.lstrip(" "))) // 2
            txt = ln.strip()
            if txt.startswith("'") and len(txt) - 2 >= 30:      # our outline cuts text at 30 characters
                txt = txt[:-1] + "…'"
            bad = "onerror" in txt and txt.startswith("<")
            col = NO if bad else (DATA if txt.startswith("<") else GREY_A)
            if bad:
                a, b = txt.split(" onerror", 1)
                body = code_block([a, "  onerror" + b], size=16, color=col, buff=0.06)
            else:
                body = code_block([txt], size=16, color=col)
            box = SurroundingRectangle(body, buff=0.1, corner_radius=0.06, stroke_color=col, stroke_width=1.8,
                                       fill_color=NO if bad else BG, fill_opacity=0.18 if bad else 1)
            node = VGroup(box, body)
            node.move_to([0, 0, 0]).align_to([x0 + 0.5 * depth, y, 0], UL)
            y = node.get_bottom()[1] - 0.14
            del stack[depth:]
            if stack:
                p = stack[-1][0]
                px = p.get_left()[0] + 0.22
                links.add(VMobject(stroke_color=GREY_C, stroke_width=1.6).set_points_as_corners(
                    [[px, p.get_bottom()[1], 0], [px, node.get_y(), 0], [node.get_left()[0], node.get_y(), 0]]))
            stack.append(node)
            nodes.add(node)
        return nodes, links

    def xss(self):
        x = load("xss")
        assert x["handlers"] and x["handlers"][0][:2] == ["img", "onerror"]
        head = label(r"Cross-site scripting", font_size=36).to_edge(UP, buff=0.3)
        tmpl = code_block(['html = "<p>Hello, " + name + "!</p>"', f"name = '{x['name']}'"], size=17)
        tmpl[1].set_color(NO)
        tmpl.move_to([0, 2.45, 0]).to_edge(LEFT, buff=0.4)

        def three(s):
            a, b = s.split(" onerror", 1)
            b = "onerror" + b
            i = b.index(")") + 1
            return [a, b[:i], b[i:]]
        cols = []
        for key, outline, title, tcol, x0 in (("raw", "raw_outline", r"inserted as written", NO, -6.5),
                                              ("escaped", "escaped_outline", r"escaped first", YES, 0.7)):
            t = label(title, font_size=21, color=tcol)
            src = code_block(three(x[key]), size=16, color=GREY_A)
            top = VGroup(t, src).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            top.move_to([0, 0, 0]).align_to([x0, 1.75, 0], UL)
            nodes, links = self._tree(x[outline], x0, top.get_bottom()[1] - 0.25)
            cols.append((top, nodes, links))
        bad = cols[0][1][2]
        notes = VGroup(
            wrapped_label(r"the image fails to load, \ and its handler runs with all of the page's authority: \ "
                          r"\textbf{cross-site scripting}", 12.6, font_size=19, color=NO),
            wrapped_label(r"escaped, \ the angle brackets and quotes become character references: \ the same parser "
                          r"makes one text node, \ shown, \ not run", 12.6, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The commonest attack breaks no rule: it gets the attacker's code served from your origin. <bookmark "
            "mark='a'/> A page greets users by pasting their name into its HTML, and someone picks a name that is "
            "itself HTML. <bookmark mark='b'/> Our parser from Chapter 2 builds the tree, and beside the greeting is "
            "an image with an error handler. The image fails to load, the handler runs with the page's authority, and "
            "the cookies go wherever it sends them. This is cross-site scripting. <bookmark mark='c'/> Escape the "
            "name, so the angle brackets become character references, and the same parser makes one text node: shown, "
            "not run."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tmpl[0]))
            vo.wait_until("a")
            self.play(FadeIn(tmpl[1]))
            vo.wait_until("b")
            top, nodes, links = cols[0]
            self.play(FadeIn(top))
            self.play(LaggedStart(*[FadeIn(n) for n in nodes], lag_ratio=0.3), Create(links), run_time=1.6)
            self.play(Indicate(bad, color=NO, scale_factor=1.06), FadeIn(notes[0]))
            vo.wait_until("c")
            top, nodes, links = cols[1]
            self.play(FadeIn(top))
            self.play(LaggedStart(*[FadeIn(n) for n in nodes], lag_ratio=0.3), Create(links), FadeIn(notes[1]),
                      run_time=1.6)
        self.wait(0.4)
        self.clear_scene()

    def csp(self):
        head = label(r"Content Security Policy", font_size=36).to_edge(UP, buff=0.3)
        hdr = mono("Content-Security-Policy: script-src 'self'", size=22, color=KERN).move_to([0, 2.35, 0])
        items = [('<script src="/app.js">', YES, r"same origin: \ runs"),
                 ('onerror="steal(document.cookie)"', NO, r"an inline handler: \ refused"),
                 ('<script src="https://evil.example/x.js">', NO, r"another origin: \ refused")]
        rows = VGroup()
        for i, (code, col, why) in enumerate(items):
            mark = MathTex(r"\checkmark" if col == YES else r"\times", font_size=34, color=col)
            c = mono(code, size=18, color=GREY_A)
            w = label(why, font_size=20, color=col)
            row = VGroup(mark, c).arrange(RIGHT, buff=0.3)
            row.move_to([0, 1.3 - 0.62 * i, 0]).align_to([-6.0, 0, 0], LEFT)
            w.move_to([0, row.get_y(), 0]).align_to([2.5, 0, 0], LEFT)
            rows.add(VGroup(row, w))
        cookie = mono("Set-Cookie: session=...; HttpOnly; Secure; SameSite=Lax", size=18, color=HEAD)
        cookie.next_to(rows, DOWN, buff=0.6).align_to([-6.0, 0, 0], LEFT)
        lines = VGroup(
            wrapped_label(r"a whitelist sent by the server: \ the browser refuses, \ and can report, \ every script "
                          r"it does not allow; \ a second line of defence, \ behind escaping", 12.4, font_size=20,
                          color=WHITE),
            wrapped_label(r"\texttt{HttpOnly}: \ scripts cannot read the cookie at all, \ so even code that does "
                          r"run cannot steal the session", 12.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A Content Security Policy is the second line of defence. <bookmark mark='a'/> The server lists where "
            "scripts may come from, here only its own origin, <bookmark mark='b'/> and the browser refuses "
            "everything else: inline handlers like our injected one, and scripts from other origins. "
            "<bookmark mark='c'/> And marking the session cookie HttpOnly hides it from scripts altogether."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hdr), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]), FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(cookie), FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def csrf(self):
        head = label(r"Cookies, \ CSRF and SameSite", font_size=36).to_edge(UP, buff=0.3)
        evil = RoundedRectangle(width=5.4, height=1.4, corner_radius=0.12, stroke_color=NO,
                                stroke_width=2).move_to([-3.9, 1.9, 0])
        etitle = mono("evil.example", size=17, color=NO).next_to(evil.get_corner(UL), DR, buff=0.1)
        form = code_block(['<form method=POST', '  action="https://bank.example/pay">'], size=16,
                          color=GREY_A).next_to(etitle, DOWN, buff=0.12).align_to(etitle, LEFT)
        bank = RoundedRectangle(width=3.0, height=1.4, corner_radius=0.12, stroke_color=DATA,
                                stroke_width=2).move_to([5.1, 1.9, 0])
        bname = mono("bank.example", size=17, color=DATA).move_to(bank)
        post = Arrow(evil.get_right(), bank.get_left(), buff=0.05, color=GREY_B, stroke_width=3)
        chip = tag_box("session=...", color=NO, size=16).next_to(post, UP, buff=0.08)
        verdict = label(r"the bank sees you signed in", font_size=18, color=NO).next_to(post, DOWN, buff=0.12)
        verdict2 = label(r"no cookie: \ refused", font_size=18, color=YES).move_to(verdict)
        tab = grid_table([r"SameSite", r"the cookie is sent on a cross-site request"],
                         [[r"Strict", r"never"],
                          [r"Lax", r"only on a top-level navigation, \ such as following a link, \ with GET"],
                          [r"None", r"always \ (and the cookie must be Secure)"]],
                         widths=[2.2, 10.0], row_h=0.48, font_size=19, mono_cols=())
        tab.next_to(VGroup(evil, bank), DOWN, buff=0.75).set_x(0)
        tab.cells[2][0].set_color(YES)
        lines = VGroup(
            wrapped_label(r"since 2020, \ Chrome treats a cookie without the attribute as Lax", 12.4, font_size=19,
                          color=HEAD),
            wrapped_label(r"a \textbf{site} is a scheme and a registrable domain: \ \texttt{a.example} and "
                          r"\texttt{b.a.example} are two origins, \ but one site", 12.4, font_size=19,
                          color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Cookies bring the opposite danger. <bookmark mark='a'/> The browser attaches a site's cookies to every "
            "request to that site, whoever starts it, so another site's page can submit a hidden form to your bank, "
            "which sees you signed in: cross-site request forgery. <bookmark mark='b'/> The SameSite attribute stops "
            "it. A Lax cookie crosses sites only when you follow a link at the top level; a Strict cookie never does. "
            "<bookmark mark='c'/> Since 2020, Chrome treats a cookie without the attribute as Lax."
        ) as vo:
            self.play(FadeIn(head), Create(evil), FadeIn(etitle), FadeIn(form), Create(bank), FadeIn(bname))
            vo.wait_until("a")
            self.play(GrowArrow(post), FadeIn(chip, shift=RIGHT * 0.3))
            self.play(FadeIn(verdict))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[0])), Create(tab.rule), *[FadeIn(VGroup(*r)) for r in tab.cells[1:]])
            self.play(Indicate(VGroup(*tab.cells[2]), color=YES), chip.animate.set_opacity(0.15),
                      Transform(verdict, verdict2))
            vo.wait_until("c")
            self.play(FadeIn(lines))
        self.wait(0.4)
        self.clear_scene()

    def isolation(self):
        head = label(r"Processes, \ sandboxes, \ site isolation", font_size=36).to_edge(UP, buff=0.3)

        def frame(name, col):
            return module_box(rf"\texttt{{{name}}}", col, w=2.2, h=0.55, font=17)

        def proc(title, inner, col=GREY_B, w=2.7):
            body = VGroup(*inner).arrange(DOWN, buff=0.15)
            box = RoundedRectangle(width=w, height=body.height + 0.75, corner_radius=0.1, stroke_color=col,
                                   stroke_width=2)
            t = label(title, font_size=17, color=col).next_to(box.get_top(), DOWN, buff=0.1)
            body.next_to(t, DOWN, buff=0.12)
            return VGroup(box, t, body)
        # before: one renderer holds both sites
        one = proc(r"one renderer process", [frame("bank.example", DATA), frame("evil.example", NO)], w=3.2)
        one.move_to([-4.4, 0.85, 0])
        a, b = one[2][0], one[2][1]
        leak = CurvedArrow(b.get_left() + LEFT * 0.05, a.get_left() + LEFT * 0.05, angle=-TAU / 4, color=NO,
                           stroke_width=3)
        leak_t = label(r"speculative read \ (Part 8)", font_size=17, color=NO).next_to(one, DOWN, buff=0.15)
        before_t = label(r"before", font_size=20, color=GREY_A).next_to(one, UP, buff=0.15)
        # after: a browser process over one sandboxed renderer per site
        bp = module_box(r"browser process: \ files, \ network, \ the screen", KERN, w=5.6, h=0.55, font=17)
        r1 = proc(r"renderer \ (sandboxed)", [frame("bank.example", DATA)], col=YES)
        r2 = proc(r"renderer \ (sandboxed)", [frame("evil.example", NO)], col=YES)
        rr = VGroup(r1, r2).arrange(RIGHT, buff=0.4)
        after = VGroup(bp, rr).arrange(DOWN, buff=0.45).move_to([3.4, 0.75, 0])
        ipc = VGroup(*[Line(bp.get_bottom() + RIGHT * dx, r.get_top(), color=GREY_C, stroke_width=1.6)
                       for dx, r in ((-1.4, r1), (1.4, r2))])
        after_t = label(r"after: \ site isolation", font_size=20, color=YES).next_to(after, UP, buff=0.15)
        arrow = Arrow([-2.4, 0.85, 0], [0.2, 0.85, 0], color=GREY_B, stroke_width=3, buff=0)
        lines = VGroup(
            wrapped_label(r"Spectre \ (2018): \ speculative execution plus cache timing lets a script read memory "
                          r"in its own process, \ whatever the language's checks say", 12.6, font_size=19, color=NO),
            wrapped_label(r"so each site gets its own process, \ and the hardware's memory protection \ (Part 32) "
                          r"keeps them apart", 12.6, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "<bookmark mark='a'/> Browsers split themselves into processes: a privileged browser process, and "
            "sandboxed renderers that run pages and cannot touch files or the network directly. <bookmark mark='b'/> "
            "In 2018, Spectre showed that speculative execution, from Part 8, lets a script read memory in its own "
            "process through cache timing, so an attacker's frame could read the page beside it. <bookmark mark='c'/> "
            "The answer was site isolation: each site gets its own renderer process, kept apart by the hardware's "
            "memory protection rather than the engine's checks."
        ) as vo:
            self.play(FadeIn(head), FadeIn(one), FadeIn(before_t))
            vo.wait_until("a")
            self.play(FadeIn(bp))
            vo.wait_until("b")
            self.play(Create(leak), FadeIn(leak_t), FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(GrowArrow(arrow), FadeIn(rr), Create(ipc), FadeIn(after_t), FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def wasm(self):
        head = label(r"WebAssembly", font_size=36).to_edge(UP, buff=0.3)
        steps = [module_box(r"C, \ C++, \ Rust", DATA, w=2.0), module_box(r"a compiler", GREY_B, w=1.8),
                 module_box(r"\texttt{.wasm}: \ typed bytecode", LAM, w=2.9),
                 module_box(r"validate", YES, w=1.6), module_box(r"compile to machine code", KERN, w=3.1)]
        row = VGroup(*steps).arrange(RIGHT, buff=0.45).move_to([0, 1.7, 0])
        if row.width > 13.4:
            row.width = 13.4
        arrows = VGroup(*[Arrow(steps[i].get_right(), steps[i + 1].get_left(), buff=0.05, stroke_width=2.5,
                                color=GREY_B, max_tip_length_to_length_ratio=0.3) for i in range(4)])
        sandbox = DashedVMobject(SurroundingRectangle(VGroup(steps[3], steps[4]), buff=0.22, corner_radius=0.1,
                                                      color=YES, stroke_width=2), num_dashes=60)
        sb_t = label(r"inside the browser's sandbox", font_size=17, color=YES).next_to(sandbox, DOWN, buff=0.1)
        # linear memory: one array of bytes; an access past its end traps
        n = 16
        cells = VGroup(*[Square(0.42, stroke_color=GREY_C, stroke_width=1.5, fill_color=LAM,
                                fill_opacity=0.2) for _ in range(n)]).arrange(RIGHT, buff=0).move_to([-0.6, -0.6, 0])
        mem_t = label(r"linear memory: \ the only memory the module can address", font_size=18,
                      color=LAM).next_to(cells, UP, buff=0.15)
        out = Square(0.42, stroke_color=NO, stroke_width=2).next_to(cells, RIGHT, buff=0.35)
        ok_ptr = Arrow(cells[5].get_bottom() + DOWN * 0.6, cells[5].get_bottom(), buff=0.03, color=YES,
                       stroke_width=3, max_tip_length_to_length_ratio=0.3)
        bad_ptr = Arrow(out.get_bottom() + DOWN * 0.6, out.get_bottom(), buff=0.03, color=NO, stroke_width=3,
                        max_tip_length_to_length_ratio=0.3)
        trap = label(r"out of bounds: \ trap", font_size=18, color=NO).next_to(bad_ptr, DOWN, buff=0.08)
        ok_t = label(r"in bounds", font_size=18, color=YES).next_to(ok_ptr, DOWN, buff=0.08)
        lines = wrapped_label(r"shipped in every major browser in 2017: \ near-native speed for compiled languages, "
                              r"\ with no new way out of the sandbox; \ the engine compiles it like Part 15's JIT, \ "
                              r"but from a typed format it can check first", 12.6, font_size=19,
                              color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "WebAssembly, in every major browser since 2017, brings compiled languages into the same sandbox. "
            "<bookmark mark='a'/> C, C++ or Rust compile to a compact, typed bytecode. The browser validates it "
            "before it runs, then compiles it to machine code, as Part 15's JIT did. <bookmark mark='b'/> A module "
            "can address only its own linear memory, and an access outside it traps."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in steps], lag_ratio=0.3), Create(arrows), run_time=2)
            self.play(Create(sandbox), FadeIn(sb_t), FadeIn(lines))
            vo.wait_until("b")
            self.play(FadeIn(cells), FadeIn(mem_t), FadeIn(out))
            self.play(GrowArrow(ok_ptr), FadeIn(ok_t))
            self.play(GrowArrow(bad_ptr), FadeIn(trap), out.animate.set_fill(NO, opacity=0.3))
        self.wait(0.4)
        self.clear_scene()


_ = (HEAD,)
