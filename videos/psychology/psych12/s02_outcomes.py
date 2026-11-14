from __future__ import annotations

import numpy as np

from videos.psychology.psych12.common import *  # noqa: F403


class Outcomes(VoiceoverScene):
    def construct(self):
        self.card()
        self.table()
        self.payoffs()
        self.guessing()

    def card(self):
        card = chapter_card(1, r"Four outcomes", r"What does a hit rate tell you on its own?",
                            lit={1954: r"Tanner and Swets"}, part=PART, scale=("mind", "person"), marr=("what",))
        with self.voiceover(
            "Chapter one. Four outcomes."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def table(self):
        head = heading(r"Two states of the world, \ two answers")
        t = outcome_table(width=6.6, font_size=28).move_to([-2.6, -0.1, 0])
        rows = rows_of([
            (r"a signal was there and the observer said yes: \ a hit", HIT),
            (r"it was there and the observer said no: \ a miss", MISS),
            (r"nothing was there and the observer said yes: \ a false alarm", FA),
            (r"nothing was there and the observer said no: \ a correct rejection", HIT),
            (r"misses are the hits' complement, \ correct rejections the false alarms': \ two numbers carry it all", THRESH),
        ], 5.2, 27, 0.26).move_to([4.2, -0.2, 0])
        keep_in_frame(rows)
        with self.voiceover(
            "Every detection has two states of the world and two answers, so four outcomes. "
            "<bookmark mark='a'/> A signal was there, and the observer said yes: a hit. <bookmark mark='b'/> It "
            "was there, and the observer said no: a miss. <bookmark mark='c'/> Nothing was there, and the "
            "observer said yes: a false alarm. <bookmark mark='d'/> Nothing was there, and the observer said "
            "no: a correct rejection. <bookmark mark='e'/> Misses are just the hits that didn't happen, and "
            "correct rejections the false alarms that didn't. So two numbers carry everything: the hit rate "
            "and the false-alarm rate. Hold on to both, because one of them on its own is worth nothing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(t.cells[0][0], t.cells[1][0], t.cells[2][0], t.cells[3][0]), FadeIn(t[1]), FadeIn(t[2]))
            for i, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(t.cells[i][1]), FadeIn(rows[i]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]), t.cells[1].animate.fade(0.6), t.cells[3].animate.fade(0.6))
        self.clear_scene()

    def payoffs(self):
        d = load("payoffs")
        head = heading(r"One observer, \ five reward schemes")
        n = len(d["names"])
        A = axes([-0.5, n - 0.5], [0, 1.05], x_length=7.2, y_length=3.8, xticks=[], yticks=[0, 0.5, 1],
                 yfmt=lambda v: f"{v:g}", xlabel=r"", ylabel=r"share answered ``yes''", center=[-2.8, 0.15, 0])
        ax = A.ax
        bars, names = VGroup(), VGroup()
        for i in range(n):
            for j, (v, col) in enumerate(((d["hit"][i], HIT), (d["fa"][i], FA))):
                x = i - 0.18 + 0.36 * j
                bars.add(Rectangle(width=0.3, height=max(ax.c2p(0, float(v))[1] - ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                                   fill_color=col, fill_opacity=0.85).move_to(ax.c2p(x, 0), aligned_edge=DOWN))
            names.add(wrapped_label(d["names"][i], 1.35, 19, GREY_A).next_to(ax.c2p(i, 0), DOWN, buff=0.18))
        lg = legend([(HIT, r"hits (signal trials)"), (FA, r"false alarms (blank trials)")], font_size=23).move_to(ax.c2p(3.3, 0.95))
        dp = label(rf"$d' = {d['dprime'][0]:.1f}$ \ in every scheme", font_size=28, color=MODEL).next_to(A, DOWN, buff=1.05)
        rows = rows_of([
            (r"the same eyes, \ the same signals: \ only the rewards change", WHITE),
            (rf"hits run from {pct(d['hit'][0])} down to {pct(d['hit'][-1])}", HIT),
            (r"a ``threshold'' read from the hit rate would move fourfold", MISS),
            (r"but the false alarms move with them, \ in lockstep", FA),
            (r"what stays fixed is a combination of the two: \ the sensitivity, \ chapter 2", MODEL),
        ], 4.6, 27, 0.26).move_to([4.6, 0.0, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ Psyche with $d' = 1.5$, \ the best criterion for each scheme")
        with self.voiceover(
            "Here's why. Take one of Psyche's observers and run five experiments. The signals are the same, "
            "the observer's eyes are the same. <bookmark mark='a'/> Only the rewards change: in one, a miss costs "
            "four times as much as a false alarm; in another, it's the other way round. The hit rate "
            f"runs from {100 * d['hit'][0]:.0f} percent down to {100 * d['hit'][-1]:.0f} percent. "
            "<bookmark mark='b'/> If you defined a threshold by the hit rate, it would move with the money. "
            "<bookmark mark='c'/> But look at the false alarms. They move in lockstep: when the observer "
            "says yes more often to signals, it says yes more often to blanks. <bookmark mark='d'/> Something "
            "stays fixed underneath, and it's a combination of the two rates. That combination is the "
            "sensitivity, and finding it is chapter two. Tanner and Swets made exactly this argument in "
            "1954: the yes-no threshold is not a property of the eye. It's a decision."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[0::2]], lag_ratio=0.2), FadeIn(lg), FadeIn(rows[1]),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[1::2]], lag_ratio=0.2), FadeIn(rows[3]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(dp), FadeIn(rows[4]))
        self.clear_scene()

    def guessing(self):
        d = load("guessing")
        head = heading(r"The old fix: \ ``correct for guessing''")
        eq = MathTex(r"p = \frac{H - F}{1 - F}", font_size=46, color=RIVAL).move_to([-3.4, 2.0, 0])
        A = axes([-0.5, 4.5], [0, 1.0], x_length=6.0, y_length=3.2, xticks=[], yticks=[0, 0.5, 1], yfmt=lambda v: f"{v:g}",
                 xlabel=r"five criteria, \ from lax to strict", ylabel=r"", center=[-3.2, -1.15, 0])
        ax = A.ax
        cor = VGroup(*[Dot(ax.c2p(i, float(v)), radius=0.09, color=RIVAL) for i, v in enumerate(d["corrected"])])
        cline = curve(ax, np.arange(5), d["corrected"], RIVAL, stroke_width=3)
        dl = curve(ax, np.arange(5), d["dprime"] / 2.0, MODEL, stroke_width=4)
        lg = legend([(RIVAL, r"``corrected'' hit rate"), (MODEL, r"$d'$ (scaled by $\tfrac12$)")], font_size=22
                    ).move_to(ax.c2p(3.2, 0.92))
        rows = rows_of([
            (r"a formula long used on yes-no and multiple-choice tests: \ subtract the false alarms as guesses", WHITE),
            (r"it assumes a gate: \ either the signal got through, \ or the observer guessed (chapter 8)", RIVAL),
            (rf"run it on one detection observer at five criteria: \ it slides from {d['corrected'][0]:.2f} to "
             rf"{d['corrected'][-1]:.2f}", RIVAL),
            (rf"$d'$ stays at {d['d']:.1f} throughout", MODEL),
            (r"a correction is a model. \ Choose the wrong one, \ and caution still leaks into the score", THRESH),
        ], 5.0, 26, 0.28).move_to([3.9, 0.0, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ $d' = 1.5$")
        with self.voiceover(
            "There was an older fix for this, and it's still found in multiple-choice scoring and some clinical "
            "tests. <bookmark mark='a'/> Correct for guessing: treat the false alarms as lucky guesses, subtract them "
            "from the hits, and rescale. <bookmark mark='b'/> The formula quietly assumes a gate: on each trial "
            "either the signal got through, or the observer guessed blindly. Chapter eight puts that assumption on "
            "trial. <bookmark mark='c'/> Run it on one of Psyche's detection observers at five different criteria. "
            f"The corrected score slides from {d['corrected'][0]:.2f} down to {d['corrected'][-1]:.2f}. "
            f"<bookmark mark='d'/> d prime stays at {d['d']:.1f} the whole way. <bookmark mark='e'/> Every correction is "
            "a model of how the answer was produced. Pick the wrong model, and the observer's caution leaks back "
            "into the score."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(Write(eq), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(cline), LaggedStart(*[FadeIn(c) for c in cor], lag_ratio=0.2), FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(Create(dl), FadeIn(lg), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

