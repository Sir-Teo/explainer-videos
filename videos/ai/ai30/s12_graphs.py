from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai30.common import CAUSE, CTRL, FEAT, FEATURE_COLORS, MONO, PART, RESID, load, show, ticks

PLT, CLT = C.MLP, C.BITS
OUT = C.TRUE_P


class Graphs(VoiceoverScene):
    def construct(self):
        self.card()
        self.transcoders()
        self.training()
        self.graph()
        self.check()
        self.biology()

    def card(self):
        card = chapter_card(11, r"Transcoders and attribution graphs", r"Which features made the model say that?",
                            part=PART)
        with self.voiceover("Chapter eleven. Transcoders and attribution graphs."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def transcoders(self):
        # four layers; per-layer transcoders replace each MLP; a cross-layer transcoder's features write to all later ones
        ys = [-2.4, -0.9, 0.6, 2.1]

        def column(x, cross, color, title):
            g = VGroup()
            stream = Line([x, -3.0, 0], [x, 2.8, 0], color=RESID, stroke_width=5)
            g.add(stream)
            boxes = VGroup()
            for l_, y in enumerate(ys):
                b = RoundedRectangle(width=1.6, height=0.6, corner_radius=0.1, stroke_color=color, stroke_width=2.5,
                                     fill_color=color, fill_opacity=0.12).move_to([x + 1.4, y, 0])
                boxes.add(VGroup(b, label(rf"layer ${l_ + 1}$", font_size=18, color=color).move_to(b)))
            g.add(boxes)
            wires = VGroup()
            for s in range(4):
                for t in range(s, 4):
                    if not cross and t != s:
                        continue
                    if t == s:
                        wires.add(Arrow(boxes[s].get_left(), [x, ys[s] + 0.25, 0], buff=0.02, color=color, stroke_width=2,
                                        max_tip_length_to_length_ratio=0.2))
                    else:
                        wires.add(CurvedArrow(boxes[s].get_right() + UP * 0.1, boxes[t].get_right() + DOWN * 0.1, angle=-0.9,
                                              color=color, stroke_width=1.6, tip_length=0.12))
            g.add(wires)
            g.add(label(title, font_size=22, color=color).move_to([x + 1.0, 3.25, 0]))
            return g

        a = column(-6.0, False, PLT, r"a transcoder per layer")
        b = column(-1.6, True, CLT, r"a cross-layer transcoder")
        colors = {r"u_\ell": RESID, r"f_\ell": CLT}
        eqs = VGroup(cmath(r"f_\ell = \operatorname{TopK}(W^{\mathrm{enc}}_\ell\, ", r"u_\ell", r")", colors=colors, font_size=28),
                     cmath(r"\widehat{\mathrm{MLP}}_\ell = \sum_{s \le \ell} W^{\mathrm{dec}}_{s \to \ell}\, ", r"f_s",
                           colors={r"f_s": CLT}, font_size=28)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.4, 1.2, 0])
        w = label(r"$u_\ell$: \ the MLP's input; \ trained to match the MLP's output, \\ not to rebuild its input",
                  font_size=18, color=GREY_A).next_to(eqs, DOWN, buff=0.25)
        hc = VGroup(history_card(2024, r"J.~Dunefsky, P.~Chlenski \& N.~Nanda", r"transcoders: \ a sparse stand-in for "
                                 r"an MLP", width=4.4, color=PLT, font_size=17),
                    history_card(2025, r"E.~Ameisen, J.~Lindsey et al.", r"cross-layer transcoders, \ and graphs built "
                                 r"from them", width=4.4, color=CLT, font_size=17)).arrange(DOWN, buff=0.15).move_to([4.4, -2.0, 0])
        with self.voiceover(
            "An autoencoder on the residual stream finds features, but between two of them sits an MLP, still a "
            "black box. <bookmark mark='a'/> A transcoder replaces the box. It reads the MLP's input, through a "
            "sparse code, and is trained to produce the MLP's output: a wide, sparse stand-in whose units can be "
            "read. Jacob Dunefsky, Philippe Chlenski and Neel Nanda introduced it in 2024. <bookmark mark='b'/> "
            "Anthropic's version goes further. A cross-layer transcoder's feature reads one layer and writes to the "
            "outputs of every MLP after it, because a computation spread over several layers then needs only one "
            "feature. <bookmark mark='c'/> We trained both on all four MLPs of Part 13's transformer."
        ) as vo:
            self.play(FadeIn(a[0]), FadeIn(a[1]), FadeIn(a[3]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(w_) for w_ in a[2]], lag_ratio=0.2), Write(eqs[0]), FadeIn(w))
            vo.wait_until("b")
            self.play(FadeIn(b[0]), FadeIn(b[1]), FadeIn(b[3]), Write(eqs[1]))
            self.play(LaggedStart(*[Create(w_) for w_ in b[2]], lag_ratio=0.1), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(hc))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def training(self):
        d = load("clt")
        pc, cc = np.asarray(d["plt_curve"]), np.asarray(d["clt_curve"])
        S = float(pc[-1, 0])
        top = float(min(1.0, max(pc[:, 1:].max(), cc[:, 1:].max())))
        g = axes([0, S], [0, top * 1.05], x_length=6.0, y_length=3.6, xlabel=r"training steps",
                 ylabel=r"MLP output left unexplained, \ per layer", xticks=[0, S], yticks=ticks(0, top, 3),
                 center=[-2.8, -0.2, 0])
        cs = VGroup()
        for cur, col in ((pc, PLT), (cc, CLT)):
            for l_ in range(4):
                cs.add(curve(g.ax, cur[:, 0], np.clip(cur[:, 1 + l_], 0, top * 1.05), col, 2.5).set_stroke(opacity=0.5 + 0.15 * l_))
        lg = legend([(PLT, r"per-layer transcoders"), (CLT, r"cross-layer transcoder")], font_size=20)
        lg.next_to(g, UP, buff=0.1).align_to(g, RIGHT)
        clean, mm = float(d["bits_clean"]), float(d["bits_mlp_mean"])
        pb, cb = float(d["plt_bits"]), float(d["clt_bits"])
        pa, ca = float(d["plt_agree"]), float(d["clt_agree"])
        tab = VGroup(label(r"every MLP replaced, \ bits per character:", font_size=22),
                     label(rf"the model itself: \ ${clean:.2f}$", font_size=22, color=CTRL),
                     label(rf"per-layer transcoders: \ ${pb:.2f}$ \ (same top guess ${100 * pa:.0f}\%$)", font_size=22, color=PLT),
                     label(rf"cross-layer transcoder: \ ${cb:.2f}$ \ (${100 * ca:.0f}\%$)", font_size=22, color=CLT),
                     label(rf"MLPs replaced by their average: \ ${mm:.2f}$", font_size=22, color=CTRL))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.7, -0.4, 0])
        better = cb < pb
        verdict = (f"The cross-layer transcoder does better, {cb:.2f} bits against {pb:.2f}" if better else
                   f"Here the per-layer transcoders do as well or better, {pb:.2f} bits against {cb:.2f}")
        with self.voiceover(
            f"Each was trained for {int(S):,} steps, with sixteen features on per layer, and here is each layer's "
            "unexplained share falling. <bookmark mark='a'/> The test that matters: replace every MLP with its "
            f"transcoder and let the model write. The model itself costs {clean:.2f} bits per character; with the "
            f"MLPs replaced by their average output, {mm:.2f}. <bookmark mark='b'/> {verdict}, and its top guess "
            f"matches the real model's {100 * ca:.0f} percent of the time. The gap that remains, the part no feature "
            "explains, is what Anthropic calls dark matter, and every graph has to carry it as error nodes."
        ) as vo:
            self.play(FadeIn(g), FadeIn(lg))
            self.play(*[Create(c) for c in cs], run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(tab[:2]), FadeIn(tab[4]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]), FadeIn(tab[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def layout(self, d):
        prompt = str(d["prompt"])
        T = len(prompt)
        nv = 18
        off = T - nv
        W = 12.0
        step = W / nv
        boxes = VGroup()
        for i, ch in enumerate(prompt[-nv:]):
            b = VGroup(RoundedRectangle(width=step * 0.9, height=0.45, corner_radius=0.06, stroke_color=GREY_C, stroke_width=1.2),
                       data_text(show(ch), font=MONO, font_size=20, color=GREY_A))
            b[1].move_to(b[0])
            boxes.add(b.move_to([-W / 2 + step * (i + 0.5) - 0.4, -3.1, 0]))
        return prompt, T, nv, off, step, boxes

    def graph(self):
        d = load("graph")
        prompt, T, nv, off, step, boxes = self.layout(d)
        nodes = list(d["nodes"])[:12]
        ids = [int(i) for i in d["node_ids"]][:12]
        idx = {g_: k for k, g_ in enumerate(ids)}
        li = int(d["logit_index"])
        ymap = [-2.0, -0.95, 0.1, 1.15]
        used = {}
        circles = VGroup()
        for k, n in enumerate(nodes):
            p = int(n["pos"]) - off
            x = boxes[max(p, 0)].get_x() if p >= 0 else boxes[0].get_x() - 0.6
            key = (int(n["layer"]), p)
            dx = 0.36 * used.get(key, 0)
            used[key] = used.get(key, 0) + 1
            col = FEATURE_COLORS[k % len(FEATURE_COLORS)]
            c = Circle(radius=0.17, stroke_color=col, stroke_width=2.5, fill_color=col, fill_opacity=0.3)
            c.move_to([x + dx, ymap[int(n["layer"])], 0])
            circles.add(c)
        out = VGroup(RoundedRectangle(width=0.9, height=0.6, corner_radius=0.1, stroke_color=OUT, stroke_width=3,
                                      fill_color=OUT, fill_opacity=0.2),
                     data_text(show(str(d["target"])), font=MONO, font_size=30, color=WHITE)).move_to([boxes[-1].get_x(), 2.55, 0])
        out[1].move_to(out[0])
        ol = label(rf"next: \ ${100 * float(d['p_target']):.0f}\%$", font_size=22, color=OUT).next_to(out, LEFT, buff=0.2)
        ll = VGroup(*[label(rf"layer ${l_ + 1}$", font_size=16, color=GREY_B).move_to([-6.6, y, 0]) for l_, y in enumerate(ymap)])
        edges = VGroup()
        wmax = max([abs(w) for a, b, w in d["edges"]] + [1e-9])
        for a, b, w in d["edges"]:
            a, b = int(a), int(b)
            if a not in idx or (b not in idx and b != li) or abs(w) < 0.08 * wmax:
                continue
            p0 = circles[idx[a]].get_center()
            p1 = out[0].get_bottom() if b == li else circles[idx[b]].get_center()
            edges.add(Line(p0, p1, stroke_width=0.6 + 5 * abs(w) / wmax, color=OUT if w > 0 else CAUSE).set_stroke(opacity=0.55))
        emax = max([abs(w) for _, _, w in d["emb_edges"]] + [1e-9])
        eedges = VGroup()
        for p, b, w in d["emb_edges"]:
            p, b = int(p) - off, int(b)
            if p < 0 or b not in idx or abs(w) < 0.15 * emax:
                continue
            eedges.add(Line(boxes[p].get_top(), circles[idx[b]].get_center(), stroke_width=0.5 + 3 * abs(w) / emax,
                            color=GREY_B if w > 0 else CAUSE).set_stroke(opacity=0.45))
        fe, ee, er = float(d["feat_logit"]), float(d["emb_logit"]), float(d["err_total"])
        tot = float(d["logit"])
        dec = label(rf"the logit ${tot:.2f}$ \ = \ features ${fe:+.2f}$ \ + \ inputs ${ee:+.2f}$ \ + \ errors ${er:+.2f}$ \ + \ biases",
                    font_size=20, color=GREY_A).to_edge(UP, buff=0.25).shift(LEFT * 1.2)
        tag = note(rf"computed: \ the local replacement model reproduces the logits to ${float(d['exact']):.0e}$; \ "
                   rf"${int(d['n_features'])}$ active features, \ the $12$ most influential shown").to_corner(DR, buff=0.15)
        lgd = label(r"lines: \ green raises, \ red lowers", font_size=16, color=GREY_B).next_to(tag, UP, buff=0.08).align_to(tag, RIGHT)
        with self.voiceover(
            "Now a graph for one prediction. The prompt ends 'she sai', and the model expects "
            f"'{d['target']}'. <bookmark mark='a'/> Freeze the prompt's attention patterns and layer-norm scales, "
            "replace every MLP with the cross-layer transcoder's features, and add, at each position and layer, an "
            "error term for whatever the features miss. This local replacement model reproduces the real one exactly "
            "on this prompt, and from the features onward everything in it is linear. <bookmark mark='b'/> So every "
            "path from a feature to the output can be scored: its activation times the gradient. Of the "
            f"{int(d['n_features'])} active features, here are the twelve with the most influence, by layer and "
            "position. <bookmark mark='c'/> The lines are their direct effects on each other and on the output; the "
            "grey ones below come from the input characters. <bookmark mark='d'/> And the books balance: the logit "
            f"of '{d['target']}' is {tot:.2f}, of which the features account for {fe:.2f}, the characters' own "
            f"embeddings {ee:.2f}, and the error nodes {er:.2f}."
        ) as vo:
            self.play(FadeIn(boxes), FadeIn(out), FadeIn(ol), FadeIn(ll))
            vo.wait_until("a")
            self.play(FadeIn(tag))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromCenter(c) for c in circles], lag_ratio=0.1))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.02), FadeIn(lgd), run_time=2)
            self.play(LaggedStart(*[Create(e) for e in eedges], lag_ratio=0.02), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(dec))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def check(self):
        d = load("graph")
        meas, pred = np.asarray(d["measured"]), np.asarray(d["predicted"])
        lo, hi = float(min(meas.min(), pred.min())), float(max(meas.max(), pred.max()))
        pad = 0.1 * (hi - lo + 1e-6)
        g = axes([lo - pad, hi + pad], [lo - pad, hi + pad], x_length=4.6, y_length=4.6,
                 xlabel=r"predicted by the graph", ylabel=r"measured in the real model", xticks=ticks(lo - pad, hi + pad, 3),
                 yticks=ticks(lo - pad, hi + pad, 3), center=[-2.6, -0.3, 0])
        diag = DashedLine(g.ax.c2p(lo - pad, lo - pad), g.ax.c2p(hi + pad, hi + pad), color=GREY_C, dash_length=0.06)
        dots = VGroup(*[Dot(g.ax.c2p(p, m), radius=0.07, color=FEAT) for p, m in zip(pred, meas)])
        r = float(d["corr"])
        res = label(rf"$16$ features, \ each switched off: \\ the change in the logit of `{show(str(d['target']))}' \\ "
                    rf"correlation $r = {r:.2f}$", font_size=22, color=WHITE).move_to([3.6, 0.8, 0])
        how = label(r"switched off: \ its decoder's contribution removed \\ from the real MLPs' outputs; \ attention "
                    r"and \\ everything after it recomputed", font_size=18, color=GREY_A).next_to(res, DOWN, buff=0.4)
        verdict = ("The graph predicts the real model's response well." if r > 0.8 else
                   "The graph gets the direction right more often than the size." if r > 0.4 else
                   "Here the graph is a poor guide to the real model: the frozen attention and the error terms hide too "
                   "much.")
        with self.voiceover(
            "A graph is a hypothesis about the model, so test it. <bookmark mark='a'/> Take the sixteen most "
            "influential features, and switch each one off in the real model: remove its contribution from the MLP "
            "outputs, and let attention and everything downstream recompute. <bookmark mark='b'/> Compare the "
            "change in the logit with what the graph predicted, its paths through other features included. "
            f"<bookmark mark='c'/> The correlation is {r:.2f}. {verdict}"
        ) as vo:
            self.play(FadeIn(g), Create(diag), FadeIn(how))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromCenter(d_) for d_ in dots], lag_ratio=0.08))
            vo.wait_until("c")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def biology(self):
        def nb(t, col):
            tx = label(t, font_size=22, color=col)
            r = RoundedRectangle(width=tx.width + 0.4, height=0.6, corner_radius=0.12, stroke_color=col, stroke_width=2,
                                 fill_color=col, fill_opacity=0.1)
            return VGroup(r, tx.move_to(r))

        a = nb(r"Dallas", GREY_A).move_to([-5.0, 0.6, 0])
        b = nb(r"capital", GREY_A).move_to([-5.0, -0.8, 0])
        t = nb(r"Texas", FEAT).move_to([-2.4, 0.6, 0])
        s = nb(r"say a capital", FEAT).move_to([-2.4, -0.8, 0])
        o = nb(r"Austin", OUT).move_to([0.4, -0.1, 0])
        ar = VGroup(Arrow(a.get_right(), t.get_left(), buff=0.08, color=GREY_B), Arrow(b.get_right(), s.get_left(), buff=0.08, color=GREY_B),
                    Arrow(t.get_right(), o.get_left(), buff=0.08, color=GREY_B), Arrow(s.get_right(), o.get_left(), buff=0.08, color=GREY_B))
        q = label(r"``the capital of the state containing Dallas is''", font_size=20, color=GREY_A).move_to([-2.4, 1.7, 0])
        sch = note(r"schematic, \ after Lindsey et al.\ (2025)").move_to([-2.4, -1.6, 0])
        found = VGroup(
            label(r"two steps of reasoning, \ inside: \ Dallas $\rightarrow$ Texas $\rightarrow$ Austin", font_size=20),
            label(r"planning: \ a rhyme chosen before the line that ends on it", font_size=20),
            label(r"addition by two paths: \ a rough size, \ and the last digit", font_size=20),
            label(r"language-free concepts, \ with language-specific doors", font_size=20),
            label(r"a ``known entity'' circuit that suppresses ``can't answer'': \ hallucinations when it misfires",
                  font_size=20),
            label(r"insight on about a quarter of the prompts tried", font_size=20, color=CAUSE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.9, 0.1, 0])
        if found.width > 6.0:
            found.scale_to_fit_width(6.0)
        head = label(r"On the Biology of a Large Language Model \ (Claude 3.5 Haiku, \ March 2025)", font_size=26)
        head.to_edge(UP, buff=0.3)
        with self.voiceover(
            "In March 2025 Anthropic published graphs like ours for Claude 3.5 Haiku, built from cross-layer "
            "transcoders with up to thirty million features. <bookmark mark='a'/> Asked for the capital of the state "
            "containing Dallas, the model represented Texas along the way, then the capital: two steps of reasoning "
            "inside a single forward pass. <bookmark mark='b'/> Writing a rhyming couplet, it chose the rhyme before "
            "the line that ends on it. It added numbers along two paths, a rough size and the last digit. It held "
            "concepts apart from any language, and recognized familiar names with a circuit that suppresses 'I "
            "can't answer'; when that circuit misfires, it hallucinates. <bookmark mark='c'/> The authors were "
            "candid: they got satisfying insight on about a quarter of the prompts they tried."
        ) as vo:
            self.play(FadeIn(head), FadeIn(q), FadeIn(a), FadeIn(b), FadeIn(sch))
            vo.wait_until("a")
            self.play(GrowArrow(ar[0]), FadeIn(t), GrowArrow(ar[1]), FadeIn(s))
            self.play(GrowArrow(ar[2]), GrowArrow(ar[3]), FadeIn(o))
            self.play(FadeIn(found[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(f_) for f_ in found[1:5]], lag_ratio=0.6), run_time=4)
            vo.wait_until("c")
            self.play(FadeIn(found[5]))
        self.wait(0.3)
        self.clear_scene()
