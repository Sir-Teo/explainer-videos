from __future__ import annotations

from videos.psychology.psych48.common import *  # noqa: F403


class Recovery(VoiceoverScene):
    def construct(self):
        self.card()
        self.scatter_()
        self.trials()

    def card(self):
        card = chapter_card(4, r"Parameter recovery", r"If you knew the answer, \ would the fit find it?",
                            lit={2019: r"Wilson \& Collins"}, part=PART, scale=("person",), marr=("how",))
        with self.voiceover("Chapter four. Parameter recovery."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def scatter_(self):
        d = load("recovery")
        head = heading(r"Simulate, \ fit, \ compare")
        A = axes([0, 1], [0, 1], x_length=3.2, y_length=3.2, xticks=[0, 0.5, 1], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"true $\alpha$", ylabel=r"fitted $\alpha$",
                 center=[-4.6, 0.2, 0], font_size=12)
        B = axes([0, 14], [0, 20], x_length=3.2, y_length=3.2, xticks=[0, 5, 10], yticks=[0, 10, 20],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"true $\beta$", ylabel=r"fitted $\beta$",
                 center=[-0.8, 0.2, 0], font_size=12)
        jit = np.random.default_rng(48).normal(0, 0.01, len(d["true_alpha"]))
        pa = scatter(A.ax, d["true_alpha"] + jit, d["est_alpha"], MODEL, radius=0.04)
        pb = scatter(B.ax, d["true_beta"] + 10 * jit, np.minimum(d["est_beta"], 20), PERSON, radius=0.04)
        da = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(1, 1), color=GREY_B, stroke_width=1.5)
        db = DashedLine(B.ax.c2p(0, 0), B.ax.c2p(14, 14), color=GREY_B, stroke_width=1.5)
        rows = rows_of([
            (r"choose true parameters across a grid; \ simulate 200 choices from each; \ fit; \ plot fitted against "
             r"true", WHITE),
            (rf"the learning rate is recovered well (correlation {d['r_alpha']:.2f}); \ the inverse temperature less "
             rf"so ({d['r_beta']:.2f}), \ worst when it is high", MODEL),
            (r"if a parameter cannot be recovered from simulated data, \ its value in real data means nothing", AUTH),
            (r"every modelling paper should show this plot, \ for its own task and its own number of trials", YOU),
        ], 4.6, 18, 0.36).move_to([4.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{fit.recovery}, \ 75 simulated learners")
        with self.voiceover(
            "The first check on any model. <bookmark mark='a'/> Choose true parameters across a grid. Simulate two "
            "hundred choices from each, fit, and plot what the fit found against the truth. <bookmark mark='b'/> The "
            "learning rate is recovered well. The inverse temperature less so, and worst when it's high, because a "
            "nearly deterministic chooser gives little information about how deterministic it is. "
            "<bookmark mark='c'/> If a parameter can't be recovered from simulated data, its value in real data means "
            "nothing. <bookmark mark='d'/> Every modelling paper should show this plot, for its own task and its own "
            "number of trials."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(B), FadeIn(da), FadeIn(db))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(pa), FadeIn(pb))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def trials(self):
        d = load("trials")
        head = heading(r"How many trials?")
        A = axes([0, 420], [0.4, 1.0], x_length=5.6, y_length=3.0, xticks=[50, 100, 200, 400], yticks=[0.5, 0.75, 1.0],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"trials per learner",
                 ylabel=r"recovery: \ $r$(true, \ fitted)", center=[-3.3, 0.3, 0], font_size=12)
        ca = curve(A.ax, d["trials"], d["r_alpha"], MODEL, stroke_width=4)
        cb = curve(A.ax, d["trials"], d["r_beta"], PERSON, stroke_width=4)
        key = VGroup(label(r"learning rate", font_size=13, color=MODEL),
                     label(r"inverse temperature", font_size=13, color=PERSON)).arrange(RIGHT, buff=0.4)
        key.next_to(A, UP, buff=0.25)
        rows = rows_of([
            (r"the same recovery study at 50, \ 100, \ 200 and 400 trials per learner (72 learners each)", WHITE),
            (rf"at 50 trials the fitted learning rate correlates only {d['r_alpha'][0]:.2f} with the truth, \ the "
             rf"inverse temperature {d['r_beta'][0]:.2f}", AUTH),
            (rf"at 400, \ {d['r_alpha'][-1]:.2f} and {d['r_beta'][-1]:.2f}", GOOD),
            (r"so the number of trials is a design decision, \ made by recovery before the data, \ like power", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{fit.recovery}")
        with self.voiceover(
            "So how many trials does a fit need? <bookmark mark='a'/> Run the same recovery study at fifty, a "
            "hundred, two hundred and four hundred trials per learner. <bookmark mark='b'/> At fifty trials, the "
            "fitted learning rate correlates only about zero point six with the truth, and the inverse temperature "
            "less. <bookmark mark='c'/> At four hundred, both are above zero point nine. <bookmark mark='d'/> The "
            "number of trials is a design decision, made by recovery before the data are collected, just like power."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(ca), Create(cb))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
