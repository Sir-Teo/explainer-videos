from __future__ import annotations

import numpy as np
from scipy import stats

from videos.psychology.psych13.common import *  # noqa: F403


class Quanta(VoiceoverScene):
    def construct(self):
        self.card()
        self.poisson()
        self.curves()
        self.experiment()
        self.single()
        self.floor()

    def card(self):
        card = chapter_card(1, r"Counting quanta", r"How can you count something no one can see?",
                            lit={1942: r"Hecht, Shlaer, Pirenne"}, part=PART, scale=("molecule", "mind"), marr=("what",))
        with self.voiceover("Chapter one. Counting quanta."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def poisson(self):
        head = heading(r"Light arrives in packets, \ at random")
        lam = 6.0
        k = np.arange(0, 16)
        pmf = stats.poisson.pmf(k, lam)
        A = axes([-0.5, 15.5], [0, 0.18], x_length=7.0, y_length=3.6, xticks=[0, 5, 10, 15], yticks=[0, 0.05, 0.1, 0.15],
                 xlabel=r"quanta absorbed on one flash", ylabel=r"probability", center=[-2.6, -0.4, 0])
        ax = A.ax
        bars = VGroup(*[Rectangle(width=0.36, height=max(ax.c2p(0, p)[1] - ax.c2p(0, 0)[1], 0.001), stroke_width=0,
                                  fill_color=LIGHT, fill_opacity=0.85).move_to(ax.c2p(kk, 0), aligned_edge=DOWN)
                        for kk, p in zip(k, pmf)])
        thr = 6
        line = DashedLine(ax.c2p(thr - 0.5, 0), ax.c2p(thr - 0.5, 0.17), color=MODEL, stroke_width=3)
        seen = label(r"seen", font_size=24, color=MODEL).next_to(ax.c2p(thr + 3, 0.165), DOWN, buff=0)
        unseen = label(r"not seen", font_size=24, color=GREY_B).next_to(ax.c2p(thr - 3, 0.165), DOWN, buff=0)
        p_seen = float(stats.poisson.sf(thr - 1, lam))
        rows = rows_of([
            (r"the same flash, \ repeated: \ the number absorbed varies by chance", LIGHT),
            (r"a Poisson count: \ if the mean is 6, \ any one flash may give 2, \ or 10", WHITE),
            (rf"suppose the eye sees the flash when at least $k$ arrive, \ here $k = 6$: \ then it is seen "
             rf"{pct(p_seen)} of the time", MODEL),
            (r"so even a perfect, \ noiseless observer will miss some flashes and catch others", GREY_A),
        ], 4.6, 27, 0.32).move_to([4.3, -0.1, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ the Poisson distribution, \ mean 6")
        with self.voiceover(
            "Here is the idea that made it possible to count. Light doesn't flow; it arrives in packets, and the "
            "packets arrive at random. <bookmark mark='a'/> Fire the same flash again and again, and the number of "
            "quanta absorbed is different each time. <bookmark mark='b'/> It follows a Poisson distribution: with an "
            "average of six, one flash may deliver two, and another ten. <bookmark mark='c'/> Now suppose the eye "
            "sees a flash whenever at least some number, k, of quanta are absorbed. Say six. Then this flash is seen "
            "a little more than half the time. <bookmark mark='d'/> So even an observer with no noise of its own, "
            "with a fixed and perfect threshold, would see some flashes and miss others. The randomness is in the "
            "light."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.08), FadeIn(rows[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(line), FadeIn(seen), FadeIn(unseen), FadeIn(rows[2]),
                      *[b.animate.set_fill(MODEL) for kk, b in zip(k, bars) if kk >= thr])
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def curves(self):
        d = load("quanta")
        head = heading(r"The steepness of the curve gives $k$")
        lam = d["lam"]
        A = axes([np.log10(0.3), np.log10(40)], [0, 1], x_length=7.0, y_length=4.0,
                 xticks=[np.log10(v) for v in (0.5, 1, 2, 5, 10, 20)], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{10 ** v:g}", xlabel=r"mean quanta absorbed (log scale)", ylabel=r"P(seen)",
                 center=[-2.6, -0.4, 0])
        ax = A.ax
        ks = (1, 2, 4, 6, 9)
        cols = [interpolate_color(ManimColor(GREY_B), ManimColor(LIGHT), i / (len(ks) - 1)) for i in range(len(ks))]
        cs = VGroup(*[curve(ax, np.log10(lam), d["curves"][str(kk)], c, stroke_width=4) for kk, c in zip(ks, cols)])
        labs = legend([(c, rf"$k = {kk}$") for kk, c in zip(ks, cols)], font_size=20).move_to(ax.c2p(np.log10(0.75), 0.72))
        # shifting by efficiency: the k = 6 curve moved left and right
        base = d["curves"]["6"]
        shifted = VGroup(*[curve_in(ax, np.log10(lam) + s, base, MODEL, stroke_width=3).set_stroke(opacity=0.6)
                           for s in (-0.4, 0.4)])
        rows = rows_of([
            (r"the larger $k$, \ the steeper the rise from never seen to always seen", LIGHT),
            (r"nobody knew how much of the flash the eye loses: \ but a loss only slides the curve along a log axis", MODEL),
            (r"sliding does not change its steepness: \ the shape alone tells you $k$", WHITE),
            (r"the steepness at the middle grows with $k$: \ 0.8 for $k = 1$, \ 2.2 for $k = 6$, \ 2.7 for $k = 9$ "
             r"(per tenfold step)", GREY_A),
        ], 4.6, 26, 0.3).move_to([4.3, -0.1, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ Poisson tails")
        with self.voiceover(
            "Now plot the chance of seeing against the brightness of the flash, on a log scale. <bookmark mark='a'/> "
            "If one quantum is enough, the curve rises gently. If six are needed, it rises steeply; if nine, more "
            "steeply still. A threshold of many quanta is sharper, because a sum of many random arrivals is "
            "relatively less variable. <bookmark mark='b'/> Here is the clever part. Hecht and his colleagues didn't "
            "know exactly how much light the eye wastes before the rods. But a fixed loss multiplies every "
            "intensity by the same factor, and on a log axis that only slides the curve sideways. "
            "<bookmark mark='c'/> Sliding doesn't change the steepness. So the shape of the observer's own curve "
            "tells you k, without knowing the loss at all. <bookmark mark='d'/> The arithmetic is in the problems: "
            "the steepness depends on k alone."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c) for c in cs], lag_ratio=0.3), FadeIn(labs), FadeIn(rows[0]), run_time=3.0)
            vo.wait_until("b")
            self.play(cs.animate.set_stroke(opacity=0.25), labs.animate.set_opacity(0.3), FadeIn(rows[1]))
            self.play(Create(shifted), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Indicate(shifted, color=MODEL))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def experiment(self):
        d = load("quanta")
        head = heading(r"Psyche in the dark room")
        A = axes([np.log10(15), np.log10(400)], [0, 1], x_length=5.6, y_length=3.6,
                 xticks=[np.log10(v) for v in (20, 50, 100, 200)], yticks=[0, 0.5, 1], xfmt=lambda v: f"{10 ** v:g}",
                 xlabel=r"quanta at the cornea (log scale)", ylabel=r"share seen", center=[-3.6, -0.2, 0])
        ax = A.ax
        pts = scatter(ax, np.log10(d["q"]), d["seen"] / d["n"], LIGHT, radius=0.08)
        fit = curve(ax, np.log10(d["qq"]), d["fit_curve"], MODEL, stroke_width=4)
        counts = np.asarray(d["k_counts"], float)
        B = axes([1.5, 12.5], [0, 40], x_length=4.2, y_length=1.9, xticks=[2, 4, 6, 8, 10, 12], yticks=[0, 20, 40],
                 xlabel=r"$k$ fitted, \ 101 experiments", ylabel=r"experiments", center=[3.6, 1.55, 0])
        bx = B.ax
        hb = VGroup(*[Rectangle(width=0.3, height=max(bx.c2p(0, c)[1] - bx.c2p(0, 0)[1], 0.001), stroke_width=0,
                                fill_color=MODEL if i == d["k_true"] else GREY_B, fill_opacity=0.85)
                      .move_to(bx.c2p(i, 0), aligned_edge=DOWN) for i, c in enumerate(counts) if 2 <= i <= 12])
        rows = rows_of([
            (rf"Psyche needs $k = {d['k_true']}$ and absorbs {pct(d['eff_true'])} of the light: \ 7 intensities, \ "
             rf"{d['n']} flashes each", WHITE),
            (rf"fitting the curve's shape: \ $k = {d['k_fit']}$, \ and {pct(d['eff_fit'], 1)} absorbed", MODEL),
            (rf"over 101 such experiments the fitted $k$ is within one of the truth {pct(d['k_within1'])} of the time",
             GREY_A),
            (r"1942: \ the curves' shapes gave 5 to 8; \ the physics of losses gave 5 to 14. \ Two routes, \ one "
             r"answer", LIGHT),
        ], 6.0, 23, 0.2)
        rows.next_to(B, DOWN, buff=0.3).align_to(B, LEFT)
        keep_in_frame(rows)
        tag = psyche_tag(r"simulated: \ the median experiment of 101")
        with self.voiceover(
            "Psyche can sit in the same dark room. Give it a threshold of six quanta, and let it absorb nine percent "
            "of the light that reaches its eye. <bookmark mark='a'/> Seven intensities, fifty flashes each, and "
            "here's the share it saw. <bookmark mark='b'/> Fit the Poisson curve to those points, letting both k and "
            "the loss be free, and out comes k equals six, and nine percent absorbed. <bookmark mark='c'/> Repeat "
            "the whole experiment a hundred and one times, and the fitted k is within one of the truth four times in "
            "five. Fifty flashes a point is enough to count to six, roughly. <bookmark mark='d'/> In 1942 the "
            "observers' curves gave between five and eight, and the physics of the losses gave between five and "
            "fourteen. Two independent routes to the same small number."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p, scale=1.5) for p in pts], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(B), LaggedStart(*[GrowFromEdge(b, DOWN) for b in hb], lag_ratio=0.1), FadeIn(rows[2]),
                      run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def single(self):
        d = load("quanta")
        b = d["baylor"]
        p, se, pv, trials, events = d["tinsley"]
        head = heading(r"One rod, \ one quantum; \ one person, \ one photon?")
        left = rows_of([
            (r"1979: \ a single rod, \ recorded", ROD),
            (rf"one absorbed quantum: \ a current of about {b['event_pA']:g} pA, \ "
             rf"{pct(b['dark_current_share'])} of the rod's standing current", WHITE),
            (rf"and about half of the quanta a rod absorbs produce one", GREY_A),
        ], 5.6, 27, 0.3)
        A = axes([0, 1], [0.45, 0.65], x_length=4.6, y_length=2.8, yticks=[0.5, 0.55, 0.6],
                 xlabel="", ylabel=r"share correct", center=[0, 0, 0])
        ax = A.ax
        chance = DashedLine(ax.c2p(0, 0.5), ax.c2p(1, 0.5), color=GREY_B, stroke_width=2)
        bar_all = Rectangle(width=0.9, height=ax.c2p(0, p)[1] - ax.c2p(0, 0.45)[1], stroke_width=0, fill_color=LIGHT,
                            fill_opacity=0.85).move_to(ax.c2p(0.3, 0.45), aligned_edge=DOWN)
        err = Line(ax.c2p(0.3, p - 2 * se), ax.c2p(0.3, p + 2 * se), color=WHITE, stroke_width=3)
        bar_hi = Rectangle(width=0.9, height=ax.c2p(0, archive.TINSLEY_2016.data["high_confidence"])[1]
                           - ax.c2p(0, 0.45)[1], stroke_width=0, fill_color=YOU, fill_opacity=0.6).move_to(
            ax.c2p(0.75, 0.45), aligned_edge=DOWN)
        l1 = label(r"all", font_size=22, color=GREY_A).next_to(bar_all, DOWN, buff=0.12)
        l2 = label(r"``sure''", font_size=22, color=GREY_A).next_to(bar_hi, DOWN, buff=0.12)
        ch = label(r"chance", font_size=20, color=GREY_B).next_to(ax.c2p(1, 0.5), RIGHT, buff=0.1)
        right = VGroup(A, chance, bar_all, err, bar_hi, l1, l2, ch)
        rrows = rows_of([
            (rf"2016: \ single photons from a quantum source; \ which of two intervals held one? \ "
             rf"{num(trials)} trials", WHITE),
            (rf"single-photon trials: \ {pct(p, 1)} correct; \ $P = {pv}$", LIGHT),
            (r"just above chance, \ at the edge of significance; \ about 60\% when the observer felt sure. \ Not yet "
             r"repeated", GREY_A),
        ], 5.6, 25, 0.28)
        g = VGroup(VGroup(left, rrows).arrange(DOWN, buff=0.5, aligned_edge=LEFT), right).arrange(RIGHT, buff=0.7)
        g.move_to([0, -0.3, 0])
        keep_in_frame(g)
        tags = VGroup(published_tag(r"Baylor, Lamb \& Yau (1979); \ Tinsley et al.\ (2016)"))
        with self.voiceover(
            "The 1942 argument said a single rod must respond to a single quantum. Thirty-seven years later, that "
            "could be checked directly. <bookmark mark='a'/> In 1979 Denis Baylor, Trevor Lamb and King-Wai Yau "
            "drew a single rod from a toad's retina into a fine glass tube and measured its current. One absorbed "
            "quantum gave a pulse of about one picoamp, five percent of the current the rod carries in the dark. "
            "About half the quanta the rod absorbed produced one. <bookmark mark='b'/> Can a person report a single "
            "photon? In 2016 a group in Vienna used a quantum light source that emits photons one at a time, and "
            "asked which of two intervals had held one. <bookmark mark='c'/> Over thirty thousand trials, the "
            "answer on single-photon trials was right fifty-one point six percent of the time, against fifty for "
            "guessing. The p value was point oh five five: at the edge. When the observers said they were sure, "
            "about sixty percent. It is a remarkable result, and it has not yet been repeated. The Ledger will say so."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tags))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in left], lag_ratio=0.6), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(rrows[0]), FadeIn(A), Create(chance), FadeIn(ch))
            vo.wait_until("c")
            self.play(GrowFromEdge(bar_all, DOWN), Create(err), FadeIn(l1), FadeIn(rrows[1]))
            self.play(GrowFromEdge(bar_hi, DOWN), FadeIn(l2), FadeIn(rrows[2]))
        self.clear_scene()

    def floor(self):
        head = heading(r"Photon noise sets the floor")
        A = axes([-2, 4], [-1, 3], x_length=6.0, y_length=3.8, xticks=[-2, 0, 2, 4], yticks=[-1, 0, 1, 2, 3],
                 xfmt=lambda v: f"10^{{{int(v)}}}", yfmt=lambda v: f"10^{{{int(v)}}}",
                 xlabel=r"background light", ylabel=r"smallest visible increment", center=[-3.0, -0.4, 0])
        ax = A.ax
        x = np.linspace(-2, 4, 200)
        dark = np.full_like(x, -0.8)
        sqrt_law = -0.8 + 0.5 * (x + 1.6)
        weber = 0.5 * (1.4 + 1.6) - 0.8 + 1.0 * (x - 1.4)
        y = np.maximum.reduce([dark, np.where(x < 1.4, sqrt_law, -9), np.where(x >= 1.4, weber, -9)])
        cv = curve(ax, x, y, LIGHT, stroke_width=5)
        rows = rows_of([
            (r"against a dim background, \ the background's own quanta fluctuate: \ a Poisson count of $N$ varies by "
             r"$\sqrt N$", WHITE),
            (r"to be seen, \ a flash must stand out from that noise: \ the threshold grows as the square root of the "
             r"background (de Vries 1943, \ Rose 1948)", LIGHT),
            (r"brighter, \ the eye turns its own gain down, \ and Weber's law of Part 11 takes over (chapter 3)", GREY_A),
        ], 5.6, 26, 0.32).move_to([3.6, -0.2, 0])
        keep_in_frame(rows)
        sq = label(r"slope $\tfrac12$", font_size=22, color=LIGHT).next_to(ax.c2p(0.2, -0.3), UP + LEFT, buff=0.05)
        wb = label(r"slope 1", font_size=22, color=LIGHT).next_to(ax.c2p(3.0, 1.1), LEFT, buff=0.15)
        tag = note(r"the shape of the law, \ drawn; \ not data").to_corner(DR, buff=0.3)
        with self.voiceover(
            "The same arithmetic explains the eye's limits against a background. <bookmark mark='a'/> A dim "
            "background also arrives in quanta, and their count fluctuates: if N arrive on average, the count varies "
            "by about the square root of N. <bookmark mark='b'/> To be seen, an extra flash has to stand out from that "
            "noise, so the smallest visible increment grows as the square root of the background. Hessel de Vries "
            "in 1943 and Albert Rose in 1948 saw that this is what an ideal detector of quanta would do. Part 11 ran "
            "it on Psyche. <bookmark mark='c'/> In brighter light the eye does something else: it turns its own gain "
            "down, and Weber's law takes over. That is chapter three."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cv), FadeIn(sq), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(wb), FadeIn(rows[2]))
        self.clear_scene()
