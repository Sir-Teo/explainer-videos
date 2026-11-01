from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai7.common import CAUSE, HIDDEN, PART, SEEN, load

TA, TB = "#FF9F45", "#58A6FF"  # treatments A and B
COL = {r"\mathrm{do}(x)": CAUSE, r"P(y \mid \mathrm{do}(x))": CAUSE}


def wnode(text, pos, color=SEEN, r=0.55):
    c = Circle(radius=r, color=color, stroke_width=3, fill_color=color, fill_opacity=0.25).move_to(pos)
    return VGroup(c, label(text, font_size=20).move_to(pos))


def arrow(a, b, color=GREY_B):
    d = b[0].get_center() - a[0].get_center()
    d = d / np.linalg.norm(d)
    return Arrow(a[0].get_center() + d * a[0].width / 2, b[0].get_center() - d * b[0].width / 2, buff=0.04, color=color,
                 stroke_width=3, max_tip_length_to_length_ratio=0.2)


class Causes(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"From graphs to causes", r"What would happen if we intervened?", lit=(2000,), part=PART)
        with self.voiceover("Chapter twelve. From graphs to causes."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.simpson()
        self.door()
        self.simulate()

    # ------------------------------------------------------------------
    def simpson(self):
        c = load("causal")
        st = c["stones"]

        def cell(t, z):
            s_, n_ = st[t][z]
            return label(rf"${100 * s_ / n_:.0f}\%$ \ ({s_}/{n_})", font_size=28, color=TA if t == "A" else TB)

        tot = c["total"]
        heads = VGroup(label(r"open surgery (A)", font_size=26, color=TA), label(r"keyhole surgery (B)", font_size=26, color=TB))
        rows = [(r"small stones", cell("A", "small"), cell("B", "small")),
                (r"large stones", cell("A", "large"), cell("B", "large")),
                (r"all patients", label(rf"${100 * tot['A'][0] / tot['A'][1]:.0f}\%$ \ ({tot['A'][0]}/{tot['A'][1]})",
                                        font_size=28, color=TA),
                 label(rf"${100 * tot['B'][0] / tot['B'][1]:.0f}\%$ \ ({tot['B'][0]}/{tot['B'][1]})", font_size=28,
                       color=TB))]
        tab = VGroup()
        for i, (nm, a, b) in enumerate(rows):
            y = 0.9 - 0.85 * i
            tab.add(VGroup(label(nm, font_size=28).move_to([-4.0, y, 0]), a.move_to([-0.3, y, 0]), b.move_to([3.6, y, 0])))
        heads[0].move_to([-0.3, 1.8, 0])
        heads[1].move_to([3.6, 1.8, 0])
        sep = Line([-5.6, -0.95, 0], [5.4, -0.95, 0], color=GREY_C, stroke_width=1.5)
        win = VGroup(SurroundingRectangle(tab[0][1], color=TA, buff=0.08), SurroundingRectangle(tab[1][1], color=TA, buff=0.08),
                     SurroundingRectangle(tab[2][2], color=TB, buff=0.08))
        head = label(r"success of kidney-stone surgery \ (Charig et al., 1986)", font_size=30).to_edge(UP, buff=0.4)
        q = label(r"which would you choose?", font_size=30, color=CAUSE).to_edge(DOWN, buff=1.0)
        cite_ = cite(r"C.~R.~Charig et al., \textit{BMJ} (1986); \ tabulated by S.~Julious \& M.~Mullee (1994)", corner=DR)
        with self.voiceover(
            "A real study, from 1986: two ways of removing kidney stones, open surgery and a keyhole method. "
            "<bookmark mark='a'/> For small stones, open surgery succeeded more often. <bookmark mark='b'/> For "
            "large stones, open surgery succeeded more often too. <bookmark mark='c'/> But over all patients, the "
            "keyhole method wins. <bookmark mark='d'/> That's Simpson's paradox, and it isn't a trick of arithmetic. "
            "Doctors gave open surgery mostly to the hard cases, the large stones. The comparison over all patients "
            "mixes the treatment's effect with the difficulty of the cases. Which treatment would you choose? Data "
            "alone can't say. You need to know where the data came from."
        ) as vo:
            self.play(FadeIn(head), FadeIn(heads), FadeIn(cite_), FadeIn(VGroup(*[r_[0] for r_ in tab])))
            vo.wait_until("a")
            self.play(FadeIn(tab[0][1:]))
            self.play(Create(win[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab[1][1:]))
            self.play(Create(win[1]))
            vo.wait_until("c")
            self.play(Create(sep), FadeIn(tab[2][1:]))
            self.play(Create(win[2]))
            vo.wait_until("d")
            self.play(FadeIn(q))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def door(self):
        c = load("causal")
        z = wnode(r"stone size", [-4.2, 1.9, 0], color=HIDDEN, r=0.7)
        x = wnode(r"treatment", [-5.6, -0.3, 0], color=TA, r=0.7)
        y = wnode(r"success", [-2.8, -0.3, 0], color=SEEN, r=0.7)
        zx, zy, xy = arrow(z, x), arrow(z, y), arrow(x, y)
        g = VGroup(z, x, y, zx, zy, xy)
        cut = Cross(zx, stroke_color=CAUSE, stroke_width=6).scale(0.5)
        hand = label(r"$\mathrm{do}(x)$: \ set the treatment by hand", font_size=22, color=CAUSE).next_to(g, DOWN, buff=0.4)
        bd = label(r"a back door: \\ treatment $\leftarrow$ size $\rightarrow$ success", font_size=22, color=HIDDEN)
        bd.next_to(g, UP, buff=0.3)
        rows = [
            cmath(r"P(y \mid \mathrm{do}(x))", r"=", r"\sum_z P(y \mid \mathrm{do}(x), z)\, P(z \mid \mathrm{do}(x))",
                  colors=COL, font_size=32),
            cmath(r"P(y \mid \mathrm{do}(x))", r"=", r"\sum_z P(y \mid x, z)\, P(z)", colors=COL, font_size=34),
        ]
        whys = [why(r"average over the stone size"),
                why(r"$z$ blocks the back door, \\ and the treatment can't change it")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=1.6, buff=0.7, edge=6.9)
        adj = c["adjusted"]
        res = VGroup(label(('按大小标准化后的观察成功率：' if zh() else 'size-standardized observational rates:'), font_size=22, color=GREY_A),
                     label(rf"open surgery ${100 * adj['A']:.0f}\%$, \ keyhole ${100 * adj['B']:.0f}\%$", font_size=28,
                           color=CAUSE),
                     label(('因果解释需正确因果图、无遗漏混杂，\\\\ 一致性与重叠性' if zh() else 'causal only with an adequate DAG, no omitted confounding, \\\\ consistency and overlap'),
                           font_size=17, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([2.6, -2.1, 0])
        h = history_card(2000, r"Judea Pearl", r"\textit{Causality}: \ the $\mathrm{do}$-operator, the back-door "
                         r"criterion (1993), the do-calculus (1995); \ Turing Award 2011", width=5.6).to_corner(DL, buff=0.3)
        sd = VGroup(label(r"seeing: \ $P(\text{success} \mid \text{treatment})$", font_size=26, color=GREY_A),
                    label(r"doing: \ $P(\text{success} \mid \mathrm{do}(\text{treatment}))$", font_size=26, color=CAUSE))
        sd.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.6, 1.6, 0])
        better = "open surgery" if adj["A"] > adj["B"] else "the keyhole method"
        with self.voiceover(
            "Draw where the data came from. Stone size affected which treatment doctors chose, and it affected "
            "success. <bookmark mark='a'/> So there are two paths from treatment to success: the direct one, the "
            "effect we want, and a back door through stone size, which carries the confounding. "
            "<bookmark mark='b'/> Judea Pearl's question is not 'what's the success rate among patients who got open "
            "surgery', but 'what would it be if we gave everyone open surgery': y given do x. Doing means cutting the "
            "arrows into the treatment: it's set by hand, not by the stone. <bookmark mark='c'/> And if a variable, "
            "here stone size, blocks every back door in an adequate causal graph, with no omitted confounding, "
            "the observational adjustment can identify the effect. We also need consistency, so treatment denotes "
            "the same well-defined intervention, and overlap: both treatments must be possible in each relevant "
            "size stratum. Average over size, <bookmark mark='d'/> using the success rate within each size, weighted by "
            f"how common each size is in everyone. <bookmark mark='e'/> The size-standardized kidney-stone rates favour "
            f"{better}: {100 * adj['A']:.0f} against {100 * adj['B']:.0f} percent. Reading these as causal requires "
            "those assumptions; the observational table alone cannot establish them. This is the back-door "
            "adjustment, with its identification assumptions."
        ) as vo:
            self.play(FadeIn(g), FadeIn(sd[0]))
            vo.wait_until("a")
            self.play(FadeIn(bd), Indicate(VGroup(zx, zy), color=HIDDEN))
            vo.wait_until("b")
            self.play(Create(cut), FadeIn(hand), zx.animate.set_opacity(0.25), FadeIn(sd[1]))
            vo.wait_until("c")
            self.play(FadeOut(sd))
            step(0)
            vo.wait_until("d")
            step(1)
            vo.wait_until("e")
            self.play(FadeIn(res))
            self.play(FadeIn(h, shift=UP * 0.2), FadeOut(hand))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def simulate(self):
        c = load("causal")
        vals = [("naive comparison", c["naive"], GREY_B), ("back-door adjusted", c["adjusted_sim"], CAUSE),
                ("randomized experiment", c["experiment"], SEEN)]
        g = axes([0, 3, 1], [-0.15, 0.15, 0.05], x_length=6.4, y_length=4.4, ylabel=r"effect of treatment on recovery",
                 yticks=[-0.1, 0, 0.1], yfmt=lambda v: f"{v:+.1f}" if v else "0", center=[-2.4, -0.4, 0])
        ax = g.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(3, 0), color=GREY_C, stroke_width=1.5)
        truth = DashedLine(ax.c2p(0, c["truth"]), ax.c2p(3, c["truth"]), color=C.BITS, stroke_width=2)
        tl = label(rf"the truth: \ ${c['truth']:+.2f}$", font_size=22, color=C.BITS).next_to(ax.c2p(0.05, c["truth"]), UR,
                                                                                            buff=0.06)
        bars_ = VGroup()
        for k, (nm, v, col) in enumerate(vals):
            y0, y1 = ax.c2p(k + 0.5, 0)[1], ax.c2p(k + 0.5, v)[1]
            r = Rectangle(width=1.0, height=max(abs(y1 - y0), 0.02), stroke_width=0, fill_color=col, fill_opacity=0.9)
            r.move_to([ax.c2p(k + 0.5, 0)[0], (y0 + y1) / 2, 0])
            t = label(nm, font_size=20, color=col).next_to(ax.c2p(k + 0.5, -0.15), DOWN, buff=0.15)
            num = MathTex(f"{v:+.3f}", font_size=26, color=col).next_to(r, UP if v > 0 else DOWN, buff=0.08)
            bars_.add(VGroup(r, t, num))
        story = VGroup(label(r"a world we built, so we know the truth:", font_size=22, color=GREY_A),
                       label(r"severe cases: \ half", font_size=22),
                       label(rf"treated: \ ${100 * c['treated_severe']:.0f}\%$ of them severe; \ untreated: "
                             rf"${100 * c['untreated_severe']:.0f}\%$", font_size=22),
                       label(r"treatment adds $0.10$ to recovery; \ severity takes $0.35$ away", font_size=22),
                       label(rf"${c['N']:,}$ simulated patients".replace(",", "{,}"), font_size=22, color=GREY_B))
        story.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.0, 1.4, 0])
        ladder_ = VGroup(label(r"Pearl's ladder of causation:", font_size=22, color=GREY_A),
                         label(r"1. \ seeing: \ $P(y \mid x)$", font_size=22),
                         label(r"2. \ doing: \ $P(y \mid \mathrm{do}(x))$", font_size=22, color=CAUSE),
                         label(r"3. \ imagining: \ what would have happened?", font_size=22))
        ladder_.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.0, -1.9, 0])
        flipped = c["naive"] < 0 < c["adjusted_sim"]
        verdict = (f"Compare the treated with the untreated, and the treatment looks harmful: {c['naive']:+.2f}. "
                   f"Adjust for severity through the back door: {c['adjusted_sim']:+.3f}. Now run the experiment, "
                   f"flipping a coin for every patient: {c['experiment']:+.3f}. In this specified simulation, the "
                   "known causal structure makes the adjustment comparable to the randomized experiment."
                   if flipped else
                   f"The naive comparison gives {c['naive']:+.2f}, the adjustment {c['adjusted_sim']:+.3f}, and the "
                   f"experiment {c['experiment']:+.3f}.")
        with self.voiceover(
            "To be sure, build a world where we know the truth. Half the patients are severe cases; doctors treat "
            "most of the severe ones; the treatment adds ten points to recovery, and severity takes thirty-five "
            "away. <bookmark mark='a'/> " + verdict + " <bookmark mark='b'/> Correlation is not intervention. Pearl "
            "calls it a ladder: seeing, doing, and imagining what would have happened otherwise. Randomized trials "
            "climb to the second rung by force. And part thirty climbs it inside neural networks, setting an "
            "activation by hand and watching what changes."
        ) as vo:
            self.play(FadeIn(story), FadeIn(g), Create(zero))
            vo.wait_until("a")
            for b in bars_:
                self.play(GrowFromEdge(b[0], DOWN if b[0].get_y() > ax.c2p(0, 0)[1] else UP), FadeIn(b[1]), FadeIn(b[2]),
                          run_time=1.0)
                self.wait(1.5)
            self.play(Create(truth), FadeIn(tl))
            vo.wait_until("b")
            self.play(FadeIn(ladder_))
        self.wait(0.3)
        self.clear_scene()
