from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai30.common import MONO, PART, PROBE, RESID, load, show_tok, ticks

TUNED = C.MLP


def lens_table(tokens, table, probs, cell_w, cell_h, color, font_size=15):
    """Rows: layers (0 at the bottom); columns: positions; each cell the lens's top next token, shaded by its
    probability."""
    L = len(table)
    g = VGroup()
    for l_ in range(L):
        for j, t in enumerate(table[l_]):
            p = float(probs[l_][j])
            r = Rectangle(width=cell_w * 0.96, height=cell_h * 0.9, stroke_width=0, fill_color=color,
                          fill_opacity=0.08 + 0.8 * p).move_to([j * cell_w, l_ * cell_h, 0])
            tx = data_text(show_tok(str(t))[:7], font=MONO, font_size=font_size, color=WHITE)
            if tx.width > cell_w * 0.92:
                tx.scale_to_fit_width(cell_w * 0.92)
            g.add(VGroup(r, tx.move_to(r)))
    return g


class Lens(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.table()
        self.tuned()
        self.compare()

    def card(self):
        card = chapter_card(3, r"Reading the stream as it flows", r"What would the model say, if it stopped here?",
                            part=PART)
        with self.voiceover("Chapter three. Reading the stream as it flows."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def idea(self):
        L = int(load("lens")["layers"])
        x0 = -4.6
        line = Line([x0, -3.0, 0], [x0, 2.9, 0], color=RESID, stroke_width=6)
        blocks = VGroup()
        taps = VGroup()
        for l_ in range(L):
            y = -2.4 + l_ * 0.9
            b = RoundedRectangle(width=1.5, height=0.55, corner_radius=0.1, stroke_color=GREY_B, stroke_width=2,
                                 fill_color="#121722", fill_opacity=1).move_to([x0 - 1.6, y + 0.45, 0])
            bl = label(rf"block ${l_ + 1}$", font_size=18, color=GREY_A).move_to(b)
            arr = VGroup(Line([x0, y + 0.2, 0], b.get_right() + DOWN * 0.15, color=GREY_C, stroke_width=1.5),
                         Arrow(b.get_right() + UP * 0.15, [x0, y + 0.75, 0], buff=0, color=GREY_C, stroke_width=2,
                               max_tip_length_to_length_ratio=0.25))
            blocks.add(VGroup(b, bl, arr))
        for l_ in range(L + 1):
            y = -2.65 + l_ * 0.9
            t = Arrow([x0, y, 0], [x0 + 1.4, y, 0], buff=0, color=PROBE, stroke_width=3, max_tip_length_to_length_ratio=0.2)
            taps.add(VGroup(t, label(rf"$h_{l_}$", font_size=20, color=RESID).next_to([x0, y, 0], LEFT, buff=0.08)))
        tl = label(r"read each layer's $h_\ell$ with the model's own last step", font_size=22, color=PROBE)
        tl.move_to([1.6, 2.9, 0])
        colors = {r"h_\ell": RESID, r"W_U": PROBE}
        f = cmath(r"\text{logit lens}_\ell = ", r"W_U", r"\,\operatorname{norm}(", r"h_\ell", r")", colors=colors,
                  font_size=36).move_to([1.6, 1.9, 0])
        why_ = label(r"each block only \textit{adds} to the stream: \\ the last layer's readout may already work "
                     r"part-way up", font_size=22, color=GREY_A).next_to(f, DOWN, buff=0.35)
        hc = history_card(2020, r"nostalgebraist (LessWrong)", r"the logit lens: \ GPT-2's guesses, layer by layer, \ "
                          r"read with its own unembedding", width=5.6, color=PROBE, font_size=20).move_to([1.8, -1.6, 0])
        with self.voiceover(
            "A probe is trained. There is a reading you get for free. <bookmark mark='a'/> In a transformer, every "
            "block reads the residual stream and adds its result back. The last step of the model turns the final "
            "stream into a prediction: a normalization, then the unembedding matrix. <bookmark mark='b'/> So apply "
            "that last step early, to the stream after every block, and ask what the model would say if it stopped "
            "there. <bookmark mark='c'/> A pseudonymous writer, nostalgebraist, tried it on GPT-2 in 2020 and called "
            "it the logit lens."
        ) as vo:
            self.play(Create(line), LaggedStart(*[FadeIn(b) for b in blocks], lag_ratio=0.15), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(f), FadeIn(why_))
            vo.wait_until("b")
            self.play(FadeIn(tl), LaggedStart(*[GrowArrow(t[0]) for t in taps], lag_ratio=0.12),
                      LaggedStart(*[FadeIn(t[1]) for t in taps], lag_ratio=0.12), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(hc, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def build_table(self, which):
        d = load("lens")
        toks = [str(t) for t in d["prompt_tokens"]]
        n = min(10, len(toks))
        tab = [list(r)[-n:] for r in d[f"table_{which}"]]
        pr = [list(r)[-n:] for r in d[f"p_{which}"]]
        cw, ch = 1.12, 0.62
        g = lens_table(toks[-n:], tab, pr, cw, ch, PROBE if which == "logit" else TUNED)
        g.move_to([0.5, -0.45, 0])
        heads = VGroup(*[data_text(show_tok(t)[:7], font=MONO, font_size=16, color=GREY_A) for t in toks[-n:]])
        for j, h in enumerate(heads):
            h.move_to([g[j].get_x(), g.get_bottom()[1] - 0.3, 0])
        rows = VGroup(*[label(rf"$h_{l_}$", font_size=20, color=RESID).next_to(g[l_ * n], LEFT, buff=0.2)
                        for l_ in range(len(tab))])
        return g, heads, rows, n

    def table(self):
        d = load("lens")
        g, heads, rows, n = self.build_table("logit")
        toks = [str(t) for t in d["prompt_tokens"]]
        pre = data_text("".join(toks[:-n]).strip()[-40:], font=MONO, font_size=18, color=GREY_B).to_edge(UP, buff=0.35)
        cap = label(r"each cell: \ the lens's top guess for the \textit{next} token, \ brighter when surer",
                    font_size=20, color=GREY_A).next_to(pre, DOWN, buff=0.15)
        inl = label(r"the input tokens", font_size=18, color=GREY_B).next_to(heads, DOWN, buff=0.12)
        last = [str(r[-1]) for r in d["table_logit"]]
        final = show_tok(last[-1]).strip("·")
        first_right = next((l_ for l_, t in enumerate(last) if t == last[-1]), len(last) - 1)
        with self.voiceover(
            "Here is the logit lens on the novels model, reading 'it was the best of times, it was the worst of "
            "times, it was the age of'. <bookmark mark='a'/> Each row is a layer, each column a position, and each "
            "cell the lens's best guess for the next token. <bookmark mark='b'/> At the bottom, the embedding alone "
            "mostly guesses tokens that often follow the current one, and the guesses are poor. "
            f"<bookmark mark='c'/> Going up, the right continuations firm up; at the last position, the final "
            f"guess, '{final}', is already the top guess at layer {first_right}. Predictions are built "
            "gradually, refined block by block."
        ) as vo:
            self.play(FadeIn(pre), FadeIn(heads), FadeIn(inl), FadeIn(rows))
            vo.wait_until("a")
            self.play(FadeIn(cap), LaggedStart(*[FadeIn(c) for c in g[:n]], lag_ratio=0.05))
            vo.wait_until("b")
            self.play(Indicate(g[:n], color=PROBE, scale_factor=1.02))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c) for c in g[n:]], lag_ratio=0.01), run_time=2.5)
            self.play(Indicate(VGroup(*[g[l_ * n + n - 1] for l_ in range(len(last))]), color=WHITE, scale_factor=1.04))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tuned(self):
        d = load("lens")
        cur = np.asarray(d["curves"])  # (layers, checkpoints, 2)
        L = int(d["layers"])
        top = float(cur[:, :, 1].max())
        S = float(cur[0, -1, 0])
        g = axes([0, S], [0, top * 1.05], x_length=6.6, y_length=4.0, xlabel=r"training steps of the translators",
                 ylabel=r"KL to the final prediction (bits)", xticks=[0, S], yticks=ticks(0, top, 3),
                 center=[2.4, -0.4, 0])
        cols = color_gradient([TUNED, PROBE], L)
        cs = VGroup(*[curve(g.ax, cur[l_, :, 0], cur[l_, :, 1], cols[l_], 3) for l_ in range(L)])
        lbl = VGroup(*[label(rf"$h_{l_}$", font_size=18, color=cols[l_]).next_to(g.ax.c2p(S, cur[l_, -1, 1]), RIGHT, buff=0.08)
                       for l_ in range(L)])
        for a_, b_ in zip(lbl, lbl[1:]):
            if a_.get_y() - b_.get_y() < 0.25:
                b_.set_y(a_.get_y() - 0.25)
        colors = {r"A_\ell": TUNED, r"h_\ell": RESID}
        f = cmath(r"\text{tuned lens}_\ell = W_U\,\operatorname{norm}(", r"h_\ell", r" + ", r"A_\ell", r" h_\ell", r" + b_\ell)",
                  colors=colors, font_size=30).to_corner(UL, buff=0.4)
        w = label(r"one affine translator per layer, \\ trained to match the final prediction \\ (minimize the KL); "
                  r"$A_\ell = 0$ at the start", font_size=20, color=GREY_A).next_to(f, DOWN, buff=0.2).align_to(f, LEFT)
        hc = history_card(2023, r"N.~Belrose et al.", r"the tuned lens: \ more reliable and less biased than the logit "
                          r"lens", width=4.8, color=TUNED, font_size=19).to_corner(DL, buff=0.35)
        with self.voiceover(
            "The logit lens assumes every layer speaks the last layer's language. It doesn't quite: early layers "
            "store things in other directions. <bookmark mark='a'/> In 2023 Nora Belrose and colleagues added a "
            "translator: one affine map per layer, trained so the lens matches the model's final prediction. "
            "<bookmark mark='b'/> We trained one for each layer of the novels model. They start as the logit lens, "
            f"<bookmark mark='c'/> and over {int(S)} steps the gap to the final prediction falls at every layer, most "
            "at the bottom, where the logit lens is furthest off."
        ) as vo:
            self.play(Write(f), FadeIn(w))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(g), FadeIn(VGroup(*[Dot(g.ax.c2p(0, cur[l_, 0, 1]), radius=0.05, color=cols[l_]) for l_ in range(L)])))
            vo.wait_until("c")
            self.play(*[Create(c) for c in cs], run_time=3)
            self.play(FadeIn(lbl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compare(self):
        d = load("lens")
        L = int(d["layers"])
        lk, tk = np.asarray(d["logit_kl"]), np.asarray(d["tuned_kl"])
        lc, tc = np.asarray(d["logit_ce"]), np.asarray(d["tuned_ce"])
        top = float(max(lk.max(), tk.max()))
        g = axes([-0.5, L + 0.5], [0, top * 1.1], x_length=6.0, y_length=3.6, xlabel=r"layer",
                 ylabel=r"KL to the final prediction (bits, held-out text)", xticks=list(range(L + 1)),
                 yticks=ticks(0, top, 3), center=[-3.3, -0.3, 0])
        bl = VGroup(*[Rectangle(width=0.3, height=max(v / (top * 1.1) * 3.6, 0.01), stroke_width=0, fill_color=PROBE,
                                fill_opacity=0.9).move_to(g.ax.c2p(l_ - 0.17, 0), aligned_edge=DOWN) for l_, v in enumerate(lk)])
        bt = VGroup(*[Rectangle(width=0.3, height=max(v / (top * 1.1) * 3.6, 0.01), stroke_width=0, fill_color=TUNED,
                                fill_opacity=0.9).move_to(g.ax.c2p(l_ + 0.17, 0), aligned_edge=DOWN) for l_, v in enumerate(tk)])
        lg = legend([(PROBE, r"logit lens"), (TUNED, r"tuned lens")], font_size=20).next_to(g, UP, buff=0.1).align_to(g, RIGHT)
        tab, heads, rows, n = self.build_table("tuned")
        grp = Group(tab, heads, rows).scale(0.62).move_to([3.6, -0.2, 0])
        tl = label(r"the same prompt, \ tuned lens", font_size=20, color=TUNED).next_to(grp, UP, buff=0.15)
        l0 = 0
        with self.voiceover(
            f"Held out, the comparison is clear. <bookmark mark='a'/> At the embedding, the logit lens is "
            f"{lk[l0]:.1f} bits away from the final prediction, the tuned lens {tk[l0]:.1f}. "
            f"<bookmark mark='b'/> Halfway up, {lk[L // 2]:.1f} against {tk[L // 2]:.1f}. Measured as a predictor of "
            f"the next token, the embedding read by the logit lens costs {lc[0]:.1f} bits per token, by the tuned lens "
            f"{tc[0]:.1f}, and the model itself {lc[-1]:.1f}. <bookmark mark='c'/> A lens is still a reading, not a "
            "mind: it shows what a linear readout could take from each layer, and the same caveats as a probe apply."
        ) as vo:
            self.play(FadeIn(g), FadeIn(lg))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bl], lag_ratio=0.1),
                      LaggedStart(*[GrowFromEdge(b, DOWN) for b in bt], lag_ratio=0.1), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(tl), FadeIn(grp))
            vo.wait_until("c")
            self.play(Indicate(tl, color=TUNED))
        self.wait(0.3)
        self.clear_scene()
