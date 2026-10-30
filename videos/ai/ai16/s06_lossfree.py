from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai16.common import (BALC, EXPERT_COLORS, F, MODE_COLOR, MODES, PART, ROUTER, SHAREDC, gate_bars,
                                   gate_picture, load, ms, take_away)


class LossFree(VoiceoverScene):
    def construct(self):
        self.card()
        self.rule()
        self.exact()
        self.replay()
        self.compare()

    def card(self):
        card = chapter_card(5, r"Balancing without a loss", r"Can we balance without bending the model?", part=PART)
        with self.voiceover("Chapter five. Balancing without a loss."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def rule(self):
        colors = {r"b_i": BALC, r"s_i": ROUTER, r"f_i": BALC, r"\gamma": C.BITS}
        rows = [
            cmath(r"\mathcal K", r"=", r"\operatorname{top}_k\big(", r"s_i", r"+", r"b_i", r"\big)", colors=colors, font_size=36),
            cmath(r"y", r"=", r"\sum_{i\in\mathcal K} g_i\, E_i(x)", r",\qquad g_i \propto", r"s_i", colors=colors, font_size=36),
            cmath(r"b_i", r"\;\leftarrow\;", r"b_i", r"+", r"\gamma", r"\,\operatorname{sign}\!\big(\bar f -", r"f_i", r"\big)",
                  colors=colors, font_size=36),
        ]
        whys = [why(r"a bias per expert, \ used only to choose"), why(r"the weights ignore it: \ the output isn't bent"),
                why(r"after each step: \ busy experts down a notch, \ idle ones up")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-2.6, buff=0.55, edge=6.8)
        cards = VGroup(
            history_card(2024, r"Lean Wang, Huazuo Gao, Chenggang Zhao, \\ Xu Sun \& Damai Dai \ (DeepSeek)",
                         r"\textit{Auxiliary-Loss-Free Load Balancing}: \ better balance and lower perplexity than "
                         r"the auxiliary loss", width=6.0, color=C.HUMAN),
        ).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In 2024 DeepSeek removed the trade-off. Give every expert a bias, a single number, <bookmark mark='a'/> "
            "and add it to the expert's score only when choosing the top k. <bookmark mark='b'/> The gates that mix "
            "the chosen experts use the scores alone, so the bias changes who works, never what the model computes. "
            "<bookmark mark='c'/> After every step, look at the loads: an expert busier than average has its bias "
            "lowered by a small step gamma, and an idle one has it raised. There's no extra loss, so no gradient "
            "fights the language model. <bookmark mark='d'/> Lean Wang and colleagues reported both better balance "
            "and lower perplexity than the auxiliary loss, and DeepSeek-V3 was trained this way."
        ) as vo:
            self.play(FadeIn(cards, shift=UP * 0.2))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(Indicate(cards, color=WHITE, scale_factor=1.03))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def exact(self):
        r = F.DSV3_ROUTING
        colors = {r"s_i": ROUTER, r"b_i": BALC, r"g_i": C.BITS}
        eqs = VGroup(
            cmath(r"s_i", r"= \sigma\big(u^{\top} e_i\big)", colors=colors, font_size=32),
            cmath(r"\mathcal{K} = \operatorname{top}_k\big(", r"s_i", r"+", r"b_i", r"\big)", colors=colors, font_size=32),
            cmath(r"g_i", r"= \frac{", r"s_i", r"}{\sum_{j \in \mathcal{K}} s_j}, \quad i \in \mathcal{K}", colors=colors, font_size=32),
            cmath(r"h = u + \operatorname{FFN}_{\text{shared}}(u) + \sum_{i \in \mathcal{K}}", r"g_i", r"\, \operatorname{FFN}_i(u)",
                  colors=colors, font_size=32),
        ).arrange(DOWN, buff=0.42, aligned_edge=LEFT).move_to([-3.2, 0.3, 0])
        notes = VGroup(label(r"a sigmoid score per expert, \ not a softmax", font_size=18, color=GREY_A),
                       label(r"the balancing bias picks the experts...", font_size=18, color=BALC),
                       label(r"...but the weights ignore it", font_size=18, color=C.BITS),
                       label(r"one shared expert for every token", font_size=18, color=SHAREDC))
        for n_, e_ in zip(notes, eqs):
            n_.next_to(e_, DOWN, buff=0.06).align_to(e_, LEFT)
        for k in range(1, len(eqs)):
            VGroup(*eqs[k:], *notes[k:]).shift(DOWN * 0.18)
        head = label(r"DeepSeek-V3's router, \ exactly", font_size=28).to_edge(UP, buff=0.35)
        facts = VGroup(
            label(rf"$\gamma = {r['gamma']}$ \ for the first ${r['gamma_until'] / 1e12:.1f}$ trillion tokens, \ then $0$",
                  font_size=20, color=BALC),
            label(rf"plus a tiny sequence-wise balance loss, \ $\alpha = {r['alpha_seq']}$", font_size=20, color=GREY_A),
            label(r"no token is ever dropped \ (chapter seven)", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.4, -2.0, 0])
        cite_ = cite(r"DeepSeek-AI, \textit{DeepSeek-V3 Technical Report} (2024), \ Secs.~2.1.2, 4.2", corner=DL)
        gc = gloss(r"sigmoid gate", r"each expert's score squashed to between $0$ and $1$ on its own: \\ raise one, "
                   r"and the others don't have to fall", gate_picture(), width=5.2, color=ROUTER).move_to([3.75, 1.2, 0])
        gp = gc[1][-1]
        tag = note(r"illustrative scores").next_to(gc, DOWN, buff=0.1).align_to(gc, RIGHT)
        with self.voiceover(
            "Here is DeepSeek-V3's router exactly, since it's become a template. <bookmark mark='a'/> Each expert "
            "gets a score from a sigmoid, its own yes-or-no, rather than a softmax that makes experts compete. "
            "<bookmark mark='b'/> The top k are chosen by score plus the balancing bias. <bookmark mark='c'/> The "
            "gates use the scores alone, rescaled to add to one. <bookmark mark='d'/> And one shared expert sees "
            "every token, to hold what everything needs. <bookmark mark='e'/> The bias moved by a thousandth a step "
            "for the first fourteen point three trillion tokens, then froze; a tiny extra loss kept single sequences "
            "from piling onto a few experts; and no token was ever dropped."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(Write(eqs[k]), FadeIn(notes[k]))
                if k == 0:
                    self.play(FadeIn(gc, shift=UP * 0.2), FadeIn(tag))
                    for boost in (1.6, 0.0):
                        b0, b1 = gate_bars(gp, boost)
                        self.play(Transform(gp[0][0], b0), Transform(gp[1][0], b1), run_time=1.2)
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(f_) for f_ in facts], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        b = load("balance")
        E = int(b["E"])
        every = int(b["load_every"])
        loads = {k: np.asarray(b[f"{k}_loads"], float)[0, :, 0] for k, _, _ in MODES}  # seed 1, block 1: time, E
        n = len(loads["none"])
        frames = np.unique(np.linspace(0, n - 1, 22).round().astype(int))
        top = min(max(float(v.max()) for v in loads.values()), 0.6)
        sets = []
        for i, (k, title, col) in enumerate(MODES):
            bars = LiveBars(np.minimum(loads[k][0], top), max_value=top, height=2.3, bar_width=0.3, gap=0.07,
                            colors=EXPERT_COLORS[:E])
            bars.place(base_y=-0.2, x=-4.4 + 4.4 * i)
            fy = -0.2 + 2.3 / E / top
            fair = DashedLine([-4.4 + 4.4 * i - 1.6, fy, 0], [-4.4 + 4.4 * i + 1.6, fy, 0], color=GREY_B, stroke_width=1.5)
            t = label(title, font_size=22, color=col).move_to([-4.4 + 4.4 * i, 2.5, 0])
            sets.append((bars, fair, t))
        bias = np.asarray(b["bias_hist"], float)[:, 0]  # time, E (seed 1, block 1)
        ax = Axes(x_range=[0, len(bias) - 1, 25], y_range=[float(bias.min()) - 0.01, float(bias.max()) + 0.01, 0.05],
                  x_length=5.4, y_length=1.9, tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False})
        ax.move_to([3.6, -2.45, 0])
        bl = label(r"the biases $b_i$ through training", font_size=18, color=BALC).next_to(ax, UP, buff=0.08)
        blines = VGroup(*[VMobject(stroke_width=2, color=EXPERT_COLORS[j]).set_points_as_corners(
            [ax.c2p(t_, float(bias[t_, j])) for t_ in range(len(bias))]) for j in range(E)])
        clock = VGroup(label(r"training step", font_size=24, color=GREY_A), Integer(0, font_size=28, color=C.BITS))
        clock.arrange(RIGHT, buff=0.2).move_to([-3.4, -2.2, 0])
        fl = label(r"dashed: \ a fair share, \ $1/8$; \ block $1$, \ seed $1$", font_size=20, color=GREY_B).next_to(clock, DOWN, buff=0.25)
        bt = [float(np.asarray(b[f"{k}_busiest"], float)[0, 0]) for k, _, _ in MODES]
        left = ("On the left, with no balancing, the shares drift apart. " if bt[0] > bt[2] + 0.3 else
                "On the left, with no balancing, the shares wander. ")
        mid = ("In the middle, Switch's loss pulls them part of the way back. " if bt[1] > bt[2] + 0.2 else
               "In the middle, Switch's loss pulls them back. ")
        with self.voiceover(
            "Here are all three rules at once, replayed through training: each bar is one expert's share of the tokens "
            "in the first block. <bookmark mark='a'/> "
            + left + "<bookmark mark='m'/>" + mid + "<bookmark mark='r'/>On the right, the bias holds every expert near its fair share. <bookmark mark='b'/> Below, the biases "
            "themselves: each is a running tally of how often its expert was too busy or too idle."
        ) as vo:
            self.play(FadeIn(clock), FadeIn(fl), *[FadeIn(VGroup(b_, fr, t)) for b_, fr, t in sets])
            vo.wait_until("a")
            for f_ in frames[1:]:
                self.play(*[a for k_, (b_, _, _) in zip(MODES, sets) for a in b_.to(np.minimum(loads[k_[0]][f_], top))],
                          clock[1].animate.set_value(int(f_ * every)), run_time=0.35, rate_func=linear)
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(bl), Create(blines), run_time=2.0)
        self.wait(0.3)
        for b_, _, _ in sets:
            b_.freeze()
        self.clear_scene()

    # ------------------------------------------------------------------
    def compare(self):
        b = load("balance")
        keys = [k for k, _, _ in MODES]
        rows = VGroup()
        hdr = VGroup(*[label(t, font_size=20, color=GREY_A) for t in
                       (r"", r"busiest expert", r"starved experts", r"imbalance, \\ through training", r"held-out bits")])
        cells = [hdr]
        for k, name, col in MODES:
            bz = np.asarray(b[f"{k}_busiest"], float)
            sv = np.asarray(b[f"{k}_starved"], int)
            mv = ms(b[f"{k}_maxvio"])
            vb = ms(b[f"{k}_valid"])
            cells.append(VGroup(label(name, font_size=22, color=col),
                                label(rf"${bz.mean():.1f}\times$", font_size=22),
                                label(rf"${int(sv.sum())}$ of ${bz.size * int(b['E'])}$", font_size=22),
                                label(rf"${mv[0]:.2f}$", font_size=22),
                                label(rf"${vb[0]:.3f}$ \ \small{{(${vb[1]:.3f}$--${vb[2]:.3f}$)}}", font_size=22, color=C.BITS)))
        widths = [max(r[j].width for r in cells) for j in range(5)]
        for i, r in enumerate(cells):
            x = -6.6
            for j, c_ in enumerate(r):
                c_.move_to([x + widths[j] / 2, 1.6 - i * 0.9, 0])
                x += widths[j] + 0.45
            rows.add(r)
        rows.scale_to_fit_width(12.4).move_to([0, 0.5, 0])
        keep_in_frame(rows)
        note_ = note(r"three seeds each; \ busiest and imbalance: \ multiples of a fair share; \ imbalance: Wang et al.'s "
                     r"MaxVio, \ averaged over training; \ the bias model also uses sigmoid gates", font_size=17)
        note_.to_edge(DOWN, buff=0.25)
        vb = {k: ms(b[f"{k}_valid"])[0] for k in keys}
        mx = {k: ms(b[f"{k}_maxvio"])[0] for k in keys}
        best_bal = min(keys, key=lambda k: mx[k])
        best_bits = min(keys, key=lambda k: vb[k])
        if best_bal == "moe":
            v = (f"The bias balances best, with the smallest imbalance through training, {mx['moe']:.2f}, against "
                 f"{mx['aux']:.2f} with the loss and {mx['none']:.2f} without. ")
        elif best_bal == "aux":
            v = (f"Here Switch's loss balances best through training, {mx['aux']:.2f} against {mx['moe']:.2f} for the "
                 "bias. ")
        else:
            v = "Surprisingly, the unbalanced router has the smallest imbalance here. "
        best_name = MODE_NAME_SPOKEN[best_bits]
        if best_bits == "moe":
            w = (f"In held-out bits the bias model is best as well: {vb['moe']:.3f}, against {vb['aux']:.3f} with the "
                 f"loss and {vb['none']:.3f} without. ")
        else:
            w = (f"In held-out bits, though, the best is {best_name}: {vb[best_bits]:.3f}, against "
                 f"{vb['moe']:.3f} with the bias. ")
        ta = take_away(r"balance by steering the choice, \ not by changing the loss", color=BALC, font_size=26)
        with self.voiceover(
            "The scoreboard, over three seeds each. <bookmark mark='a'/> " + v + "<bookmark mark='w'/>" + w
            + "<bookmark mark='b'/> One caution: our bias model also uses DeepSeek's sigmoid gates, while the other "
            "two use softmax gates, so the comparison is between routers, not just between balancing rules. "
            "<bookmark mark='c'/> The lesson DeepSeek drew: balance by steering the choice, not by changing the loss."
        ) as vo:
            self.play(FadeIn(rows[0]), *[FadeIn(r_[0]) for r_ in rows[1:]], FadeIn(note_))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_[1:]) for r_ in rows[1:]], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("b")
            self.play(Indicate(note_, color=WHITE, scale_factor=1.02))
            vo.wait_until("c")
            self.play(FadeIn(ta))
        self.wait(0.3)
        self.clear_scene()


MODE_NAME_SPOKEN = {"none": "no balancing at all", "aux": "Switch's loss", "moe": "the bias"}
