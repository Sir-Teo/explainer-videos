from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai30.common import CTRL, FEAT, PART, PROBE, context_line, load, spread_bar

TKC, MAT = C.BITS, C.MLP


def feature_panel(f, width, color, n=3, font_size=15, head=None):
    lines = VGroup(*[context_line(c, width, font_size=font_size, color=color) for c in f["contexts"][:n]])
    lines.arrange(DOWN, buff=0.06)
    t = label(head or rf"latent {f['id']}", font_size=16, color=color).next_to(lines, UP, buff=0.08).align_to(lines, LEFT)
    return VGroup(t, lines)


class Splitting(VoiceoverScene):
    def construct(self):
        self.card()
        self.splitting()
        self.absorption()
        self.matryoshka()

    def card(self):
        card = chapter_card(10, r"Splitting and absorption", r"Are the features really there, or made by the dictionary?",
                            part=PART)
        with self.voiceover("Chapter ten. Splitting and absorption."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def splitting(self):
        sp = load("splitting")
        par = sp["parent"]
        mid, big = list(sp["mid"]), list(sp["big"])
        sizes = [int(v) for v in sp["sizes"]]
        p0 = feature_panel(par, 3.6, FEAT, n=4, head=rf"${sizes[0]}$ latents: \ latent {par['id']}").move_to([-4.6, 0.2, 0])
        pm = VGroup(*[feature_panel(f, 3.4, FEAT, n=2, head=rf"cos ${f['cos']:.2f}$") for f in mid[:3]]).arrange(DOWN, buff=0.25)
        pm.move_to([-0.3, 0.2, 0])
        pb = VGroup(*[feature_panel(f, 3.4, FEAT, n=2, head=rf"cos ${f['cos']:.2f}$") for f in big[:4]]).arrange(DOWN, buff=0.2)
        pb.move_to([4.4, 0.0, 0])
        if pb.height > 6.4:
            pb.scale_to_fit_height(6.4)
        hm = label(rf"${sizes[1]}$ latents", font_size=22, color=WHITE).next_to(pm, UP, buff=0.2)
        hb = label(rf"${sizes[2]:,}$ latents".replace(",", "{,}"), font_size=22, color=WHITE).next_to(pb, UP, buff=0.15)
        ar1 = Arrow(p0.get_right(), pm.get_left(), buff=0.15, color=GREY_B, stroke_width=3)
        ar2 = Arrow(pm.get_right(), pb.get_left(), buff=0.15, color=GREY_B, stroke_width=3)
        whole = VGroup(p0, pm, pb, ar1, ar2, hm, hb)
        f_ = min(13.4 / whole.width, 6.2 / whole.height)
        whole.scale(f_).move_to(DOWN * 0.15)
        nf, ncand = int(sp["n_same_char_families"]), int(sp["n_candidates"])
        tag = note(r"TopK, $k = 16$; \ the same data and steps; \ children: \ decoder cosine above $0.4$, \ the same character").to_corner(DR, buff=0.2)
        cite_ = cite(r"Bricken et al., \textit{Towards Monosemanticity} (2023): \ feature splitting", corner=UL)
        with self.voiceover(
            "How many features does a model have? The dictionary seems to decide. <bookmark mark='a'/> Train TopK "
            f"dictionaries of {sizes[0]}, {sizes[1]} and {sizes[2]:,} latents on the same vectors. Here is one latent "
            "of the smallest, at its strongest moments. <bookmark mark='b'/> In the next size up, the latents "
            f"pointing nearly the same way and firing on the same character: {len(mid)} of them, "
            f"<bookmark mark='c'/> and in the largest, {len(big)}, each on a narrower slice of the same moments. "
            "Bricken and colleagues called it feature splitting. Of the smallest dictionary's "
            f"{ncand} clean latents, {nf} have two or more such children in the largest."
        ) as vo:
            self.play(FadeIn(cite_), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(p0))
            vo.wait_until("b")
            self.play(GrowArrow(ar1), FadeIn(hm), LaggedStart(*[FadeIn(p) for p in pm], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(GrowArrow(ar2), FadeIn(hb), LaggedStart(*[FadeIn(p) for p in pb], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def absorption(self):
        a = load("absorption")
        seeds = [int(s) for s in a["seeds"]]
        rec = [float(a[f"topk_{s}_recall"]) for s in seeds]
        ab = [float(a[f"topk_{s}_absorption"]) for s in seeds]
        mbc = a["topk_0_miss_by_char"]
        chars = sorted(mbc, key=lambda c: -mbc[c])[:10]
        dc = definition_card(r"feature absorption", r"a general feature (\textit{upper case}) stays silent where a "
                             r"specific one (\textit{this letter}) fires and carries its direction instead: \ sparsity "
                             r"rewards one latent over two", color=CTRL, width=6.4, font_size=20).to_corner(UL, buff=0.3)
        hc = note(r"D.~Chanin et al., \textit{A is for Absorption} (2024)").next_to(dc, DOWN, buff=0.12).align_to(dc, LEFT)
        g = axes([0, len(chars)], [0, 1], x_length=5.6, y_length=2.6, ylabel=r"silent on it", yticks=[0, 0.5, 1],
                 center=[3.3, -1.5, 0])
        bs = VGroup()
        for i, c in enumerate(chars):
            v = float(mbc[c])
            r = Rectangle(width=0.35, height=max(v * 2.6, 0.01), stroke_width=0, fill_color=CTRL, fill_opacity=0.9)
            r.move_to(g.ax.c2p(i + 0.5, 0), aligned_edge=DOWN)
            bs.add(VGroup(r, data_text(c, font="DejaVu Sans Mono", font_size=20, color=WHITE).next_to(r, DOWN, buff=0.08)))
        gl = label(r"the main latent, \ letter by letter", font_size=20, color=GREY_A).next_to(g, UP, buff=0.15)
        res = label(rf"a probe reads \textit{{upper case}} at ${100 * float(a['probe_acc']):.0f}\%$ \\ the dictionary's best "
                    rf"latent for it fires on ${100 * np.mean(rec):.0f}\%$ of capitals \\ absorbed: \ ${100 * np.mean(ab):.0f}\%$ "
                    r"of capitals \ (mean of $3$ seeds)", font_size=20, color=WHITE).move_to([-3.2, -1.6, 0])
        def bubble(t, col, op):
            c = Circle(radius=0.75, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.15 * op)
            return VGroup(c, label(t, font_size=22, color=col).move_to(c)).set_opacity(op)

        gen = bubble(r"upper \\ case", GREY_B, 0.35).move_to([1.6, -1.2, 0])
        spec = bubble(r"capital \\ T", C.BITS, 1.0).move_to([4.4, -1.2, 0])
        word = data_text("The", font="DejaVu Sans Mono", font_size=40, color=WHITE).move_to([3.0, 1.2, 0])
        lt = Arrow(word.get_bottom(), spec.get_top(), buff=0.1, color=C.BITS, stroke_width=3)
        lg_ = DashedLine(word.get_bottom(), gen.get_top(), color=GREY_C, dash_length=0.08)
        abl = label(r"fires, \ and carries \\ the upper-case direction", font_size=18, color=C.BITS).next_to(spec, DOWN, buff=0.2)
        si = label(r"silent", font_size=18, color=GREY_B).next_to(gen, DOWN, buff=0.2)
        sch = VGroup(gen, spec, word, lt, lg_, abl, si)
        sch_tag = note(r"schematic").next_to(sch, RIGHT, buff=0.3).align_to(sch, DOWN)
        with self.voiceover(
            "Splitting has a nastier cousin. <bookmark mark='a'/> Some features are general, like 'this is a "
            "capital letter'; some are specific, like 'this is a capital T'. A sparse dictionary would rather use "
            "one latent than two, so where the specific one fires, it can soak up the general one's direction, and "
            "the general latent stays silent. David Chanin and colleagues named it absorption. "
            f"<bookmark mark='b'/> Measure it. A linear probe reads upper case off our vectors with "
            f"{100 * float(a['probe_acc']):.0f} percent accuracy. The dictionary's best latent for it fires on only "
            f"{100 * np.mean(rec):.0f} percent of capitals, <bookmark mark='c'/> and it is silent on some letters "
            f"far more than others. On {100 * np.mean(ab):.0f} percent of capitals, another latent carries most of "
            "the upper-case direction instead. A feature that seems to mean upper case does not fire on all of it."
        ) as vo:
            self.play(FadeIn(dc), FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(word), GrowArrow(lt), FadeIn(spec), Create(lg_), FadeIn(gen), FadeIn(sch_tag))
            self.play(FadeIn(abl), FadeIn(si))
            vo.wait_until("b")
            self.play(FadeOut(sch), FadeOut(sch_tag))
            self.play(FadeIn(res))
            vo.wait_until("c")
            self.play(FadeIn(g), FadeIn(gl), LaggedStart(*[GrowFromEdge(b[0], DOWN) for b in bs], lag_ratio=0.1),
                      FadeIn(VGroup(*[b[1] for b in bs])))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def matryoshka(self):
        a = load("absorption")
        seeds = [int(s) for s in a["seeds"]]
        pre = [int(p) for p in a["prefixes"]]
        F = int(a["F"])
        colors = {r"\hat x_{1:m}": MAT}
        f = cmath(r"\text{loss} = \frac{1}{|M| + 1}\Big(\|x - \hat x\|^2 + \sum_{m \in M} \|x - ", r"\hat x_{1:m}", r"\|^2\Big)",
                  colors=colors, font_size=32).to_edge(UP, buff=0.45)
        w = label(rf"$\hat x_{{1:m}}$: \ the rebuild from the first $m$ latents only; \ $M = \{{{', '.join(map(str, pre))}\}}$ "
                  rf"of ${F}$", font_size=20, color=GREY_A).next_to(f, DOWN, buff=0.15)
        # nested boxes: the first m latents must work alone
        nest = VGroup()
        for i, m in enumerate(pre + [F]):
            wdt = 1.2 + 1.2 * i
            nest.add(RoundedRectangle(width=wdt, height=0.5 + 0.35 * i, corner_radius=0.08, stroke_color=MAT,
                                      stroke_width=2, fill_opacity=0).move_to([-6.3 + wdt / 2, -0.9, 0]))
            nest.add(MathTex(str(m), font_size=20, color=MAT).next_to(nest[-1], UP, buff=0.04).align_to(nest[-1], RIGHT))
        stats = {}
        for kind in ("topk", "matryoshka"):
            stats[kind] = dict(rec=[float(a[f"{kind}_{s}_recall"]) for s in seeds],
                               ab=[float(a[f"{kind}_{s}_absorption"]) for s in seeds],
                               fvu=[float(a[f"{kind}_{s}_fvu"]) for s in seeds])
        g = axes([0, 3], [0, 1], x_length=6.0, y_length=3.0, yticks=[0, 0.5, 1], center=[3.0, -1.0, 0])
        nl = label(r"the first $32$ latents must work alone, \\ then the first $128$, \ then all", font_size=18,
                   color=MAT).move_to([-4.5, -2.6, 0])
        cols = {"topk": TKC, "matryoshka": MAT}
        marks = VGroup()
        for j, (key, nm) in enumerate((("rec", r"fires on capitals"), ("ab", r"capitals absorbed"),
                                       ("fvu", r"variance left"))):
            for dx, kind in ((-0.15, "topk"), (0.15, "matryoshka")):
                marks.add(spread_bar(g.ax, j + 0.5 + dx, stats[kind][key], cols[kind]))
            marks.add(label(nm, font_size=18, color=GREY_A).next_to(g.ax.c2p(j + 0.5, 0), DOWN, buff=0.15))
        lg = legend([(TKC, r"TopK"), (MAT, r"Matryoshka")], font_size=20).next_to(g, UP, buff=0.15).align_to(g, RIGHT)
        cite_ = cite(r"Bussmann et al.\ (2025); \ Nabeshima (2024)", corner=DL)
        r_t, r_m = np.mean(stats["topk"]["rec"]), np.mean(stats["matryoshka"]["rec"])
        a_t, a_m = np.mean(stats["topk"]["ab"]), np.mean(stats["matryoshka"]["ab"])
        f_t, f_m = np.mean(stats["topk"]["fvu"]), np.mean(stats["matryoshka"]["fvu"])
        if r_m > r_t and a_m <= a_t:
            verdict = (f"It helps here: the best upper-case latent fires on {100 * r_m:.0f} percent of capitals "
                       f"instead of {100 * r_t:.0f}, and absorption goes from {100 * a_t:.0f} to {100 * a_m:.0f} percent")
        elif abs(r_m - r_t) < 0.05 and abs(a_m - a_t) < 0.05:
            verdict = (f"Here the difference is small: recall {100 * r_m:.0f} against {100 * r_t:.0f} percent, "
                       f"absorption {100 * a_m:.0f} against {100 * a_t:.0f}")
        else:
            verdict = (f"Here it does not help: the best upper-case latent fires on {100 * r_m:.0f} percent of capitals "
                       f"against TopK's {100 * r_t:.0f}, and absorption is {100 * a_m:.0f} percent against "
                       f"{100 * a_t:.0f}, with a wide spread across seeds. A cure tested on large models need not work "
                       "on a small one, or on this kind of hierarchy")
        with self.voiceover(
            "One proposed cure came in 2025 from Bart Bussmann and colleagues, and independently from Noa "
            "Nabeshima: Matryoshka dictionaries, named after the nesting dolls. <bookmark mark='a'/> The first few "
            "latents must rebuild the vector on their own, then the first few hundred, then all of them. The early "
            "latents are pushed to be general, and the later ones refine them, so the general ones have less reason "
            "to stay silent. <bookmark mark='b'/> We trained both kinds, with the same size, k and steps, three seeds "
            f"each. <bookmark mark='c'/> {verdict}; the price is a little more variance left, {100 * f_m:.0f} percent "
            f"against {100 * f_t:.0f}."
        ) as vo:
            self.play(Write(f), FadeIn(w), FadeIn(cite_))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(n_) for n_ in nest], lag_ratio=0.3), FadeIn(nl))
            vo.wait_until("b")
            self.play(FadeIn(g), FadeIn(lg))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(m_) for m_ in marks], lag_ratio=0.1), run_time=2)
        self.wait(0.3)
        self.clear_scene()
