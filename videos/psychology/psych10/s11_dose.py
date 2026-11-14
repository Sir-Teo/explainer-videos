from __future__ import annotations

import numpy as np

from videos.psychology.psych10.common import *  # noqa: F403


class Dose(VoiceoverScene):
    def construct(self):
        self.card()
        self.hill()
        self.blocker()
        self.half_life()
        self.coffee()

    def card(self):
        card = chapter_card(10, r"Dose and response", r"How much is enough, and how long does it last?", lit=(),
                            part=PART, scale=("molecule", "person"), marr=("what", "how"))
        with self.voiceover(
            "Chapter ten. Dose and response."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def _axes(self, center, x_length=6.6, y_length=4.0):
        A = axes([-2, 2], [0, 1.05], x_length=x_length, y_length=y_length, xticks=[-2, -1, 0, 1, 2], yticks=[0, 0.5, 1],
                 xfmt=lambda v: {-2: r"\tfrac{1}{100}K", -1: r"\tfrac{1}{10}K", 0: "K", 1: "10K", 2: "100K"}[int(v)],
                 yfmt=lambda v: f"{v:g}", xlabel=r"dose (each step ten times the last)", ylabel=r"share of receptors occupied",
                 center=center, log_x=True)
        return A

    def hill(self):
        d = load("dose")
        head = heading(r"One receptor, \ one formula")
        steps = VGroup(
            VGroup(label(r"free receptors capture the drug", font_size=28, color=GREY_A),
                   MathTex(r"k_{+}\,D\,(1 - p)", font_size=38, color=DRUG)).arrange(RIGHT, buff=0.4),
            VGroup(label(r"occupied receptors let go", font_size=28, color=GREY_A),
                   MathTex(r"k_{-}\,p", font_size=38, color=OPP)).arrange(RIGHT, buff=0.4),
            VGroup(label(r"at balance", font_size=28, color=GREY_A),
                   MathTex(r"k_{+}\,D\,(1 - p) = k_{-}\,p", font_size=38)).arrange(RIGHT, buff=0.4),
            VGroup(MathTex(r"p = \frac{D}{D + K}", font_size=50, color=THRESH),
                   MathTex(r"K = \frac{k_{-}}{k_{+}}", font_size=36, color=GREY_A)).arrange(RIGHT, buff=0.6),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to([-3.6, 0.55, 0])
        keep_in_frame(steps)
        A = self._axes([3.55, 0.3, 0], x_length=5.6, y_length=3.6)
        ax = A.ax
        line = curve(ax, np.log10(d["dose"]), d["hill_1"], DRUG, stroke_width=4.5)
        p1 = Dot(ax.c2p(0, d["at_kd"]), radius=0.09, color=WHITE)
        p9 = Dot(ax.c2p(np.log10(9), d["at_9kd"]), radius=0.09, color=WHITE)
        l1 = label(r"half, at $K$", font_size=26, color=WHITE).next_to(p1, RIGHT, buff=0.12).shift(DOWN * 0.15)
        l9 = label(r"90\%, at $9K$", font_size=26, color=WHITE).next_to(p9, UL, buff=0.08)
        rows = rows_of([
            (r"below a tenth of $K$: \ almost nothing", WHITE),
            (r"near the top: \ doubling the dose buys almost nothing more, \ except side effects, which have curves of "
             r"their own", THRESH),
        ], 12.4, 29, 0.2).move_to([0, -2.75, 0])
        tag = psyche_tag(r"computed: the law of mass action")
        with self.voiceover(
            "How much drug does it take? Start with one kind of receptor, and a drug at concentration D. "
            "<bookmark mark='a'/> Free receptors capture the drug at a rate that grows with D, and with "
            "the share of receptors still free. <bookmark mark='b'/> Occupied receptors let go at a "
            "steady rate. <bookmark mark='c'/> At balance, the two are equal. <bookmark mark='d'/> Solve "
            "for p, the share of receptors occupied, and out comes one of the most used formulas in "
            "biology: D over D plus K. K is the concentration that fills half the receptors. "
            "<bookmark mark='e'/> Plot it against dose on a scale where each step is ten times the last, "
            "and it's an S. Half the receptors at K. Ninety percent takes nine K. Ninety-nine percent "
            "takes ninety-nine. <bookmark mark='f'/> So the curve says two things you can use. Below "
            "about a tenth of K, a drug does almost nothing. And near the top, doubling the dose buys "
            "almost nothing more, except side effects, which have curves of their own."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            for mark_, st in zip("abcd", steps):
                vo.wait_until(mark_)
                self.play(FadeIn(st, shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(Create(line), run_time=3.0)
            self.play(FadeIn(p1), FadeIn(l1), FadeIn(p9), FadeIn(l9))
            vo.wait_until("f")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
        self.clear_scene()

    def blocker(self):
        d = load("dose")
        fold = 81 ** (1 / 3)
        head = heading(r"Add a blocker, \ and steepen the curve")
        A = self._axes([-3.3, -0.35, 0])
        ax = A.ax
        x = np.log10(d["dose"])
        plain = curve(ax, x, d["hill_1"], DRUG, stroke_width=4.5)
        blocked = curve(ax, x, d["blocked"], OPP, stroke_width=4.5)
        steep = curve(ax, x, d["hill_3"], LIGHTC, stroke_width=4.5)
        arrow = Arrow(ax.c2p(0, 0.5), ax.c2p(1, 0.5), buff=0.05, color=OPP, stroke_width=5, max_tip_length_to_length_ratio=0.2)
        al = label(rf"$\times {d['shift']:.0f}$", font_size=30, color=OPP).next_to(arrow, UP, buff=0.05)
        eq = MathTex(r"p = \frac{D}{D + K\,(1 + B / K_B)}", font_size=40, color=OPP)
        rows = rows_of([
            (r"a blocker fits the same receptor and does nothing there: \ it makes the drug's $K$ look bigger", WHITE),
            (rf"at nine times its own $K$: \ the whole curve slides right, \ tenfold", OPP),
            (r"a competition: \ enough drug still wins; \ and if the antidote clears first, \ the overdose returns", BAD),
            (rf"several molecules needed at once: \ a steeper curve. \ From a tenth of the effect to nine tenths: \ "
             rf"${fold:.1f}$-fold in dose, \ not 81-fold", LIGHTC),
        ], 5.2, 28, 0.24)
        side = VGroup(eq, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.2, -0.3, 0])
        keep_in_frame(side)
        tag = psyche_tag(r"computed: competitive block, \ and a Hill curve with three sites")
        with self.voiceover(
            "Now add a blocker: a second molecule that fits the same receptor and does nothing there. "
            "Caffeine at the adenosine receptor. Naloxone at the opioid one. <bookmark mark='a'/> The "
            "formula gains one factor. The blocker makes the drug's K look bigger. <bookmark mark='b'/> "
            "With the blocker at nine times its own K, the whole curve slides to the right, by a factor "
            f"of {d['shift']:.0f}. <bookmark mark='c'/> Nothing is destroyed. Enough drug still gets to "
            "the top. It's a competition, and that cuts both ways. An antidote can be out-competed. And "
            "if the antidote is cleared from the body first, the overdose comes back. "
            "<bookmark mark='d'/> One more shape. Some receptors only open when several molecules bind "
            "at once, and then the curve steepens. With three, the climb from a tenth of the effect to "
            f"nine tenths takes about a {fold:.0f}-fold increase in dose. The plain curve needs "
            "eighty-one. A steep curve means a narrow margin between a dose that does nothing, and a "
            "dose that does everything."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(plain), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(eq))
            vo.wait_until("b")
            self.play(Create(blocked), GrowArrow(arrow), FadeIn(al), FadeIn(rows[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeOut(arrow), FadeOut(al), blocked.animate.set_stroke(opacity=0.35), Create(steep), FadeIn(rows[3]),
                      run_time=2.5)
        self.clear_scene()

    def half_life(self):
        d = load("dose")
        hl = d["half_life"]
        head = heading(r"Then the drug has to leave")
        A = axes([0, 24], [0, 1.05], x_length=6.6, y_length=4.0, xticks=[0, 5, 10, 15, 20], yticks=[0, 0.5, 1],
                 yfmt=lambda v: f"{v:g}", xlabel=r"hours after the dose", ylabel=r"share of the dose still in the body",
                 center=[-3.3, -0.35, 0])
        ax = A.ax
        first = curve(ax, d["t"], d["first"], DRUG, stroke_width=4.5)
        zero = curve(ax, d["t"], d["zero"], OPP, stroke_width=4.5)
        halves = VGroup()
        for n in (1, 2, 3):
            pt = ax.c2p(n * hl, 0.5 ** n)
            halves.add(VGroup(DashedLine(ax.c2p(n * hl, 0), pt, color=GREY_C, stroke_width=2), Dot(pt, radius=0.08, color=WHITE),
                              MathTex(rf"\tfrac{{1}}{{{2 ** n}}}", font_size=30).next_to(pt, UR, buff=0.06)))
        fl = label(r"a constant fraction each hour", font_size=26, color=DRUG).move_to(ax.c2p(17.3, 0.33))
        zl = label(r"a constant amount each hour", font_size=26, color=OPP).move_to(ax.c2p(13.5, 0.8))
        eqs = VGroup(MathTex(r"C(t) = C_0\,2^{-t / t_{1/2}}", font_size=36, color=DRUG),
                     MathTex(r"C(t) = C_0 - r\,t", font_size=36, color=OPP)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        rows = rows_of([
            (rf"most drugs: \ a half-life. \ Caffeine: about {hl:.0f} hours; \ nicotine: about 2", DRUG),
            (r"alcohol: \ a nearly constant amount per hour. \ Two drinks take twice as long as one", OPP),
            (r"the same curve again: \ the enzyme works at $D / (D + K)$ of its top speed. \ Far above $K$ it is "
             r"saturated; \ far below, \ it clears a constant fraction", THRESH),
        ], 5.2, 28, 0.26)
        side = VGroup(eqs, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.2, -0.3, 0])
        keep_in_frame(side)
        tag = psyche_tag(r"computed: first-order and zero-order elimination")
        with self.voiceover(
            "Then the drug has to leave. <bookmark mark='a'/> For most drugs the body clears a constant "
            "fraction every hour. That gives a half-life: the time for the level to fall by half, "
            f"whatever the level is. Caffeine's is about {hl:.0f} hours in a typical adult. Nicotine's "
            "is about two. After one half-life a half is left. After two, a quarter. After three, an "
            "eighth. <bookmark mark='b'/> Alcohol is the exception everyone has met. It leaves at a "
            "nearly constant amount per hour, however much is there. Two drinks take about twice as "
            "long to clear as one, and the last of a heavy evening is still there in the morning. "
            "<bookmark mark='c'/> And the reason is the same curve again. The enzyme that breaks "
            "alcohol down binds it as a receptor would, and its speed follows D over D plus K. At a "
            "drinker's concentrations it's far above its K: saturated, working flat out, and it can't go "
            "faster. Far below K, the same formula gives a constant fraction, and a half-life. One "
            "formula, and both behaviours."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(first), FadeIn(fl), FadeIn(eqs[0]), FadeIn(rows[0]), run_time=3.0)
            self.play(LaggedStart(*[FadeIn(h) for h in halves], lag_ratio=0.8), run_time=6.0)
            vo.wait_until("b")
            self.play(Create(zero), FadeIn(zl), FadeIn(eqs[1]), FadeIn(rows[1]), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def coffee(self):
        d = load("dose")
        k = (d["caf_t"] >= 6) & (d["caf_t"] <= 30)
        head = heading(r"Three coffees, \ and eleven at night")
        A = axes([6, 30], [0, 1.8], x_length=7.0, y_length=4.1, xticks=[], yticks=[0, 0.5, 1, 1.5],
                 yfmt=lambda v: f"{v:g}", xlabel=r"shaded: the night", ylabel=r"caffeine in the body, in cups", center=[-3.1, -0.4, 0])
        ax = A.ax
        A.add(hour_labels(ax, [8, 12, 16, 20, 24, 28], 0))
        night = night_bands(ax, 6, 30, y0=0, y1=1.8)
        three = curve(ax, d["caf_t"][k], d["caf"][k], DRUG, stroke_width=4.5)
        one = curve(ax, d["caf_t"][k], d["one"][k], GREY_A, stroke_width=4)
        bed = DashedLine(ax.c2p(23, 0), ax.c2p(23, 1.8), color=WHITE, stroke_width=2)
        p3 = Dot(ax.c2p(23, d["caf_at_23"]), radius=0.1, color=DRUG)
        p1 = Dot(ax.c2p(23, d["one_at_23"]), radius=0.1, color=GREY_A)
        l3 = label(rf"${d['caf_at_23']:.2f}$", font_size=30, color=DRUG).next_to(p3, UR, buff=0.08)
        l1 = label(rf"${d['one_at_23']:.2f}$", font_size=30, color=GREY_A).next_to(p1, UR, buff=0.08)
        cups = VGroup(*[Triangle(color=DRUG, fill_color=DRUG, fill_opacity=1).scale(0.11).rotate(PI).move_to(ax.c2p(h, 1.72))
                        for h in (8, 13, 16)])
        rows = rows_of([
            (r"coffee at 8:00, 13:00 and 16:00: \ each halves every five hours, \ and they stack", WHITE),
            (rf"the peak: \ ${d['caf_peak']:.2f}$ cups' worth", DRUG),
            (rf"at 23:00: \ ${d['caf_at_23']:.2f}$ of a cup is still there, \ half of the day's peak", DRUG),
            (rf"with the morning coffee only: \ ${d['one_at_23']:.2f}$", GREY_A),
            (r"so the question is not how many, \ but when the last one was. \ And half-lives differ severalfold between "
             r"people", THRESH),
        ], 5.0, 28, 0.25).move_to([4.3, -0.3, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: Psyche; \ a half-life of five hours")
        with self.voiceover(
            "So put the two halves together, for the commonest drug on earth. Three coffees: at eight, at "
            "one, and at four. Each is absorbed within the hour, and then halves every five hours. "
            f"<bookmark mark='a'/> They stack. The peak, in the late afternoon, is {d['caf_peak']:.2f} "
            "cups' worth: more than any single cup. <bookmark mark='b'/> At eleven at night, "
            f"{d['caf_at_23']:.2f} of a cup is still in the body. That's half of the day's peak, sitting "
            "on the adenosine receptors at the moment you want the pressure to be read. "
            f"<bookmark mark='c'/> With only the morning coffee, it's {d['one_at_23']:.2f}. "
            "<bookmark mark='d'/> So the question about coffee and sleep isn't how many. It's when the "
            "last one was. And these are averages. The half-life of caffeine differs severalfold from "
            "person to person: with genes, with pregnancy, with smoking. That's a Part 9 kind of fact."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(night), FadeIn(cups), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Create(three), FadeIn(rows[1]), run_time=4.0, rate_func=linear)
            vo.wait_until("b")
            self.play(Create(bed), FadeIn(p3, scale=1.5), FadeIn(l3), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(Create(one), FadeIn(p1), FadeIn(l1), FadeIn(rows[3]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[4], shift=UP * 0.1))
        self.clear_scene()
