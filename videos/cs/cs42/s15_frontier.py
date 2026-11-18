from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs42.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load


class Frontier(WatchScene):
    def construct(self):
        self.card()
        self.nesting()
        self.engines()

    def card(self):
        self.chapter(14, r"Frontier: \ layout, \ engines and proofs", r"Can a browser be fast, \ correct and safe at once?", lit=(2010, 2016), extra=((2010, r"Featherweight Firefox; \ Akhawe et al."),
                                   (2016, r"Cassius: \ CSS in a solver")), part=PART, said="Chapter fourteen, the frontier. Can a browser be fast, correct and safe, all at once?")

    def nesting(self):
        self.ask(r"Boxes nested twenty deep, each sized by its child. \\ A naive layout visits the innermost...",
                 [r"20 times", r"about two million times"], 1,
                 say="Nest twenty boxes, each sized from its content. Done naively, how many times is the innermost box laid out?",
                 reveal="About two million: each level lays out its child twice.")
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
                   color=NO).next_to(pt(dmax, rows[-1]["naive"]), LEFT, buff=0.3).shift(DOWN * 0.9 + LEFT * 0.6)
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




_ = (DATA, KERN, LAM, YES)
