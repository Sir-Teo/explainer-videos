from __future__ import annotations

from videos.psychology.psych61.common import *  # noqa: F403


class Discovery(VoiceoverScene):
    def construct(self):
        card_section(self, 7, r"Machine-assisted theory", r"Can a machine help find a theory?", marr=("what",))
        self.peterson()
        self.adaptive()
        self.simulate()

    def peterson(self):
        rows_section(self, r"Ten thousand gambles", [
            (r"Peterson and colleagues, \ 2021: \ choices on nearly 10,000 pairs of gambles (Part 26's choices13k), "
             r"\ far more than any earlier study", WHITE),
            (r"neural networks constrained to different classes of theory were fitted and compared", MODEL),
            (r"the best learned theory contained prospect theory's pieces, \ and showed where they bend with "
             r"context", GOOD),
            (r"the machine searches; \ people still read and judge what it found", YOU),
        ], "Can a machine help find a theory? <bookmark mark='a'/> In 2021 Joshua Peterson and colleagues collected "
           "choices on nearly ten thousand pairs of gambles, Part 26's choices13k, far more than any earlier study. "
           "<bookmark mark='b'/> They fitted neural networks constrained to different classes of theory, and "
           "compared them. <bookmark mark='c'/> The best learned theory contained prospect theory's pieces, and "
           "showed where they bend with context. <bookmark mark='d'/> The machine searches, and people still read "
           "and judge what it found.", tag=published_tag(r"Peterson et al.\ (2021)"))

    def adaptive(self):
        chips_section(self, r"Choosing the next experiment", [
            (r"adaptive design", r"after each trial or study, \ choose the next one that best separates the "
                                 r"theories still standing (Myung and Pitt)", MODEL),
            (r"why it works", r"the expected information about which theory is right, \ computed before running", PERSON),
            (r"Part 45's link", r"the same idea as adaptive testing: \ ask the question whose answer you cannot "
                                r"yet predict", GOOD),
            (r"the guard", r"the theories and the stopping rule are fixed in advance, \ or adaptivity becomes "
                           r"forking paths", AUTH),
        ], "Machines can also choose the next experiment. <bookmark mark='a'/> In adaptive design, after each trial "
           "or study you choose the next one that best separates the theories still standing, as Jay Myung and Mark "
           "Pitt developed. <bookmark mark='b'/> It works by computing the expected information about which theory is "
           "right, before running. <bookmark mark='c'/> It's the same idea as Part 45's adaptive testing: ask the "
           "question whose answer you can't yet predict. <bookmark mark='d'/> The guard: the theories and the "
           "stopping rule are fixed in advance, or adaptivity becomes forking paths.")

    def simulate(self):
        d = load("adaptive")
        head = heading(r"Adaptive against fixed, \ in Psyche")
        lags = np.asarray(d["lags"])
        tt = np.linspace(0, 60, 121)
        A1 = axes([0, 60], [0, 1.0], x_length=4.4, y_length=2.1, xticks=[0, 20, 40, 60], yticks=[0, 0.5, 1.0],
                  xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"delay", ylabel=r"recall",
                  center=[-4.0, 1.45, 0], font_size=11)
        pw = curve(A1.ax, tt, 0.95 * (1 + tt) ** -0.45, MODEL, stroke_width=3)
        ex = curve(A1.ax, tt, 0.95 * np.exp(-0.08 * tt), PERSON, stroke_width=3)
        k1 = label(r"power law", font_size=15, color=MODEL).move_to(A1.ax.c2p(30, 0.92), aligned_edge=LEFT)
        k2 = label(r"exponential", font_size=15, color=PERSON).move_to(A1.ax.c2p(30, 0.74), aligned_edge=LEFT)
        ticks = VGroup(*[Line(A1.ax.c2p(x, 0), A1.ax.c2p(x, 0.06), color=GREY_B, stroke_width=2) for x in lags])
        n = len(d["median_fixed"])
        g = np.arange(n)
        A2 = axes([0, n - 1], [0.5, 1.0], x_length=4.4, y_length=2.1, xticks=[0, 20, 40, 60, 80],
                  yticks=[0.5, 0.75, 1.0], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}",
                  xlabel=r"tests", ylabel=r"P(power law)", center=[-4.0, -1.6, 0], font_size=11)
        target = DashedLine(A2.ax.c2p(0, 0.95), A2.ax.c2p(n - 1, 0.95), color=GREY_B, stroke_width=1.5)
        fx = curve(A2.ax, g, d["median_fixed"], AUTH, stroke_width=3)
        ad = curve(A2.ax, g, d["median_adaptive"], GOOD, stroke_width=3)
        rows = rows_of([
            (r"two theories of forgetting, \ parameters fixed: \ they nearly agree at middling delays, \ and "
             r"part at short and long ones", WHITE),
            (rf"each simulated person forgets by the power law; \ a fixed design cycles through ten delays: \ "
             rf"a median of {d['trials_fixed']:.0f} tests to be 95\% sure", AUTH),
            (rf"the adaptive design picks the most informative delay before each test: \ the longest, \ "
             rf"{100 * d['picks'][-1]:.0f}\% of the time, \ where the exponential predicts almost no recall: \ "
             rf"{d['trials_adaptive']:.0f} tests", GOOD),
            (r"Cavagnaro, \ Myung and Pitt's criterion; \ the saving matters most when each test is costly", YOU),
        ], 6.2, 18, 0.34).move_to([3.0, -0.1, 0])
        tag = psyche_tag(r"\texttt{community.adaptive\_design}")
        with self.voiceover(
            "Here's adaptive design in Psyche. <bookmark mark='a'/> There are two theories of forgetting, a power "
            "law and an exponential, with their parameters fixed. They nearly agree at middling delays, and part at "
            "short and long ones. <bookmark mark='b'/> Each simulated person forgets by the power law, and each "
            "trial is one recall test. A fixed design cycles through ten delays. It needs a median of twenty-five "
            "tests to be ninety-five percent sure which theory is right. <bookmark mark='c'/> The adaptive design "
            "asks, before each test, which delay is most informative. It picks the longest delay almost every "
            "time, because there the exponential predicts almost no recall, and it needs eleven tests. "
            "<bookmark mark='d'/> That's the criterion Daniel Cavagnaro, Jay Myung and Mark Pitt developed, and one "
            "of their first demonstrations used this pair of theories. The saving matters most when each test is "
            "costly, as it is with patients or infants."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A1), FadeIn(A2), FadeIn(target))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(pw), Create(ex), FadeIn(k1), FadeIn(k2), FadeIn(ticks), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(fx), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(ad), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
