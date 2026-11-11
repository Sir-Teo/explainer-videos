from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs42.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, module_box, mono

# the strip across the top of every section: 1988 to 2020
Y0, Y1 = 1988, 2020
XL, XR, YA = -6.2, 6.2, 2.55


def X(yr: float) -> float:
    return XL + (XR - XL) * (yr - Y0) / (Y1 - Y0)


def piece(title, sub, color, w=3.8, h=1.05):
    """A titled box: one of the web's inventions, or one of its layers."""
    box = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=color, stroke_width=2,
                           fill_color=color, fill_opacity=0.12)
    t = label(title, font_size=24, color=color)
    s = wrapped_label(sub, w - 0.3, font_size=18, color=GREY_A)
    VGroup(t, s).arrange(DOWN, buff=0.1).move_to(box)
    return VGroup(box, t, s)


class History(VoiceoverScene):
    def construct(self):
        self.card()
        self.strip()
        self.proposal()
        self.mosaic()
        self.layers()
        self.ajax()
        self.engines()
        self.standard()

    def card(self):
        card = chapter_card(1, r"Thirty years of the web", r"How did a format for documents become a platform?",
                            lit=(1989, 1995, 2005), extra=((1989, r"Berners-Lee's proposal"),
                                                           (1995, r"JavaScript"), (2005, r"Ajax")), part=PART)
        with self.voiceover("Chapter one. Thirty years of the web."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ the strip that fills, section by section
    def strip(self):
        axis = Line([XL, YA, 0], [XR, YA, 0], color=GREY_D, stroke_width=2)
        ticks = VGroup()
        for yr in range(1990, 2021, 5):
            ticks.add(Line([X(yr), YA - 0.07, 0], [X(yr), YA + 0.07, 0], color=GREY_C, stroke_width=1.5),
                      label(f"{yr}", font_size=16, color=GREY_B).move_to([X(yr), YA - 0.28, 0]))
        self.bar = Rectangle(width=0.01, height=0.09, stroke_width=0, fill_color=YES, fill_opacity=0.8)
        self.bar.move_to([X(1989), YA, 0], aligned_edge=LEFT)
        self.dots = VGroup()
        self.tl = VGroup(axis, ticks, self.bar, self.dots)
        self.lit = []

    def mark(self, years, upto):
        """Animations that fill the strip up to ``upto`` and light this section's years."""
        new = Rectangle(width=X(upto) - X(1989), height=0.09, stroke_width=0, fill_color=YES, fill_opacity=0.8)
        new.move_to([X(1989), YA, 0], aligned_edge=LEFT)
        anims = [Transform(self.bar, new)]
        anims += [d.animate.set_color(GREY_B).scale(0.7) for d in self.lit]
        self.lit = []
        for yr in years:
            d = Dot([X(yr), YA, 0], radius=0.085, color=HEAD)
            self.dots.add(d)
            self.lit.append(d)
            anims.append(FadeIn(d, scale=2))
        return anims

    def proposal(self):
        head = label(r"A proposal at CERN", font_size=36).to_edge(UP, buff=0.3)
        parts = VGroup(piece(r"URL", r"a name for every document, \ on any machine", DATA),
                       piece(r"HTTP", r"a protocol for fetching one", KERN),
                       piece(r"HTML", r"a format for it, \ with links to others", HEAD)).arrange(RIGHT, buff=0.4)
        parts.move_to([0, 1.15, 0])
        client = piece(r"WorldWideWeb", r"browser and editor, \ NeXT, \ 1990", LAM, w=2.8, h=1.2)
        client.move_to([-5.4, -0.9, 0])
        server = piece(r"the first server", r"\texttt{info.cern.ch}, \ NeXT", YES, w=2.8, h=1.2).move_to([5.4, -0.9, 0])
        req = Arrow([-3.95, -0.6, 0], [3.95, -0.6, 0], buff=0, stroke_width=2.5, color=KERN,
                    max_tip_length_to_length_ratio=0.03)
        req_t = mono("GET /hypertext/WWW/TheProject.html", size=17, color=KERN).next_to(req, UP, buff=0.1)
        resp = Arrow([3.95, -1.2, 0], [-3.95, -1.2, 0], buff=0, stroke_width=2.5, color=HEAD,
                     max_tip_length_to_length_ratio=0.03)
        resp_t = mono("<TITLE>The World Wide Web project</TITLE> ...", size=17, color=HEAD).next_to(resp, DOWN,
                                                                                                    buff=0.1)
        doc = RoundedRectangle(width=4.6, height=2.6, corner_radius=0.1, stroke_color=GREY_B, stroke_width=1.5,
                               fill_color=BG, fill_opacity=1).move_to([0, 0.2, 0])
        doc_t = VGroup(label(r"Information Management: \ a Proposal", font_size=24, color=WHITE),
                       label(r"Tim Berners-Lee, \ CERN, \ March 1989", font_size=19, color=GREY_A)).arrange(
            DOWN, buff=0.2).move_to(doc).shift(UP * 0.3)
        boxes_ = VGroup(*[module_box(t, c, w=1.1, h=0.45, font=16) for t, c in ((r"page", DATA), (r"page", DATA),
                                                                                 (r"page", DATA))])
        boxes_.arrange(RIGHT, buff=0.35).next_to(doc_t, DOWN, buff=0.3)
        links_ = VGroup(*[Arrow(boxes_[k].get_right(), boxes_[k + 1].get_left(), buff=0.04, stroke_width=1.5,
                                color=GREY_B, max_tip_length_to_length_ratio=0.3) for k in range(2)])
        vague = label(r"``Vague but exciting''", font_size=21, color=HEAD).rotate(0.12).next_to(doc, UR, buff=-0.35)
        prop = VGroup(doc, doc_t, boxes_, links_, vague)
        cap = wrapped_label(r"the first HTTP: \ one line in, \ one document out, \ then the connection closes; \ "
                            r"no headers, \ no status codes", 12.4, font_size=20, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "In March 1989 Tim Berners-Lee, at CERN, proposed keeping track of the laboratory's information as "
            "documents linked to one another. His supervisor wrote on the cover: vague, but exciting. <bookmark "
            "mark='a'/> By the end of 1990 he had built the three pieces still underneath every page: a name for any "
            "document, which became the URL; a protocol for fetching it, HTTP; and a format with links, HTML. "
            "<bookmark mark='b'/> He wrote the first browser, called WorldWideWeb, on a NeXT computer, and the first "
            "server. <bookmark mark='c'/> In August 1991 he announced the project to the world."
        ) as vo:
            self.play(FadeIn(head), Create(self.tl[0]), FadeIn(self.tl[1]), FadeIn(self.bar))
            self.add(self.dots)
            self.play(*self.mark([1989], 1989.3), FadeIn(doc), FadeIn(doc_t))
            self.play(FadeIn(boxes_), Create(links_))
            self.play(FadeIn(vague, scale=1.3))
            vo.wait_until("a")
            self.play(FadeOut(prop))
            self.play(*self.mark([1990], 1990.9), LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in parts],
                                                             lag_ratio=0.4), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(client), FadeIn(server))
            self.play(GrowArrow(req), FadeIn(req_t))
            self.play(GrowArrow(resp), FadeIn(resp_t))
            vo.wait_until("c")
            self.play(*self.mark([1991], 1991.7), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene(self.tl)

    def mosaic(self):
        head = label(r"Pictures in the page", font_size=36).to_edge(UP, buff=0.3)
        win = RoundedRectangle(width=5.6, height=3.7, corner_radius=0.12, stroke_color=GREY_B, stroke_width=1.5,
                               fill_color=BG, fill_opacity=1).move_to([-3.6, -0.75, 0])
        bar = Rectangle(width=5.6, height=0.32, stroke_width=0, fill_color=GREY_D, fill_opacity=1).align_to(
            win, UP).set_x(win.get_x())
        page = VGroup()
        top = win.get_top()[1] - 0.7
        h1 = Rectangle(width=2.2, height=0.22, stroke_width=0, fill_color=WHITE, fill_opacity=0.85)
        h1.move_to([win.get_left()[0] + 0.3, top, 0], aligned_edge=LEFT)
        page.add(h1)
        for k, w in enumerate((4.8, 4.5, 3.1)):
            page.add(Rectangle(width=w, height=0.09, stroke_width=0, fill_color=GREY_B, fill_opacity=0.8).move_to(
                [win.get_left()[0] + 0.3, top - 0.45 - k * 0.25, 0], aligned_edge=LEFT))
        img = Rectangle(width=2.0, height=1.2, stroke_color=DATA, stroke_width=2, fill_color=DATA,
                        fill_opacity=0.35).move_to([win.get_left()[0] + 0.3, top - 1.85, 0], aligned_edge=LEFT)
        img_t = label(r"image", font_size=18, color=WHITE).move_to(img)
        after = VGroup(*[Rectangle(width=w, height=0.09, stroke_width=0, fill_color=GREY_B, fill_opacity=0.8)
                         .move_to([img.get_right()[0] + 0.25, img.get_top()[1] - 0.2 - k * 0.25, 0],
                                  aligned_edge=LEFT) for k, w in enumerate((2.2, 2.0, 2.3, 1.4))])
        illus = note(r"illustrative", font_size=16).next_to(win, DOWN, buff=0.1).align_to(win, LEFT)
        code = code_block(['<H1>Hydrogen</H1>', '<P>The simplest atom has one', 'proton and one electron.',
                           '<IMG SRC="atom.gif">', 'Its spectrum ...'], size=17)
        code[3].set_color(DATA)
        code.move_to([3.3, 0.85, 0])
        notes = VGroup(
            wrapped_label(r"1993: \ \textbf{Mosaic} \ (Andreessen and Bina, NCSA): \ an image tag that puts "
                          r"pictures among the words", 5.8, font_size=19, color=DATA),
            wrapped_label(r"April 1993: \ CERN puts the web's software in the public domain", 5.8, font_size=19,
                          color=YES),
            wrapped_label(r"1994: \ \textbf{Netscape} Navigator; \ Berners-Lee founds the \textbf{W3C} to write the "
                          r"standards", 5.8, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(code, DOWN, buff=0.45).align_to(code, LEFT)
        with self.voiceover(
            "The web spread when it became pleasant to look at. <bookmark mark='a'/> In 1993 Marc Andreessen and Eric"
            " Bina, at the National Center for Supercomputing Applications, released Mosaic, whose image tag put "
            "pictures in the page itself, among the words. <bookmark mark='b'/> That April, CERN put the web's "
            "software in the public domain. <bookmark mark='c'/> In 1994 Andreessen co-founded Netscape, whose "
            "Navigator soon dominated, and Berners-Lee founded the World Wide Web Consortium, the W3C, to write the "
            "standards."
        ) as vo:
            self.play(FadeIn(head), *self.mark([], 1992.5))
            vo.wait_until("a")
            self.play(*self.mark([1993], 1993.5), FadeIn(win), FadeIn(bar), FadeIn(page), FadeIn(code))
            self.play(GrowFromCenter(img), FadeIn(img_t), FadeIn(after), FadeIn(illus), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(*self.mark([1994], 1994.9), FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene(self.tl)

    def layers(self):
        head = label(r"Style and behaviour", font_size=36).to_edge(UP, buff=0.3)
        rows = [
            (r"HTML", r"what the page says", DATA, ['<h1>The web</h1>', '<button>more</button>'],
             r"structure: \ Berners-Lee, \ 1990; \ HTML 2.0 standardized in 1995"),
            (r"CSS", r"how it looks", LAM, ['h1 { color: navy;', '     font-size: 2em }'],
             r"proposed by H\aa kon Wium Lie, \ October 1994; \ CSS level 1 a W3C Recommendation, \ December 1996"),
            (r"JavaScript", r"what it does", HEAD, ['button.onclick = () =>', '  more.hidden = false'],
             r"Brendan Eich at Netscape, \ May 1995, \ in about ten days; \ shipped in Navigator 2; \ "
             r"standardized as ECMAScript, \ 1997"),
        ]
        g = VGroup()
        for name, sub, col, src, who in rows:
            box = piece(name, sub, col, w=2.6, h=1.1)
            code = code_block(src, size=16, color=col)
            cred = wrapped_label(who, 5.2, font_size=19, color=GREY_A)
            g.add(VGroup(box, code, cred))
        for r in g:
            r[1].next_to(r[0], RIGHT, buff=0.35)
            r[2].next_to(r[0], RIGHT, buff=3.75)
        g.arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to([0, -0.15, 0]).to_edge(LEFT, buff=0.35)
        for r in g:
            r[2].set_x(XR + 0.6 - r[2].width / 2)
        wars = wrapped_label(r"the browser wars: \ Internet Explorer \ (1995), \ bundled with Windows, \ against "
                             r"Navigator; \ each invented its own tags and scripting, \ and pages said which browser "
                             r"they were ``best viewed in''", 12.6, font_size=20, color=NO).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Two more languages joined HTML. <bookmark mark='a'/> In October 1994 Håkon Wium Lie proposed cascading "
            "style sheets, so that how a page looks could be written apart from what it says. CSS level one became a "
            "W3C recommendation in December 1996. <bookmark mark='b'/> In May 1995, at Netscape, Brendan Eich wrote "
            "the first JavaScript in about ten days. It was standardized as ECMAScript in 1997, and some of its hasty"
            " decisions are with us still. <bookmark mark='c'/> Microsoft answered with Internet Explorer, bundled "
            "with Windows. In the browser wars each side invented its own tags, and by the early two-thousands "
            "Internet Explorer had most of the market, and its development slowed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g[0]))
            vo.wait_until("a")
            self.play(*self.mark([1994], 1994.9), FadeIn(g[1], shift=UP * 0.15))
            vo.wait_until("b")
            self.play(*self.mark([1995], 1995.5), FadeIn(g[2], shift=UP * 0.15))
            vo.wait_until("c")
            self.play(*self.mark([1996, 1997], 2001), FadeIn(wars))
        self.wait(0.4)
        self.clear_scene(self.tl)

    def ajax(self):
        head = label(r"Pages that talk back", font_size=36).to_edge(UP, buff=0.3)

        def lane(cx, title, color):
            t = label(title, font_size=21, color=color).move_to([cx, 1.75, 0])
            b = label(r"browser", font_size=18, color=GREY_A).move_to([cx - 1.5, 1.3, 0])
            s = label(r"server", font_size=18, color=GREY_A).move_to([cx + 1.5, 1.3, 0])
            lb = Line([cx - 1.5, 1.1, 0], [cx - 1.5, -2.45, 0], color=GREY_C, stroke_width=1.5)
            ls = Line([cx + 1.5, 1.1, 0], [cx + 1.5, -2.45, 0], color=GREY_C, stroke_width=1.5)
            return VGroup(t, b, s, lb, ls)
        left, right = lane(-3.4, r"a classic page", GREY_A), lane(3.4, r"with XMLHttpRequest", YES)
        classic = []
        for k in range(3):
            y = 0.85 - k * 1.15
            a = Arrow([-4.9, y, 0], [-1.9, y - 0.2, 0], buff=0, stroke_width=2, color=GREY_B,
                      max_tip_length_to_length_ratio=0.08)
            at = label(r"click", font_size=16, color=GREY_B).next_to(a.get_start(), LEFT, buff=0.12)
            r = Arrow([-1.9, y - 0.35, 0], [-4.9, y - 0.75, 0], buff=0, stroke_width=7, color=NO,
                      max_tip_length_to_length_ratio=0.1)
            rt = label(r"a whole new page", font_size=16, color=NO).next_to(r, DOWN, buff=0.0)
            classic.append(VGroup(a, at, r, rt))
        page = Rectangle(width=0.22, height=3.5, stroke_width=0, fill_color=YES, fill_opacity=0.5).move_to(
            [1.9, -0.68, 0])
        page_t = label(r"the page stays", font_size=16, color=YES).rotate(PI / 2).next_to(page, LEFT, buff=0.08)
        small = []
        for k in range(6):
            y = 0.85 - k * 0.55
            a = Arrow([2.0, y, 0], [4.9, y - 0.12, 0], buff=0, stroke_width=1.6, color=DATA,
                      max_tip_length_to_length_ratio=0.06)
            r = Arrow([4.9, y - 0.22, 0], [2.0, y - 0.34, 0], buff=0, stroke_width=1.6, color=YES,
                      max_tip_length_to_length_ratio=0.06)
            small.append(VGroup(a, r))
        small_t = label(r"small pieces of data, \ in the background", font_size=16, color=DATA).move_to(
            [3.4, -2.75, 0])
        illus = note(r"illustrative", font_size=16).move_to([-3.4, -2.75, 0])
        cap = wrapped_label(r"1999: \ XMLHTTP in Internet Explorer 5, \ copied by others as XMLHttpRequest; \ "
                            r"Gmail \ (2004) \ and Google Maps \ (2005) \ showed what it allowed; \ Jesse James "
                            r"Garrett named it \textbf{Ajax} \ (February 2005)", 12.6, font_size=19,
                            color=GREY_A).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "The next leap came from a feature that almost nobody noticed. <bookmark mark='a'/> A classic page asks "
            "the server for a whole new page on every click. <bookmark mark='b'/> In 1999 Internet Explorer 5 shipped"
            " an object that let a script fetch data without leaving the page, and other browsers copied it as "
            "XMLHttpRequest. Now a page could stay put and fetch small pieces of data in the background. <bookmark "
            "mark='c'/> Gmail in 2004 and Google Maps in 2005 showed what that allowed, and in February 2005 Jesse "
            "James Garrett named the technique Ajax, for asynchronous JavaScript and XML."
        ) as vo:
            self.play(FadeIn(head), FadeIn(left), FadeIn(right), FadeIn(illus))
            vo.wait_until("a")
            for c in classic:
                self.play(GrowArrow(c[0]), FadeIn(c[1]), run_time=0.5)
                self.play(GrowArrow(c[2]), FadeIn(c[3]), run_time=0.6)
            vo.wait_until("b")
            self.play(*self.mark([1999], 1999.5), FadeIn(page), FadeIn(page_t))
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(s[0]), GrowArrow(s[1])) for s in small],
                                  lag_ratio=0.5), FadeIn(small_t), run_time=3)
            vo.wait_until("c")
            self.play(*self.mark([2004, 2005], 2005.3), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene(self.tl)

    def engines(self):
        head = label(r"New engines, \ new processes", font_size=36).to_edge(UP, buff=0.3)
        one = RoundedRectangle(width=5.4, height=2.7, corner_radius=0.12, stroke_color=GREY_B, stroke_width=2,
                               fill_color=GREY_D, fill_opacity=0.15).move_to([-3.6, -0.25, 0])
        one_t = label(r"one process for every tab", font_size=19, color=GREY_A).next_to(one, UP, buff=0.1)
        tabs = VGroup(*[module_box(rf"tab {k + 1}", DATA, w=2.2, h=0.8, font=18) for k in range(4)])
        tabs.arrange_in_grid(2, 2, buff=0.3).move_to(one)
        bp = module_box(r"browser process: \ windows, \ network, \ disk", KERN, w=5.6, h=0.6, font=18)
        bp.move_to([3.6, 0.8, 0])
        rend = VGroup(*[VGroup(module_box(rf"tab {k + 1}", DATA, w=1.25, h=0.5, font=17),
                               label(r"V8", font_size=16, color=HEAD)).arrange(DOWN, buff=0.08)
                        for k in range(4)]).arrange(RIGHT, buff=0.18).move_to([3.6, -0.85, 0])
        frames = VGroup(*[SurroundingRectangle(r, buff=0.08, color=GREY_B, stroke_width=1.2, corner_radius=0.08)
                          for r in rend])
        links = VGroup(*[Line(bp.get_bottom(), f.get_top(), color=GREY_C, stroke_width=1.5) for f in frames])
        rend_t = label(r"Chrome \ (2008): \ a process per tab, \ roughly", font_size=19, color=YES).next_to(
            frames, DOWN, buff=0.15)
        crash_one = Cross(tabs[2], stroke_color=NO, stroke_width=5)
        crash_two = Cross(rend[2], stroke_color=NO, stroke_width=5)
        notes = VGroup(
            wrapped_label(r"Safari and WebKit \ (Apple, 2003); \ Firefox 1.0 \ (Mozilla, November 2004)", 12.4,
                          font_size=19, color=DATA),
            wrapped_label(r"V8 compiles JavaScript to machine code \ (the JIT compilers of Part 15, \ opened up in "
                          r"Chapter 7); \ separate processes come from Part 31", 12.4, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Competition came back. <bookmark mark='a'/> Apple released Safari, on its WebKit engine, in 2003, and "
            "Mozilla released Firefox 1.0 in November 2004. <bookmark mark='b'/> In September 2008 Google released "
            "Chrome, with two ideas. Its engine, V8, compiled JavaScript to machine code, the just-in-time "
            "compilation of Part 15, and began a race that made JavaScript many times faster. <bookmark mark='c'/> "
            "And where browsers had run every page in one process, so that one bad page could take down them all, "
            "Chrome gave each tab, roughly, a process of its own: the isolation of Part 31."
        ) as vo:
            self.play(FadeIn(head), FadeIn(one), FadeIn(one_t), FadeIn(tabs))
            vo.wait_until("a")
            self.play(*self.mark([2003, 2004], 2004.9), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(*self.mark([2008], 2008.8), FadeIn(bp), FadeIn(rend), FadeIn(frames), Create(links),
                      FadeIn(rend_t), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Create(crash_one))
            self.play(one.animate.set_stroke(NO).set_fill(NO, opacity=0.25), tabs.animate.set_opacity(0.3))
            self.play(Create(crash_two))
            self.play(frames[2].animate.set_stroke(NO), rend[2].animate.set_opacity(0.3),
                      *[Indicate(rend[k], color=YES, scale_factor=1.08) for k in (0, 1, 3)])
        self.wait(0.4)
        self.clear_scene(self.tl)

    def standard(self):
        head = label(r"A living standard", font_size=36).to_edge(UP, buff=0.3)
        yw, yl = 0.95, -0.65
        w3c_t = label(r"W3C versions", font_size=19, color=DATA).move_to([-5.3, yw, 0])
        wl = Line([X(1994.5), yw, 0], [X(2019), yw, 0], color=GREY_D, stroke_width=1.5)
        vers = [(1995, r"2.0"), (1997, r"3.2"), (1999, r"4.01"), (2000, r"XHTML 1.0"), (2014, r"HTML5"),
                (2016, r"5.1"), (2017, r"5.2")]
        vg = VGroup()
        for k, (yr, name) in enumerate(vers):
            col = NO if "XHTML" in name else DATA
            d = Dot([X(yr), yw, 0], radius=0.08, color=col)
            t = label(name, font_size=16, color=col).next_to(d, UP if k % 2 == 0 else DOWN, buff=0.1)
            vg.add(VGroup(d, t))
        x_note = label(r"served as XML, \ one error and no page", font_size=16, color=NO).next_to(
            vg[3], DOWN, buff=0.08).shift(RIGHT * 0.6)
        wh_t = label(r"WHATWG", font_size=19, color=YES).move_to([X(2004) - 0.75, yl, 0])
        band = Rectangle(width=X(2020) - X(2004), height=0.34, stroke_width=0, fill_color=YES, fill_opacity=0.45)
        band.move_to([X(2004), yl, 0], aligned_edge=LEFT)
        pulses = VGroup(*[Line([X(2004.4 + k * 0.55), yl - 0.17, 0], [X(2004.4 + k * 0.55), yl + 0.17, 0],
                               color=YES, stroke_width=1.2) for k in range(28)])
        band_t = label(r"the living standard: \ edited continuously, \ no version numbers", font_size=16,
                       color=YES).next_to(band, DOWN, buff=0.1)
        merge = Arrow([X(2019), yw - 0.05, 0], [X(2019), yl + 0.2, 0], buff=0, stroke_width=3, color=HEAD,
                      max_tip_length_to_length_ratio=0.25)
        merge_t = label(r"2019", font_size=16, color=HEAD).next_to(merge, LEFT, buff=0.08)
        notes = VGroup(
            wrapped_label(r"June 2004: \ Apple, \ Mozilla and Opera found the WHATWG, \ to extend HTML as browsers "
                          r"really used it", 12.4, font_size=19, color=YES),
            wrapped_label(r"HTML5 specifies, \ for the first time, \ exactly how to parse \textit{any} page, \ "
                          r"valid or not: \ Chapter 2", 12.4, font_size=19, color=HEAD),
            wrapped_label(r"May 2019: \ the W3C and the WHATWG agree on one HTML and one DOM, \ the WHATWG's living "
                          r"standards", 12.4, font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The standards, meanwhile, had stalled. <bookmark mark='a'/> The W3C published numbered versions of HTML "
            "through the nineties, and then XHTML, which, served as XML, treated a single error as fatal, though real"
            " pages were full of errors. <bookmark mark='b'/> In June 2004 people from Apple, Mozilla and Opera "
            "founded the WHATWG, to extend HTML as browsers really used it. Their HTML5 said, for the first time, "
            "exactly how to parse any page, valid or not, and the W3C published it in 2014. <bookmark mark='c'/> In "
            "May 2019 the two bodies agreed on one HTML: the WHATWG's living standard, edited continuously, with no "
            "version numbers. Its parser is next."
        ) as vo:
            self.play(FadeIn(head), FadeIn(w3c_t), Create(wl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(v, scale=1.5) for v in vg[:4]], lag_ratio=0.4), run_time=2)
            self.play(FadeIn(x_note))
            vo.wait_until("b")
            self.play(*self.mark([2004], 2014.5), FadeIn(wh_t), GrowFromEdge(band, LEFT), FadeIn(band_t),
                      FadeIn(notes[0]), run_time=1.5)
            self.play(LaggedStart(*[Create(p) for p in pulses], lag_ratio=0.1), FadeIn(vg[4]), FadeIn(notes[1]),
                      run_time=2)
            vo.wait_until("c")
            self.play(*self.mark([2019], 2019.8), FadeIn(vg[5:]), GrowArrow(merge), FadeIn(merge_t),
                      FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()


_ = (LAM, YES, mono)
