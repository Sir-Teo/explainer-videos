from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai26.common import (AGENT, GAMMA_C, PART, REWARD, TDERR, VALUE, axes, curve, legend, load)

MC, TDC = C.MODEL_Q, C.TRUE_P


class TD(VoiceoverScene):
    def construct(self):
        self.card()
        self.rules()
        self.walk()
        self.errors()
        self.lam()
        self.gammon()
        self.dopamine()

    def card(self):
        card = chapter_card(5, r"Temporal differences", r"Can you learn a guess from a guess?",
                            lit=(1959, 1992), part=PART)
        with self.voiceover("Chapter five. Temporal differences."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def rules(self):
        mc = cmath(r"V(s_t)", r"\leftarrow", r"V(s_t)", r"+", r"\alpha", r"\big[\,", r"G_t", r"-", r"V(s_t)",
                   r"\,\big]", font_size=40)
        td = cmath(r"V(s_t)", r"\leftarrow", r"V(s_t)", r"+", r"\alpha", r"\big[\,", r"r_{t+1} + \gamma V(s_{t+1})",
                   r"-", r"V(s_t)", r"\,\big]", font_size=40)
        for m in (mc, td):
            for i in (0, 2, 8):
                m[i].set_color(VALUE)
        mc[6].set_color(REWARD)
        td[6].set_color(TDERR)
        mc.move_to([-2.0, 1.9, 0])
        td.move_to([-2.0, -0.3, 0])
        ml = label(r"Monte Carlo: \ wait for the actual return", font_size=26, color=MC).next_to(mc, UP, buff=0.3)
        tl = label(r"TD(0): \ use the next state's estimate instead", font_size=26, color=TDC).next_to(td, UP, buff=0.3)
        delta = brace_note(VGroup(*td[5:10]), r"the TD error $\delta_t$", color=TDERR, font_size=26)
        boot = label(r"bootstrapping: \ updating a guess toward a guess", font_size=26, color=GREY_A)
        boot.to_edge(DOWN, buff=0.6)
        hc = history_card(1988, r"Richard Sutton, \textit{Learning to Predict by the Methods of Temporal Differences}",
                          r"after Samuel's checkers player (1959), which tuned its evaluation toward its own later "
                          r"evaluations", width=4.8, color=TDC).move_to([4.5, 1.0, 0])
        with self.voiceover(
            "Without a model, we learn values from experience: play episodes, and watch what happens. The simplest "
            "way is Monte Carlo: <bookmark mark='a'/> after an episode ends, nudge each state's value toward the "
            "return that actually followed it. Alpha is the step size. Average enough returns and you get the "
            "value. But you have to wait until the end, and a single return can be wildly noisy. "
            "<bookmark mark='b'/> Temporal-difference learning doesn't wait. After one step, it nudges the value "
            "toward the reward just received plus gamma times its own current estimate of the next state. "
            "<bookmark mark='c'/> The bracket is the TD error, delta: the difference between what you predicted "
            "a moment ago and what you predict now. <bookmark mark='d'/> Learning a guess from a guess sounds "
            "circular, but it converges, and Richard Sutton made it a theory in 1988. The idea goes back to Arthur "
            "Samuel's checkers program of 1959, which tuned its evaluation of a position toward its own evaluation "
            "a few moves later."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(ml), Write(mc))
            vo.wait_until("b")
            self.play(FadeIn(tl), Write(td))
            vo.wait_until("c")
            self.play(FadeIn(delta))
            vo.wait_until("d")
            self.play(FadeIn(boot), FadeIn(hc, shift=LEFT * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def walk(self):
        d = load("walk")
        snaps = np.asarray(d["snaps"])
        eps = d["snap_eps"]
        names = "ABCDE"
        xs = np.linspace(-4.0, 4.0, 5)
        y0 = 1.9
        nodes = VGroup(*[Circle(radius=0.32, color=VALUE, stroke_width=3).move_to([x, y0, 0]) for x in xs])
        nl = VGroup(*[MathTex(n, font_size=30).move_to(c) for n, c in zip(names, nodes)])
        ends = VGroup(Square(0.5, color=GREY_B).move_to([-5.4, y0, 0]), Square(0.5, color=REWARD).move_to([5.4, y0, 0]))
        el = VGroup(MathTex(r"0", font_size=28, color=GREY_B).move_to(ends[0]),
                    MathTex(r"1", font_size=28, color=REWARD).move_to(ends[1]))
        links = VGroup(*[DoubleArrow(a.get_right(), b.get_left(), buff=0.05, stroke_width=2, color=GREY_C, tip_length=0.12)
                         for a, b in zip([ends[0]] + list(nodes), list(nodes) + [ends[1]])])
        rule = label(r"start at C; \ step left or right at random; \ reward $1$ for leaving on the right",
                     font_size=24, color=GREY_A).next_to(nodes, UP, buff=0.45)
        g = axes([-0.5, 4.5], [0, 1], x_length=7.2, y_length=2.8, ylabel=r"value", yticks=[0, 0.5, 1],
                 center=[-1.0, -1.6, 0])
        ax = g.ax
        xl = VGroup(*[MathTex(n, font_size=26).next_to(ax.c2p(i, 0), DOWN, buff=0.12) for i, n in enumerate(names)])
        truth = VGroup(*[Line(ax.c2p(i - 0.3, (i + 1) / 6), ax.c2p(i + 0.3, (i + 1) / 6), color=REWARD, stroke_width=4)
                         for i in range(5)])
        tlab = label(r"true values: \ $\tfrac16, \tfrac26, \dots, \tfrac56$", font_size=22, color=REWARD)
        tlab.move_to([5.4, -0.9, 0])
        k = ValueTracker(0)

        def est():
            i = int(k.get_value())
            return VGroup(*[Dot(ax.c2p(j, v), radius=0.09, color=TDC) for j, v in enumerate(snaps[i])])

        dots = always_redraw(est)
        def cnt_text():
            e = eps[int(k.get_value())]
            return label(rf"after ${e}$ episode{'' if e == 1 else 's'}" + r" \\ (TD, $\alpha = 0.1$)", font_size=22,
                         color=TDC).move_to([5.4, -1.9, 0])

        cnt = always_redraw(cnt_text)
        with self.voiceover(
            "A small test, from Sutton and Barto: five states in a row. You start in the middle and step left or "
            "right at random. Leaving on the right pays one; on the left, nothing. <bookmark mark='a'/> The true "
            "value of each state is the chance of leaving on the right: one sixth up to five sixths. "
            "<bookmark mark='b'/> Start every estimate at one half and run TD. After one episode, only the state "
            "next to the exit it took has moved. <bookmark mark='c'/> After ten, the news has spread inward. "
            "<bookmark mark='d'/> After a hundred, the estimates sit near the truth."
        ) as vo:
            self.play(FadeIn(ends), FadeIn(el), FadeIn(nodes), FadeIn(nl), LaggedStart(*[Create(l_) for l_ in links]),
                      FadeIn(rule))
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(xl), LaggedStart(*[Create(t_) for t_ in truth], lag_ratio=0.15), FadeIn(tlab))
            vo.wait_until("b")
            self.add(dots, cnt)
            self.play(k.animate.set_value(1), run_time=0.8)
            vo.wait_until("c")
            self.play(k.animate.set_value(2), run_time=0.8)
            vo.wait_until("d")
            self.play(k.animate.set_value(3), run_time=0.8)
        dots.clear_updaters()
        cnt.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def errors(self):
        d = load("walk")
        E = len(d["td_0.1"]) - 1
        g = axes([0, E], [0, 0.25], x_length=7.0, y_length=4.0, xlabel=r"episodes",
                 ylabel=r"error in the values \ (RMS, averaged over $100$ runs)", xticks=[0, 50, 100],
                 yticks=[0, 0.1, 0.2], center=[-1.4, -0.3, 0])
        ax = g.ax
        ep = np.arange(E + 1)
        lines = VGroup()
        items = []
        for a, op in ((0.05, 1.0), (0.1, 0.75), (0.15, 0.5)):
            lines.add(curve(ax, ep, d[f"td_{a}"], TDC, 3).set_stroke(opacity=op))
            items.append((TDC, rf"TD, \ $\alpha = {a}$"))
        for a, op in ((0.01, 1.0), (0.02, 0.8), (0.03, 0.6), (0.04, 0.45)):
            lines.add(curve(ax, ep, d[f"mc_{a}"], MC, 3).set_stroke(opacity=op))
            items.append((MC, rf"Monte Carlo, \ $\alpha = {a}$"))
        lg = legend(items, font_size=18, buff=0.1).next_to(g, RIGHT, buff=0.3).shift(UP * 0.9)
        tag = note(r"computed").to_corner(DR, buff=0.25)
        why_ = wrapped_label(r"TD pools what it learns: \ every visit to D also teaches C, \ through $V(D)$", 4.0,
                             font_size=22, color=GREY_A).next_to(lg, DOWN, buff=0.45).align_to(lg, LEFT)
        with self.voiceover(
            "Now compare the two methods properly: the error of the estimates, averaged over a hundred runs, for "
            "several step sizes. <bookmark mark='a'/> Monte Carlo, in orange, improves slowly. <bookmark mark='b'/> "
            "TD, in blue, learns faster at every step size we tried. <bookmark mark='c'/> The reason is the Markov property again. "
            "Monte Carlo treats each state's returns separately. TD's update for C uses the current estimate of D, "
            "which every past visit to D has improved, so experience is shared between states."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines[3:]], lag_ratio=0.2), FadeIn(VGroup(*lg[3:])), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(l_) for l_ in lines[:3]], lag_ratio=0.2), FadeIn(VGroup(*lg[:3])), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(why_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lam(self):
        d = load("walk")
        lams = list(d["lams"])
        best = np.asarray(d["lam_rms"]).min(1)
        rows = [
            cmath(r"G_t^{(n)}", r"=", r"r_{t+1} + \gamma r_{t+2} + \cdots + \gamma^{n-1} r_{t+n}", r"+",
                  r"\gamma^n V(s_{t+n})", font_size=34),
            cmath(r"G_t^\lambda", r"=", r"(1-\lambda) \sum_{n=1}^{\infty} \lambda^{n-1}", r"G_t^{(n)}", font_size=34),
        ]
        rows[0][4].set_color(VALUE)
        rows[1][0].set_color(TDERR)
        whys = [why(r"$n$ real rewards, \ then a guess"), why(r"$\lambda = 0$: \ TD(0); \ $\lambda = 1$: \ Monte Carlo")]
        step = ladder(self, rows, whys, keep=2, top=3.1, x=-2.6, buff=0.45, edge=6.9)
        trace = cmath(r"z", r"\leftarrow", r"\gamma \lambda z + \mathbf 1[s_t]", r",\qquad", r"V", r"\leftarrow",
                      r"V + \alpha\, \delta_t\, z", font_size=34).move_to([-2.6, 0.5, 0])
        trace[4].set_color(VALUE)
        tl = label(r"eligibility traces: \ the same thing, online", font_size=24, color=GREY_A).next_to(trace, DOWN,
                                                                                                    buff=0.2)
        g = axes([0, 1], [0.2, 0.6], x_length=4.4, y_length=2.6, xlabel=r"$\lambda$",
                 ylabel=r"error after $10$ episodes \ (best $\alpha$)", xticks=[0, 0.5, 1], yticks=[0.2, 0.4, 0.6],
                 center=[3.6, -1.6, 0])
        pts = VGroup(*[Dot(g.ax.c2p(l, b), radius=0.07, color=TDERR) for l, b in zip(lams, best)])
        line = curve(g.ax, lams, best, TDERR, 3)
        bi = int(np.argmin(best))
        tag = note(r"$19$-state walk; \ computed").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Monte Carlo and TD are the two ends of a spectrum. Use n real rewards, then a guess: that's the n-step "
            "return. <bookmark mark='a'/> Blend all of them, with weights falling off like lambda to the n: lambda "
            "zero is one-step TD, lambda one is pure Monte Carlo. <bookmark mark='b'/> You don't need to wait for "
            "the blend either. Keep a fading trace of recently visited states, and spread each TD error back over "
            "them: that's an eligibility trace, an answer to credit assignment in one line. <bookmark mark='c'/> On a "
            "longer walk, the error after ten episodes, at each lambda's best step size, is lowest in between: "
            f"here at lambda {lams[bi]}. The best methods mix real rewards with their own guesses."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(Write(trace), FadeIn(tl))
            vo.wait_until("c")
            self.play(FadeIn(g), FadeIn(tag))
            self.play(Create(line), LaggedStart(*[FadeIn(p, scale=1.4) for p in pts], lag_ratio=0.1))
            self.play(Indicate(pts[bi], color=TDERR, scale_factor=1.8))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gammon(self):
        hc = history_card(1992, r"Gerald Tesauro, \ IBM: \ TD-Gammon",
                          r"a neural network value function, trained by TD($\lambda$) on games against itself. "
                          r"Version 2.1, after $1.5$ million games, played close to the world's best; \ its taste in "
                          r"opening moves changed how experts play.", width=7.6, color=TDC).move_to(UP * 1.2)
        net = VGroup()
        layers = [6, 8, 1]
        xs = [-2.0, 0, 2.0]
        cols = [GREY_B, AGENT, VALUE]
        for x, n, col in zip(xs, layers, cols):
            net.add(VGroup(*[Dot([x, (j - (n - 1) / 2) * 0.32, 0], radius=0.07, color=col) for j in range(n)]))
        edges = VGroup(*[Line(a.get_center(), b.get_center(), stroke_width=0.6, color=GREY_D)
                         for L in range(2) for a in net[L] for b in net[L + 1]])
        lbl = VGroup(label(r"board", font_size=20, color=GREY_B).next_to(net[0], DOWN, buff=0.15),
                     label(r"$V(s)$: \ chance of winning", font_size=20, color=VALUE).next_to(net[2], RIGHT, buff=0.15))
        pic = VGroup(edges, net, lbl).move_to(DOWN * 1.9)
        cite_ = cite(r"G.~Tesauro, \textit{Temporal Difference Learning and TD-Gammon}, CACM (1995)")
        with self.voiceover(
            "The first great success of these ideas came in 1992, from Gerald Tesauro at IBM. TD-Gammon was a neural "
            "network that looked at a backgammon board and estimated the chance of winning. <bookmark mark='a'/> It "
            "learned only from games against itself, nudging each position's value toward the next position's by "
            "TD lambda. After a million and a half games, it played close to the level of the world's best players, "
            "and some of its unusual opening moves were adopted by human experts. Self-play, a learned value, "
            "temporal differences: keep those three in mind."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(net), Create(edges), FadeIn(lbl), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dopamine(self):
        heads = [r"reward comes \\ unexpectedly", r"after learning: \\ the cue predicts it", r"predicted reward \\ is withheld"]
        panels = VGroup()
        rng = np.random.default_rng(3)
        for p, h in enumerate(heads):
            box = VGroup()
            base = Line([-1.6, 0, 0], [1.6, 0, 0], color=GREY_C, stroke_width=1.5)
            cue_x, rew_x = -0.8, 0.8
            spikes = VGroup()
            for trial in range(6):
                y = -0.25 - trial * 0.18
                xs = rng.uniform(-1.5, 1.5, 6)
                burst = {0: rew_x, 1: cue_x}.get(p)
                if burst is not None:
                    xs = np.concatenate([xs, burst + rng.normal(0, 0.05, 5)])
                if p == 2:
                    xs = xs[np.abs(xs - rew_x) > 0.25]
                for x in xs:
                    spikes.add(Line([x, y - 0.07, 0], [x, y + 0.07, 0], color=TDERR, stroke_width=1.5))
            marks = VGroup()
            if p > 0:
                marks.add(label(r"cue", font_size=18, color=GREY_A).move_to([cue_x, 0.25, 0]))
            marks.add(label(r"reward" if p < 2 else r"(no reward)", font_size=18,
                            color=REWARD if p < 2 else C.PENALTY).move_to([rew_x, 0.25, 0]))
            title = label(h, font_size=22, color=GREY_A).move_to([0, 1.0, 0])
            box.add(base, spikes, marks, title)
            panels.add(box)
        panels.arrange(RIGHT, buff=0.6).move_to(UP * 0.3)
        eq = label(r"dopamine firing $\approx$ the TD error $\delta = r + \gamma V(s') - V(s)$", font_size=28,
                   color=TDERR).to_edge(DOWN, buff=1.0)
        cite_ = cite(r"W.~Schultz, P.~Dayan \& P.~R.~Montague, \textit{A Neural Substrate of Prediction and Reward}, "
                     r"Science (1997)")
        tag = note(r"schematic").to_corner(UR, buff=0.25)
        with self.voiceover(
            "And there's a postscript from neuroscience. In monkeys, dopamine neurons fire a burst when a reward "
            "arrives unexpectedly. <bookmark mark='a'/> Once a cue reliably predicts the reward, the burst moves to "
            "the cue, and the reward itself gets no response. <bookmark mark='b'/> And if the predicted reward "
            "doesn't come, firing dips below normal, exactly when it was due. <bookmark mark='c'/> In 1997 Schultz, "
            "Dayan and Montague pointed out that this is the TD error: surprise about future reward, positive or "
            "negative, moving back to the earliest thing that predicts it."
        ) as vo:
            self.play(FadeIn(panels[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(panels[1]))
            vo.wait_until("b")
            self.play(FadeIn(panels[2]))
            vo.wait_until("c")
            self.play(FadeIn(eq), FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()
