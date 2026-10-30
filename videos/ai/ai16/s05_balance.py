from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai16.common import (BALC, EXPERT_COLORS, MODE_COLOR, PART, ROUTER, load, load_image, ms, take_away)


def loads_panel(b, mode, seed, layer, width, height, title, color):
    L = np.asarray(b[f"{mode}_loads"], float)[seed, :, layer]  # time, E
    img = load_image(L, width, height, E=L.shape[1])
    frame = SurroundingRectangle(img, buff=0, color=GREY_D, stroke_width=1.5)
    t = label(title, font_size=22, color=color).next_to(img, UP, buff=0.12)
    el = label(rf"${L.shape[1]}$ experts", font_size=16, color=GREY_B).rotate(PI / 2).next_to(img, LEFT, buff=0.08)
    tl = label(r"training $\to$", font_size=16, color=GREY_B).next_to(img, DOWN, buff=0.06)
    return Group(img, frame, t, el, tl)


class Balance(VoiceoverScene):
    def construct(self):
        self.card()
        self.collapse()
        self.importance()
        self.derive()
        self.result()

    def card(self):
        card = chapter_card(4, r"Collapse, and Switch's loss", r"What stops the router from playing favourites?", part=PART)
        with self.voiceover("Chapter four. Collapse, and Switch's loss."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def collapse(self):
        b = load("balance")
        busy = np.asarray(b["none_busiest"], float)  # seeds, layers
        starved = np.asarray(b["none_starved"], int)
        s0 = int(np.argmax(busy.max(1)))  # show the seed whose router collapsed furthest (said)
        panels = Group(*[loads_panel(b, "none", s0, li, 4.6, 2.0, rf"block {li + 1}", MODE_COLOR["none"])
                         for li in range(busy.shape[1])]).arrange(DOWN, buff=0.55).move_to([-3.2, -0.2, 0])
        head = label(r"the mixture trained without balancing: \ each expert's share of the tokens", font_size=26)
        head.to_edge(UP, buff=0.3)
        expl = label(r"bright: \ more than its fair share \ ($1/8$); \\ dark: \ starved", font_size=22, color=GREY_A)
        expl.move_to([3.4, 1.6, 0])
        loop = VGroup(*[label(t, font_size=22, color=c) for t, c in (
            (r"chosen more", ROUTER), (r"trained more", C.EXPERT), (r"better", C.BITS), (r"chosen even more", ROUTER))])
        loop.arrange(DOWN, buff=0.35).move_to([3.4, -0.6, 0])
        arrs = VGroup(*[Arrow(loop[i].get_bottom(), loop[i + 1].get_top(), buff=0.06, stroke_width=2.5, color=GREY_B,
                              max_tip_length_to_length_ratio=0.25) for i in range(3)])
        mb = float(busy.mean())
        worst = float(busy.max())
        ns = int(starved.sum())
        collapsed = worst > 2.0 or ns > 0
        verdict = (f"Left alone, the router plays favourites. In the worst of three seeds, shown here, the busiest "
                   f"expert ends with {worst:.1f} times its fair share; across the three seeds and both blocks, "
                   f"{ns} experts end up with less than a quarter of theirs. " if collapsed else
                   f"In our small model the router stays fairly even on its own: the busiest expert ends at "
                   f"{worst:.1f} times a fair share at worst. Big models are less lucky. ")
        tag = note(rf"computed; \ seed {s0 + 1} of $3$", font_size=18).to_corner(DR, buff=0.25)
        with self.voiceover(
            "A router learns only from the experts it tries. So what happens to the ones it stops trying? Train our "
            "mixture with no help, and watch how the tokens are shared out. <bookmark mark='a'/> " + verdict
            + "<bookmark mark='b'/> It's a rich-get-richer loop: an expert that's chosen more is trained more, gets "
            "better, and is chosen even more; a starved expert stops learning, and its parameters are wasted. Shazeer "
            "saw it in 2017, and called it a self-reinforcing imbalance."
        ) as vo:
            self.play(FadeIn(head), FadeIn(expl), FadeIn(tag))
            covers = []
            for p in panels:
                img = p[0]
                cv = Rectangle(width=img.width + 0.02, height=img.height + 0.02, stroke_width=0, fill_color="#121722",
                               fill_opacity=1).move_to(img)
                covers.append(cv)
                self.add(img, cv, p[1])
            self.play(*[FadeIn(Group(*p[2:])) for p in panels])
            u = ValueTracker(0.0)
            for p, cv in zip(panels, covers):
                cv.add_updater(lambda c_, img=p[0]: c_.stretch_to_fit_width(max((img.width + 0.02) * (1 - u.get_value()), 1e-3))
                               .move_to(img.get_right() + RIGHT * 0.01, aligned_edge=RIGHT))
            self.play(u.animate.set_value(1.0), run_time=4.0, rate_func=linear)
            for cv in covers:
                cv.clear_updaters()
                self.remove(cv)
            vo.wait_until("a")
            self.play(*[Indicate(p[0], scale_factor=1.0) for p in panels])
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(l_) for l_ in loop], *[GrowArrow(a_) for a_ in arrs], lag_ratio=0.25), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def importance(self):
        b = load("balance")
        busy = np.asarray(b["none_busiest"], float)
        s0 = int(np.argmax(busy.max(1)))
        L = np.asarray(b["none_loads"], float)[s0, -10:, 0].mean(0)  # the shown seed's block 1, the last 200 steps
        cv = float(L.std() / L.mean())
        colors = {r"\mathrm{Imp}_i": C.ROUTER}
        f1 = cmath(r"\mathrm{Imp}_i", r"= \sum_{x \in \text{batch}} g_i(x)", colors=colors, font_size=34)
        f2 = cmath(r"\mathcal L_{\text{imp}}", r"= w \cdot \operatorname{CV}\big(", r"\mathrm{Imp}", r"\big)^2",
                   r",\qquad \operatorname{CV} = \frac{\text{standard deviation}}{\text{mean}}", font_size=34)
        eqs = VGroup(f1, f2).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([-2.6, 1.6, 0])
        bars = VGroup(*[Rectangle(width=0.45, height=max(2.4 * v / L.max(), 0.02), stroke_width=0, fill_color=EXPERT_COLORS[i],
                                  fill_opacity=0.85) for i, v in enumerate(L)]).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
        bars.move_to([-2.6, -1.4, 0])
        base = Line(bars.get_corner(DL) + LEFT * 0.1, bars.get_corner(DR) + RIGHT * 0.1, color=GREY_C)
        mean_l = DashedLine(base.get_left() + UP * 2.4 * L.mean() / L.max(), base.get_right() + UP * 2.4 * L.mean() / L.max(),
                            color=GREY_B, stroke_width=1.5)
        bl = label(rf"our unbalanced router, \ block 1: \ $\operatorname{{CV}} = {cv:.2f}$", font_size=22, color=C.SURPRISE)
        bl.next_to(base, DOWN, buff=0.2)
        card = history_card(2017, r"Shazeer et al.", r"two extra losses: \ one on each expert's total gate weight, \ "
                            r"one on its expected number of tokens", width=4.6, color=C.HUMAN).move_to([4.2, 1.2, 0])
        pc = pause_card(r"Why penalize the coefficient of variation, \ and not the variance?", width=4.8, font_size=22)
        pc.move_to([4.2, -1.6, 0])
        with self.voiceover(
            "Shazeer's team met this in 2017 and added losses to fight it. <bookmark mark='a'/> The first: add up "
            "each expert's gate values over the batch, its importance, and penalize the squared coefficient of "
            "variation of those totals, the standard deviation divided by the mean. It's zero only when every "
            "expert is equally important. <bookmark mark='b'/> For our unbalanced router, measured on its token "
            f"shares, the coefficient of variation is {cv:.2f}. <bookmark mark='c'/> Pause and think: why divide "
            "by the mean? Because then the penalty doesn't care about the overall scale of the gates, only about "
            "how unevenly they're spread. A second loss balanced the expected number of tokens, since equal "
            "importance can still hide unequal counts."
        ) as vo:
            self.play(Write(eqs[0]), FadeIn(card, shift=LEFT * 0.2))
            vo.wait_until("a")
            self.play(Write(eqs[1]))
            vo.wait_until("b")
            self.play(Create(base), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.1), Create(mean_l),
                      FadeIn(bl))
            vo.wait_until("c")
            self.play(FadeIn(pc, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        colors = {r"f_i": BALC, r"P_i": ROUTER, r"\alpha": C.BITS}
        rows = [
            cmath(r"f_i", r"=", r"\frac{1}{kN}\sum_{t=1}^{N} \mathbf 1\big[\,i \in \mathcal K_t\big]", colors=colors, font_size=34),
            cmath(r"P_i", r"=", r"\frac1N \sum_{t=1}^{N} p_i(x_t)", colors=colors, font_size=34),
            cmath(r"\mathcal L_{\text{aux}}", r"=", r"\alpha", r"\, E \sum_{i=1}^{E}", r"f_i", r"\,", r"P_i", colors=colors,
                  font_size=34),
            cmath(r"f = P:\quad", r"E \sum_i", r"f_i", r"^2", r"\;\ge\;", r"1", colors=colors, font_size=34),
            cmath(r"\frac{\partial \mathcal L_{\text{aux}}}{\partial", r"P_i", r"}", r"=", r"\alpha", r"\, E\,", r"f_i",
                  colors=colors, font_size=34),
        ]
        whys = [why(r"the share of token-slots sent to $i$: \ counted, \ no gradient"),
                why(r"its mean router probability: \ differentiable"),
                why(r"Switch Transformer (2021); \ $\alpha = 0.01$"),
                why(r"Cauchy--Schwarz: \ equal only when every $f_i = 1/E$"),
                why(r"the busier the expert, \ the harder its probability is pushed down")]
        step = ladder(self, rows, whys, keep=5, top=3.1, x=-3.0, buff=0.34, edge=6.8)
        cite_ = cite(r"W.~Fedus, B.~Zoph \& N.~Shazeer (2021); \ D.~Lepikhin et al., \textit{GShard} (2020)", corner=DL)
        zl = VGroup(label(r"ST-MoE (2022) adds a router $z$-loss: \ keep the scores small", font_size=22, color=GREY_A),
                    cmath(r"\mathcal L_z = \frac1N \sum_t \Big(\log \sum_{j} e^{s_{tj}}\Big)^2", font_size=30)).arrange(RIGHT, buff=0.4)
        zl.to_edge(DOWN, buff=0.85)
        with self.voiceover(
            "The classic fix adds a penalty to the loss. Two numbers per expert. <bookmark mark='a'/> f i, the share "
            "of the batch's token slots actually sent to expert i: a count, so it has no gradient. "
            "<bookmark mark='b'/> P i, the router's average probability for expert i: that one is differentiable. "
            "<bookmark mark='c'/> The Switch Transformer's penalty is alpha times E times the sum of f i times P i, "
            "with alpha a hundredth. <bookmark mark='d'/> Why that product? If the router's probabilities match "
            "where tokens go, it's E times the sum of f i squared, which by Cauchy-Schwarz is at least one, with "
            "equality only when every expert gets one E-th. <bookmark mark='e'/> And its gradient pushes each "
            "expert's probability down in proportion to how busy that expert already is: the favourites get pushed "
            "hardest. <bookmark mark='f'/> GShard had used a similar penalty a year earlier, and in 2022 ST-MoE "
            "added a second, the z-loss, which keeps the router's scores from growing huge."
        ) as vo:
            self.play(FadeIn(cite_))
            for i, mk in enumerate("abcde"):
                vo.wait_until(mk)
                step(i)
            vo.wait_until("f")
            self.play(FadeIn(zl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def result(self):
        b = load("balance")
        bn, ba = np.asarray(b["none_busiest"], float), np.asarray(b["aux_busiest"], float)
        sn, sa = np.asarray(b["none_starved"], int), np.asarray(b["aux_starved"], int)
        s_show = int(np.argmax(bn.max(1)))
        pn = Group(*[loads_panel(b, "none", s_show, li, 3.6, 1.5, rf"no balancing, \ block {li + 1}", MODE_COLOR["none"])
                     for li in range(bn.shape[1])]).arrange(DOWN, buff=0.45)
        pa = Group(*[loads_panel(b, "aux", s_show, li, 3.6, 1.5, rf"Switch's loss, \ block {li + 1}", MODE_COLOR["aux"])
                     for li in range(ba.shape[1])]).arrange(DOWN, buff=0.45)
        Group(pn, pa).arrange(RIGHT, buff=0.9).move_to([-1.9, -0.1, 0])
        vn, va = ms(b["none_valid"]), ms(b["aux_valid"])
        stats = VGroup(
            label(r"at the end, \ three seeds, \ both blocks:", font_size=22, color=GREY_A),
            label(rf"busiest expert: \ ${bn.mean():.1f}\times$ \ vs.\ ${ba.mean():.1f}\times$ a fair share", font_size=22,
                  color=WHITE),
            label(rf"starved \ ($<\tfrac14$ share): \ ${int(sn.sum())}$ \ vs.\ ${int(sa.sum())}$ experts", font_size=22,
                  color=WHITE),
            label(rf"held-out bits: \ ${vn[0]:.3f}$ \ vs.\ ${va[0]:.3f}$", font_size=22, color=C.BITS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.6, 0.4, 0])
        keep_in_frame(stats)
        evened = ba.mean() < bn.mean() - 0.3
        better = va[0] < vn[0] - 0.003
        worse = va[0] > vn[0] + 0.003
        if evened and sn.sum() > sa.sum():
            v1 = (f"With Switch's penalty at its usual strength, the busiest expert falls from {bn.mean():.1f} to "
                  f"{ba.mean():.1f} times a fair share, on average over seeds and blocks, and the starved experts from "
                  f"{int(sn.sum())} to {int(sa.sum())}. ")
        elif evened:
            v1 = (f"With Switch's penalty at its usual strength, the busiest expert falls from {bn.mean():.1f} to "
                  f"{ba.mean():.1f} times a fair share, on average over seeds and blocks. ")
        else:
            v1 = (f"With Switch's penalty at its usual strength, the loads barely change: the busiest expert goes from "
                  f"{bn.mean():.1f} to {ba.mean():.1f} times a fair share. ")
        if better:
            v2 = (f"And the model is better for it: {va[0]:.3f} bits against {vn[0]:.3f}, because experts that work are "
                  "experts that learn. ")
        elif worse:
            v2 = f"But the model is no better for it: {va[0]:.3f} bits against {vn[0]:.3f}. "
        else:
            v2 = f"In held-out bits it makes little difference here: {va[0]:.3f} against {vn[0]:.3f}. "
        ta = take_away(r"the penalty is a second goal competing with the first: \ too weak, \ collapse; \ too strong, "
                       r"\ it bends the routing away from what's best", color=BALC, font_size=24)
        with self.voiceover(
            "Here is our mixture again, the same seed, trained with and without the penalty. <bookmark mark='a'/> "
            + v1 + "<bookmark mark='b'/> " + v2 + "<bookmark mark='c'/> But the penalty is a second goal, competing "
            "with the first. Make alpha too small and the router collapses; make it too big and it bends the routing "
            "away from what predicts best. The next chapter removes the trade-off."
        ) as vo:
            self.play(FadeIn(pn), FadeIn(pa))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in stats[:3]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(stats[3]))
            vo.wait_until("c")
            self.play(FadeIn(ta))
        self.wait(0.3)
        self.clear_scene()
