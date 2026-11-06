from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs61.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load

COLS = (NO, HEAD, YES, DATA, LAM, KERN)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.sky()
        self.small_cases()
        self.choose()

    def card(self):
        card = chapter_card(9, r"Frontier: \ the open-problems map",
                            r"What is still unknown, \ and where would you start?", lit=(1900, 2024),
                            extra=((1900, r"Hilbert's twenty-three problems"), (2024, r"BB(5) settled")), part=PART)
        with self.voiceover("Chapter nine, the frontier. What is still unknown, and where would you start?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def sky(self):
        rows = load("open")["rows"]
        head = label(r"A sky of open problems over the tower", font_size=36).to_edge(UP, buff=0.3)
        tower = VGroup(*[Rectangle(width=2.2 - 0.12 * i, height=0.32, stroke_color=GREY_C, stroke_width=1.2,
                                   fill_color=GREY_E, fill_opacity=1) for i in range(10)]).arrange(UP, buff=0.04)
        tower.to_edge(DOWN, buff=0.5)
        # three tiers of the sky, staggered so that no two labels meet and the lowest tier clears the tower
        slots = [(x, 2.55) for x in (-5.1, -1.7, 1.7, 5.1)] + [(x, 1.45) for x in (-3.4, 0.0, 3.4)] + \
                [(x, 0.4) for x in (-5.4, -2.7, 2.7, 5.4)]
        stars = VGroup()
        for i, r in enumerate(rows):
            x, y = slots[i % len(slots)]
            s = Star(n=5, outer_radius=0.12, color=COLS[i % 6], fill_opacity=1).move_to([x, y, 0])
            t = label(r["problem"], font_size=15, color=COLS[i % 6]).next_to(s, DOWN, buff=0.08)
            if t.width > 2.6:
                t.width = 2.6
            parts = ", ".join(str(p) for p in r["parts"])
            pl = label(rf"Part{'s' if len(r['parts']) > 1 else ''} {parts}; \ since {r['since']}", font_size=12,
                       color=GREY_B).next_to(t, DOWN, buff=0.04)
            stars.add(VGroup(s, t, pl))
        with self.voiceover(
            "Here is every open problem the series met, as a sky over the tower. <bookmark mark='a'/> Each star is "
            "a question nobody has answered, labelled with the parts where we met it and the year it was first "
            "asked. Some are decades old: P against NP since 1971, the exponent of matrix multiplication since "
            "Strassen's surprise in 1969, the gate counts of circuits since Shannon in 1949. <bookmark mark='b'/> "
            "Some have moved recently: the fifth Busy Beaver number was proved in 2024, and the record for matrix "
            "multiplication keeps creeping down. <bookmark mark='c'/> None of them is closed, and each is someone's "
            "life's work. The rest of this chapter asks how a person would start on one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tower))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s, scale=0.6) for s in stars[:6]], lag_ratio=0.3), run_time=3)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s, scale=0.6) for s in stars[6:]], lag_ratio=0.3), run_time=3)
            vo.wait_until("c")
            self.play(*[Indicate(s[0], scale_factor=1.6) for s in stars])
        self.wait(0.4)
        self.clear_scene()

    def small_cases(self):
        g = load("goldbach")
        c = load("collatz")
        head = label(r"Start with the small cases", font_size=36).to_edge(UP, buff=0.3)
        left = VGroup(label(r"Goldbach \ (1742)", font_size=24, color=HEAD),
                      wrapped_label(rf"every even number from 4 to {g['limit']:,} is a sum of two primes: \ checked "
                                    rf"in under a second; \ the hardest case below {g['limit']:,} is {g['worst']:,}, "
                                    rf"\ whose smallest prime is {g['worst_p']}", 5.6, font_size=19, color=GREY_A),
                      note(r"verified to $4 \times 10^{18}$ \ (Oliveira e Silva, \ Herzog and Pardi, \ 2014)",
                           font_size=16)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        rec = c["records"][-1]
        right = VGroup(label(r"Collatz \ (1937)", font_size=24, color=YES),
                       wrapped_label(rf"every start below {c['limit']:,} reaches 1; \ the longest is {rec['n']:,}, \ "
                                     rf"{rec['steps']} steps", 5.6, font_size=19, color=GREY_A),
                       note(r"checked far beyond, \ by large distributed searches", font_size=16)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25)
        VGroup(left, right).arrange(RIGHT, buff=1.0, aligned_edge=UP).next_to(head, DOWN, buff=0.5)

        def records(rows, xkey, ykey, ymax, col, ylab, x0=0, y0=0):
            ax = Axes(x_range=[x0, 6.2, 1], y_range=[y0, ymax, (ymax - y0) / 4], x_length=5.2, y_length=2.2,
                      axis_config={"color": GREY_D, "include_ticks": False})
            pts = [ax.c2p(math.log10(r[xkey]), r[ykey]) for r in rows]
            stair = VMobject(color=col, stroke_width=2.5).set_points_as_corners(
                [p for a, b in zip(pts, pts[1:] + [ax.c2p(6.2, rows[-1][ykey])]) for p in (a, [b[0], a[1], 0])])
            dots = VGroup(*[Dot(p, radius=0.045, color=col) for p in pts])
            xt = VGroup(*[label(rf"$10^{{{k}}}$", font_size=14, color=GREY_B).next_to(ax.c2p(k, y0), DOWN, buff=0.08)
                          for k in range(x0, 7, 2 if x0 == 0 else 1)])
            yt = VGroup(*[label(rf"{v}", font_size=14, color=GREY_B).next_to(ax.c2p(x0, v), LEFT, buff=0.08)
                          for v in (y0, ymax)])
            yl = label(ylab, font_size=15, color=GREY_B).next_to(ax, UP, buff=0.08).align_to(ax, LEFT)
            return VGroup(ax, VGroup(xt, yt), yl, stair, dots)

        gplot = records(g["records"], "n", "p", 650, HEAD, r"smallest prime needed, \ each new record")
        cplot = records(c["records"], "n", "steps", 550, YES, r"steps to reach 1, \ each new record", x0=4, y0=300)
        gplot.next_to(left, DOWN, buff=0.4).align_to(left, LEFT)
        cplot.next_to(right, DOWN, buff=0.4).align_to(right, LEFT)
        VGroup(gplot, cplot).align_to(VGroup(gplot, cplot), DOWN)
        foot = wrapped_label(r"small cases never prove a theorem about all numbers, \ but they find counterexamples, "
                             r"\ suggest patterns, \ and tell you where a proof must work hardest", 12.4, font_size=21,
                             color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "One honest way to start is with the small cases. <bookmark mark='a'/> Goldbach conjectured in 1742 that "
            f"every even number above two is a sum of two primes. Our sieve checks every even number up to "
            f"{g['limit']:,} in under a second, and finds that the hardest is {g['worst']:,}, whose smallest prime "
            "partner is the largest. <bookmark mark='b'/> The Collatz problem, from 1937, says that halving even "
            "numbers and tripling-plus-one the odd ones always reaches one. Every start below a million does; the "
            f"slowest takes {rec['steps']} steps. <bookmark mark='c'/> Checking small cases never proves a theorem "
            "about all numbers, but it finds counterexamples, suggests patterns, and shows where a proof will have "
            "to work hardest."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left), FadeIn(gplot[:3]))
            self.play(Create(gplot[3]), FadeIn(gplot[4]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(right), FadeIn(cplot[:3]))
            self.play(Create(cplot[3]), FadeIn(cplot[4]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def choose(self):
        head = label(r"Choosing a problem", font_size=36).to_edge(UP, buff=0.3)
        items = VGroup(
            wrapped_label(r"1. \ \textbf{Important and attackable}: \ Hamming asked what the important problems in "
                          r"your field are, \ and why you are not working on them.", 12.4, font_size=23, color=WHITE),
            wrapped_label(r"2. \ \textbf{A special case first}: \ every $\bigstar$ problem in this series has a "
                          r"smaller version someone could finish.", 12.4, font_size=23, color=YES),
            wrapped_label(r"3. \ \textbf{A new tool, \ an old problem}: \ topology for agreement, \ spectra for flows, "
                          r"\ SAT for proofs.", 12.4, font_size=23, color=HEAD),
            wrapped_label(r"4. \ \textbf{Measure the headroom}: \ a limit study \ (Part 7) \ tells you whether a "
                          r"problem is worth solving.", 12.4, font_size=23, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.5)
        star = wrapped_label(r"$\bigstar$ \ this part's research problem: \ pick one star from the series, \ find "
                             r"its smallest open special case, \ and settle it", 12.4, font_size=23,
                             color=LAM).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "How do you choose? <bookmark mark='a'/> Richard Hamming asked his colleagues what the important problems "
            "in their field were, and then why they were not working on them. <bookmark mark='b'/> Every problem "
            "marked with a star in this series has a smaller version that someone could finish. <bookmark mark='c'/> "
            "Many breakthroughs bring a new tool to an old problem: topology to agreement, spectra to flows, SAT to "
            "proofs. <bookmark mark='d'/> And a limit study, like Part 7's, tells you whether there is headroom "
            "worth having. <bookmark mark='e'/> So this last research problem is yours to define: pick one star "
            "from the series, find its smallest open special case, and settle it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it))
            vo.wait_until("e")
            self.play(FadeIn(star))
        self.wait(0.6)
        self.clear_scene()


_ = (BG, DATA, KERN, LAM, NO, YES)
