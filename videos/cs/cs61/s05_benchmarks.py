from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs61.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, load

_ONES = ("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
         "seventeen eighteen nineteen").split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def say(n) -> str:
    """A whole number as a speaker says it (British: 'one hundred and twenty-eight')."""
    n = int(round(n))
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ("" if n % 10 == 0 else "-" + _ONES[n % 10])
    if n < 1000:
        return _ONES[n // 100] + " hundred" + ("" if n % 100 == 0 else " and " + say(n % 100))
    return say(n // 1000) + " thousand" + ("" if n % 1000 == 0 else " " + say(n % 1000))


def box(text: str, color, size=18, w=None, h=0.55, fill=0.12):
    """A rounded box with a Tex caption."""
    t = label(text, font_size=size, color=WHITE)
    r = RoundedRectangle(width=w or t.width + 0.35, height=h, corner_radius=0.1, stroke_color=color,
                         stroke_width=1.8, fill_color=color, fill_opacity=fill)
    if t.width > r.width - 0.15:
        t.width = r.width - 0.15
    t.move_to(r)
    return VGroup(r, t)


B = load("bias")
FAST = min(B["env"], key=lambda r: r["median"])
SLOW = max(B["env"], key=lambda r: r["median"])
ALPHA, K = 0.05, 20
P_ANY = 1 - (1 - ALPHA) ** K
GAIN = SLOW["median"] / FAST["median"] - 1


class Benchmarks(VoiceoverScene):
    def construct(self):
        self.card()
        self.failures()
        self.goodhart()
        self.spec()
        self.forking()
        self.reproduce()

    def card(self):
        card = chapter_card(4, r"Benchmarks and reproducibility", r"What does a benchmark score promise?",
                            lit=(1975, 2016), extra=((1975, r"Goodhart's law"), (1988, r"SPEC founded"),
                                                     (2011, r"artifact evaluation")), part=PART)
        with self.voiceover("Chapter four. Benchmarks and reproducibility."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def failures(self):
        head = label(r"When benchmarks break", font_size=36).to_edge(UP, buff=0.3)
        y0, ya, yb = 1.25, 0.45, -0.45
        xp = lambda yr: -6.0 + (yr - 1982) / (2020 - 1982) * 12.2  # noqa: E731
        axis = Line([xp(1982), y0, 0], [xp(2020), y0, 0], color=GREY_C, stroke_width=2)
        ticks = VGroup(*[VGroup(Line([xp(y), y0 - 0.08, 0], [xp(y), y0 + 0.08, 0], color=GREY_C),
                                label(rf"{y}", font_size=18, color=GREY_B).move_to([xp(y), y0 + 0.3, 0]))
                         for y in (1984, 1989, 1992, 1995, 2000, 2006, 2017)])
        dhry = VGroup(Dot([xp(1984), ya, 0], color=KERN, radius=0.08),
                      label(r"Dhrystone", font_size=21, color=KERN).next_to([xp(1984), ya, 0], RIGHT, buff=0.15))
        suites = VGroup()
        for a, b, nm in ((1989, 1992, r"CPU89"), (1992, 1995, r"92"), (1995, 2000, r"95"), (2000, 2006, r"2000"),
                         (2006, 2017, r"CPU2006"), (2017, 2020, r"2017")):
            r = Rectangle(width=xp(b) - xp(a) - 0.05, height=0.5, stroke_color=DATA, stroke_width=1.4,
                          fill_color=DATA, fill_opacity=0.15).move_to([(xp(a) + xp(b)) / 2, yb, 0])
            t = label(nm, font_size=18, color=WHITE).move_to(r)
            if t.width > r.width - 0.08:
                t.width = r.width - 0.08
            suites.add(VGroup(r, t))
        spec_l = label(r"SPEC CPU suites", font_size=20, color=DATA).next_to(suites, LEFT, buff=0.3)

        def dropped(name, suite):
            t = label(name, font_size=20, color=NO).next_to(suite, DOWN, buff=0.3).align_to(suite, LEFT)
            strike = Line(t.get_left() + LEFT * 0.05, t.get_right() + RIGHT * 0.05, color=NO, stroke_width=2.5)
            d = label(r"dropped", font_size=18, color=GREY_A).next_to(t, RIGHT, buff=0.15)
            return VGroup(t, strike, d)
        m300 = dropped(r"matrix300", suites[0])
        lq = dropped(r"libquantum", suites[4])
        notes = VGroup(
            wrapped_label(r"\textbf{Dhrystone} \ (Weicker, \ 1984): \ synthetic and small; \ it fit in a cache, \ "
                          r"and a few string operations that compilers and libraries could tune dominated it", 12.4,
                          font_size=19, color=KERN),
            wrapped_label(r"\textbf{matrix300} \ (SPEC89): \ compilers learned to transform it wholesale; \ dropped "
                          r"from the next suite \ (Hennessy and Patterson recount it)", 12.4, font_size=19, color=NO),
            wrapped_label(r"\textbf{libquantum} \ (CPU2006): \ notorious for compiler speedups far beyond other "
                          r"programs'; \ not in CPU2017", 12.4, font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.3)
        top = wrapped_label(r"a benchmark is a promise: \ its speed stands for the speed of the programs you care "
                            r"about", 12.4, font_size=21, color=WHITE).next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "A benchmark is a promise: a program whose speed stands for the speed of the programs you care about. "
            "<bookmark mark='a'/> Reinhold Weicker's Dhrystone, from "
            "1984, was small and synthetic. It fitted in a cache, and much of its time went into a few string "
            "operations that compilers and libraries could tune for it. <bookmark mark='b'/> The SPEC consortium, "
            "founded in 1988 by computer makers, chose real programs instead, and replaces its suite every few "
            "years. <bookmark mark='c'/> Yet its first suite included matrix300, a matrix multiplication. As "
            "Hennessy and Patterson recount, compilers learned to transform it so thoroughly that it measured that "
            "one trick, and it was dropped from the next suite. <bookmark mark='d'/> Later, libquantum, in the "
            "2006 suite, became notorious for compiler speedups far beyond what other programs saw; it is not in "
            "the 2017 suite. Each time, a score rose while the programs people ran did not."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top), Create(axis), FadeIn(ticks))
            vo.wait_until("a")
            self.play(FadeIn(dhry), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.2) for s in suites], lag_ratio=0.3), FadeIn(spec_l),
                      run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(m300[0]), FadeIn(notes[1]))
            self.play(Create(m300[1]), FadeIn(m300[2]))
            vo.wait_until("d")
            self.play(FadeIn(lq[0]), FadeIn(notes[2]))
            self.play(Create(lq[1]), FadeIn(lq[2]))
        self.wait(0.4)
        self.clear_scene()

    def goodhart(self):
        head = label(r"Goodhart's law", font_size=36).to_edge(UP, buff=0.3)
        quote = wrapped_label(r"``When a measure becomes a target, \ it ceases to be a good measure.''", 12.4,
                              font_size=26, color=HEAD).next_to(head, DOWN, buff=0.35)
        who = note(r"Strathern \ (1997), \ phrasing Goodhart \ (1975)", font_size=17).next_to(quote, DOWN, buff=0.1)
        # the loop
        c = np.array([-3.6, -0.75, 0])
        nodes = VGroup(box(r"goal: \ fast real programs", YES, size=17, w=3.1),
                       box(r"measure: \ a benchmark score", DATA, size=17, w=3.1),
                       box(r"target: \ raise the score", HEAD, size=17, w=3.1),
                       box(r"tune for the benchmark", NO, size=17, w=3.1))
        for n, d in zip(nodes, (UP, RIGHT, DOWN, LEFT)):
            n.move_to(c + d * np.array([1.75, 1.15, 0]))
        nodes[1].shift(RIGHT * 0.05)
        nodes[3].shift(LEFT * 0.05)
        arrows = VGroup(*[CurvedArrow(nodes[i].get_corner(dr) + v, nodes[(i + 1) % 4].get_corner(dl) + w,
                                      angle=-PI / 4, color=GREY_B, stroke_width=2, tip_length=0.15)
                          for i, (dr, v, dl, w) in enumerate(((RIGHT, 0, UP, 0), (DOWN, 0, RIGHT, 0),
                                                              (LEFT, 0, DOWN, 0), (UP, 0, LEFT, 0)))])
        # the drift (illustrative)
        ax = Axes(x_range=[0, 10, 2], y_range=[0, 10, 2], x_length=4.6, y_length=3.0,
                  axis_config={"color": GREY_D, "include_numbers": False, "include_ticks": False}).move_to(
            [3.9, -0.6, 0])
        score = ax.plot(lambda t: 1 + 0.85 * t, x_range=[0, 10], color=HEAD, stroke_width=3)
        real = ax.plot(lambda t: 1 + 3.2 * (1 - np.exp(-t / 3)), x_range=[0, 10], color=YES, stroke_width=3)
        gap = ax.get_area(score, x_range=[0, 10], bounded_graph=real, color=NO, opacity=0.25)
        sl = label(r"score", font_size=17, color=HEAD).next_to(score.get_end(), UP, buff=0.08)
        rl = label(r"real programs", font_size=17, color=YES).next_to(real.get_end(), DOWN, buff=0.1).shift(
            LEFT * 0.4)
        axl = label(r"years of tuning", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.1)
        ill = note(r"illustrative", font_size=16).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        cases = wrapped_label(r"2013: \ phones found raising their clock speeds for benchmark apps \ \ $\cdot$ \ \ "
                              r"2015: \ Volkswagen diesels found detecting the emissions test", 12.4, font_size=19,
                              color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Economists have a name for this. <bookmark mark='a'/> In 1975 Charles Goodhart observed that a "
            "statistical regularity tends to collapse once it is used as a lever of control; the anthropologist "
            "Marilyn Strathern later put it as: when a measure becomes a target, it ceases to be a good measure. "
            "<bookmark mark='b'/> A benchmark begins as a measure of what we want: fast real programs. Make the "
            "score a target, and effort flows into whatever raises it, including tuning for the benchmark itself. "
            "<bookmark mark='c'/> The score keeps rising, and the real programs stop following it. "
            "<bookmark mark='d'/> Sometimes it is deliberate. "
            "In 2013 several phones were found raising their clock speeds when they recognized a benchmark app, "
            "and in 2015 Volkswagen's diesel cars were found detecting the emissions test, and running cleaner "
            "only then."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(quote), FadeIn(who))
            vo.wait_until("b")
            for i in range(4):
                self.play(FadeIn(nodes[i]), Create(arrows[i - 1]) if i else Wait(0.01), run_time=0.8)
            self.play(Create(arrows[3]), run_time=0.8)
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(axl), FadeIn(ill))
            self.play(Create(score), Create(real), run_time=2)
            self.play(FadeIn(gap), FadeIn(sl), FadeIn(rl))
            vo.wait_until("d")
            self.play(FadeIn(cases))
        self.wait(0.4)
        self.clear_scene()

    def spec(self):
        head = label(r"How SPEC keeps score", font_size=36).to_edge(UP, buff=0.3)
        cols = {r"t_{\text{ref},i}": DATA, r"\text{score}": YES, r"\frac{\text{score}_X}{\text{score}_Y}": YES}
        r0 = cmath(r"\text{ratio}_i", r"=", r"\frac{t_{\text{ref},i}}{t_i}", colors=cols, font_size=34)
        r1 = cmath(r"\text{score}", r"=", r"\Big(\prod_{i=1}^{n} \text{ratio}_i\Big)^{1/n}", colors=cols,
                   font_size=34)
        r2 = cmath(r"\frac{\text{score}_X}{\text{score}_Y}", r"=",
                   r"\Big(\prod_{i=1}^{n} \frac{t_{\text{ref},i} / t_{X,i}}{t_{\text{ref},i} / t_{Y,i}}\Big)^{1/n}",
                   colors=cols, font_size=34)
        r3 = cmath(r"\frac{\text{score}_X}{\text{score}_Y}", r"=",
                   r"\Big(\prod_{i=1}^{n} \frac{t_{Y,i}}{t_{X,i}}\Big)^{1/n}", colors=cols, font_size=34)
        der = VGroup(r0, r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([-3.2, 0.5, 0])
        r3.move_to(r2, aligned_edge=LEFT)
        whys = VGroup(
            label(r"a reference machine's time over yours: \ bigger is better", font_size=17, color=GREY_B),
            label(r"the geometric mean \ (Chapter 3)", font_size=17, color=GREY_B),
            label(r"compare two machines", font_size=17, color=GREY_B),
        )
        for w, r in zip(whys, der):
            w.next_to(r, DOWN, buff=0.12).align_to(r, LEFT)
        why3 = label(r"the reference times cancel: \ the ranking does not depend on them", font_size=17,
                     color=YES).move_to(whys[2], aligned_edge=LEFT)
        rules = VGroup(
            box(r"\textbf{base}: \ one set of flags for every benchmark in a language", DATA, size=17, w=5.6, h=0.7),
            box(r"\textbf{peak}: \ flags tuned for each benchmark", LAM, size=17, w=5.6, h=0.7),
            box(r"full disclosure: \ hardware, \ software, \ flags", HEAD, size=17, w=5.6, h=0.7),
            box(r"results reviewed before SPEC publishes them", YES, size=17, w=5.6, h=0.7),
            box(r"broken benchmarks retired with the next suite", NO, size=17, w=5.6, h=0.7),
        ).arrange(DOWN, buff=0.22).move_to([3.7, 0.0, 0])
        rl = label(r"the rules", font_size=21, color=GREY_A).next_to(rules, UP, buff=0.2)
        with self.voiceover(
            "SPEC's answer to Goodhart is a careful score and strict rules. <bookmark mark='a'/> Each benchmark's "
            "time is divided into the time a fixed reference machine took, giving a ratio where bigger is better. "
            "<bookmark mark='b'/> The score is the geometric mean of the ratios, the mean from chapter three. "
            "<bookmark mark='c'/> Divide two machines' scores, and the reference times cancel, so the ranking does "
            "not depend on which reference machine was chosen. <bookmark mark='d'/> Then the rules. A base result "
            "must use one set of compiler flags for every benchmark in a language; a peak result may tune each. "
            "Every result discloses its hardware, software and flags, and is reviewed before SPEC publishes "
            "it. And when a benchmark breaks, it is retired with the next suite."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(r0), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(r0.copy(), r1), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(r1.copy(), r2), FadeIn(whys[2]))
            self.play(TransformMatchingTex(r2, r3), ReplacementTransform(whys[2], why3))
            vo.wait_until("d")
            self.play(FadeIn(rl), LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in rules], lag_ratio=0.35),
                      run_time=3)
        self.wait(0.4)
        self.clear_scene()

    def forking(self):
        head = label(r"The garden of forking paths", font_size=36).to_edge(UP, buff=0.3)
        # a tree of reasonable choices
        root = box(r"the runs", DATA, size=17)
        root.move_to([-3.6, 2.2, 0])
        lv1 = VGroup(*[box(t, GREY_B, size=16) for t in (r"mean", r"median", r"fastest")]).arrange(RIGHT, buff=0.7)
        lv1.move_to([-3.6, 1.0, 0])
        e1 = VGroup(*[Line(root.get_bottom(), n.get_top(), color=GREY_C, stroke_width=1.5) for n in lv1])
        lv2, e2 = VGroup(), VGroup()
        for n in lv1:
            kids = VGroup(*[box(t, GREY_B, size=16) for t in (r"keep", r"trim")]).arrange(RIGHT, buff=0.15)
            kids.next_to(n, DOWN, buff=0.55)
            lv2.add(kids)
            e2.add(*[Line(n.get_bottom(), k.get_top(), color=GREY_C, stroke_width=1.5) for k in kids])
        leaves, e3 = VGroup(), VGroup()
        rng = np.random.default_rng(4)
        for kids in lv2:
            for k in kids:
                for dx in (-0.22, 0.22):
                    d = Dot(k.get_bottom() + DOWN * 0.7 + RIGHT * dx, radius=0.09, color=GREY_B)
                    leaves.add(d)
                    e3.add(Line(k.get_bottom(), d.get_center(), color=GREY_C, stroke_width=1.2))
        win = int(rng.integers(0, len(leaves)))
        lbl = VGroup(label(r"estimator", font_size=16, color=GREY_A).next_to(lv1, LEFT, buff=0.25),
                     label(r"outliers", font_size=16, color=GREY_A).next_to(lv2, LEFT, buff=0.25),
                     label(r"benchmarks", font_size=16, color=GREY_A).next_to(leaves, LEFT, buff=0.25))
        star = label(r"$p < 0.05$: \ the paper", font_size=18, color=YES).next_to(leaves[win], DOWN, buff=0.15)
        ill = note(r"schematic", font_size=16).next_to(leaves, DOWN, buff=0.55).align_to(lbl, LEFT)
        cite = wrapped_label(r"Simmons, \ Nelson and Simonsohn \ (2011); \ Gelman and Loken \ (2013)", 5.6,
                             font_size=17, color=GREY_B).next_to(ill, DOWN, buff=0.1).align_to(lbl, LEFT)
        cols = {r"(1-\alpha)^k": HEAD, r"\alpha": HEAD}
        rows = VGroup(
            cmath(r"P(\text{no false alarm})", r"=", r"1-\alpha", colors=cols, font_size=30),
            cmath(r"P(\text{none in } k \text{ tries})", r"=", r"(1-\alpha)^k", colors=cols, font_size=30),
            cmath(r"P(\text{at least one})", r"=", r"1 -", r"(1-\alpha)^k", colors=cols, font_size=30),
            cmath(r"1 - 0.95^{20}", r"\approx", rf"{P_ANY:.2f}", colors={rf"{P_ANY:.2f}": NO}, font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([3.7, 1.2, 0])
        whys = VGroup(label(r"one honest test at $\alpha = 0.05$", font_size=17, color=GREY_B),
                      label(r"$k$ independent tries", font_size=17, color=GREY_B),
                      label(r"the complement", font_size=17, color=GREY_B),
                      label(rf"twenty tries: \ {100 * P_ANY:.0f}\%", font_size=17, color=NO))
        for w, r in zip(whys, rows):
            w.next_to(r, DOWN, buff=0.1).align_to(r, LEFT)
        ours = wrapped_label(rf"in our data: \ the fastest of {len(B['env'])} environment sizes against the slowest "
                             rf"is a {100 * GAIN:.1f}\% ``speedup'' \ from a "
                             r"variable the program never reads", 5.6, font_size=19, color=KERN).to_edge(
            DOWN, buff=0.35).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "The same pressure acts on researchers. <bookmark mark='a'/> Between the runs and the claim lie many "
            "reasonable choices: the mean, the median or the fastest run; whether to trim outliers; which "
            "benchmarks to show. In 2011 Joseph Simmons, Leif Nelson and Uri Simonsohn showed, for psychology, that "
            "freely combining such choices can make almost anything look significant; Andrew Gelman and Eric Loken "
            "called it the garden of forking paths. <bookmark mark='b'/> An honest test at "
            "the five percent level raises a false alarm one time in twenty, and stays quiet nineteen times in "
            "twenty. <bookmark mark='c'/> Over k independent tries, the chance that all stay quiet is that, to "
            "the power k, <bookmark mark='d'/> so the "
            f"chance of at least one is one minus it, <bookmark mark='e'/> and with twenty tries about "
            f"{say(100 * P_ANY)} percent. <bookmark mark='f'/> In systems research, pick our "
            f"fastest environment size against our slowest, and you have a {say(100 * GAIN)} percent speedup"
            " from a variable the program never reads. The remedies: decide the analysis "
            "before you see the results, report every benchmark and every run, and randomize the setup."
        ) as vo:
            self.play(FadeIn(head), FadeIn(root))
            vo.wait_until("a")
            self.play(Create(e1), FadeIn(lv1), FadeIn(lbl[0]))
            self.play(Create(e2), FadeIn(lv2), FadeIn(lbl[1]))
            self.play(Create(e3), FadeIn(leaves), FadeIn(lbl[2]), FadeIn(ill), FadeIn(cite))
            self.play(leaves[win].animate.set_color(YES).scale(1.4), FadeIn(star))
            vo.wait_until("b")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]), FadeIn(whys[3]))
            vo.wait_until("f")
            self.play(FadeIn(ours))
        self.wait(0.4)
        self.clear_scene()

    def reproduce(self):
        head = label(r"Let others check", font_size=36).to_edge(UP, buff=0.3)
        rungs = VGroup()
        for t, d, c in ((r"repeatable", r"same team, \ same setup", GREY_A),
                        (r"reproducible", r"another team, \ the authors' artifacts", DATA),
                        (r"replicable", r"another team, \ its own setup", YES)):
            r = RoundedRectangle(width=5.6, height=0.85, corner_radius=0.1, stroke_color=c, stroke_width=1.8,
                                 fill_color=c, fill_opacity=0.1)
            g = VGroup(label(t, font_size=22, color=c), label(d, font_size=18, color=WHITE)).arrange(
                RIGHT, buff=0.35).move_to(r)
            rungs.add(VGroup(r, g))
        rungs.arrange(UP, buff=0.18).move_to([-3.5, 0.9, 0])
        acm = note(r"the ACM's terms", font_size=17).next_to(rungs, DOWN, buff=0.12).align_to(rungs, LEFT)
        badges = VGroup(box(r"Artifacts Available", GREY_A, size=16, w=2.9),
                        box(r"Artifacts Evaluated", DATA, size=16, w=2.9),
                        box(r"Results Reproduced", YES, size=16, w=2.9),
                        box(r"Results Replicated", YES, size=16, w=2.9)).arrange_in_grid(2, 2, buff=0.18)
        badges.move_to([3.6, 1.55, 0])
        bl = label(r"artifact-evaluation badges", font_size=18, color=GREY_A).next_to(badges, UP, buff=0.15)
        ae = wrapped_label(r"since 2011, \ many conferences ask a committee to run the authors' code and data", 5.8,
                           font_size=18, color=WHITE).next_to(badges, DOWN, buff=0.25).align_to(badges, LEFT)
        cp = wrapped_label(r"Collberg and Proebsting \ (2016) \ tried to obtain and build the code of hundreds of "
                           r"systems papers; \ for many they could not", 5.8, font_size=18, color=NO).next_to(
            ae, DOWN, buff=0.2).align_to(ae, LEFT)
        pipe = VGroup(code_block(["python -m videos.cs.cs61.compute"], size=16),
                      code_block([".cache/cs61/bias.json"], size=16),
                      code_block(['load("bias")'], size=16)).arrange(RIGHT, buff=0.9)
        pipe.to_edge(DOWN, buff=0.75)
        parrows = VGroup(*[Arrow(pipe[i].get_right(), pipe[i + 1].get_left(), buff=0.12, color=GREY_B,
                                 stroke_width=2) for i in range(2)])
        pl = label(r"this series: \ every measured number on screen is recomputed by code anyone can run", font_size=19,
                   color=HEAD).next_to(pipe, DOWN, buff=0.18)
        with self.voiceover(
            "The last defence is to let others check. <bookmark mark='a'/> The ACM distinguishes three levels. A "
            "result is repeatable when the same team gets it again with the same setup; reproducible when another "
            "team gets it using the authors' artifacts; and replicable when another team gets it with a setup of "
            "its own. <bookmark mark='b'/> In 2016 Christian Collberg and Todd Proebsting reported trying to "
            "obtain and build the code behind hundreds of systems papers; for many, they could not. "
            "<bookmark mark='c'/> Since 2011, many conferences have run artifact evaluation: a committee runs the "
            "authors' code and data, and papers earn badges for artifacts that are available, that work, and whose "
            "results were reproduced. <bookmark mark='d'/> This series keeps the same rule. Every measured number "
            "on screen is computed by code in the repository, cached, and recomputed by one command, so that "
            "anyone can check it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.15) for r in rungs], lag_ratio=0.5), FadeIn(acm),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(cp))
            vo.wait_until("c")
            self.play(FadeIn(bl), LaggedStart(*[FadeIn(b) for b in badges], lag_ratio=0.3), FadeIn(ae))
            vo.wait_until("d")
            self.play(FadeIn(pipe[0]))
            self.play(GrowArrow(parrows[0]), FadeIn(pipe[1]))
            self.play(GrowArrow(parrows[1]), FadeIn(pipe[2]), FadeIn(pl))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, LAM)
