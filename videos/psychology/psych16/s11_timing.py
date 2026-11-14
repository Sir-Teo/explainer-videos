from __future__ import annotations

import numpy as np

from videos.psychology.psych16.common import *  # noqa: F403


class Timing(VoiceoverScene):
    def construct(self):
        self.card()
        self.peak()
        self.spacing()

    def card(self):
        card = chapter_card(10, r"Time", r"Do animals learn when, \ as well as what?",
                            lit={2000: r"Gallistel \& Gibbon"}, part=PART, scale=("mind",), marr=("what", "how"))
        with self.voiceover("Chapter ten. Time."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def peak(self):
        d = load("timing")
        head = heading(r"The conditioned response is timed")
        A = axes([0, 120], [0, 1.05], x_length=5.6, y_length=3.2, xticks=[0, 20, 40, 60, 80, 100, 120],
                 yticks=[0, 0.5, 1], xlabel=r"seconds into the trial", ylabel=r"response rate", center=[-3.5, 0.6, 0],
                 font_size=18)
        B = axes([0, 2.5], [0, 1.05], x_length=4.6, y_length=3.2, xticks=[0, 1, 2], yticks=[0, 0.5, 1],
                 xlabel=r"time $\div$ the trained interval", ylabel="", center=[3.6, 0.6, 0], font_size=18)
        t = d["t"]
        cols = {20: CS, 40: US, 60: CR}
        cs = VGroup(*[curve(A.ax, t, d[f"p{T}"], cols[T], 3) for T in (20, 40, 60)])
        sc = VGroup(*[curve_in(B.ax, t / T, d[f"p{T}"], cols[T], 3) for T in (20, 40, 60)])
        sl = label(r"three curves, \ one on top of another", font_size=19, color=GREY_A).move_to(B.ax.c2p(1.95, 0.55))
        lg = legend([(cols[T], rf"trained interval {T} s") for T in (20, 40, 60)], font_size=19)
        lg.move_to(A.ax.c2p(96, 0.75))
        rows = rows_of([
            (r"the peak procedure: \ the outcome at a fixed time, \ then occasional long trials with none", WHITE),
            (r"responding peaks at the trained time, \ with a spread that grows in proportion to it", CR),
            (r"rescale time by the interval, \ and the curves lie on top of each other: \ Weber's law for time", YOU),
        ], 12.4, 25, 0.24).to_edge(DOWN, buff=0.55)
        tag = psyche_tag(r"computed: \ \texttt{conditioning.peak\_curve}, \ a coefficient of variation of 0.2")
        with self.voiceover(
            "In Rescorla-Wagner, time doesn't exist: there are only trials. Animals, though, learn when. "
            "<bookmark mark='a'/> In the peak procedure, a reward arrives a fixed time after a signal starts, and "
            "now and then a long trial comes with no reward at all. On those trials, responding rises, peaks around "
            "the trained time, and falls away. <bookmark mark='b'/> The longer the interval, the wider the peak, and "
            "the width grows in proportion to the interval. <bookmark mark='c'/> Divide time by the trained interval "
            "and the curves fall on top of each other. That's the scalar property, Weber's law from Part 11, applied "
            "to time: an animal timing twenty seconds is as precise, relatively, as one timing sixty."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag), FadeIn(lg))
            vo.wait_until("a")
            self.play(Create(cs[0]), FadeIn(rows[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(cs[1]), Create(cs[2]), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(B), *[Create(c) for c in sc], FadeIn(sl), FadeIn(rows[2]), run_time=2.0)
        self.clear_scene()

    def spacing(self):
        d = load("timing")
        head = heading(r"Rate estimation: \ a rival to associations")
        lr = np.log10(d["ratio"])
        A = axes([0, np.log10(30)], [0.8, 2.6], x_length=6.4, y_length=3.6, xticks=[0, np.log10(3), 1, np.log10(30)],
                 xfmt=lambda v: f"{10 ** v:.0f}", yticks=[1, 2], yfmt=lambda v: f"{10 ** v:.0f}",
                 xlabel=r"$I/T$: \ the gap between trials over the signal's length",
                 ylabel=r"reinforcements to learn", center=[-2.8, 0.4, 0])
        ax = A.ax
        gg = curve(ax, lr, np.log10(d["gg"]), US, 4)
        rw = curve(ax, lr, np.log10(d["rw"]), GREY_B, 4)
        lg = legend([(US, r"autoshaping data, \ as summarized: \ $n \approx 300\,(I/T)^{-1}$"),
                     (GREY_B, r"Rescorla-Wagner with a context, \ Psyche")], font_size=19).next_to(A, DOWN, buff=0.25)
        rows = rows_of([
            (r"spread the trials out and animals need fewer of them: \ in proportion to $I/T$", US),
            (r"only the ratio matters, \ not the gap or the signal's length on its own", WHITE),
            (r"Rescorla-Wagner, \ counting trials, \ barely notices", GREY_B),
            (r"Gallistel and Gibbon: \ animals estimate the rate of reward with the signal and without it, \ and "
             r"respond when the ratio is clear", YOU),
        ], 4.6, 23, 0.3).move_to([4.5, 0.2, 0])
        keep_in_frame(rows)
        tag = published_tag(archive.GALLISTEL_GIBBON_2000.cite)
        tag2 = psyche_tag(r"computed: \ \texttt{rw\_trials\_to\_criterion}")
        with self.voiceover(
            "Time also breaks the rule in a deeper way. <bookmark mark='a'/> In autoshaping, a key lights up before "
            "food, and pigeons come to peck it. Spread the trials further apart and the birds need fewer of them to "
            "learn: across many experiments, the number of rewards needed falls in proportion to the ratio of the "
            "gap between trials to the length of the signal, about three hundred divided by that ratio. "
            "<bookmark mark='b'/> Only the ratio matters. Double the gap and the signal together and nothing changes. "
            "<bookmark mark='c'/> Rescorla-Wagner, counting trials and letting the context compete, barely notices "
            "the spacing. <bookmark mark='d'/> Randy Gallistel and John Gibbon proposed a different machine. The "
            "animal doesn't strengthen links at all. It estimates two rates of reward, one while the signal is on and "
            "one overall, and starts to respond when their ratio is clearly greater than one. The ratio of rates is "
            "set by I over T, so the law falls out. Associations or computations of rate: the argument isn't settled, "
            "and the ratio law itself turns out to have exceptions."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag), FadeIn(tag2))
            vo.wait_until("a")
            self.play(Create(gg), FadeIn(lg[0]), FadeIn(rows[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(rw), FadeIn(lg[1]), FadeIn(rows[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
