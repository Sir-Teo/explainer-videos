from __future__ import annotations

from videos.economics.econ53.common import *  # noqa: F403

CHOICES = (0.0, 0.2, 3 / 7, 0.6)


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Play it: \ design the investigation", r"How often should it flag the innocent?",
             "Chapter one. Play it: design the investigation.", lit={2011: r"Kamenica and Gentzkow"},
             scale=("person",), horizon=("a day",))
        self.ask()
        self.reveal()
        self.bayes()

    def ask(self):
        Pr = load("prosecutor")
        rows = VGroup(
            label(r"the investigation always flags the guilty", font_size=23, color=GUILTY),
            label(r"you choose how often it also flags an innocent defendant", font_size=23, color=INNOCENT),
            label(r"the judge convicts a flagged defendant only if, \ given your design, \ guilt is at least 50\%",
                  font_size=23, color=RECEIVER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(UP, buff=0.7)
        q = label(r"Which design convicts the most defendants?", font_size=26, color=E.ACCENT).next_to(
            rows, DOWN, buff=0.6)
        opts = VGroup()
        cols = (GRID, SIGNAL, SENDER, ERR)
        for x, c in zip(CHOICES, cols):
            b = RoundedRectangle(width=2.7, height=0.9, corner_radius=0.1, stroke_color=c, stroke_width=2,
                                 fill_color=c, fill_opacity=0.1)
            t = label(rf"flag {100 * x:.0f}\% \\ of the innocent", font_size=19, color=c).move_to(b)
            opts.add(VGroup(b, t))
        opts.arrange(RIGHT, buff=0.3).next_to(q, DOWN, buff=0.5)
        ring = countdown().scale(0.55).next_to(opts, DOWN, buff=0.4)
        with self.voiceover(
            "Your turn. You design the investigation. <bookmark mark='a'/> It always flags a guilty defendant. "
            "<bookmark mark='b'/> You choose how often it also flags an innocent one. <bookmark mark='c'/> The "
            f"judge, who knows that {100 * Pr['prior']:.0f} percent are guilty and knows your design, convicts a "
            "flagged defendant only if, given what the flag means, guilt is at least fifty percent likely. "
            "<bookmark mark='d'/> Which design convicts the most: flagging none of the innocent, a fifth of them, "
            "three in seven, or sixty percent? Pause, and choose."
        ) as vo:
            for mk, r_ in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(q), LaggedStart(*[FadeIn(o) for o in opts], lag_ratio=0.3), FadeIn(ring),
                      run_time=1.5)
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.play(FadeOut(ring))
        self.clear_scene()

    def reveal(self):
        Pr = load("prosecutor")
        ps = np.array(Pr["ps"])
        conv = np.array(Pr["convict"])
        post = np.array(Pr["posterior"])
        ax = plane([0, 1], [0, 1], center=LEFT * 1.8 + DOWN * 0.3, x_length=7.4, y_length=4.8,
                   xticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"share of the innocent flagged", ylabel=r"share of all defendants convicted",
                   xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        pstar = Pr["p_innocent"]
        k = int(np.searchsorted(ps, pstar))
        lx = np.concatenate([ps[:k], [pstar]])
        left = path(ax, lx, Pr["prior"] + (1 - Pr["prior"]) * lx, SENDER, 3.2, smooth=False)
        right = path(ax, np.concatenate([[pstar + 1e-6], ps[k:]]), np.zeros(len(ps) - k + 1), SENDER, 3.2,
                     smooth=False)
        postc = path(ax, ps, post, BELIEF, 2.0)
        half = DashedLine(ax.ax.c2p(0, 0.5), ax.ax.c2p(1, 0.5), color=RECEIVER, stroke_width=1.6)
        best = dot(ax, pstar, Pr["optimal"], SENDER, 0.12)
        marks = VGroup(*[dot(ax, x, (Pr["prior"] + (1 - Pr["prior"]) * x) if x <= pstar + 1e-9 else 0.0, c, 0.09)
                         for x, c in zip(CHOICES, (GRID, SIGNAL, SENDER, ERR))])
        del conv
        side = VGroup(
            label(r"gold: \ convictions", font_size=19, color=SENDER),
            label(r"purple: \ the judge's belief \\ in guilt after a flag", font_size=19, color=BELIEF),
            label(rf"best: \ flag 3 in 7 innocent: \\ {100 * Pr['optimal']:.0f}\% convicted", font_size=20,
                  color=SENDER),
            label(r"one step further, \\ and the flag means nothing \\ to the judge", font_size=19, color=ERR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Here is every design. <bookmark mark='a'/> The more innocent defendants the investigation flags, the "
            "more defendants are flagged, so convictions rise: from thirty percent if it flags none of the "
            "innocent. <bookmark mark='b'/> But each innocent one flagged lowers what a flag means. The purple "
            "line is the judge's belief in guilt after a flag. <bookmark mark='c'/> At three innocent flagged for "
            "every seven, that belief is exactly one half, the judge still convicts, and "
            f"{100 * Pr['optimal']:.0f} percent of defendants are convicted. <bookmark mark='d'/> Flag one more, "
            "and the belief falls below one half: the judge ignores the flag, and convictions fall to zero. The "
            "best design sits on the edge of the judge's willingness."
        ) as vo:
            self.play(FadeIn(ax), Create(half), FadeIn(marks))
            vo.wait_until("a")
            self.play(Create(left), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(postc), FadeIn(side[1]), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(best, scale=1.5), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(right), FadeIn(side[3]))
        self.clear_scene()

    def bayes(self):
        Pr = load("prosecutor")
        eq = MathTex(r"\Pr(\text{guilty}\mid\text{flag}) = \frac{0.3 \times 1}{0.3 \times 1 + 0.7 \times p}",
                     r"\;=\; \tfrac{1}{2} \iff p = \tfrac{3}{7}", font_size=40, color=THEORY).move_to(UP * 1.6)
        rows = VGroup(
            label(r"the judge is never fooled: \ on average, \ beliefs equal the truth", font_size=22,
                  color=WHITE),
            label(rf"of those convicted, \ half are innocent: \ {100 * Pr['innocent_convicted']:.0f} in 100 "
                  r"defendants", font_size=22, color=INNOCENT),
            label(r"the prosecutor uses only the judge's own standard of proof", font_size=22, color=SENDER),
        ).arrange(DOWN, buff=0.35).next_to(eq, DOWN, buff=0.7)
        with self.voiceover(
            "The arithmetic is Bayes's rule. The chance of guilt after a flag is the thirty percent who are guilty, "
            "all flagged, over everyone flagged. Set it equal to one half, and the innocent must be flagged three "
            "times in seven. <bookmark mark='a'/> Nobody is fooled: averaged over flags and no flags, the judge's "
            "beliefs are exactly right. <bookmark mark='b'/> But of those convicted, half are innocent: "
            f"{100 * Pr['innocent_convicted']:.0f} defendants in a hundred. <bookmark mark='c'/> The prosecutor "
            "has used nothing but the judge's own standard of proof. That is the lever this part studies."
        ) as vo:
            self.play(Write(eq), run_time=2.0)
            for mk, r_ in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
