from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs42.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.nesting()
        self.verified()
        self.engines()
        self.models()
        self.open()

    def card(self):
        card = chapter_card(14, r"Frontier: \ layout, \ engines and proofs",
                            r"Can a browser be fast, \ correct and safe at once?", lit=(2010, 2024),
                            extra=((2010, r"Featherweight Firefox; \ Akhawe et al."),
                                   (2016, r"Cassius: \ CSS in a solver")), part=PART)
        with self.voiceover("Chapter fourteen, the frontier. Can a browser be fast, correct and safe, all at once?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def nesting(self):
        rows = load("nesting")["rows"]
        head = label(r"How expensive is layout?", font_size=36).to_edge(UP, buff=0.3)
        # nested boxes: each level measures its child, then lays it out
        nest = VGroup()
        for k in range(5):
            w, h = 3.4 - 0.55 * k, 3.2 - 0.55 * k
            nest.add(Rectangle(width=w, height=h, stroke_color=[DATA, YES, HEAD, KERN, LAM][k], stroke_width=2))
        nest.move_to([-4.6, -0.2, 0])
        cap = wrapped_label(r"a flex column inside a flex column \ldots: \ each level asks its child for its "
                            r"preferred size, \ then lays it out for real", 3.6, font_size=18, color=GREY_A).next_to(
            nest, DOWN, buff=0.25)
        # log-scale chart of layouts against depth
        x0, y0, xw, yh = -1.6, -2.3, 7.8, 4.6
        lmax = math.log10(rows[-1]["naive"])
        ax = VGroup(Line([x0, y0, 0], [x0 + xw, y0, 0], color=GREY_C), Line([x0, y0, 0], [x0, y0 + yh, 0],
                                                                              color=GREY_C))
        dmax = rows[-1]["depth"]

        def pt(d, v):
            return [x0 + d / dmax * xw, y0 + math.log10(v) / lmax * yh, 0]
        ticks = VGroup()
        for e in range(0, int(lmax) + 1, 2):
            ticks.add(label(rf"$10^{{{e}}}$", font_size=16, color=GREY_B).move_to([x0 - 0.4, y0 + e / lmax * yh, 0]))
        for r in rows:
            ticks.add(label(f"{r['depth']}", font_size=16, color=GREY_B).move_to([pt(r["depth"], 1)[0], y0 - 0.25,
                                                                                   0]))
        xl = label(r"depth of nesting", font_size=17, color=GREY_B).next_to(ax[0], DOWN, buff=0.4)
        yl = label(r"layouts performed", font_size=17, color=GREY_B).next_to(ax[1], UP, buff=0.1)
        naive = VMobject(color=NO, stroke_width=3).set_points_as_corners([pt(r["depth"], r["naive"]) for r in rows])
        cached = VMobject(color=YES, stroke_width=3).set_points_as_corners([pt(r["depth"], r["cached"]) for r in rows])
        nl = label(rf"no cache: \ $2^{{d+1}}-1$, \ {rows[-1]['naive']:,} at depth {dmax}", font_size=18,
                   color=NO).next_to(pt(dmax, rows[-1]["naive"]), LEFT, buff=0.15).shift(DOWN * 0.3)
        cl = label(rf"cached by (box, \ width): \ $2d+1$, \ {rows[-1]['cached']}", font_size=18,
                   color=YES).next_to(pt(dmax, rows[-1]["cached"]), UP, buff=0.35).shift(LEFT * 1.4)
        with self.voiceover(
            "Is layout cheap? In normal flow, one pass down the tree and one back up is enough, so the cost is linear "
            "in the size of the page. <bookmark mark='a'/> Modern layout asks harder questions. A flex container "
            "inside a flex container first asks each child for its preferred size, and then lays it out again at "
            "the size it actually gets. Two layouts of the child per level. <bookmark mark='b'/> Nest that twenty "
            f"levels deep and, without care, the innermost box is laid out about two million times: "
            f"{rows[-1]['naive']:,}, counted by our model. <bookmark mark='c'/> With a cache keyed by the box and "
            f"the width it was offered, it is laid out {rows[-1]['cached']} times. Real engines keep exactly such "
            "caches, and pathological pages that defeat them still turn up. Whether the full CSS layout model always "
            "admits a linear algorithm, and how to make relayout cost proportional to the change, are open."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[Create(r) for r in nest], lag_ratio=0.2), FadeIn(cap))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(ticks), FadeIn(xl), FadeIn(yl))
            vo.wait_until("b")
            self.play(Create(naive), run_time=2)
            self.play(FadeIn(nl))
            vo.wait_until("c")
            self.play(Create(cached), run_time=1.5)
            self.play(FadeIn(cl))
        self.wait(0.4)
        self.clear_scene()

    def verified(self):
        head = label(r"Specifications you can check", font_size=36).to_edge(UP, buff=0.3)
        spec = RoundedRectangle(width=3.6, height=1.3, corner_radius=0.12, stroke_color=HEAD, fill_color=BG,
                                fill_opacity=1)
        st = VGroup(label(r"the CSS specification", font_size=20, color=HEAD),
                    label(r"as logical formulas", font_size=17, color=GREY_A)).arrange(DOWN, buff=0.1).move_to(spec)
        page = RoundedRectangle(width=3.6, height=1.3, corner_radius=0.12, stroke_color=DATA, fill_color=BG,
                                fill_opacity=1)
        pt = VGroup(label(r"a page and its stylesheet", font_size=20, color=DATA),
                    label(r"as constraints", font_size=17, color=GREY_A)).arrange(DOWN, buff=0.1).move_to(page)
        solver = RoundedRectangle(width=3.0, height=1.3, corner_radius=0.12, stroke_color=KERN, fill_color=BG,
                                  fill_opacity=1)
        so = VGroup(label(r"an SMT solver", font_size=20, color=KERN),
                    label(r"(Part 26)", font_size=17, color=GREY_A)).arrange(DOWN, buff=0.1).move_to(solver)
        left = VGroup(VGroup(spec, st), VGroup(page, pt)).arrange(DOWN, buff=0.4)
        VGroup(left, VGroup(solver, so)).arrange(RIGHT, buff=1.4).next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.6)
        arr = VGroup(Arrow(left[0].get_right(), solver.get_left(), buff=0.1, color=GREY_B, stroke_width=2),
                     Arrow(left[1].get_right(), solver.get_left(), buff=0.1, color=GREY_B, stroke_width=2))
        out = VGroup(label(r"``no text ever overlaps''", font_size=19, color=YES),
                     label(r"$\Rightarrow$ \ proved, \ or a counterexample page", font_size=17, color=GREY_A)).arrange(
            DOWN, buff=0.1).next_to(solver, RIGHT, buff=0.35)
        if out.get_right()[0] > 6.9:
            out.shift(LEFT * (out.get_right()[0] - 6.9))
        lines = VGroup(
            wrapped_label(r"\textbf{Cassius} \ (Panchekha and Torlak, \ 2016): \ CSS layout encoded for a solver, \ "
                          r"used to check and to synthesize stylesheets; \ \textbf{VizAssert} \ (2018) \ checks "
                          r"accessibility and usability properties for every screen size", 12.4, font_size=20,
                          color=WHITE),
            wrapped_label(r"parallel layout as attribute grammars \ (Meyerovich and Bod\'ik, \ 2010); \ Servo's "
                          r"parallel styling, \ now in Firefox \ (2017)", 12.4, font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "If layout is a constraint problem, a solver can reason about it. <bookmark mark='a'/> Cassius, by "
            "Pavel Panchekha and Emina Torlak in 2016, wrote the rules of CSS layout as logical formulas. "
            "<bookmark mark='b'/> Give a solver the formulas and a page, and it can prove that a property holds, "
            "such as no text ever overlapping, or produce a page where it fails. The same encoding can synthesize a "
            "stylesheet from a sketch, and its successor VizAssert checks accessibility and usability properties "
            "for every screen size at once. <bookmark mark='c'/> Another line of work treats layout as an "
            "attribute grammar, computed by tree traversals that can run in parallel; Leo Meyerovich and Rastislav "
            "Bodík did this in 2010, and Mozilla's Servo engine, whose parallel styling has shipped in Firefox since "
            "2017, carried the idea into practice."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left[0]))
            vo.wait_until("b")
            self.play(FadeIn(left[1]), FadeIn(VGroup(solver, so)), Create(arr))
            self.play(FadeIn(out), FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def engines(self):
        head = label(r"The JIT as an attack surface", font_size=36).to_edge(UP, buff=0.3)
        steps = [(r"the optimizer assumes \texttt{x} is always a small integer", HEAD),
                 (r"a bug removes a bounds check it thinks is redundant", NO),
                 (r"the attacker's script reads and writes past an array", NO),
                 (r"from there, \ arbitrary memory in the renderer process", NO),
                 (r"the sandbox \ (Part 31's processes) \ still stands between it and the system", YES)]
        chain = VGroup(*[label(t, font_size=21, color=c) for t, c in steps]).arrange(DOWN, aligned_edge=LEFT,
                                                                                      buff=0.32)
        arrows = VGroup(*[Arrow(chain[i].get_left() + LEFT * 0.35 + DOWN * 0.05, chain[i + 1].get_left() + LEFT *
                                0.35 + UP * 0.05, buff=0.02, stroke_width=2, color=GREY_C,
                                max_tip_length_to_length_ratio=0.35) for i in range(4)])
        VGroup(chain, arrows).next_to(head, DOWN, buff=0.5)
        lines = VGroup(
            wrapped_label(r"defences: \ a heap sandbox inside the engine \ (V8, \ 2024), \ pointer compression and "
                          r"checks, \ and fuzzers that generate JavaScript \ (Part 40)", 12.4, font_size=20,
                          color=YES),
            wrapped_label(r"open: \ JIT compilers whose optimizations are proved correct, \ as CompCert's are for C, "
                          r"\ fast enough to ship", 12.4, font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The JavaScript engine is where speed and safety collide. <bookmark mark='a'/> Its optimizing compiler "
            "makes assumptions from type feedback, and removes checks it believes are redundant. "
            "<bookmark mark='b'/> If one of those deductions is wrong, a bounds check disappears that was needed, "
            "and a script from any web page can read and write past the end of an array, and from there reach "
            "arbitrary memory in its process. Bugs of this shape, in the engines' compilers and type systems, have "
            "been among the most valuable browser exploits for a decade. <bookmark mark='c'/> What still stands "
            "between such a script and the computer is the sandbox around the renderer process. "
            "<bookmark mark='d'/> Defences grow in layers: V8 added a sandbox inside its own heap in 2024, and "
            "fuzzers generate millions of JavaScript programs to find such bugs first. <bookmark mark='e'/> The open "
            "goal is a JIT whose optimizations are proved correct, as CompCert's are for C, and still fast enough "
            "to ship."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(chain[0]))
            vo.wait_until("b")
            for i in (1, 2, 3):
                self.play(GrowArrow(arrows[i - 1]), FadeIn(chain[i]), run_time=0.8)
            vo.wait_until("c")
            self.play(GrowArrow(arrows[3]), FadeIn(chain[4]))
            vo.wait_until("d")
            self.play(FadeIn(lines[0]))
            vo.wait_until("e")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def models(self):
        head = label(r"The web as a formal model", font_size=36).to_edge(UP, buff=0.3)
        actors = [(r"browser", DATA, [-4.5, 1.2]), (r"honest server", YES, [0.0, 1.2]),
                  (r"attacker's server", NO, [4.5, 1.2])]
        boxes = VGroup()
        for t, c, p in actors:
            r = RoundedRectangle(width=3.0, height=0.8, corner_radius=0.12, stroke_color=c, fill_color=BG,
                                 fill_opacity=1).move_to([*p, 0])
            boxes.add(VGroup(r, label(t, font_size=20, color=c).move_to(r)))
        msgs = VGroup(
            Arrow(boxes[0].get_bottom() + RIGHT * 0.3, boxes[1].get_bottom() + LEFT * 0.3, path_arc=0.6, color=GREY_B,
                  stroke_width=2),
            Arrow(boxes[2].get_bottom() + LEFT * 0.3, boxes[0].get_bottom() + RIGHT * 0.9, path_arc=-0.5, color=NO,
                  stroke_width=2))
        ml = VGroup(label(r"requests, \ cookies, \ redirects", font_size=16, color=GREY_B).next_to(msgs[0], DOWN,
                                                                                               buff=0.05),
                    label(r"a forged cross-site request", font_size=16, color=NO).next_to(msgs[1], DOWN, buff=0.05))
        rows = VGroup(
            wrapped_label(r"\textbf{Akhawe, \ Barth, \ Lam, \ Mitchell and Song} \ (2010): \ the web's actors and "
                          r"rules in Alloy; \ the analyzer found new attacks on proposed defences", 12.4, font_size=20,
                          color=WHITE),
            wrapped_label(r"\textbf{Featherweight Firefox} \ (Bohannon and Pierce, \ 2010): \ a browser's core as a "
                          r"small formal model; \ \textbf{the Web Infrastructure Model} \ (Fett, \ K\"usters and "
                          r"Schmitz, \ 2014 onwards) \ found attacks on OAuth 2.0 and proved fixed versions secure",
                          12.4, font_size=20, color=YES),
            wrapped_label(r"\textbf{WebSpec} \ (Veronese et al., \ 2023): \ browser rules checked by a solver found "
                          r"new attacks on cookie integrity", 12.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Security has its own formal frontier. The web's rules are scattered across hundreds of documents, and "
            "attacks live in the gaps between them. <bookmark mark='a'/> In 2010, Devdatta Akhawe, Adam Barth and "
            "colleagues wrote the web's actors and rules, browsers, servers, cookies, redirects and an attacker "
            "with a server of its own, as a model in the Alloy analyzer, and it found new attacks on defences that "
            "had been proposed. <bookmark mark='b'/> Featherweight Firefox, by Aaron Bohannon and Benjamin Pierce, "
            "modelled a browser's core. The Web Infrastructure Model of Daniel Fett, Ralf Küsters and Guido Schmitz "
            "has been used to find attacks on OAuth, the protocol behind signing in with another site's account, "
            "and to prove the repaired versions secure. <bookmark mark='c'/> And WebSpec, in 2023, checked browser "
            "rules with a solver and found new attacks on the integrity of cookies."
        ) as vo:
            self.play(FadeIn(head), FadeIn(boxes))
            self.play(Create(msgs[0]), FadeIn(ml[0]))
            vo.wait_until("a")
            self.play(Create(msgs[1]), FadeIn(ml[1]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.wait(0.4)
        self.clear_scene()

    def open(self):
        head = label(r"Open", font_size=36).to_edge(UP, buff=0.3)
        items = VGroup(
            wrapped_label(r"1. \ \textbf{Incremental layout}: \ relayout whose cost is provably proportional to the "
                          r"change, \ for flexbox and grid with intrinsic sizes.", 12.4, font_size=24, color=WHITE),
            wrapped_label(r"2. \ \textbf{Verified engines}: \ a JavaScript JIT whose optimizations are proved "
                          r"correct, \ and fast enough to ship.", 12.4, font_size=24, color=YES),
            wrapped_label(r"3. \ \textbf{Whole-web security proofs}: \ a model of the web platform complete enough "
                          r"that a proof about it covers real browsers.", 12.4, font_size=24, color=HEAD),
            wrapped_label(r"4. \ \textbf{Scheduling frames}: \ the best way to split a page's work into tasks so "
                          r"that no input waits longer than a bound, \ online.", 12.4, font_size=24, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.45)
        star = wrapped_label(r"$\bigstar$ \ this part's research problem: \ an algorithm for flex layout with "
                             r"intrinsic sizing whose relayout cost is bounded by the size of the change, \ with a "
                             r"matching lower bound", 12.4, font_size=23, color=LAM).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Open problems. <bookmark mark='a'/> Incremental layout: relayout whose cost is provably proportional to "
            "the size of a change, even with flexbox, grid and intrinsic sizes. <bookmark mark='b'/> Verified "
            "engines: a JavaScript compiler whose optimizations are proved correct, and fast enough to ship. "
            "<bookmark mark='c'/> Security proofs about the whole web: a model complete enough that a proof about it "
            "covers the browsers people use. <bookmark mark='d'/> And scheduling: splitting a page's work into "
            "tasks so that no input waits longer than a bound, deciding online as the work arrives. "
            "<bookmark mark='e'/> This part's research problem asks for a flex-layout algorithm with intrinsic sizing "
            "whose relayout cost is bounded by the size of the change, together with a matching lower bound."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it))
            vo.wait_until("e")
            self.play(FadeIn(star))
        self.wait(0.6)
        self.clear_scene()


_ = (DATA, KERN, LAM, YES)
