from __future__ import annotations

from videos.psychology.psych25.common import *  # noqa: F403


class Brain(VoiceoverScene):
    def construct(self):
        self.card()
        self.task()
        self.averages()
        self.steps()

    def card(self):
        card = chapter_card(8, r"Accumulators in the brain", r"Can you watch a decision form?",
                            lit={1996: r"Shadlen \& Newsome", 2002: r"Roitman \& Shadlen", 2015: r"Latimer et al.",
                                 2024: r"Steinemann et al."},
                            part=PART, scale=("neuron", "circuit"), marr=("how",))
        with self.voiceover("Chapter eight. Accumulators in the brain."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def task(self):
        head = heading(r"A monkey, \ moving dots, \ one neuron")
        screen = Rectangle(width=6.6, height=4.2, stroke_color=GREY_B, fill_color="#12161D", fill_opacity=1
                           ).move_to([-3.2, 0.0, 0])
        fixp = Dot([-3.2, 0.2, 0], radius=0.07, color=YOU)
        ap = Circle(radius=0.9, color=GREY_D, stroke_width=2).move_to([-3.2, 0.2, 0])
        rng = np.random.default_rng(6)
        rr = 0.85 * np.sqrt(rng.random(40))
        th = 2 * np.pi * rng.random(40)
        dots = VGroup(*[Dot([-3.2 + r * np.cos(t), 0.2 + r * np.sin(t), 0], radius=0.035, color=WHITE)
                        for r, t in zip(rr, th)])
        tin = Dot([-0.6, 0.2, 0], radius=0.14, color=MODEL)
        tout = Dot([-5.8, 0.2, 0], radius=0.14, color=GREY_B)
        rf = DashedVMobject(Circle(radius=0.55, color=MODEL).move_to(tin), num_dashes=20)
        rfl = label(r"the neuron's response field", font_size=17, color=MODEL).next_to(rf, DOWN, buff=0.1)
        sac = Arrow([-3.0, 0.2, 0], [-0.8, 0.2, 0], buff=0.1, color=YOU, stroke_width=3)
        sacl = label(r"the answer: \ an eye movement", font_size=18, color=YOU).move_to([-1.9, 1.55, 0])
        rows = rows_of([
            (r"Newsome and colleagues, \ late 1980s: \ monkeys judge the direction of dots like yours, \ "
             r"answering with their eyes", WHITE),
            (r"Shadlen \& Newsome, \ 1996 and 2001: \ neurons in the lateral intraparietal area \ (LIP) \ fire "
             r"more and more as evidence for \emph{their} target builds", MODEL),
            (r"Roitman \& Shadlen, \ 2002: \ the rise is steeper for stronger motion, \ and the monkey answers "
             r"when the firing reaches about the same level", BOUND),
        ], 5.4, 22, 0.36).move_to([3.7, 0.0, 0])
        tag = published_tag(r"Shadlen \& Newsome (1996, \ 2001); \ Roitman \& Shadlen (2002)")
        with self.voiceover(
            "Can you watch a decision form? <bookmark mark='a'/> From the late 1980s William Newsome and his "
            "colleagues trained monkeys on the task you did at the start: a cloud of dots, some drifting one way, "
            "and the answer given with the eyes, by looking at one of two targets. <bookmark mark='b'/> Michael "
            "Shadlen and Newsome recorded neurons in a region of parietal cortex called LIP, each of which "
            "responds when the eyes are about to move to one place. During the dots, such a neuron fires more and "
            "more when the evidence favours its target. <bookmark mark='c'/> In 2002 Jamie Roitman and Shadlen "
            "showed that the rise is steeper when the motion is stronger, and that the monkey answers when the "
            "firing reaches about the same level, whatever the motion was. A drift, and a bound, in a neuron."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(screen), FadeIn(fixp))
            vo.wait_until("a")
            self.play(FadeIn(ap), FadeIn(dots), FadeIn(tin), FadeIn(tout), FadeIn(rows[0]))
            self.play(dots.animate.shift(RIGHT * 0.15), run_time=1.5, rate_func=linear)
            vo.wait_until("b")
            self.play(Create(rf), FadeIn(rfl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(GrowArrow(sac), FadeIn(sacl), FadeIn(rows[2]))
        self.clear_scene()

    def averages(self):
        d = load("brain")
        head = heading(r"What the averages look like")
        cols = [GREY_B, DRIFT, EVIDENCE, MODEL]
        A = axes([0, 0.8], [1.0, 2.05], x_length=4.4, y_length=3.4, xticks=[0, 0.4, 0.8], yticks=[1.0, 1.5, 2.0],
                 xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}", xlabel=r"time from motion onset, \ s",
                 ylabel=r"accumulated evidence", center=[-4.3, -0.1, 0], font_size=15)
        B = axes([-0.4, 0], [1.0, 2.05], x_length=2.6, y_length=3.4, xticks=[-0.4, -0.2, 0], yticks=[],
                 xfmt=lambda v: f"{v:.1f}", xlabel=r"time to the answer, \ s", center=[-0.6, -0.1, 0], font_size=15)
        sc = VGroup(*[curve(A.ax, d["t_stim"][np.isfinite(s)], s[np.isfinite(s)], c, 3)
                      for s, c in zip(d["stim"], cols)])
        rc = VGroup(*[curve(B.ax, d["t_resp"], r, c, 3) for r, c in zip(d["resp"], cols)])
        bound = DashedLine(B.ax.c2p(-0.4, 2.0), B.ax.c2p(0, 2.0), color=BOUND, stroke_width=2)
        bl = label(r"the bound", font_size=16, color=BOUND).next_to(bound, UP, buff=0.05)
        key = legend([(c, rf"drift {v:.1f}") for v, c in zip(d["vs"], cols)], font_size=18).move_to(
            A.ax.c2p(0.22, 1.82))
        assert np.all(np.diff(d["stim"][:, 30]) > 0) and np.ptp(d["resp"][:, -1]) < 1e-9
        rows = rows_of([
            (r"Psyche's accumulators, \ averaged the way Roitman and Shadlen averaged their neurons: \ only trials "
             r"that chose this side, \ cut at the answer", WHITE),
            (r"from the motion's onset: \ rises graded by the drift", DRIFT),
            (r"lined up on the answer: \ every strength converges on the same level, \ the bound", BOUND),
            (r"the neurons look like this; \ these curves are the model's", MODEL),
        ], 4.4, 21, 0.34).move_to([4.6, 0.0, 0])
        tag = psyche_tag(r"\texttt{decide.aligned\_means}; \ 1{,}500 trials per drift")
        with self.voiceover(
            "Here is what that looks like, using Psyche's accumulators in place of neurons. <bookmark mark='a'/> "
            "Psyche averages its trials the way Roitman and Shadlen averaged their neurons: only trials that chose "
            "this neuron's side, and only up to the moment of the answer. <bookmark mark='b'/> Lined up on the start "
            "of the motion, the averages rise faster the stronger the drift. <bookmark mark='c'/> Lined up on the "
            "answer instead, they all converge on the same level just before it. <bookmark mark='d'/> The neurons' "
            "averages look remarkably like this. But an average can hide what single trials do."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(B))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(sc), FadeIn(key), FadeIn(rows[1]), run_time=2)
            vo.wait_until("c")
            self.play(Create(rc), Create(bound), FadeIn(bl), FadeIn(rows[2]), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def steps(self):
        d = load("brain")
        head = heading(r"Ramp, \ or step?")
        A = axes([0, 0.8], [0, 1.0], x_length=5.6, y_length=3.4, xticks=[0, 0.4, 0.8], yticks=[0.2, 0.9],
                 xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}", xlabel=r"time, \ s", ylabel=r"firing, \ scaled",
                 center=[-3.3, -0.1, 0], font_size=16)
        singles = VGroup(*[curve(A.ax, d["step_t"], tr + 0.012 * (k - 3), GREY_B, 1.6)
                           for k, tr in enumerate(d["step_trials"])])
        mean = curve(A.ax, d["step_t"], d["step_mean"], MODEL, 4)
        key = legend([(GREY_B, r"single trials: \ one jump each"), (MODEL, r"their average")], font_size=17
                     ).move_to(A.ax.c2p(0.55, 0.12))
        assert np.all(np.diff(d["step_mean"]) >= -1e-12)
        rows = rows_of([
            (r"Latimer, \ Yates, \ Meister, \ Huk \& Pillow, \ 2015: \ fitted to single trials, \ about three "
             r"quarters of LIP neurons looked more like a step than a ramp", WHITE),
            (r"steps at random times average to a ramp: \ the average alone cannot tell them apart", MODEL),
            (r"Shadlen and colleagues, \ 2016: \ the data do not show one-time steps; \ the dispute went on", LOST),
            (r"Steinemann, \ Shadlen and colleagues, \ 2024: \ up to 203 LIP neurons at once; \ their weighted sum "
             r"drifts and diffuses within single decisions", EVIDENCE),
        ], 5.6, 21, 0.32).move_to([3.6, 0.0, 0])
        tag = published_tag(r"Latimer et al. (2015); \ Shadlen et al. (2016); \ Steinemann et al. (2024)")
        with self.voiceover(
            "Is each single neuron really ramping? <bookmark mark='a'/> In 2015 Kenneth Latimer, Jonathan Pillow, "
            "Alexander Huk and colleagues fitted models to single trials, and found that about three quarters of "
            "the LIP neurons were better described as jumping, once, from low to high firing at a random moment, "
            "than as ramping. <bookmark mark='b'/> Psyche shows why the averages couldn't tell: steps at random "
            "times average to a smooth ramp. <bookmark mark='c'/> Shadlen and colleagues replied that the data "
            "didn't show one-time steps, and the dispute went on for years. <bookmark mark='d'/> In 2024 Natalie "
            "Steinemann, Shadlen and colleagues recorded up to two hundred and three LIP neurons at once. A "
            "weighted sum of their activity, read out on single trials, drifted and diffused toward a bound, much "
            "as the model says. Single neurons may step; the population seems to accumulate. The Ledger keeps the "
            "single-neuron question open."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(s) for s in singles], lag_ratio=0.3), FadeIn(rows[0]), run_time=3)
            vo.wait_until("b")
            self.play(Create(mean), FadeIn(key), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
