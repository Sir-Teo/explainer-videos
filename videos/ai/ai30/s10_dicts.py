from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai30.common import CTRL, FEAT, PART, RESID, load, spread_bar, ticks

L1C, JRC, TKC = C.SURPRISE, C.TRUE_P, C.BITS
KINDS = (("l1", "l1s", L1C, r"L1"), ("jumprelu", "jumps", JRC, r"JumpReLU"), ("topk", "ks", TKC, r"TopK"))


def runs(o, kind, key, field):
    """[(param, [value per seed])] for one kind of autoencoder."""
    return [(p, [float(o[f"{kind}_{p:g}_{s}_{field}"]) for s in o["seeds"]]) for p in o[key]]


class Dicts(VoiceoverScene):
    def construct(self):
        self.card()
        self.shrinkage()
        self.recipes()
        self.training()
        self.frontier()
        self.downstream()
        self.dead()

    def card(self):
        card = chapter_card(9, r"Better dictionaries", r"Which sparse autoencoder, measured fairly?", part=PART)
        with self.voiceover("Chapter nine. Better dictionaries."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def shrinkage(self):
        o = load("frontier")
        rows = [
            cmath(r"\ell(f)", r"=", r"(a - f)^2 + \lambda f, \qquad f \ge 0", font_size=36),
            cmath(r"\ell'(f)", r"=", r"-2(a - f) + \lambda = 0", font_size=36),
            cmath(r"f^*", r"=", r"\max\!\big(a - \tfrac{\lambda}{2},\, 0\big)", font_size=36),
        ]
        whys = [why(r"one feature, true size $a$: \ rebuild error plus the L1 price"), why(r"set the slope to zero"),
                why(r"every active feature comes out $\lambda/2$ too small")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-2.6, buff=0.55, edge=6.8)
        sh = [np.mean(v) for _, v in runs(o, "l1", "l1s", "shrink")]
        lams = [float(p) for p in o["l1s"]]
        tab = VGroup(*[label(rf"$\lambda = {l:g}$: \ the best rescale of the rebuild is ${v:.2f}$", font_size=22,
                             color=L1C) for l, v in zip(lams, sh)]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        tab.to_edge(DOWN, buff=0.45).shift(LEFT * 2.0)
        tag = note(r"computed: \ our L1 autoencoders, \ $3$ seeds each").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Chapter eight's autoencoder paid for sparsity with an L1 penalty, and the penalty has a side effect you "
            "can derive in three lines. <bookmark mark='a'/> Take a single feature whose true size is a, and its "
            "code f: the cost is the rebuild error plus lambda times f. <bookmark mark='b'/> Set the slope to zero. "
            "<bookmark mark='c'/> The best code is a minus lambda over two: every active feature is shrunk by the "
            "same amount, so the rebuild comes out too short. <bookmark mark='d'/> Measured on ours: the factor that "
            f"would best stretch the rebuild back is {sh[0]:.2f} at the weakest penalty and {sh[-1]:.2f} at the "
            "strongest."
        ) as vo:
            step(0)
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(t) for t in tab], lag_ratio=0.3), FadeIn(tag))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recipes(self):
        colors = {r"\operatorname{TopK}_k": TKC, r"\theta": JRC, r"\lambda": L1C}
        eqs = VGroup(
            cmath(r"f = \operatorname{ReLU}(W_e x + b_e), \quad \text{loss} + ", r"\lambda", r"\|f\|_1", colors=colors, font_size=30),
            cmath(r"f = ", r"\operatorname{TopK}_k", r"\big(W_e x + b_e\big)", colors=colors, font_size=30),
            cmath(r"f_i = z_i \cdot \mathbf{1}[z_i >", r"\theta", r"_i], \quad \text{loss} + ", r"\lambda", r"\|f\|_0",
                  colors=colors, font_size=30),
        ).arrange(DOWN, buff=0.7, aligned_edge=LEFT).move_to([-3.4, 0.6, 0])
        names = VGroup(label(r"L1 \ (Bricken et al.; \ Cunningham et al., \ 2023)", font_size=19, color=L1C),
                       label(r"TopK \ (Gao et al., \ OpenAI, \ 2024): \ exactly $k$ on, \ no penalty", font_size=19,
                             color=TKC),
                       label(r"JumpReLU \ (Rajamanoharan et al., \ DeepMind, \ 2024): \ a learned threshold each",
                             font_size=19, color=JRC))
        for n_, e_ in zip(names, eqs):
            n_.next_to(e_, DOWN, buff=0.1).align_to(e_, LEFT)
        st = label(r"the step in JumpReLU has no gradient: \ it is trained \\ through a straight-through estimate with "
                   r"a narrow kernel", font_size=18, color=GREY_B).to_edge(DOWN, buff=0.4).align_to(eqs, LEFT)
        zv = [0.3, 1.4, 0.2, 0.9, 0.1, 1.8, 0.5, 0.7, 0.15, 1.1, 0.4, 0.25]
        th = [0.5, 1.0, 0.1, 1.2, 0.3, 0.6, 0.4, 0.9, 0.4, 0.6, 0.6, 0.2]
        base_y, hs = -1.0, 1.2
        zb = VGroup(*[Rectangle(width=0.3, height=v * hs, stroke_width=0, fill_color=GREY_B, fill_opacity=0.85)
                      .move_to([1.4 + 0.46 * i, base_y + v * hs / 2, 0]) for i, v in enumerate(zv)])
        zbase = Line([1.1, base_y, 0], [1.4 + 0.46 * 11 + 0.3, base_y, 0], color=GREY_C, stroke_width=1.5)
        zl = label(r"one vector's $12$ candidate features \ (schematic)", font_size=20, color=GREY_A).next_to(zbase, DOWN, buff=0.15)
        top3 = set(np.argsort(zv)[-3:].tolist())
        tkl = label(r"TopK, \ $k = 3$: \ keep the $3$ biggest", font_size=22, color=TKC).move_to([3.9, 2.0, 0])
        thl = VGroup(*[Line([b_.get_x() - 0.2, base_y + t_ * hs, 0], [b_.get_x() + 0.2, base_y + t_ * hs, 0], color=JRC,
                            stroke_width=3) for b_, t_ in zip(zb, th)])
        jrl = label(r"JumpReLU: \ a threshold line per feature", font_size=22, color=JRC).move_to([3.9, 2.0, 0])
        with self.voiceover(
            "Two fixes came in 2024. <bookmark mark='a'/> Leo Gao and colleagues at OpenAI dropped the penalty: TopK "
            "keeps each vector's k largest features and zeroes the rest, so sparsity is set directly and nothing is "
            "shrunk. They trained one with sixteen million latents on GPT-4. <bookmark mark='b'/> Senthooran "
            "Rajamanoharan and colleagues at DeepMind kept a penalty, but on the count of active features, with a "
            "learned threshold per feature: JumpReLU, the recipe behind their open Gemma Scope dictionaries. A step "
            "has no gradient, so the threshold is trained through a straight-through estimate."
        ) as vo:
            self.play(Write(eqs[0]), FadeIn(names[0]))
            vo.wait_until("a")
            self.play(Write(eqs[1]), FadeIn(names[1]), Create(zbase), FadeIn(zb), FadeIn(zl), FadeIn(tkl))
            self.play(*[b_.animate.set_fill(TKC if i in top3 else GREY_D, opacity=0.9 if i in top3 else 0.3)
                        for i, b_ in enumerate(zb)])
            vo.wait_until("b")
            self.play(Write(eqs[2]), FadeIn(names[2]), FadeIn(st))
            self.play(*[b_.animate.set_fill(GREY_B, opacity=0.85) for b_ in zb], FadeOut(tkl), FadeIn(jrl), Create(thl))
            self.play(*[b_.animate.set_fill(JRC if v > t_ else GREY_D, opacity=0.9 if v > t_ else 0.3)
                        for b_, v, t_ in zip(zb, zv, th)])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def training(self):
        """One run of each kind, at the sparsity nearest 16 features per vector: its training replayed."""
        o = load("frontier")
        picks = []
        for k, key, col, nm in KINDS:
            best = min(o[key], key=lambda q: abs(math.log(max(o[f"{k}_{q:g}_0_l0"], 1e-3)) - math.log(16)))
            picks.append((k, best, col, nm, np.asarray(o[f"{k}_{best:g}_0_curve"])))
        S = float(picks[0][4][-1, 0])
        top = float(max(min(c[:, 2].max(), 1.0) for *_, c in picks))
        g1 = axes([0, S], [0, top * 1.05], x_length=5.6, y_length=3.4, xlabel=r"training steps",
                  ylabel=r"variance left unexplained", xticks=[0, S], yticks=ticks(0, top, 3), center=[-3.3, -0.4, 0])
        l0max = float(max(c[:, 1].max() for *_, c in picks))
        g2 = axes([0, S], [0, math.log2(max(l0max, 2)) * 1.05], x_length=5.6, y_length=3.4, xlabel=r"training steps",
                  ylabel=r"features on per vector \ (log scale)", xticks=[0, S],
                  yticks=list(range(0, int(math.log2(max(l0max, 2))) + 1, 2)), yfmt=lambda v: f"{2 ** int(v)}",
                  center=[3.3, -0.4, 0])
        t = ValueTracker(0)
        cs = VGroup()
        for k, q, col, nm, c in picks:
            def mk(c=c, col=col):
                n = max(2, int(np.searchsorted(c[:, 0], t.get_value(), side="right")))
                return VGroup(curve(g1.ax, c[:n, 0], np.clip(c[:n, 2], 0, top * 1.05), col, 3),
                              curve(g2.ax, c[:n, 0], np.log2(np.clip(c[:n, 1], 1, None)), col, 3))
            cs.add(always_redraw(mk))
        lg = legend([(col, rf"{nm}, \ ${'k' if k == 'topk' else r'\lambda'} = {q:g}$") for k, q, col, nm, _ in picks],
                    font_size=18).to_edge(UP, buff=0.3)
        lg.arrange(RIGHT, buff=0.5).to_edge(UP, buff=0.3)
        with self.voiceover(
            "All three train the same way, on the same batches. <bookmark mark='a'/> Here is one run of each, the "
            "one nearest sixteen features per vector, replayed: the unexplained variance falling on the left, and "
            "on the right the number of features each vector uses. <bookmark mark='b'/> TopK holds exactly k from "
            "the first step; the penalized kinds start dense and are pruned as their penalty bites."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(lg))
            self.add(cs)
            vo.wait_until("a")
            self.play(t.animate.set_value(S * 0.3), run_time=2.5, rate_func=linear)
            vo.wait_until("b")
            self.play(t.animate.set_value(S), run_time=3, rate_func=linear)
        for c in cs:
            c.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plot(self, field, ylabel, center, ylo=None, yhi=None, x_len=6.0):
        o = load("frontier")
        pts = {k: [(np.mean(runs(o, k, key, "l0")[i][1]), runs(o, k, key, "l0")[i][1], v)
                   for i, (_, v) in enumerate(runs(o, k, key, field))] for k, key, _, _ in KINDS}
        allx = [x for k in pts for x, _, _ in pts[k] if x > 0]
        x0, x1 = math.floor(math.log2(max(min(allx), 1))), math.ceil(math.log2(max(allx)))
        ys = [y for k in pts for _, _, v in pts[k] for y in v]
        lo = ylo if ylo is not None else min(ys)
        hi = yhi if yhi is not None else max(ys)
        pad = 0.08 * (hi - lo)
        g = axes([x0, x1], [lo - pad, hi + pad], x_length=x_len, y_length=3.8, xlabel=r"features on per vector, \ $L_0$ "
                 r"\ (log scale)", ylabel=ylabel, xticks=list(range(x0, x1 + 1)), xfmt=lambda v: f"{2 ** int(v)}",
                 yticks=ticks(lo - pad, hi + pad, 3), center=center)
        curves = VGroup()
        for k, key, col, nm in KINDS:
            pp = sorted(pts[k])
            xs = [math.log2(max(x, 1e-3)) for x, _, _ in pp]
            c = curve(g.ax, xs, [np.mean(v) for _, _, v in pp], col, 3.5)
            sp = VGroup(*[spread_bar(g.ax, x_, v, col, width=0.1) for x_, (_, _, v) in zip(xs, pp)])
            curves.add(VGroup(c, sp))
        return g, curves

    def frontier(self):
        o = load("frontier")
        g, cs = self.plot("fvu", r"variance left unexplained", [-2.2, -0.3, 0])
        lg = legend([(col, nm) for _, _, col, nm in KINDS], font_size=20).to_corner(UR, buff=0.4).shift(DOWN * 0.3)
        tag = note(rf"computed: \ ${int(o['F'])}$ latents each, \ ${int(o['steps']):,}$ steps, \ the same data; \ "
                   rf"${len(o['seeds'])}$ seeds, \ min to max".replace(",", "{,}")).to_corner(DR, buff=0.2)
        at = {k: float(np.nanmean(o[f"at16_{k}_fvu"])) for k, _, _, _ in KINDS}
        order = sorted(at, key=lambda k: at[k])
        nm = {"l1": "L1", "jumprelu": "JumpReLU", "topk": "TopK"}
        tab = VGroup(*[label(rf"{nm[k]}: \ ${100 * at[k]:.0f}\%$" if np.isfinite(at[k]) else rf"{nm[k]}: \ out of range",
                             font_size=22, color=dict(l1=L1C, jumprelu=JRC, topk=TKC)[k]) for k in order])
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        th = label(r"at $16$ features per vector:", font_size=22, color=WHITE)
        box = VGroup(th, tab).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(lg, DOWN, buff=0.4).align_to(lg, LEFT)
        fin = {k: at[k] for k in at if np.isfinite(at[k])}
        best, worst = min(fin, key=fin.get), max(fin, key=fin.get)
        n_sp, n_l1 = len(o["ks"]), len(o["l1s"])
        verdict = (f"{nm[best]} leaves {100 * fin[best]:.0f} percent of the variance unexplained, {nm[worst]} "
                   f"{100 * fin[worst]:.0f}" if len(fin) >= 2 else "the kinds barely overlap in sparsity")
        with self.voiceover(
            "Now the fair test. We trained all three on the same vectors, with the same 512 latents, steps and "
            f"batches, {n_sp} sparsities for TopK, {n_l1} for the others, and three seeds each. <bookmark mark='a'/> Plot how many features each "
            "uses per vector against the variance it leaves unexplained: lower and further left is better. Pause and "
            "predict which kind wins. <bookmark mark='b'/> The L1 autoencoders, <bookmark mark='c'/> JumpReLU, <bookmark mark='d'/> and TopK. "
            f"The bars are the three seeds; they barely differ. <bookmark mark='e'/> At sixteen features per vector, "
            f"{verdict}."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            pz = pause_card(r"Same size, \ same steps: \ L1, \ JumpReLU or TopK?", width=4.4, font_size=22)
            pz.move_to([4.4, -1.6, 0])
            self.play(FadeIn(pz))
            for i, mk in enumerate("bcd"):
                if mk == "b":
                    vo.wait_until(mk)
                    self.play(FadeOut(pz), Create(cs[i][0]), FadeIn(cs[i][1]), FadeIn(lg[i]), run_time=1.3)
                    continue
                vo.wait_until(mk)
                self.play(Create(cs[i][0]), FadeIn(cs[i][1]), FadeIn(lg[i]), run_time=1.3)
            vo.wait_until("e")
            self.play(FadeIn(box))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def downstream(self):
        o = load("frontier")
        clean, mean_ = float(o["bits_clean"]), float(o["bits_mean"])
        g, cs = self.plot("bits", r"bits per character, \ the rebuild spliced in", [-2.2, -0.3, 0], ylo=clean)
        ref = DashedLine(g.ax.c2p(g.ax.x_range[0], clean), g.ax.c2p(g.ax.x_range[1], clean), color=CTRL, dash_length=0.06)
        rl = label(rf"the model itself: \ ${clean:.2f}$", font_size=18, color=CTRL).next_to(ref, UP, buff=0.05).align_to(ref, RIGHT)
        lg = legend([(col, nm) for _, _, col, nm in KINDS], font_size=20).to_corner(UR, buff=0.4).shift(DOWN * 0.3)
        at = {k: float(np.nanmean(o[f"at16_{k}_bits"])) for k, _, _, _ in KINDS}
        nm = {"l1": "L1", "jumprelu": "JumpReLU", "topk": "TopK"}
        fin = {k: at[k] for k in at if np.isfinite(at[k])}
        best = min(fin, key=fin.get) if fin else "topk"
        gap = {k: fin[k] - clean for k in fin}
        txt = label(r"\\ ".join(rf"{nm[k]}: \ ${fin[k]:.2f}$ \ (${gap[k]:+.2f}$)" for k in sorted(fin, key=fin.get)),
                    font_size=22, color=WHITE)
        box = VGroup(label(r"at $16$ features per vector:", font_size=22), txt).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        box.next_to(lg, DOWN, buff=0.4).align_to(lg, LEFT)
        with self.voiceover(
            "Variance is a proxy. What matters is whether the model still works when it runs on the dictionary's "
            "rebuild instead of its own vectors. <bookmark mark='a'/> So splice each rebuild into the transformer "
            f"after block two and measure the bits per character: {clean:.2f} for the model itself, and "
            f"{mean_:.2f} if the vectors are replaced by their average. <bookmark mark='b'/> At sixteen features "
            f"per vector, the best here is {nm[best]}, at {fin.get(best, float('nan')):.2f}. Even the best "
            "dictionary costs the model something: the part of the vector it fails to explain still mattered."
        ) as vo:
            self.play(FadeIn(g), Create(ref), FadeIn(rl), FadeIn(lg))
            vo.wait_until("a")
            self.play(*[Create(c[0]) for c in cs], *[FadeIn(c[1]) for c in cs], run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(box))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dead(self):
        o = load("frontier")
        sp = load("splitting")
        d16 = [int(o[f"topk_16_{s}_dead"]) for s in o["seeds"]]
        da = [int(o[f"topk_aux_16_{s}_dead"]) for s in o["seeds"]]
        fa = [float(o[f"topk_aux_16_{s}_fvu"]) for s in o["seeds"]]
        f16 = [float(o[f"topk_16_{s}_fvu"]) for s in o["seeds"]]
        d2048 = int(sp["2048_dead"])
        dc = definition_card(r"dead latent", r"a feature that never switches on: \ its gradient is zero, \ so it can "
                             r"never recover. \ Without fixes, \ Gao et al.\ found up to $90\%$ dead; \ with them, "
                             r"$7\%$ of $16$ million.", color=CTRL, width=6.4, font_size=21).to_corner(UL, buff=0.35)
        aux = definition_card(r"AuxK", r"an extra loss: \ the latents that have been dead for a while are asked to "
                              r"rebuild what the live ones miss, \ so they get gradient again", color=TKC, width=6.4,
                              font_size=21).next_to(dc, DOWN, buff=0.3).align_to(dc, LEFT)
        rows = VGroup(label(rf"TopK, $k = 16$, $512$ latents: \ ${', '.join(map(str, d16))}$ dead \ (3 seeds)", font_size=22, color=TKC),
                      label(rf"the same with AuxK: \ ${', '.join(map(str, da))}$ dead", font_size=22, color=TKC),
                      label(rf"TopK, $k = 16$, $2{{,}}048$ latents: \ ${d2048}$ dead", font_size=22, color=TKC))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.4, -1.0, 0])
        few = max(d16 + [d2048]) <= 5
        verdict = ("At our size almost nothing dies, so the fix has little to do here; at millions of latents it "
                   "is what keeps the dictionary alive." if few else
                   f"With AuxK, the count falls from {np.mean(d16):.0f} to {np.mean(da):.0f} on average.")
        with self.voiceover(
            "One more failure grows with size. <bookmark mark='a'/> A latent that never switches on gets no "
            "gradient, so once dead it stays dead; without fixes, Gao and colleagues found up to 90 percent of "
            "latents dead, and with them only 7 percent of their sixteen million. <bookmark mark='b'/> Their fix, AuxK, asks the dead latents to rebuild what the "
            f"live ones miss. <bookmark mark='c'/> Ours: with 512 latents and k of sixteen, {d16[0]}, {d16[1]} and "
            f"{d16[2]} dead across three seeds; with AuxK, {da[0]}, {da[1]} and {da[2]}; with 2,048 latents, "
            f"{d2048}. {verdict}"
        ) as vo:
            self.play(FadeIn(dc, shift=UP * 0.2))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(aux, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()
