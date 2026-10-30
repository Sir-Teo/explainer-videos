from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai16.common import EXPERT_COLORS, EXPERTC, HISTC, PART, ROUTER, load, ms, take_away


class Origins(VoiceoverScene):
    def construct(self):
        self.card()
        self.define()
        self.derive()
        self.replay()
        self.sparse()

    def card(self):
        card = chapter_card(1, r"Competing experts, 1991", r"How should several networks share one job?", part=PART)
        with self.voiceover("Chapter one. Competing experts, 1991."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def define(self):
        colors = {r"g_i(x)": ROUTER, r"E_i(x)": EXPERTC}
        f = cmath(r"y", r"=", r"\sum_{i=1}^{n}", r"g_i(x)", r"\,", r"E_i(x)", colors=colors, font_size=40)
        g_ = cmath(r"g(x)", r"=", r"\operatorname{softmax}(W_g\, x)", colors={r"g(x)": ROUTER}, font_size=34)
        body = VGroup(f, g_).arrange(DOWN, buff=0.3)
        card = definition_card(r"Mixture of experts", body, color=ROUTER, width=6.6).move_to([-3.2, 0.6, 0])
        notes = VGroup(label(r"$E_i$: \ an expert, \ a small network of its own", font_size=22, color=EXPERTC),
                       label(r"$g_i$: \ the gate's trust in expert $i$ \ (they add to one)", font_size=22, color=ROUTER),
                       label(r"$W_g$: \ the gate, \ one more matrix", font_size=22, color=GREY_A))
        notes.arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(card, DOWN, buff=0.35).align_to(card, LEFT)
        # the picture: an input, a gate, n experts, one output
        x = Dot([2.0, 0.4, 0], radius=0.09, color=C.EMBED)
        xl = MathTex("x", font_size=30, color=C.EMBED).next_to(x, LEFT, buff=0.15)
        gate = node_box(r"gate", ROUTER, font_size=22).move_to([3.6, 2.0, 0])
        exps = VGroup(*[node_box(rf"$E_{i + 1}$", EXPERT_COLORS[i], font_size=22) for i in range(4)])
        exps.arrange(DOWN, buff=0.22).move_to([4.2, -0.3, 0])
        y = Dot([6.0, 0.4, 0], radius=0.09, color=C.BITS)
        yl = MathTex("y", font_size=30, color=C.BITS).next_to(y, RIGHT, buff=0.15)
        wires = VGroup(*[Line(x.get_center(), e.get_left(), color=GREY_C, stroke_width=1.5) for e in exps],
                       Line(x.get_center(), gate.get_left(), color=ROUTER, stroke_width=1.5))
        outs = VGroup(*[Line(e.get_right(), y.get_center(), color=EXPERT_COLORS[i], stroke_width=2.5)
                        for i, e in enumerate(exps)])
        trust = [0.08, 0.7, 0.17, 0.05]
        for o, t in zip(outs, trust):
            o.set_stroke(width=1 + 7 * t)
        gl = DashedLine(gate.get_bottom(), exps.get_top() + UP * 0.05, color=ROUTER, stroke_width=1.5)
        tag = schematic_tag(corner=DR)
        cite_ = cite(r"R.~Jacobs, M.~Jordan, S.~Nowlan \& G.~Hinton, \textit{Neural Computation} (1991)", corner=DL)
        hist = history_card(1991, r"Robert Jacobs, Michael Jordan, \\ Steven Nowlan \& Geoffrey Hinton",
                            r"\textit{Adaptive Mixtures of Local Experts}: \ several networks, \ one job", width=5.6,
                            color=HISTC).move_to([-3.4, 0.6, 0])
        with self.voiceover(
            "In 1991 the question was how to make several networks share one job, instead of training one network "
            "to do everything. <bookmark mark='a'/> Jacobs, Jordan, Nowlan and Hinton's answer is the mixture of "
            "experts. Several small networks, the experts, each make a guess, and a gate, one more matrix and a "
            "softmax, decides how much to trust each one for this input. The answer is the trusted mix. "
            "<bookmark mark='b'/> The gate's numbers are like part seven's mixture weights, except that they "
            "change with the input: for one input the gate leans on expert two, for another on expert four. "
            "<bookmark mark='c'/> Their test was telling apart vowel sounds spoken by many people."
        ) as vo:
            self.play(FadeIn(x), FadeIn(xl), FadeIn(exps), FadeIn(y), FadeIn(yl), Create(wires[:4]), FadeIn(tag),
                      FadeIn(cite_), FadeIn(hist, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(hist), FadeIn(card, shift=UP * 0.2), FadeIn(gate), Create(wires[4]), Create(gl))
            self.play(LaggedStart(*[FadeIn(n_) for n_ in notes], lag_ratio=0.3), Create(outs))
            vo.wait_until("b")
            for t in ([0.05, 0.1, 0.15, 0.7], [0.1, 0.6, 0.2, 0.1]):
                self.play(*[o.animate.set_stroke(width=1 + 7 * v) for o, v in zip(outs, t)], run_time=1.0)
            vo.wait_until("c")
            self.play(Indicate(exps, color=WHITE, scale_factor=1.03))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        colors = {r"g_i": ROUTER, r"o_i": EXPERTC, r"h_i": C.BITS}
        rows = [
            cmath(r"L_{\text{coop}}", r"=", r"\tfrac12 \big\| y - \textstyle\sum_i", r"g_i", r"o_i", r"\big\|^2",
                  colors=colors, font_size=34),
            cmath(r"\frac{\partial L_{\text{coop}}}{\partial", r"o_i", r"}", r"=", r"-", r"g_i", r"\big(y - \textstyle\sum_j",
                  r"g_j", r"o_j", r"\big)", colors=colors, font_size=34),
            cmath(r"L_{\text{comp}}", r"=", r"-\log \textstyle\sum_i", r"g_i", r"\, e^{-\frac12 \| y - ", r"o_i", r"\|^2}",
                  colors=colors, font_size=34),
            cmath(r"\frac{\partial L_{\text{comp}}}{\partial", r"o_i", r"}", r"=", r"-", r"h_i", r"\,(y - ", r"o_i", r")",
                  colors=colors, font_size=34),
            cmath(r"h_i", r"=", r"\frac{", r"g_i", r"\, e^{-\frac12\|y - ", r"o_i", r"\|^2}}{\sum_j", r"g_j",
                  r"\, e^{-\frac12\|y - ", r"o_j", r"\|^2}}", colors=colors, font_size=34),
        ]
        whys = [why(r"fit the blend: \ the 'obvious' loss"), why(r"each expert chases the blend's error"),
                why(r"a mixture's likelihood \ (Part 7)"), why(r"each expert chases its own error..."),
                why(r"...weighted by how well it already explains $y$")]
        step = ladder(self, rows, whys, keep=5, top=3.1, x=-2.6, buff=0.32, edge=6.8)
        head = label(r"two ways to train the same mixture", font_size=26, color=GREY_A).to_edge(DOWN, buff=1.1)
        ta = take_away(r"compete: \ an expert learns most from the cases it already wins \ $\Rightarrow$ \ specialists",
                       color=C.BITS, font_size=24)
        with self.voiceover(
            "The new idea was in the loss. <bookmark mark='a'/> The obvious loss fits the blend: the squared error of "
            "the gated sum. <bookmark mark='b'/> Its gradient tells every expert to chase the blend's error, so each "
            "expert's lesson depends on all the others: they cooperate, and they all end up a little responsible for "
            "everything. <bookmark mark='c'/> Jacobs and his colleagues instead treated the experts as a mixture of "
            "Gaussians, part seven's mixture model, and minimized the negative log likelihood. <bookmark mark='d'/> "
            "Now each expert chases its own error, <bookmark mark='e'/> weighted by h, the posterior probability "
            "that it was the one responsible: how much the gate trusted it, times how well it already explains the "
            "answer. Part seven's EM called this the responsibility. An expert learns most from the cases it already "
            "wins. They compete, and they become specialists."
        ) as vo:
            self.play(FadeIn(head))
            for i, mk in enumerate("abcde"):
                vo.wait_until(mk)
                step(i)
            self.play(FadeOut(head), FadeIn(ta))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def panel(self, d, loss, center, title, color):
        grid = np.asarray(d["grid"], float)
        ax = Axes(x_range=[-1, 1, 0.5], y_range=[-0.8, 1.0, 0.5], x_length=5.6, y_length=2.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to(center + UP * 0.9)
        gx = Axes(x_range=[-1, 1, 0.5], y_range=[0, 1, 0.5], x_length=5.6, y_length=1.1, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).next_to(ax, DOWN, buff=0.35)
        pts = VGroup(*[Dot(ax.c2p(a, b), radius=0.022, color=GREY_B) for a, b in zip(d["x"][::2], d["y"][::2])])
        t = label(title, font_size=24, color=color).next_to(ax, UP, buff=0.15)
        gl = label(r"the gate: \ $g_i(x)$", font_size=18, color=ROUTER).next_to(gx, UP, buff=0.04).align_to(gx, LEFT)
        G, Ex, Mx = (np.asarray(d[f"{loss}_{k}"], float) for k in ("gate", "experts", "mix"))

        def lines(k):
            out = VGroup()
            for i in range(G.shape[2]):
                seg = [(x_, y_) for x_, y_ in zip(grid, Ex[k, :, i]) if -0.8 <= y_ <= 1.0]
                if len(seg) > 1:
                    out.add(VMobject(stroke_width=1.6, color=EXPERT_COLORS[i]).set_points_as_corners(
                        [ax.c2p(a, b) for a, b in seg]).set_stroke(opacity=0.55))
            out.add(VMobject(stroke_width=3.5, color=WHITE).set_points_as_corners(
                [ax.c2p(a, b) for a, b in zip(grid, np.clip(Mx[k], -0.8, 1.0))]))
            gates = VGroup(*[VMobject(stroke_width=3, color=EXPERT_COLORS[i]).set_points_as_corners(
                [gx.c2p(a, b) for a, b in zip(grid, G[k, :, i])]) for i in range(G.shape[2])])
            return VGroup(out, gates)

        return VGroup(ax, gx, pts, t, gl), lines

    def replay(self):
        d = load("mix1991")
        steps = [int(s) for s in d["snaps"]]
        pa, la = self.panel(d, "compete", np.array([-3.45, 0.0, 0]), r"competing \ (1991)", C.BITS)
        pb, lb = self.panel(d, "cooperate", np.array([3.45, 0.0, 0]), r"cooperating", GREY_A)
        cur_a, cur_b = la(0), lb(0)
        clock = VGroup(label(r"training step", font_size=24, color=GREY_A), Integer(0, font_size=28, color=C.BITS))
        clock.arrange(RIGHT, buff=0.2).to_edge(UP, buff=0.25)
        tag = note(rf"computed: \ ${int(d['n_experts'])}$ straight-line experts and a softmax gate on one input; \ "
                   r"white: \ the mixture", font_size=18).to_edge(DOWN, buff=0.2)
        sa, sb = ms(d["compete_sharp_final"]), ms(d["cooperate_sharp_final"])
        oa = [int(d[f"compete_s{s}_owners"]) for s in d["seeds"]]
        ob = [int(d[f"cooperate_s{s}_owners"]) for s in d["seeds"]]
        ea, eb = ms(d["compete_mse_final"]), ms(d["cooperate_mse_final"])
        sharper = sa[0] > sb[0] + 0.1
        verdict = (f"Competing, the gate ends up sure of itself: on average it gives {100 * sa[0]:.0f} percent of its "
                   f"trust to one expert, against {100 * sb[0]:.0f} percent when they cooperate, over three seeds each. "
                   if sharper else
                   f"Here the two end up about equally decided: {100 * sa[0]:.0f} percent of the trust to one expert "
                   f"competing, {100 * sb[0]:.0f} cooperating. ")
        fit_word = 'about as well' if abs(ea[0] - eb[0]) < 0.3 * eb[0] else ('better' if ea[0] < eb[0] else 'worse')
        own = (f"With competition, {min(oa)} to {max(oa)} experts each own a stretch of the line, one per regime, and "
               f"the blend fits {fit_word}: each expert does one simple thing.")
        with self.voiceover(
            "Here's that difference, trained on this computer. A curve with three regimes, a rise, a plateau and a "
            "fall, and four experts that can each draw only a straight line, with a gate that looks at x. "
            "<bookmark mark='a'/> The same mixture, trained the two ways. Watch the gates below the curves. "
            "<bookmark mark='b'/> " + verdict + "<bookmark mark='v'/>" + own
        ) as vo:
            self.play(FadeIn(pa), FadeIn(pb), FadeIn(clock), FadeIn(tag), FadeIn(cur_a), FadeIn(cur_b))
            vo.wait_until("a")
            for k in range(1, len(steps)):
                na, nb = la(k), lb(k)
                self.play(Transform(cur_a, na), Transform(cur_b, nb), clock[1].animate.set_value(steps[k]),
                          run_time=0.8 if k < 4 else 0.6)
            vo.wait_until("b")
            self.play(Indicate(cur_a[1], color=WHITE, scale_factor=1.02))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sparse(self):
        colors = {r"H(x)_i": ROUTER, r"\epsilon_i": C.SURPRISE}
        f1 = cmath(r"H(x)_i", r"= (W_g x)_i +", r"\epsilon_i", r"\cdot \operatorname{softplus}\big((W_{\text{noise}}\, x)_i\big)",
                   colors=colors, font_size=32)
        f2 = cmath(r"g(x) = \operatorname{softmax}\big(\operatorname{KeepTopK}(", r"H(x)", r", k)\big)",
                   colors={r"H(x)": ROUTER}, font_size=32)
        f3 = label(r"KeepTopK: \ the $k$ largest scores stay, \ the rest become $-\infty$ \ (a gate of exactly $0$)",
                   font_size=20, color=GREY_A)
        f4 = label(r"$\epsilon_i \sim \mathcal N(0, 1)$: \ noise, \ so the router keeps trying other experts", font_size=20,
                   color=C.SURPRISE)
        eqs = VGroup(f1, f2, f3, f4).arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to([-2.2, 1.1, 0])
        cards = VGroup(
            history_card(1994, r"Jordan \& Jacobs", r"hierarchies of gates, \ trained by EM", width=4.2, color=HISTC),
            history_card(2017, r"Shazeer et al.", r"thousands of experts between LSTM layers; \ only $k$ run: \ "
                         r"$137$ billion parameters, \ over $1{,}000\times$ the capacity", width=4.2, color=HISTC),
        ).arrange(DOWN, buff=0.2).move_to([4.7, 0.5, 0])
        exps = VGroup(*[Square(0.2, stroke_width=0.8, stroke_color=EXPERTC, fill_color=EXPERTC,
                               fill_opacity=0.85 if i in (5, 22) else 0.05) for i in range(32)])
        exps.arrange_in_grid(rows=2, cols=16, buff=0.06).move_to([-2.4, -2.0, 0])
        el = label(r"only the chosen experts compute: \ the work stays the same as the experts multiply", font_size=22,
                   color=C.BITS).next_to(exps, DOWN, buff=0.2)
        cite_ = cite(r"N.~Shazeer et al., \textit{Outrageously Large Neural Networks}, ICLR (2017)", corner=UL)
        old = cmath(r"y = \sum_{i=1}^{n}", r"g_i(x)", r"\, E_i(x)", r"\quad \text{(every } E_i \text{ runs)}",
                    colors={r"g_i(x)": ROUTER}, font_size=36).move_to(eqs)
        with self.voiceover(
            "In those early mixtures, every expert ran on every input, and the gate only weighed them. "
            "<bookmark mark='a'/> In 1994 Jordan and Jacobs stacked gates into hierarchies and trained them with "
            "EM. <bookmark mark='b'/> In 2017 Noam Shazeer and colleagues at Google turned the mixture into a way "
            "to grow. Keep only the top k gate scores, and set the rest to minus infinity, so their gates are "
            "exactly zero and those experts need never run. <bookmark mark='c'/> Add a little noise to the scores, "
            "so the router keeps trying other experts. <bookmark mark='d'/> Then the number of experts can grow "
            "without the work per token growing: they put thousands of experts between the layers of an LSTM, a "
            "hundred and thirty-seven billion parameters, more than a thousand times the capacity of the models "
            "before. That's the sparse mixture of experts every model in this part uses."
        ) as vo:
            self.play(FadeIn(cite_), FadeIn(exps.copy().set_fill(opacity=0.05)), FadeIn(old))
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(old))
            self.play(Write(f1[:2]), Write(f2), FadeIn(f3))
            vo.wait_until("c")
            self.play(Write(f1[2:]), FadeIn(f4))
            vo.wait_until("d")
            self.play(FadeIn(cards[1], shift=LEFT * 0.2), FadeIn(exps), FadeIn(el))
        self.wait(0.3)
        self.clear_scene()


def node_box(text, color, font_size=22):
    from videos.ai.ai16.common import node_box as nb

    return nb(text, color, font_size=font_size)
