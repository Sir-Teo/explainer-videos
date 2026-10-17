from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai20.common import FEAT, FEATURE_COLORS, MONO, NEURON, RESID, context_line, load, show, vec_bars


def pick_features(feats, n=4, min_purity=0.75):
    """Clear features to show: mostly on one character, each a different character, frequent ones first."""
    out, seen = [], set()
    for f in feats:
        last = [c[-2] for c in f["contexts"]]
        top = max(set(last), key=last.count)
        if f["purity"] >= min_purity and top not in seen and top not in " \n":
            out.append((f, top))
            seen.add(top)
        if len(out) == n:
            break
    return out


class SAE(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.gallery()
        self.neurons()
        self.frontier()

    def card(self):
        card = chapter_card(2, r"Pulling the features apart", r"Can we find the directions the model uses?", part=20)
        with self.voiceover("Chapter two. Pulling the features apart."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def idea(self):
        s = load("sae")
        text = str(s["demo_text"])
        X, Fz, Xh = np.asarray(s["demo_resid"]), np.asarray(s["demo_feats"]), np.asarray(s["demo_rec"])
        k = int(np.argmax([c.isalpha() for c in text[20:]])) + 20
        W, x0 = 7.2, -2.6
        bx = vec_bars(X[k], W, 1.3, RESID).move_to([x0, 2.3, 0])
        bf = vec_bars(Fz[k], W, 1.3, FEAT, signed=False)
        bf.shift([x0 - bf.get_x(), -0.6 - bf.get_bottom()[1], 0])
        bh = vec_bars(Xh[k], W, 1.3, RESID).move_to([x0, -2.5, 0])
        bh.set_fill(opacity=0.55)
        lx = label(r"$x$: \ $128$ numbers", font_size=22, color=RESID).next_to(bx, UP, buff=0.1).align_to(bx, LEFT)
        lf = label(rf"$f$: \ $512$ features, \ ${int((Fz[k] > 0).sum())}$ on", font_size=22, color=FEAT).next_to(bf, UP, buff=0.1)
        lf.align_to(bf, LEFT)
        lh = label(r"$\hat x$: \ rebuilt", font_size=22, color=RESID).next_to(bh, UP, buff=0.1).align_to(bh, LEFT)
        a1 = Arrow(bx.get_bottom() + DOWN * 0.05, bf.get_top() + UP * 0.45, buff=0, stroke_width=3, color=GREY_B,
                   max_tip_length_to_length_ratio=0.2)
        a2 = Arrow(bf.get_bottom() + DOWN * 0.05, bh.get_top() + UP * 0.05, buff=0, stroke_width=3, color=GREY_B,
                   max_tip_length_to_length_ratio=0.2)
        el = label(r"encode", font_size=20, color=GREY_B).next_to(a1, RIGHT, buff=0.1)
        dl = label(r"decode", font_size=20, color=GREY_B).next_to(a2, RIGHT, buff=0.1)
        colors = {r"f": FEAT, r"x": RESID, r"\lambda": C.SURPRISE}
        eqs = VGroup(cmath(r"f", r" = \operatorname{ReLU}(W_e", r"x", r" + b_e)", colors=colors, font_size=32),
                     cmath(r"\hat{", r"x", r"} = \sum_k ", r"f", r"_k\, d_k + b_d", colors=colors, font_size=32),
                     cmath(r"\text{loss} = \|", r"x", r" - \hat{", r"x", r"}\|^2 + ", r"\lambda", r"\,\|", r"f", r"\|_1",
                           colors=colors, font_size=32)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.3, 1.2, 0])
        why = label(r"the $\|f\|_1$ term charges for every feature used: \\ most stay at zero", font_size=20,
                    color=GREY_A).next_to(eqs, DOWN, buff=0.3).align_to(eqs, LEFT)
        res = VGroup(label(rf"on average ${float(s['l0']):.0f}$ of $512$ on per character", font_size=24, color=FEAT),
                     label(rf"rebuilds ${100 * (1 - float(s['fvu'])):.0f}\%$ of the variance", font_size=24, color=RESID),
                     label(rf"trained on ${int(s['n_vectors']):,}$ vectors".replace(",", "{,}"), font_size=20, color=GREY_B))
        res.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(why, DOWN, buff=0.45).align_to(eqs, LEFT)
        cite_ = cite(r"T.~Bricken et al., \textit{Towards Monosemanticity} (2023); \ H.~Cunningham et al.\ (2023)", corner=DR)
        with self.voiceover(
            "If the model stores features as directions, can we find them? The tool is a sparse autoencoder. "
            "<bookmark mark='a'/> Take the model's vector x at some character, <bookmark mark='b'/> and encode it into "
            "many more numbers, five hundred and twelve, with a ReLU so they're never negative. <bookmark mark='c'/> "
            "Then rebuild x as a sum of directions, one per feature, weighted by how strongly each is on. "
            "<bookmark mark='d'/> Train it to rebuild well, while paying for every feature it uses. That penalty is "
            "the whole trick: it forces the code to be sparse, so each vector is explained by a few directions. "
            f"<bookmark mark='e'/> Trained on {int(s['n_vectors']) // 1000} thousand vectors from our transformer, "
            f"it uses about {float(s['l0']):.0f} features per character and rebuilds "
            f"{100 * (1 - float(s['fvu'])):.0f} percent of the variance."
        ) as vo:
            self.play(FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(bx), FadeIn(lx))
            vo.wait_until("b")
            self.play(GrowArrow(a1), FadeIn(el), FadeIn(eqs[0]), ReplacementTransform(bx.copy(), bf), FadeIn(lf), run_time=1.5)
            vo.wait_until("c")
            self.play(GrowArrow(a2), FadeIn(dl), FadeIn(eqs[1]), ReplacementTransform(bf.copy(), bh), FadeIn(lh), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(eqs[2]), FadeIn(why))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in res], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gallery(self):
        s = load("sae")
        feats = pick_features(s["features"])
        n_tot = len(s["features"])
        panels = VGroup()
        for j, (f, ch) in enumerate(feats):
            col = FEATURE_COLORS[j]
            head = label(rf"feature {f['id']}: \ on for ${100 * f['freq']:.1f}\%$ of characters", font_size=20, color=col)
            lines = VGroup(*[context_line(c, 5.6, font_size=18, color=col) for c in f["contexts"][:4]]).arrange(DOWN, buff=0.12)
            head.next_to(lines, UP, buff=0.15).align_to(lines, LEFT)
            panels.add(VGroup(head, lines))
        panels.arrange_in_grid(rows=2, cols=2, buff=(0.6, 0.55)).move_to(DOWN * 0.25)
        top = label(r"where each feature fires hardest: \ the lit character, \ with the text before it", font_size=24,
                    color=GREY_A).to_edge(UP, buff=0.35)
        pure = sum(1 for f in s["features"] if f["purity"] >= 0.75)
        with self.voiceover(
            "So what are the features? For each one, find where in the novels it fires hardest, and look. "
            f"<bookmark mark='a'/> Here are four. Each lights up on the same kind of moment, again and again. Of the "
            f"{n_tot} features that ever fire, {pure} put at least six of their eight strongest moments on the same "
            "character. They're not all this clean, and in a model this small they're mostly about spelling and "
            "punctuation. In big models, the same method finds features for cities, for code bugs, for flattery, for "
            "the Golden Gate Bridge."
        ) as vo:
            self.play(FadeIn(top))
            vo.wait_until("a")
            for p in panels:
                self.play(FadeIn(p[0]), LaggedStart(*[FadeIn(l_, shift=RIGHT * 0.1) for l_ in p[1]], lag_ratio=0.15), run_time=1.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def neurons(self):
        s = load("sae")
        npur, fpur = np.asarray(s["neuron_purity"]), np.asarray(s["feature_purity"])
        bins = np.arange(1, 9) / 8

        def hist(v):
            return np.array([np.mean(np.isclose(v, b)) for b in bins])

        hn, hf = hist(npur), hist(fpur)
        top = max(hn.max(), hf.max())
        ax = Axes(x_range=[0, 8, 1], y_range=[0, top * 1.1, top], x_length=6.4, y_length=3.2, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.0, -0.9, 0])
        bw = 0.3
        bn = VGroup(*[Rectangle(width=bw, height=max(v / top * 3.2 / 1.1, 0.01), stroke_width=0, fill_color=NEURON, fill_opacity=0.85)
                      .move_to(ax.c2p(i + 0.5, 0) + LEFT * 0.17, aligned_edge=DOWN) for i, v in enumerate(hn)])
        bf = VGroup(*[Rectangle(width=bw, height=max(v / top * 3.2 / 1.1, 0.01), stroke_width=0, fill_color=FEAT, fill_opacity=0.85)
                      .move_to(ax.c2p(i + 0.5, 0) + RIGHT * 0.17, aligned_edge=DOWN) for i, v in enumerate(hf)])
        xt = VGroup(*[MathTex(f"{i + 1}", font_size=22, color=GREY_B).next_to(ax.c2p(i + 0.5, 0), DOWN, buff=0.1) for i in range(8)])
        xn = label(r"of a unit's $8$ strongest moments, \ how many on its most common character", font_size=20,
                   color=GREY_A).next_to(xt, DOWN, buff=0.12)
        kn = label(rf"the model's own neurons: \ average ${8 * npur.mean():.1f}$", font_size=22, color=NEURON)
        kf = label(rf"the autoencoder's features: \ average ${8 * fpur.mean():.1f}$", font_size=22, color=FEAT)
        keys = VGroup(kn, kf).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(ax, UP, buff=0.3).align_to(ax, LEFT)
        ctx = [str(c) for c in s["neuron_contexts"]][:6]
        nl = VGroup(*[context_line(c, 5.0, font_size=17, color=NEURON) for c in ctx]).arrange(DOWN, buff=0.1).move_to([3.7, -0.6, 0])
        nh = label(rf"neuron {int(s['neuron'])}, \ a typical one: \\ its strongest moments", font_size=22, color=NEURON)
        nh.next_to(nl, UP, buff=0.2)
        better = fpur.mean() > npur.mean()
        with self.voiceover(
            "Why not just read the model's own neurons? <bookmark mark='a'/> Here's a typical one, from the second "
            "block, at its strongest moments: a mix of unrelated things. Neurons are polysemantic, because features are "
            "packed in superposition across them. <bookmark mark='b'/> Count it up: of each unit's eight strongest "
            f"moments, how many share one character? For neurons, {8 * npur.mean():.1f} on average; for the features, "
            f"{8 * fpur.mean():.1f}." + (" The autoencoder has pulled the tangle apart." if better else
                                         " In a model this small, the gap is narrow.")
        ) as vo:
            self.play(FadeIn(nh), LaggedStart(*[FadeIn(l_) for l_ in nl], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(Indicate(nl, color=NEURON, scale_factor=1.03))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(xt), FadeIn(xn))
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bn], lag_ratio=0.08), FadeIn(kn))
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bf], lag_ratio=0.08), FadeIn(kf))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def frontier(self):
        import math

        o = load("frontier")
        l1s, ks = [float(v) for v in o["l1s"]], [int(v) for v in o["ks"]]
        L1C, TKC = C.SURPRISE, FEAT
        pl = [(float(o[f"l1_{p:g}_l0"]), float(o[f"l1_{p:g}_fvu"])) for p in l1s]
        pt = [(float(o[f"topk_{k:g}_l0"]), float(o[f"topk_{k:g}_fvu"])) for k in ks]
        sl = [float(o[f"l1_{p:g}_shrink"]) for p in l1s]
        st = [float(o[f"topk_{k:g}_shrink"]) for k in ks]
        lo = min(v[0] for v in pl + pt)
        hi = max(v[0] for v in pl + pt)
        x0, x1 = math.floor(math.log2(max(lo, 1))), math.ceil(math.log2(hi))
        ytop = math.ceil(max(v[1] for v in pl + pt) * 10) / 10
        ax = CornerAxes(x_range=[x0, x1, 1], y_range=[0, ytop, 0.1], x_length=5.4, y_length=3.8, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([3.3, -0.5, 0])
        xt = VGroup(*[MathTex(str(2 ** e), font_size=20, color=GREY_B).next_to(ax.c2p(e, 0), DOWN, buff=0.08) for e in range(x0, x1 + 1)])
        yt = VGroup(*[MathTex(f"{v:.1f}", font_size=20, color=GREY_B).next_to(ax.c2p(x0, v), LEFT, buff=0.08)
                      for v in np.arange(0, ytop + 1e-9, 0.1)])
        xn = label(r"features active per vector \ (log scale)", font_size=20, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        yn = label(r"variance left unexplained", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)

        def path(pts, col):
            q = [ax.c2p(math.log2(a), b) for a, b in sorted(pts)]
            return VGroup(VMobject(color=col, stroke_width=3.5).set_points_as_corners(q), *[Dot(p, radius=0.06, color=col) for p in q])

        cl, ct = path(pl, L1C), path(pt, TKC)
        kl = VGroup(label(r"L1 penalty", font_size=22, color=L1C), label(r"TopK", font_size=22, color=TKC)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        kl.next_to(ax.c2p(x1, ytop), DL, buff=0.2)
        colors = {r"\operatorname{TopK}_k": TKC, r"\theta": C.BITS, r"\lambda": L1C}
        eqs = VGroup(
            cmath(r"f = \operatorname{ReLU}(W_e x + b_e), \quad \text{loss} + ", r"\lambda", r"\|f\|_1", colors=colors, font_size=28),
            cmath(r"f = ", r"\operatorname{TopK}_k", r"\big(W_e x + b_e\big)", colors=colors, font_size=28),
            cmath(r"f_i = z_i \cdot \mathbf{1}[z_i >", r"\theta", r"_i], \quad \text{loss} + ", r"\lambda", r"\|f\|_0", colors=colors, font_size=28),
        ).arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to([-3.6, 1.2, 0])
        names = VGroup(label(r"chapter two's: \ the penalty also shrinks every activation", font_size=18, color=L1C),
                       label(r"TopK \ (OpenAI, 2024): \ exactly $k$ features, \ no penalty", font_size=18, color=TKC),
                       label(r"JumpReLU \ (Gemma Scope, 2024): \ a learned threshold per feature", font_size=18, color=C.BITS))
        for n_, e_ in zip(names, eqs):
            n_.next_to(e_, DOWN, buff=0.08).align_to(e_, LEFT)
        shr = label(rf"rebuilds too small by: \ L1 ${100 * (np.mean(sl) - 1):.0f}\%$ \ on average, \ TopK ${100 * (np.mean(st) - 1):.0f}\%$",
                    font_size=20, color=GREY_A).move_to([-3.6, -1.6, 0])
        more = label(r"newer still: \ transcoders predict a layer's output from its input; \\ crosscoders share one dictionary "
                     r"across layers, \ or across a model before and after fine-tuning", font_size=18, color=GREY_A).move_to([-3.4, -2.6, 0])
        keep_in_frame(more)
        cite_ = cite(r"L.~Gao et al., \textit{Scaling and Evaluating Sparse Autoencoders} (2024); \ S.~Rajamanoharan et al., "
                     r"\textit{JumpReLU SAEs} (2024)", corner=UR)
        mid = [k for k in ks if 6 <= k <= 20]
        kk = mid[0] if mid else ks[1]
        l0k, fk = float(o[f"topk_{kk:g}_l0"]), float(o[f"topk_{kk:g}_fvu"])
        near = min(pl, key=lambda v: abs(math.log2(v[0]) - math.log2(l0k)))
        with self.voiceover(
            "Sparse autoencoders have moved on since the first ones, and ours used the first recipe. "
            "<bookmark mark='a'/> An L1 penalty buys sparsity, but it also pulls every active feature toward zero, so "
            "the rebuilt vector comes out too short. <bookmark mark='b'/> OpenAI's TopK autoencoders simply keep the k "
            "strongest features and zero the rest: sparsity is set directly, and nothing is shrunk. "
            "<bookmark mark='c'/> DeepMind's JumpReLU gives each feature its own threshold, learned, with the count of "
            "active features as the penalty. <bookmark mark='d'/> We trained both of the first two kinds on the same "
            "vectors, at several sparsities. "
            + (f"TopK is better at every sparsity we tried: with {l0k:.0f} features per vector it leaves "
               f"{100 * fk:.0f} percent of the variance unexplained, where the L1 model at about {near[0]:.0f} leaves "
               f"{100 * near[1]:.0f}. " if fk < near[1] else
               f"On vectors this small the two are close: about {100 * fk:.0f} against {100 * near[1]:.0f} percent "
               "unexplained at similar sparsity. ")
            + f"<bookmark mark='e'/> And the L1 rebuilds come out {100 * (np.mean(sl) - 1):.0f} percent too short on "
            "average. <bookmark mark='f'/> The newest tools go further: transcoders, which replace a whole MLP with "
            "sparse features, are what Anthropic's circuit tracing uses, and crosscoders compare two models feature "
            "by feature."
        ) as vo:
            self.play(FadeIn(cite_))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(Write(eqs[k]), FadeIn(names[k]))
            vo.wait_until("d")
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn))
            self.play(Create(cl[0]), FadeIn(cl[1:]), FadeIn(kl[0]), run_time=1.5)
            self.play(Create(ct[0]), FadeIn(ct[1:]), FadeIn(kl[1]), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(shr))
            vo.wait_until("f")
            self.play(FadeIn(more))
        self.wait(0.3)
        self.clear_scene()
