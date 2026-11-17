from __future__ import annotations

import numpy as np

from videos.psychology.psych17.common import *  # noqa: F403


class Dopamine(VoiceoverScene):
    def construct(self):
        self.card()
        self.migration()
        self.three()
        self.causal()

    def card(self):
        card = chapter_card(3, r"The error moves to the cue", r"Do dopamine neurons compute $\delta$?",
                            lit={1997: r"Schultz, \ Dayan \& Montague", 2013: r"Steinberg et al."}, part=PART,
                            scale=("neuron", "circuit", "mind"), marr=("what", "how", "tissue"))
        with self.voiceover("Chapter three. The error moves to the cue."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def migration(self):
        d = load("migration")
        D = d["delta"]
        head = heading(r"The TD error, \ trial by trial")
        n_tr, n_t = D.shape
        cell_w, cell_h = 7.2 / n_t, 4.2 / 60
        grid = VGroup()
        for i, tr in enumerate(range(0, n_tr, 2)):
            for j in range(n_t):
                v = float(D[tr, j])
                if abs(v) < 0.02:
                    continue
                col = interpolate_color(ManimColor("#0B1A12"), ManimColor(DELTA), min(1.0, v)) if v > 0 else \
                    interpolate_color(ManimColor("#1A0B0B"), ManimColor(INHIB), min(1.0, -v))
                grid.add(Rectangle(width=cell_w, height=cell_h, stroke_width=0, fill_color=col, fill_opacity=1)
                         .move_to([-5.6 + (j + 0.5) * cell_w, 2.3 - (i + 0.5) * cell_h, 0]))
        frame = Rectangle(width=7.2, height=4.2, stroke_color=GREY_C, stroke_width=2).move_to([-2.0, 0.2, 0])
        xc = -5.6 + (5 + 0.5) * cell_w
        xr = -5.6 + (20 + 0.5) * cell_w
        lc = label(r"cue", font_size=22, color=CUE).move_to([xc, 2.6, 0])
        lr = label(r"juice", font_size=22, color=REWARD).move_to([xr, 2.6, 0])
        ly = label(r"trial 1", font_size=18, color=GREY_A).next_to(frame.get_corner(UL), LEFT, buff=0.1).shift(DOWN * 0.1)
        ly2 = label(r"trial 120", font_size=18, color=GREY_A).next_to(frame.get_corner(DL), LEFT, buff=0.1).shift(UP * 0.1)
        lx = label(r"time within the trial", font_size=20, color=GREY_A).next_to(frame, DOWN, buff=0.15)
        rows = rows_of([
            (r"trial 1: \ all of the error is at the juice", REWARD),
            (r"value creeps backward, \ one step per trial, \ and the error with it", DELTA),
            (r"trained: \ the error is at the cue, \ whose arrival nobody predicts", CUE),
            (r"the juice, \ now predicted, \ brings no error at all", WHITE),
        ], 4.4, 24, 0.34).move_to([4.4, 0.4, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ \texttt{rl.td\_conditioning}, \ $\alpha = 0.2$, \ $\gamma = 0.98$; \ every "
                         r"second trial shown")
        with self.voiceover(
            "Here is that clock running on Pavlov's task, for a hundred and twenty trials. Each row is a trial; "
            "time runs left to right; green is a positive error. <bookmark mark='a'/> On the first trial nothing is "
            "predicted, so all the error is at the juice. <bookmark mark='b'/> The juice raises the value of the "
            "moment just before it. On the next trial, reaching that moment is itself a pleasant surprise, so the "
            "error appears a step earlier, and the value of the step before that grows in turn. "
            "<bookmark mark='c'/> Trial by trial the error slides back until it reaches the cue. The cue itself "
            "can't be predicted, because nothing announces it, so the error stops there. <bookmark mark='d'/> And the "
            "juice, now fully predicted, produces no error at all. In a real brain, with a fuzzier clock, the error "
            "doesn't visibly slide; it fades at the reward and grows at the cue. Either way, the endpoint is "
            "Schultz's second recording."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(lc), FadeIn(lr), FadeIn(ly), FadeIn(ly2), FadeIn(lx),
                      FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(g) for g in grid], lag_ratio=0.01), FadeIn(rows[1]), run_time=4.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def three(self):
        d = load("cases")
        t = d["t"]
        head = heading(r"Every feature of the recordings, \ from one line")
        rows = rows_of([
            (r"unpredicted juice: \ $\delta = r - 0 > 0$, \ a burst", DELTA),
            (r"a predicted cue... \ but the cue itself is unpredicted: \ $\delta = \gamma V(\text{cue}) > 0$", CUE),
            (r"predicted juice: \ $\delta = r + 0 - V \approx 0$, \ nothing", WHITE),
            (r"omitted juice: \ $\delta = 0 - V < 0$, \ a dip, \ timed by the clock", INHIB),
            (r"and later tests: \ bursts scale with the probability and size of a reward the cue promises", GREY_A),
        ], 6.4, 25, 0.42).to_edge(LEFT, buff=0.6).shift(DOWN * 0.1)
        panels = VGroup()
        for k, (key, name, col) in enumerate([("first", r"trial 1", DELTA), ("trained", r"trained", CUE),
                                               ("omitted", r"trained, \ juice omitted", INHIB)]):
            A = axes([-0.5, 2.5], [-1.0, 1.0], x_length=4.4, y_length=1.15, xticks=[0, 1.5], yticks=[-1, 0, 1],
                     center=[3.7, 1.85 - 1.75 * k, 0], font_size=16,
                     xfmt=lambda v: {0: r"\text{cue}", 1.5: r"\text{juice}"}[v])
            ax = A.ax
            zero = DashedLine(ax.c2p(-0.5, 0), ax.c2p(2.5, 0), color=GREY_D, stroke_width=1.2)
            tr = VMobject(color=col, stroke_width=3).set_points_as_corners(
                [ax.c2p(x, y) for x, y in zip(np.repeat(t, 2)[1:], np.repeat(d[key], 2)[:-1])])
            nm = label(name, font_size=20, color=col).next_to(ax, UP, buff=0.06).align_to(ax, LEFT)
            panels.add(VGroup(A, zero, tr, nm))
        cap = label(r"$\delta_t$ \ within one trial, \ from Psyche's TD learner", font_size=19, color=GREY_A)
        cap.next_to(panels, DOWN, buff=0.2)
        tag = published_tag(archive.SCHULTZ_1997.cite)
        with self.voiceover(
            "So each of the three recordings is one case of the equation. <bookmark mark='a'/> Juice with no "
            "warning: reward minus a prediction of zero, a positive error, a burst. <bookmark mark='b'/> A cue that "
            "predicts juice: the cue itself arrives unannounced, so reaching it is a jump in value, a positive error. "
            "<bookmark mark='c'/> The juice after the cue: reward, minus the value that predicted it, about zero. "
            "<bookmark mark='d'/> And the omitted juice: zero minus the prediction, a negative error, the dip, at the "
            "time the clock said the juice was due. <bookmark mark='e'/> Later experiments pushed the match further. "
            "A cue that promises juice half the time produces a burst about half as large, and a larger reward a "
            "larger one: the neurons report expected value, as the theory says they should."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cap), *[FadeIn(p[0]) for p in panels])
            vo.wait_until("a")
            self.play(FadeIn(rows[0], shift=RIGHT * 0.15), FadeIn(panels[0][1:]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1], shift=RIGHT * 0.15), FadeIn(panels[1][1:]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2], shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=RIGHT * 0.15), FadeIn(panels[2][1:]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4], shift=RIGHT * 0.15))
        self.clear_scene()

    def causal(self):
        d = load("steinberg")
        head = heading(r"Not only correlated: \ causal")
        rows = rows_of([
            (r"2013: \ Steinberg and colleagues give rats Kamin's blocking design", WHITE),
            (r"the added cue is blocked: \ the reward is predicted, \ so there is no error", CUE),
            (r"now switch on the rats' dopamine neurons with light, \ at the moment of the reward", DELTA),
            (r"the blocked cue is learned: \ an artificial prediction error teaches, \ as a real one would", YOU),
            (r"stimulation at other times does not; \ the timing is the error's", GREY_A),
        ], 6.4, 25, 0.42).to_edge(LEFT, buff=0.6).shift(DOWN * 0.1)
        A = axes([0, 4], [0, 0.6], x_length=5.2, y_length=3.4, yticks=[0, 0.25, 0.5], ylabel=r"$V_X$, \ what the added cue learned",
                 center=[3.6, 0.4, 0], font_size=18)
        ax = A.ax
        cols = [GREY_B, CUE, DELTA, GREY_B]
        names = [r"no blocking", r"blocking", r"light at the reward", r"light at another time"]
        bars, labs = VGroup(), VGroup()
        for k, (v, c, n) in enumerate(zip(d["vx"], cols, names)):
            lo, hi = ax.c2p(k + 0.5, 0), ax.c2p(k + 0.5, max(v, 0.004))
            b = Rectangle(width=0.8, height=max(hi[1] - lo[1], 0.02), stroke_width=0, fill_color=c, fill_opacity=0.85)
            b.move_to([lo[0], (lo[1] + hi[1]) / 2, 0])
            bars.add(b)
            labs.add(wrapped_label(n, 1.2, 17, c).next_to(ax.c2p(k + 0.5, 0), DOWN, buff=0.15))
        ptag = psyche_tag(r"Rescorla-Wagner on Steinberg et al.'s design, \ light adds 0.5 to the error; \ not their data")
        tag = published_tag(archive.STEINBERG_2013.cite)
        with self.voiceover(
            "A correlation between a neuron and an equation is suggestive. A causal test is better. "
            "<bookmark mark='a'/> In 2013 Elizabeth Steinberg, Patricia Janak and colleagues gave rats Part 16's "
            "blocking design. <bookmark mark='b'/> The added cue should teach nothing, because the reward is already "
            "predicted and there's no error. <bookmark mark='c'/> Then they used light, through optogenetics, to "
            "switch on the rats' dopamine neurons for a moment, just when the predicted reward arrived. "
            "<bookmark mark='d'/> The blocked cue was learned. An artificial prediction error taught the rats exactly "
            "what a real one would have. <bookmark mark='e'/> The same stimulation at other times didn't. Dopamine at "
            "the moment of reward acts as the teaching signal. Part 16's rule, with the light added to the error, "
            "draws the same four bars."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(ptag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0], shift=RIGHT * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(rows[1], shift=RIGHT * 0.15), FadeIn(bars[:2]), FadeIn(labs[:2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2], shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=RIGHT * 0.15), GrowFromEdge(bars[2], DOWN), FadeIn(labs[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4], shift=RIGHT * 0.15), FadeIn(bars[3]), FadeIn(labs[3]))
        self.clear_scene()
