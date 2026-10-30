from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai16.common import (DENSEC, F, HISTC, MONO, PART, ROUTER, load, ms, show, take_away)

MODC = C.DEPTH


class Depth(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.cost()
        self.frontier()
        self.causal()

    def card(self):
        card = chapter_card(11, r"Mixture-of-depths", r"Does every token need every layer?", part=PART)
        with self.voiceover("Chapter eleven. Mixture-of-depths."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def idea(self):
        n, L = 12, 4
        g = np.random.default_rng(11)
        routed = {1, 3}
        cols = VGroup()
        keep = {li: set(g.choice(n, 3, replace=False)) for li in routed}
        for li in range(L):
            col = VGroup(*[Square(0.34, stroke_width=1, stroke_color=GREY_C,
                                  fill_color=MODC if (li not in routed or i in keep[li]) else GREY_D,
                                  fill_opacity=0.75 if (li not in routed or i in keep[li]) else 0.12) for i in range(n)])
            col.arrange(RIGHT, buff=0.08)
            nm = label(rf"block {li + 1}" + (r": \ routed" if li in routed else ""), font_size=20,
                       color=ROUTER if li in routed else GREY_A).next_to(col, LEFT, buff=0.3)
            cols.add(VGroup(col, nm))
        cols.arrange(UP, buff=0.35, aligned_edge=RIGHT).move_to([-1.6, -0.3, 0])
        toks = VGroup(*[data_text(ch, font=MONO, font_size=22, color=GREY_A).next_to(cols[0][0][i], DOWN, buff=0.2)
                        for i, ch in enumerate("the falcon i")])
        eq = cmath(r"x_{\ell+1}", r"=", r"x_\ell", r"+", r"\mathbf 1[\,t \in \operatorname{top}_k(r)\,]", r"\; \sigma(r_t)\,",
                   r"f_\ell(x_\ell)", colors={r"\mathbf 1[\,t \in \operatorname{top}_k(r)\,]": ROUTER,
                                               r"\; \sigma(r_t)\,": ROUTER}, font_size=32).to_edge(UP, buff=0.4)
        el = label(r"a router scores each token; \ only the top $k$ go through the block, \ the rest skip it", font_size=20,
                   color=GREY_A).next_to(eq, DOWN, buff=0.12)
        card = history_card(2024, r"David Raposo et al.\ (Google DeepMind)", r"\textit{Mixture-of-Depths}: \ best with "
                            r"$12.5\%$ of the tokens in every other block", width=4.2, color=HISTC).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Experts make the width sparse. Can the depth be sparse too? Does every token need every layer? "
            "<bookmark mark='a'/> In 2024 David Raposo and colleagues at Google DeepMind gave some blocks a router "
            "of their own. It scores every token in the sequence; only the top k go through the block, attention "
            "and feed-forward both, and the rest skip it along the residual stream. <bookmark mark='b'/> The block's "
            "output is multiplied by the router's score, so the router learns from the loss, as in a mixture of "
            "experts. <bookmark mark='c'/> They found it worked best with only an eighth of the tokens in every "
            "other block, and sampling from their models was upwards of fifty percent faster."
        ) as vo:
            self.play(FadeIn(cols), FadeIn(toks))
            vo.wait_until("a")
            self.play(Write(eq), FadeIn(el))
            vo.wait_until("b")
            self.play(Indicate(eq[4:6], color=ROUTER))
            vo.wait_until("c")
            self.play(FadeIn(card, shift=LEFT * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cost(self):
        colors = {r"c": ROUTER}
        rows = [
            cmath(r"\text{matrices}", r"\;\propto\;", r"c", r"\,T", colors=colors, font_size=36),
            cmath(r"\text{attention scores}", r"\;\propto\;", r"(", r"c", r"\,T)^2", colors=colors, font_size=36),
            cmath(r"c = \tfrac18:", r"\quad", r"\tfrac18", r"\ \text{and}\ ", r"\tfrac1{64}", colors=colors, font_size=36),
            cmath(r"\text{per token, 4 blocks}", r"\;\approx\;", r"\frac{2 + 2 \cdot \frac18}{4}", r"=", r"\frac{9}{16}",
                  font_size=36),
        ]
        whys = [why(r"the weights act on the $cT$ chosen tokens only"), why(r"the chosen attend only to each other"),
                why(r"an eighth of the matrix work, \ a sixty-fourth of the scores"),
                why(r"two full blocks, \ two at an eighth")]
        step = ladder(self, rows, whys, keep=4, top=2.4, x=-1.6, buff=0.55, edge=6.8)
        head = label(r"a routed block: \ $T$ tokens arrive, \ the router keeps a fraction $c$ of them", font_size=26,
                     color=GREY_A).to_edge(UP, buff=0.4)
        ta = take_away(r"the savings are real arithmetic \ \textemdash\ if the router's choice is cheap and causal",
                       color=ROUTER, font_size=24)
        with self.voiceover(
            "What does it save? In a routed block that takes a fraction c of the T tokens, <bookmark mark='a'/> the "
            "matrices act on only c T tokens, <bookmark mark='b'/> and attention, among the chosen tokens only, "
            "computes c T squared scores. <bookmark mark='c'/> At an eighth, that's an eighth of the matrix work and "
            "a sixty-fourth of the attention. <bookmark mark='d'/> Route every other block of four, and the "
            "matrices cost about nine sixteenths of the full model's, per token."
        ) as vo:
            self.play(FadeIn(head))
            for i, mk in enumerate("abcd"):
                vo.wait_until(mk)
                step(i)
            self.play(FadeIn(ta))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def frontier(self):
        d = load("mod")
        names = [("dense_active", r"$2$ blocks", DENSEC), ("dense_l3", r"$3$ blocks", DENSEC),
                 ("dense_l4", r"$4$ blocks", DENSEC), ("mod50", r"$4$ blocks, \ $2$ routed at $50\%$", MODC),
                 ("mod12", r"$4$ blocks, \ $2$ routed at $12.5\%$", MODC)]
        fl = {k: float(d[f"{k}_flops"]) / 1e6 for k, _, _ in names}
        vb = {k: ms(d[f"{k}_valid"]) for k, _, _ in names}
        x0, x1 = min(fl.values()) * 0.9, max(fl.values()) * 1.08
        y0 = min(v[1] for v in vb.values()) - 0.02
        y1 = max(v[2] for v in vb.values()) + 0.02
        ax = Axes(x_range=[x0, x1, 0.2], y_range=[y0, y1, 0.02], x_length=7.6, y_length=4.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-1.6, -0.3, 0])
        xt = VGroup(*[MathTex(f"{v:.1f}", font_size=20, color=GREY_B).next_to(ax.c2p(v, y0), DOWN, buff=0.1)
                      for v in np.arange(np.ceil(x0 * 5) / 5, x1, 0.2)])
        yt = VGroup(*[MathTex(f"{v:.2f}", font_size=20, color=GREY_B).next_to(ax.c2p(x0, v), LEFT, buff=0.1)
                      for v in np.arange(np.ceil(y0 * 50) / 50, y1, 0.04)])
        xl = label(r"training compute per character \ (MFLOP)", font_size=20, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yl = label(r"held-out bits \ (two seeds)", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        dense_line = curve(ax, [fl[k] for k in ("dense_active", "dense_l3", "dense_l4")],
                           [vb[k][0] for k in ("dense_active", "dense_l3", "dense_l4")], DENSEC, 2.5)
        pts = VGroup()
        for k, nm, col in names:
            p_ = ax.c2p(fl[k], vb[k][0])
            dot = Dot(p_, radius=0.08, color=col)
            er = Line(ax.c2p(fl[k], vb[k][1]), ax.c2p(fl[k], vb[k][2]), color=col, stroke_width=2)
            lab = label(nm, font_size=18, color=col)
            pts.add(VGroup(dot, er, lab))
        place_labels([p_[0] for p_ in pts], [p_[2] for p_ in pts])
        m12, m50, l3, l4, l2 = (vb[k][0] for k in ("mod12", "mod50", "dense_l3", "dense_l4", "dense_active"))
        # the dense curve's bits at the MoD model's compute (linear between neighbours)
        xs = [fl[k] for k in ("dense_active", "dense_l3", "dense_l4")]
        ys = [l2, l3, l4]
        at12 = float(np.interp(fl["mod12"], xs, ys))
        at50 = float(np.interp(fl["mod50"], xs, ys))
        if m12 < at12 - 0.003 and m50 < at50 - 0.003:
            v = (f"The routed models sit below the dense line: at the same compute, mixture-of-depths predicts better, "
                 f"{m12:.3f} bits at an eighth against {at12:.3f} for a dense model of the same compute. ")
        elif m12 < at12 - 0.003:
            v = (f"At an eighth of the tokens, the routed model sits below the dense line, {m12:.3f} bits against "
                 f"{at12:.3f} for a dense model of the same compute. ")
        elif m50 < at50 - 0.003:
            v = f"At half the tokens, the routed model sits below the dense line, {m50:.3f} against {at50:.3f}. "
        else:
            v = ("At our scale the routed models land on or above the dense line: they save compute, but they don't "
                 "beat a dense model that spends the same. ")
        w = (f"Against the full four-block model, routing an eighth of the tokens costs {m12 - l4:.3f} bits and "
             f"saves {100 * (1 - fl['mod12'] / fl['dense_l4']):.0f} percent of its compute.")
        with self.voiceover(
            "We trained it. Our four-block transformer, with blocks two and four routed, against dense models of two, "
            "three and four blocks. Compute per character on one axis, held-out bits on the other. "
            "<bookmark mark='a'/> The dense models make a line: more blocks, more compute, fewer bits. "
            "<bookmark mark='b'/> " + v + "<bookmark mark='w'/>" + w
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(dense_line), *[FadeIn(pts[i]) for i in range(3)])
            vo.wait_until("b")
            self.play(*[FadeIn(pts[i], scale=0.6) for i in (3, 4)])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def causal(self):
        d = load("mod")
        text = str(d["mod12_example"])[-32:]
        K = np.asarray(d["mod12_example_keep"], float)[:, -32:]  # routed blocks, positions (the last 32)
        row = VGroup(*[VGroup(Square(0.38, stroke_width=0.8, stroke_color=GREY_D), data_text(show(ch), font=MONO, font_size=24,
                                                                                               color=GREY_A)) for ch in text])
        for b_ in row:
            b_[1].move_to(b_[0])
        row.arrange(RIGHT, buff=0.02)
        if row.width > 13.0:
            row.width = 13.0
        rows = VGroup()
        for bi in range(K.shape[0]):
            r = row.copy()
            for j, sq in enumerate(r):
                if K[bi, j] > 0.5:
                    sq[0].set_fill(MODC, opacity=0.7)
                    sq[1].set_color(WHITE)
            rows.add(VGroup(r, label(rf"block {2 * bi + 2}", font_size=22, color=ROUTER).next_to(r, UP, buff=0.08).align_to(r, LEFT)))
        rows.arrange(DOWN, buff=0.45).move_to([0, 1.5, 0])
        cs = d["mod12_class_share"]
        share = VGroup(*[label(rf"{nm}: \ ${100 * float(cs[nm]):.0f}\%$", font_size=26, color=GREY_A) for nm in cs])
        share.arrange(RIGHT, buff=0.45).next_to(rows, DOWN, buff=0.3)
        sh_h = label(r"the share of each kind of character the routed blocks take", font_size=18, color=GREY_B).next_to(share, DOWN, buff=0.1)
        cb, cf = ms(d["mod12_valid"]), ms(d["mod12_causal"])
        frac = ms(d["mod12_causal_frac"])[0]
        cap = float(d["mod12_cap"])
        res = VGroup(
            label(r"choosing the top $12.5\%$ looks at the whole sequence, \ later tokens included", font_size=22, color=C.SURPRISE),
            label(r"writing one token at a time, \ the router must decide alone: \ $\sigma(r_t) > \tfrac12$", font_size=22, color=ROUTER),
            label(rf"held-out bits: \ ${cb[0]:.3f}$ \ choosing the top $12.5\%$, \ ${cf[0]:.3f}$ \ deciding alone, \ which "
                  rf"routes ${100 * frac:.0f}\%$", font_size=22, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.45)
        key = max(cs, key=lambda k_: float(cs[k_]))
        close = abs(cf[0] - cb[0]) < 0.02 and abs(frac - cap) < 0.08
        v = (f"Deciding alone, the router sends {100 * frac:.0f} percent of the tokens through, close to the eighth it "
             f"was trained for, and the bits barely move, {cf[0]:.3f} against {cb[0]:.3f}. " if close else
             f"Deciding alone, the router sends {100 * frac:.0f} percent of the tokens through, not the eighth it was "
             f"trained for, and the bits move from {cb[0]:.3f} to {cf[0]:.3f}: a real gap, which the paper closes with "
             "a small separate predictor trained for this. ")
        with self.voiceover(
            "Which tokens get the deep treatment? Here's one stretch of held-out text: lit, the characters the "
            "routed blocks process. <bookmark mark='a'/> " + f"The router favours {key}: it takes "
            f"{100 * float(cs[key]):.0f} percent of them. <bookmark mark='b'/> But there's a catch. Choosing the top "
            "eighth of a sequence means looking at the whole sequence, later tokens included, which a model writing "
            "one token at a time can't do. The paper trains the router to predict its own top-k choice, with an "
            "extra loss, so that at generation it can decide alone. <bookmark mark='c'/> " + v
        ) as vo:
            self.play(FadeIn(rows))
            vo.wait_until("a")
            self.play(FadeIn(share), FadeIn(sh_h))
            vo.wait_until("b")
            self.play(FadeOut(share), FadeOut(sh_h), FadeIn(res[:2]))
            vo.wait_until("c")
            self.play(FadeIn(res[2]))
        self.wait(0.3)
        self.clear_scene()
