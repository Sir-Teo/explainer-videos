from __future__ import annotations

import numpy as np

from videos.psychology.psych12.common import *  # noqa: F403


class Model(VoiceoverScene):
    def construct(self):
        self.card()
        self.picture()
        self.algebra()
        self.two_knobs()
        self.payoffs_again()

    def card(self):
        card = chapter_card(2, r"Two distributions and a line", r"How do you separate seeing from saying?",
                            lit={1954: r"Peterson, Birdsall and Fox"}, part=PART, scale=("mind",), marr=("what", "how"))
        with self.voiceover(
            "Chapter two. Two distributions and a line."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def _axes(self, center, x_length=7.6, y_length=3.2):
        return axes([-3.5, 5.0], [0, 0.45], x_length=x_length, y_length=y_length, xticks=[-2, 0, 2, 4], yticks=[],
                    xfmt=lambda v: f"{v:g}", xlabel=r"the evidence on one trial", ylabel=r"", center=center)

    def picture(self):
        d = load("model")
        head = heading(r"What the observer has to go on")
        A = self._axes([-2.6, 0.4, 0])
        ax = A.ax
        g = gauss_pair(ax, d["d"])
        ln = label(r"blank trials", font_size=25, color=NOISEC).move_to(ax.c2p(-1.9, 0.38))
        ls = label(r"signal trials", font_size=25, color=SIGNALC).move_to(ax.c2p(3.4, 0.38))
        k = d["k"]
        crit = DashedLine(ax.c2p(k, 0), ax.c2p(k, 0.44), color=CRIT, stroke_width=4)
        cl = label(r"the criterion", font_size=24, color=CRIT).next_to(crit, UP, buff=0.08)
        hit_area = area_under(ax, g.x, g.ys, k, 5.0, HIT, 0.45)
        fa_area = area_under(ax, g.x, g.yn, k, 5.0, FA, 0.55)
        rows = rows_of([
            (r"each trial gives the observer one number: \ the evidence", WHITE),
            (r"on blank trials it varies around 0; \ on signal trials around $d'$, \ here 1.5", SIGNALC),
            (r"the observer says yes when the evidence passes a line: \ the criterion", CRIT),
            (rf"area of signal past the line: \ the hit rate, \ {pct(d['hit'])}", HIT),
            (rf"area of noise past the line: \ the false-alarm rate, \ {pct(d['fa'])}", FA),
        ], 4.6, 27, 0.26).move_to([4.6, 0.0, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ $d' = 1.5$, \ criterion at 1.0")
        with self.voiceover(
            "Here's the picture behind the theory, worked out by engineers at Michigan for radar receivers and "
            "brought into psychology by Wilson Tanner and John Swets. <bookmark mark='a'/> On every trial the "
            "observer has one number to go on: how much evidence there seems to be. It's noisy. "
            "<bookmark mark='b'/> On blank trials it varies around zero; on signal trials, around a higher "
            "value. The distance between the two centres, in units of the noise, is called d prime. Here it's "
            "one and a half. <bookmark mark='c'/> The observer can't know which kind of trial it is. It can "
            "only draw a line and say yes whenever the evidence passes it. That line is the criterion. "
            "<bookmark mark='d'/> The part of the signal distribution past the line is the hit rate: "
            f"{100 * d['hit']:.0f} percent. <bookmark mark='e'/> The part of the noise distribution past the "
            f"line is the false-alarm rate: {100 * d['fa']:.0f} percent."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(g.noise), FadeIn(ln), Create(g.signal), FadeIn(ls), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(crit), FadeIn(cl), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(hit_area), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(fa_area), FadeIn(rows[4]))
        self.clear_scene()

    def algebra(self):
        d = load("model")
        head = heading(r"Back from two rates to two numbers")
        lines = VGroup(
            MathTex(r"\text{false-alarm rate} = 1 - \Phi(k) \;\Rightarrow\; z(F) = -k", font_size=38, color=FA),
            MathTex(r"\text{hit rate} = 1 - \Phi(k - d') \;\Rightarrow\; z(H) = d' - k", font_size=38, color=HIT),
            MathTex(r"d' = z(H) - z(F)", font_size=46, color=MODEL),
            MathTex(r"c = -\tfrac12\,\bigl(z(H) + z(F)\bigr)", font_size=46, color=CRIT),
        ).arrange(DOWN, buff=0.38).move_to([-2.4, 0.3, 0])
        ex = rows_of([
            (rf"here: \ $H = {d['hit']:.3f}$, \ $z(H) = {d['z_hit']:.2f}$", HIT),
            (rf"$F = {d['fa']:.3f}$, \ $z(F) = {d['z_fa']:.2f}$", FA),
            (rf"$d' = {d['z_hit']:.2f} - ({d['z_fa']:.2f}) = {d['dprime']:.2f}$", MODEL),
            (rf"$c = {d['c']:.2f}$: \ the line sits {d['c']:.2f} above the midpoint, \ a little cautious", CRIT),
            (r"$z$: \ the normal distribution's quantile, \ the inverse of $\Phi$", GREY_A),
        ], 4.4, 27, 0.28).move_to([4.6, 0.0, 0])
        keep_in_frame(ex)
        with self.voiceover(
            "Now run it backwards. From an experiment you get two rates, and you want the two numbers behind "
            "them. <bookmark mark='a'/> The false-alarm rate is the noise distribution's tail past the "
            "criterion, so its z score, the normal quantile, is minus the criterion. <bookmark mark='b'/> The "
            "hit rate is the signal distribution's tail, so its z score is d prime minus the criterion. "
            "<bookmark mark='c'/> Subtract, and the criterion cancels: d prime is z of the hit rate minus z of "
            "the false-alarm rate. <bookmark mark='d'/> Add them instead, and d prime cancels: minus half the "
            "sum is c, where the line sits relative to the midpoint between the two distributions. "
            "<bookmark mark='e'/> With our rates: z of the hit rate is "
            f"{d['z_hit']:.1f}, z of the false-alarm rate is minus {abs(d['z_fa']):.1f}, so d prime is "
            f"{d['dprime']:.1f}, and c is {d['c']:.2f}: slightly cautious. Two rates in, two numbers out, one for "
            "seeing and one for saying."
        ) as vo:
            self.play(FadeIn(head))
            for i, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(Write(lines[i]), run_time=1.5)
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(r) for r in ex], lag_ratio=0.5), run_time=4.0)
        self.clear_scene()

    def two_knobs(self):
        d = load("model")
        head = heading(r"Two knobs: \ move the line, \ or move the distributions")
        A = self._axes([-3.4, 1.15, 0], x_length=6.0, y_length=2.2)
        B = self._axes([3.4, 1.15, 0], x_length=6.0, y_length=2.2)
        ga, gb = gauss_pair(A.ax, d["d"]), gauss_pair(B.ax, d["d"])
        crit_a = DashedLine(A.ax.c2p(1.0, 0), A.ax.c2p(1.0, 0.44), color=CRIT, stroke_width=4)
        crit_b = DashedLine(B.ax.c2p(1.0, 0), B.ax.c2p(1.0, 0.44), color=CRIT, stroke_width=4)
        ta = label(r"the criterion moves", font_size=27, color=CRIT).next_to(A, UP, buff=0.15)
        tb = label(r"the sensitivity changes", font_size=27, color=MODEL).next_to(B, UP, buff=0.15)
        gb_far = gauss_pair(B.ax, 3.0)
        rows = rows_of([
            (r"slide the line left: \ hits and false alarms rise together, \ $d'$ unchanged", CRIT),
            (r"pull the distributions apart: \ hits rise and false alarms fall, \ $c$ unchanged", MODEL),
            (r"payoffs, \ base rates and instructions turn the first knob; \ practice, \ louder signals and better "
             r"eyes turn the second", WHITE),
        ], 12.4, 28, 0.24).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "So the observer has two knobs. <bookmark mark='a'/> Turn the first, and the line slides. Move it "
            "left and the observer says yes more, to signals and to blanks alike: hits and false alarms rise "
            "together, and d prime doesn't change. <bookmark mark='b'/> Turn the second, and the distributions "
            "move apart. Hits rise and false alarms fall at the same time. That's better seeing. "
            "<bookmark mark='c'/> Payoffs, base rates and instructions turn the first knob. Practice, stronger "
            "signals and better eyes turn the second. A yes-no threshold mixes them. The two numbers keep them "
            "apart."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(B), FadeIn(ga), FadeIn(gb), FadeIn(crit_a), FadeIn(crit_b), FadeIn(ta),
                      FadeIn(tb))
            vo.wait_until("a")
            self.play(crit_a.animate.move_to(A.ax.c2p(0.1, 0.22)), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Transform(gb.signal, gb_far.signal), crit_b.animate.move_to(B.ax.c2p(1.5, 0.22)), FadeIn(rows[1]),
                      run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def payoffs_again(self):
        d = load("payoffs")
        head = heading(r"Chapter 1's five schemes, \ in the two numbers")
        rows_t = VGroup()
        hdr = VGroup(*[label(t, font_size=26, color=GREY_A) for t in (r"scheme", r"hits", r"false alarms", r"$d'$", r"$c$")])
        widths = [4.2, 1.5, 2.2, 1.2, 1.4]

        def row(cells, colors):
            g = VGroup()
            x = 0.0
            for c, w, col in zip(cells, widths, colors):
                t = label(c, font_size=25, color=col)
                t.move_to([x + w / 2, 0, 0])
                g.add(t)
                x += w
            return g
        rows_t.add(row([r"scheme", r"hits", r"false alarms", r"$d'$", r"$c$"], [GREY_A] * 5))
        for i, name in enumerate(d["names"]):
            cval = 0.0 if abs(d["c"][i]) < 0.005 else d["c"][i]
            rows_t.add(row([name, pct(d["hit"][i]), pct(d["fa"][i]), f"{d['dprime'][i]:.2f}", f"{cval:+.2f}"],
                           [WHITE, HIT, FA, MODEL, CRIT]))
        for i, r in enumerate(rows_t):
            r.shift(DOWN * 0.55 * i)
        rows_t.move_to([0, 0.5, 0])
        del hdr
        rows = rows_of([
            (r"the sensitivity does not move; \ the criterion does all the moving", MODEL),
            (r"a hit rate on its own mixes the two. \ Report both rates, \ or both numbers", THRESH),
        ], 12.0, 29, 0.24).to_edge(DOWN, buff=0.7)
        tag = psyche_tag(r"computed: \ Psyche, \ chapter 1")
        with self.voiceover(
            "Now go back to chapter one's five reward schemes and convert each pair of rates. "
            "<bookmark mark='a'/> d prime comes out at one and a half every time. The criterion runs from "
            f"{d['c'][0]:.1f} when misses are expensive to plus {d['c'][-1]:.1f} when false alarms are. "
            "<bookmark mark='b'/> All the movement was in the saying. That's the first lesson of the theory: "
            "a hit rate on its own mixes seeing with saying. Report both rates, or both numbers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows_t[0]))
            self.play(LaggedStart(*[FadeIn(r) for r in rows_t[1:]], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("a")
            self.play(*[Indicate(r[3], color=MODEL) for r in rows_t[1:]], FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
        self.clear_scene()
