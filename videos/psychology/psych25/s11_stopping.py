from __future__ import annotations

from videos.psychology.psych25.common import *  # noqa: F403


class Stopping(VoiceoverScene):
    def construct(self):
        self.card()
        self.race()
        self.inhibition()

    def card(self):
        card = chapter_card(10, r"Stopping", r"How long does it take to cancel an action?",
                            lit={1984: r"Logan \& Cowan", 2019: r"Verbruggen et al.", 2021: r"Bissett et al."},
                            part=PART, scale=("mind",), marr=("how",))
        with self.voiceover("Chapter ten. Stopping."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def race(self):
        d = load("stop")
        head = heading(r"Derivation: \ the stop-signal race")
        A = axes([0, 1.0], [0, 4.6], x_length=7.0, y_length=3.4, xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[],
                 xfmt=lambda v: f"{v:.2f}", xlabel=r"time from the go signal, \ s", center=[-2.6, -0.5, 0],
                 font_size=16)
        mids = (d["edges"][:-1] + d["edges"][1:]) / 2
        ssd = 0.25
        cut = ssd + d["ssrt"]
        w = float(np.diff(d["edges"])[0]) * 0.95
        left = bars(A.ax, mids[mids < cut], d["go_hist"][mids < cut], LOST, width=w, opacity=0.85)
        rm = (mids >= cut) & (mids <= 0.99)
        right = bars(A.ax, mids[rm], d["go_hist"][rm], GREY_B, width=w, opacity=0.6)
        go_l = label(r"go times: \ how long the response would take, \ unopposed", font_size=18, color=GREY_A
                     ).next_to(A.ax.c2p(0.55, 4.3), RIGHT, buff=0.0)
        s1 = DashedLine(A.ax.c2p(0, 4.5), A.ax.c2p(0, 0), color=WHITE, stroke_width=2)
        s2 = DashedLine(A.ax.c2p(ssd, 4.5), A.ax.c2p(ssd, 0), color=TIME, stroke_width=2)
        s3 = DashedLine(A.ax.c2p(cut, 4.5), A.ax.c2p(cut, 0), color=BOUND, stroke_width=3)
        ar1 = DoubleArrow(A.ax.c2p(0, 3.8), A.ax.c2p(ssd, 3.8), buff=0, color=TIME, stroke_width=2, tip_length=0.12)
        ar2 = DoubleArrow(A.ax.c2p(ssd, 3.8), A.ax.c2p(cut, 3.8), buff=0, color=BOUND, stroke_width=2,
                          tip_length=0.12)
        t1 = label(r"stop-signal delay", font_size=16, color=TIME).next_to(ar1, UP, buff=0.05)
        t2 = label(r"stop time: \ SSRT", font_size=16, color=BOUND).next_to(ar2, UP, buff=0.05)
        lt = label(r"too fast to stop: \ responds", font_size=17, color=LOST).next_to(A.ax.c2p(0.27, 2.4), LEFT,
                                                                                   buff=0.1)
        p = float(np.interp(ssd, d["ssd"], d["p_respond"]))
        assert d["go_hist"].max() < 4.6
        eqs = VGroup(
            MathTex(r"P(\text{respond} \mid \text{SSD}) = P(T_{\text{go}} < \text{SSD} + \text{SSRT})", font_size=26,
                    color=WHITE),
            MathTex(r"\Rightarrow\; \text{SSRT} = F_{\text{go}}^{-1}\!\big(P(\text{respond})\big) - \text{SSD}",
                    font_size=28, color=MODEL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.6, 2.2, 0])
        rows = rows_of([
            (r"Logan \& Cowan, \ 1984: \ on a few trials a stop signal follows the go signal; \ two processes race, "
             r"\ independently", WHITE),
            (r"the response escapes when the go process finishes before the stop process: \ the red area", LOST),
            (r"you never see the stop time, \ but you can solve for it: \ read the go distribution at the share "
             r"that escaped", MODEL),
        ], 5.4, 21, 0.32).move_to([3.7, -1.2, 0])
        tag = psyche_tag(r"\texttt{decide.stop\_race}, \ \texttt{ssrt\_integration}; \ Logan \& Cowan (1984)")
        with self.voiceover(
            "Some decisions are to not act. <bookmark mark='a'/> In the stop-signal task you respond as fast as "
            "you can to a go signal, but on a few trials a second signal follows after a short delay, telling you "
            "to stop. In 1984 Gordon Logan and William Cowan modelled this as a race between two independent "
            "processes. <bookmark mark='b'/> The grey and red bars are the go times: how long the response would "
            "take if nothing opposed it. The stop process starts at the stop signal and takes a time of its own, "
            "the stop-signal reaction time. Any go process that finishes before the stop process does escapes, and "
            "the person responds: the red area. <bookmark mark='c'/> You can never observe a stop time directly, "
            "because a successful stop leaves no response to time. But the race lets you solve for it. The share "
            f"of stop trials with a response, here about {spct(p)}, picks out a point on the go distribution, and "
            "subtracting the delay gives the stop time."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(right), FadeIn(left), FadeIn(go_l), Create(s1))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(s2), GrowFromCenter(ar1), FadeIn(t1))
            vo.wait_until("b")
            self.play(Create(s3), GrowFromCenter(ar2), FadeIn(t2), FadeIn(lt), FadeIn(rows[1]),
                      Indicate(left, color=LOST, scale_factor=1.0))
            vo.wait_until("c")
            self.play(Write(eqs), FadeIn(rows[2]))
        self.clear_scene()

    def inhibition(self):
        d = load("stop")
        head = heading(r"The inhibition function, \ and the stop time recovered")
        A = axes([0, 0.5], [0, 1], x_length=5.6, y_length=3.2, xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5],
                 yticks=[0, 0.5, 1], xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}",
                 xlabel=r"stop-signal delay, \ s", ylabel=r"P(respond on a stop trial)", center=[-3.3, 0.8, 0],
                 font_size=15)
        inh = curve(A.ax, d["ssd"], d["p_respond"], LOST, 3)
        B = axes([0, 0.5], [0.15, 0.3], x_length=5.6, y_length=1.6, xticks=[0, 0.25, 0.5], yticks=[0.15, 0.22, 0.3],
                 xfmt=lambda v: f"{v:.2f}", yfmt=lambda v: f"{v:.2f}", ylabel=r"SSRT estimate, \ s",
                 center=[-3.3, -2.3, 0], font_size=15)
        ok = np.isfinite(d["estimates"])
        est = scatter(B.ax, d["ssd"][ok], d["estimates"][ok], MODEL, 0.07, 1)
        truth = DashedLine(B.ax.c2p(0, d["ssrt"]), B.ax.c2p(0.5, d["ssrt"]), color=BOUND, stroke_width=2)
        tl = label(rf"the true stop time, \ {1000 * d['ssrt']:.0f} ms", font_size=16, color=BOUND).next_to(
            B.ax.c2p(0.5, d["ssrt"]), UP, buff=0.05).align_to(truth, RIGHT)
        e = d["estimates"][ok]
        assert np.all(np.abs(e - d["ssrt"]) < 0.01) and np.all(np.diff(d["p_respond"]) >= -1e-9)
        rows = rows_of([
            (r"later delays leave the stop process less time: \ more responses escape", LOST),
            (rf"the integration method, \ at every delay where 10 to 90\% escape, \ recovers the stop time to "
             rf"within {1000 * np.abs(e - d['ssrt']).max():.0f} ms", MODEL),
            (r"healthy adults: \ typically about 200 to 250 ms; \ used to study impulse control, \ ADHD, \ "
             r"addiction and the effects of drugs", WHITE),
            (r"Verbruggen and colleagues, \ 2019: \ a consensus guide; \ Bissett, \ Jones, \ Poldrack \& Logan, "
             r"\ 2021: \ at short delays independence is badly violated, \ so estimates there are biased", BOUND),
        ], 5.6, 21, 0.32).move_to([3.6, -0.2, 0])
        tag = psyche_tag(r"\texttt{decide.ssrt\_integration}; \ Verbruggen et al. (2019); \ Bissett et al. (2021)")
        with self.voiceover(
            "Vary the delay and you get the whole picture. <bookmark mark='a'/> The later the stop signal comes, "
            "the less time the stop process has, and the more often the response escapes: the inhibition function. "
            "<bookmark mark='b'/> At every delay where between ten and ninety percent escape, the integration "
            f"method recovers the stop time Psyche was given, {1000 * d['ssrt']:.0f} milliseconds, to within a few "
            "milliseconds. <bookmark mark='c'/> In healthy adults stop times are typically around two hundred to "
            "two hundred and fifty milliseconds, and they're used to study impulse control, attention deficit "
            "disorder, addiction and the effects of drugs. <bookmark mark='d'/> Two cautions. In 2019 Frederick "
            "Verbruggen and colleagues from many laboratories published a consensus guide to running and analysing the task, "
            "because small choices change the answer. And in 2021 Patrick Bissett, Gordon Logan and colleagues "
            "showed that the race's central assumption, independence, is badly violated at short delays, so "
            "estimates that lean on them are biased."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(inh), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(B), Create(truth), FadeIn(tl), FadeIn(est), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
