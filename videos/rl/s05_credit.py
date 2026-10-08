from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.rl.common import label, load, mtex, note, real_tag, source, tokens, why
from videos.rl.compute import prompt_text


class Credit(VoiceoverScene):
    def construct(self):
        self.d = load("critic")
        self.prompt = prompt_text(self.d["a"], self.d["b"])
        self.shows = {(s["mode"], s["r"]): s for s in self.d["shows"]}
        self.problem()
        self.values()
        self.real_critic()
        self.gae()

    # ------------------------------------------------------------------
    def problem(self):
        s = self.shows[("direct", 0.0)]
        strip = tokens(self.prompt, s["text"], font_size=30).move_to(UP * 0.6)
        ans = strip[len(self.prompt):]
        right = f"{self.d['a'] + self.d['b']:05d}"
        bad = [i for i, (x, y) in enumerate(zip(s["text"], right)) if x != y]
        downs = VGroup(*[Arrow(c.get_bottom() + DOWN * 0.05, c.get_bottom() + DOWN * 0.8, buff=0, stroke_width=4,
                               color=C.PENALTY, max_tip_length_to_length_ratio=0.35) for c in ans])
        r0 = label(r"reward $0$: every token pushed down by the same amount", font_size=28, color=C.PENALTY)
        r0.next_to(downs, DOWN, buff=0.25)
        corr = label(rf"the right answer is \texttt{{{right}}}", font_size=26, color=GREY_A).next_to(strip, UP, buff=1.3)
        boxes = VGroup(*[SurroundingRectangle(ans[i], color=YELLOW, buff=0.04, stroke_width=3) for i in bad])
        q = label(r"only this digit was wrong", font_size=26, color=YELLOW).next_to(boxes, UP, buff=0.55)
        with self.voiceover(
            "Here is a real answer from the model we'll train later, to the problem "
            f"{self.d['a']} plus {self.d['b']}. It's wrong, so the reward is zero, and the policy gradient pushes "
            "every one of its tokens down equally. <bookmark mark='b'/> But most of those digits were fine. Only "
            "one was a mistake: a forgotten carry. A single reward at the end can't say which token earned it."
        ) as vo:
            self.play(FadeIn(strip, lag_ratio=0.05))
            self.play(LaggedStart(*[GrowArrow(a) for a in downs], lag_ratio=0.05), FadeIn(r0))
            vo.wait_until("b")
            self.play(FadeIn(corr), Create(boxes), FadeIn(q))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def values(self):
        V = mtex(r"V(s_t)", r"=", r"\mathbb{E}\big[\,R \;\big|\; s_t = (x, y_1, \dots, y_t)\,\big]", font_size=40)
        V[0].set_color(C.BASELINE)
        Vl = label(r"the chance of ending up right, from here", font_size=26, color=C.BASELINE)
        B = mtex(r"V(s_t)", r"=", r"\mathbb{E}_{y_{t+1} \sim \pi}\big[\, V(s_{t+1}) \,\big]", font_size=40)
        B[0].set_color(C.BASELINE)
        B[2].set_color(C.BASELINE)
        Bl = label(r"Bellman: the next token is the only thing that happens", font_size=26, color=GREY_A)
        A = mtex(r"A(s_t, y_{t+1})", r"=", r"V(s_{t+1})", r"-", r"V(s_t)", font_size=40)
        A[0].set_color(C.ADVANTAGE)
        A[2].set_color(C.BASELINE)
        A[4].set_color(C.BASELINE)
        Al = label(r"a token's advantage: how much it changed the odds", font_size=26, color=C.ADVANTAGE)
        D = mtex(r"\delta_t", r"=", r"r_t", r"+", r"V(s_{t+1})", r"-", r"V(s_t)", font_size=40)
        D[0].set_color(C.ADVANTAGE)
        D[2].set_color(C.REWARD)
        Dl = label(r"with a learned $V$: the TD error ($r_t = R$ at the last token, else $0$)", font_size=26, color=GREY_A)
        rows = VGroup(*[VGroup(m, l).arrange(DOWN, buff=0.12) for m, l in ((V, Vl), (B, Bl), (A, Al), (D, Dl))])
        rows.arrange(DOWN, buff=0.38).move_to(DOWN * 0.1)
        with self.voiceover(
            "The fix is to measure progress along the way. Define the value of a partial answer: the expected "
            "final reward, given the prompt and the tokens written so far. With a zero-one reward, it's simply the "
            "chance of ending up right from here. <bookmark mark='b'/> For a language model, nothing random "
            "happens between tokens except the next token itself, so the value now is the average value after one "
            "more token. That's the Bellman equation. <bookmark mark='a'/> And it hands us exactly what we wanted: "
            "a token's advantage is how much it changed the odds. The value after it, minus the value before. "
            "<bookmark mark='d'/> With an estimated value function, this difference is called the temporal "
            "difference error, delta."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("a")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def value_view(self, s, y_strip=-1.6, scale=2.6, font_size=26):
        """Token strip with the critic's V(s_t) drawn above it at the token boundaries, and delta bars below."""
        strip = tokens(self.prompt, s["text"], font_size=font_size, cell=0.5, height=0.6).move_to([0, y_strip, 0])
        n0 = len(self.prompt)
        ans = strip[n0:]
        V = np.array(s["V"], float)
        T = len(V)
        base_y = y_strip + 0.75
        # V(s_t) sits at the left edge of answer token t (state before token t is written); V(s_T) := R
        xs = [c.get_left()[0] for c in ans] + [ans[-1].get_right()[0]]
        vals = list(V) + [s["r"]]
        pts = [np.array([x, base_y + scale * v, 0]) for x, v in zip(xs, vals)]
        axis = DashedLine([xs[0] - 0.3, base_y, 0], [xs[-1] + 0.3, base_y, 0], color=GREY_D, stroke_width=1.5)
        top = DashedLine([xs[0] - 0.3, base_y + scale, 0], [xs[-1] + 0.3, base_y + scale, 0], color=GREY_D, stroke_width=1.5)
        l0 = MathTex("0", font_size=22, color=GREY_B).next_to(axis, LEFT, buff=0.1)
        l1 = MathTex("1", font_size=22, color=GREY_B).next_to(top, LEFT, buff=0.1)
        curve = VMobject().set_points_as_corners(pts).set_stroke(C.BASELINE, 4)
        dots = VGroup(*[Dot(p, radius=0.06, color=C.BASELINE) for p in pts])
        delta = np.array(s["delta"], float)
        bars = VGroup()
        for c, dlt in zip(ans, delta):
            h = abs(dlt) * 1.4
            r = Rectangle(width=0.32, height=max(h, 0.02), stroke_width=0,
                          fill_color=C.REWARD if dlt >= 0 else C.PENALTY, fill_opacity=0.9)
            yb = y_strip - 0.45
            r.move_to([c.get_x(), yb - 0.75 + (h / 2 if dlt >= 0 else -h / 2) + 0.75 * 0, 0])
            r.move_to([c.get_x(), (yb - 0.8) + (h / 2 if dlt >= 0 else -h / 2), 0])
            bars.add(r)
        zl = Line([xs[0] - 0.3, y_strip - 1.25, 0], [xs[-1] + 0.3, y_strip - 1.25, 0], color=GREY_D, stroke_width=1.5)
        g = VGroup(strip, axis, top, l0, l1, curve, dots, bars, zl)
        g.strip, g.curve, g.dots, g.bars, g.ans, g.zl = strip, curve, dots, bars, ans, zl
        g.vaxis = VGroup(axis, top, l0, l1)
        return g

    def real_critic(self):
        d = self.d
        tag = real_tag(r"real critic, trained on the model's own answers")
        head = label(r"A value network (a critic) learned $V$ from 400 batches of the model's answers", font_size=28)
        head.to_edge(UP, buff=0.35)
        vlab = label(r"$V(s_t)$", font_size=28, color=C.BASELINE)
        dlab = label(r"$\delta_t$", font_size=28, color=C.ADVANTAGE)
        views = []
        for key in [("think", 1.0), ("direct", 1.0), ("direct", 0.0)]:
            if key in self.shows:
                views.append((key, self.value_view(self.shows[key], y_strip=-0.6)))
        v0 = d["V_prompt"]
        first = views[0][1]
        vlab.next_to(first.vaxis, LEFT, buff=0.5).shift(UP * 0.6)
        dlab.next_to(first.zl, LEFT, buff=0.5)
        sw = self.shows[("direct", 0.0)]
        k_bad = int(np.argmin(sw["delta"]))
        assert sw["delta"][k_bad] < -0.2, sw["delta"]
        st = self.shows[("think", 1.0)]
        assert st["delta"][0] > 0.1, st["delta"][:2]
        with self.voiceover(
            "We can't compute V exactly, so we learn it: a second network, the critic, trained to predict the "
            "final reward from every prefix of the model's own answers. Here is a real one, reading three real "
            f"answers. Before the model writes anything, the critic gives it a {v0 * 100:.0f} percent chance. "
            "<bookmark mark='t'/> In this first answer the model starts by showing its work, and the value jumps: "
            "the critic has learned that worked answers are almost always right. Every later token barely changes "
            "anything."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            self.play(FadeIn(first.strip, lag_ratio=0.03), FadeIn(first.vaxis), FadeIn(vlab), FadeIn(dlab), Create(first.zl))
            vo.wait_until("t")
            self.play(Create(first.curve), FadeIn(first.dots, lag_ratio=0.05), run_time=2)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in first.bars], lag_ratio=0.05))
        cur = first
        for key, view in views[1:]:
            text = ("This one answers directly, and gets it right. Each digit nudges the value a little, as the "
                    "carries go by without a slip." if key == ("direct", 1.0) else
                    "And here's our wrong answer. <bookmark mark='x'/> The value drops at exactly one token: the "
                    "digit where the carry was forgotten. That negative delta is the credit assignment we wanted.")
            with self.voiceover(text) as vo:
                self.play(FadeOut(cur), FadeIn(view.strip, lag_ratio=0.03), FadeIn(view.vaxis), Create(view.zl))
                self.play(Create(view.curve), FadeIn(view.dots, lag_ratio=0.05), run_time=1.6)
                self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in view.bars], lag_ratio=0.05))
                if key == ("direct", 0.0):
                    vo.wait_until("x")
                    self.play(Indicate(view.ans[k_bad], color=YELLOW, scale_factor=1.3),
                              Indicate(view.bars[k_bad], color=YELLOW))
            cur = view
        self.view_wrong = cur
        self.wait(0.3)
        self.clear_scene(cur)
        self.play(FadeOut(cur))

    # ------------------------------------------------------------------
    def gae(self):
        s = self.shows[("direct", 0.0)]
        f = mtex(r"\hat A_t", r"=", r"\sum_{l \ge 0}", r"\lambda^{l}", r"\delta_{t+l}", font_size=44).to_edge(UP, buff=0.4)
        f[0].set_color(C.ADVANTAGE)
        f[3].set_color(YELLOW)
        f[4].set_color(C.ADVANTAGE)
        name = label(r"Generalized Advantage Estimation (Schulman et al.\ 2015)", font_size=26, color=GREY_A).next_to(f, DOWN, buff=0.15)
        lim0 = mtex(r"\lambda = 0:\quad \hat A_t = \delta_t", font_size=32)
        lim1 = mtex(r"\lambda = 1:\quad \hat A_t = \delta_t + \delta_{t+1} + \dots = R - V(s_t)", font_size=32)
        n0 = label(r"trust the critic: low noise, biased if $V$ is wrong", font_size=24, color=GREY_A)
        n1 = label(r"trust the outcome: unbiased, but noisy (the sum telescopes)", font_size=24, color=GREY_A)
        lims = VGroup(VGroup(lim0, n0).arrange(RIGHT, buff=0.4), VGroup(lim1, n1).arrange(RIGHT, buff=0.4))
        lims.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(name, DOWN, buff=0.35)
        V0 = float(self.d["V_prompt"])

        def strip_for(sh):
            return tokens(self.prompt, sh["text"], font_size=28, cell=0.5, height=0.6).move_to(DOWN * 1.35)

        def bar_group(strip, n_prompt, A):
            ans = strip[n_prompt:]
            g = VGroup()
            for c, v in zip(ans, A):
                h = abs(v) * 1.8
                r = Rectangle(width=0.32, height=max(h, 0.02), stroke_width=0, fill_color=C.REWARD if v >= 0 else C.PENALTY,
                              fill_opacity=0.9)
                y = strip.get_bottom()[1] - 0.12 - h / 2 if v < 0 else strip.get_top()[1] + 0.12 + h / 2
                r.move_to([c.get_x(), y, 0])
                g.add(r)
            return g

        def gae_of(sh, l):
            delta = np.array(sh["delta"], float)
            T = len(delta)
            return np.array([sum((l ** j) * delta[t + j] for j in range(T - t)) for t in range(T)])

        strip = strip_for(s)
        n_p = len(self.prompt)
        lam = ValueTracker(0.0)
        bb = always_redraw(lambda: bar_group(strip, n_p, gae_of(s, lam.get_value())))
        lt = always_redraw(lambda: mtex(rf"\lambda = {lam.get_value():.2f}", font_size=34, color=YELLOW).next_to(strip, LEFT, buff=0.35))
        tag = real_tag(r"real critic, real answers")
        with self.voiceover(
            "Using delta alone trusts the critic completely, and the critic is only a guess. Generalized advantage "
            "estimation blends in the actual outcome: add up the deltas from here to the end, discounting each step "
            "by a factor lambda. <bookmark mark='z'/> With lambda zero, you get the critic's one-step opinion. "
            "<bookmark mark='o'/> With lambda one, the sum telescopes into the final reward minus the value now: "
            "unbiased, but noisier."
        ) as vo:
            self.play(Write(f), FadeIn(name))
            vo.wait_until("z")
            self.play(FadeIn(lims[0]))
            vo.wait_until("o")
            self.play(FadeIn(lims[1]))
        with self.voiceover(
            "On our wrong answer, <bookmark mark='s'/> slide lambda from zero to one. Almost nothing changes. This "
            "critic is good: the value already collapsed at the bad digit, so the later tokens owe nothing either way."
        ) as vo:
            self.play(FadeIn(strip, lag_ratio=0.03), FadeIn(bb), FadeIn(lt), FadeIn(tag))
            vo.wait_until("s")
            self.play(lam.animate.set_value(1.0), run_time=3.0, rate_func=linear)
        flat = bar_group(strip, n_p, np.full(len(s["delta"]), s["r"] - V0))
        nolab = label(r"no critic: $\hat A_t = R - b$ for every token (GRPO, RLOO)", font_size=26, color=C.BASELINE)
        nolab.next_to(strip, DOWN, buff=1.3)
        bb.clear_updaters()
        lt.clear_updaters()
        with self.voiceover(
            "Now take the critic away and use one number per prompt, the way GRPO and RLOO do. <bookmark mark='f'/> "
            "Every token gets the same blame, the correct digits included."
        ) as vo:
            vo.wait_until("f")
            self.play(Transform(bb, flat), FadeOut(lt), FadeIn(nolab))
        st = self.shows[("think", 1.0)]
        strip2 = strip_for(st)
        crit = bar_group(strip2, n_p, gae_of(st, 1.0))
        flat2 = bar_group(strip2, n_p, np.full(len(st["delta"]), st["r"] - V0))
        clab = label(r"with the critic: the credit lands on the one token that chose to show the work", font_size=26, color=C.BASELINE)
        clab.move_to(nolab)
        with self.voiceover(
            "And on a right answer that showed its work: <bookmark mark='c'/> the critic puts nearly all the credit "
            "on the single token that decided to show the work. <bookmark mark='g'/> Without a critic, that decision "
            "is just one token among thirteen, all sharing the same reward."
        ) as vo:
            self.play(FadeOut(bb), FadeOut(strip), FadeOut(nolab), FadeIn(strip2, lag_ratio=0.03))
            vo.wait_until("c")
            self.play(FadeIn(crit), FadeIn(clab))
            vo.wait_until("g")
            self.play(Transform(crit, flat2), FadeOut(clab), FadeIn(nolab))
        cost = label(r"the price of a critic: a second network as large as the policy, trained alongside it", font_size=28, color=C.BASELINE)
        cost.move_to(nolab)
        with self.voiceover(
            "The price is a critic network as large as the policy itself, trained alongside it. The algorithm "
            "behind today's reasoning models decided that price wasn't worth paying."
        ):
            self.play(FadeOut(nolab), FadeIn(cost))
        self.wait(0.4)
        self.clear_scene()
