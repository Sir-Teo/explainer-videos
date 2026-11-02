from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai30.common import BASEM, CHAT, FEAT, MONO, PART, RESID, load, model_text, show_tok, ticks

SHARED = C.BITS


class Diffing(VoiceoverScene):
    def construct(self):
        self.card()
        self.crosscoder()
        self.histogram()
        self.latents()
        self.difflens()

    def card(self):
        card = chapter_card(12, r"What fine-tuning changed", r"Can we diff two models, feature by feature?", part=PART)
        with self.voiceover("Chapter twelve. What fine-tuning changed."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def crosscoder(self):
        hb = VGroup(RoundedRectangle(width=2.8, height=0.8, corner_radius=0.12, stroke_color=BASEM, stroke_width=2.5),
                    label(r"the novels model", font_size=20, color=BASEM)).move_to([-4.6, 1.3, 0])
        hb[1].move_to(hb[0])
        hc = VGroup(RoundedRectangle(width=2.8, height=0.8, corner_radius=0.12, stroke_color=CHAT, stroke_width=2.5),
                    label(r"Part 27's chat fine-tune", font_size=20, color=CHAT)).move_to([-4.6, -1.3, 0])
        hc[1].move_to(hc[0])
        code = VGroup(RoundedRectangle(width=1.8, height=2.6, corner_radius=0.15, stroke_color=FEAT, stroke_width=3,
                                       fill_color=FEAT, fill_opacity=0.1),
                      label(r"one shared \\ sparse code $f$", font_size=20, color=FEAT)).move_to([-0.8, 0, 0])
        code[1].move_to(code[0])
        db = VGroup(RoundedRectangle(width=2.2, height=0.8, corner_radius=0.12, stroke_color=BASEM, stroke_width=2.5),
                    MathTex(r"\hat z_{\text{base}} = f\, D_{\text{base}} + b_{\text{base}}", font_size=24, color=BASEM)).move_to([3.2, 1.3, 0])
        db[1].move_to(db[0])
        dc = VGroup(RoundedRectangle(width=2.2, height=0.8, corner_radius=0.12, stroke_color=CHAT, stroke_width=2.5),
                    MathTex(r"\hat z_{\text{chat}} = f\, D_{\text{chat}} + b_{\text{chat}}", font_size=24, color=CHAT)).move_to([3.2, -1.3, 0])
        dc[1].move_to(dc[0])
        for b in (db, dc):
            b[0].stretch_to_fit_width(b[1].width + 0.4)
        ar = VGroup(Arrow(hb.get_right(), code.get_left() + UP * 0.6, buff=0.1, color=BASEM),
                    Arrow(hc.get_right(), code.get_left() + DOWN * 0.6, buff=0.1, color=CHAT),
                    Arrow(code.get_right() + UP * 0.6, db.get_left(), buff=0.1, color=BASEM),
                    Arrow(code.get_right() + DOWN * 0.6, dc.get_left(), buff=0.1, color=CHAT))
        rel = cmath(r"r_j = \frac{\|d^{\text{chat}}_j\|}{\|d^{\text{base}}_j\| + \|d^{\text{chat}}_j\|}", font_size=34).to_edge(DOWN, buff=0.55)
        rl = label(r"normalized decoder norms: \ $0$: base only; \ $\tfrac12$: equal norms; \ $1$: chat only",
                   font_size=19, color=GREY_A).next_to(rel, UP, buff=0.15)
        head = label(r"the same tokens through both models \\ each residual stream scaled separately: \ $z=h/s$", font_size=21,
                     color=RESID).to_edge(UP, buff=0.35)
        cite_ = cite(r"Lindsey et al., \textit{Sparse Crosscoders} (2024); \ Minder et al.\ (2025)", corner=UR).shift(DOWN * 0.5)
        with self.voiceover(
            "Part 27 fine-tuned the novels model into an assistant. What changed inside? "
            "Comparing two models this way is called model diffing. <bookmark mark='a'/> The tool is a crosscoder, "
            "introduced by Jack Lindsey and colleagues in 2024: one dictionary that reads both models' vectors on the "
            "same tokens, and reconstructs each through a decoder and output bias, after separate scaling. "
            "<bookmark mark='b'/> We compare the decoder norms in those normalized coordinates. Similar norms do not "
            "establish matching directions, and a small base decoder does not prove a concept was newly created. "
            "<bookmark mark='c'/> Each latent gets a number between zero and one: the chat decoder norm divided by "
            "the sum of the two norms. This is a descriptive proxy, not a causal test of model-specific features."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hb), FadeIn(hc))
            vo.wait_until("a")
            self.play(GrowArrow(ar[0]), GrowArrow(ar[1]), FadeIn(code), FadeIn(cite_))
            vo.wait_until("b")
            self.play(GrowArrow(ar[2]), GrowArrow(ar[3]), FadeIn(db), FadeIn(dc))
            vo.wait_until("c")
            self.play(Write(rel), FadeIn(rl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def histogram(self):
        d = load("diffing")
        L3, L = [int(v) for v in d["layers"]][0], [int(v) for v in d["layers"]][-1]
        r = np.asarray(d[f"rel_{L}"])[np.asarray(d[f"alive_{L}"]) > 0]
        if not len(r) or not np.isfinite(r).all() or np.any((r < 0) | (r > 1)):
            raise ValueError("Live decoder-norm shares must be finite fractions in [0, 1]")
        h, e = np.histogram(r, bins=np.linspace(0, 1, 26))
        top = float(h.max())
        g = axes([0, 1], [0, top * 1.1], x_length=7.4, y_length=3.6, xlabel=r"the chat model's share of the decoder, \ $r_j$",
                 ylabel=r"latents", xticks=[0, 0.5, 1], yticks=ticks(0, top, 3), center=[-1.8, -0.3, 0])
        cols = [BASEM if (a + b) / 2 < 0.1 else CHAT if (a + b) / 2 > 0.9 else SHARED for a, b in zip(e, e[1:])]
        bars_ = VGroup(*[Rectangle(width=7.4 / 25 * 0.9, height=max(v / (top * 1.1) * 3.6, 0.005), stroke_width=0,
                                   fill_color=c_, fill_opacity=0.9).move_to(g.ax.c2p((a + b) / 2, 0), aligned_edge=DOWN)
                         for v, a, b, c_ in zip(h, e, e[1:], cols)])
        nb, nc, ns = int(d[f"n_base_only_{L}"]), int(d[f"n_chat_only_{L}"]), int(d[f"n_shared_{L}"])
        lo, hi = float(d[f"rel_lo_{L}"]), float(d[f"rel_hi_{L}"])
        lo3, hi3 = float(d[f"rel_lo_{L3}"]), float(d[f"rel_hi_{L3}"])
        nc3, nb3 = int(d[f"n_chat_only_{L3}"]), int(d[f"n_base_only_{L3}"])
        tab = VGroup(label(rf"after block ${L}$:", font_size=22, color=WHITE),
                     label(rf"balanced norms \ ($0.3 < r < 0.7$): \ ${ns}$", font_size=22, color=SHARED),
                     label(rf"chat-dominant norm \ ($r > 0.9$): \ ${nc}$", font_size=22, color=CHAT),
                     label(rf"base-dominant norm \ ($r < 0.1$): \ ${nb}$", font_size=22, color=BASEM),
                     label(rf"other live latents: \ ${len(r) - ns - nc - nb}$", font_size=18, color=GREY_B),
                     label(rf"$r$ from ${lo:.2f}$ to ${hi:.2f}$; \ after block ${L3}$: \ ${lo3:.2f}$ to ${hi3:.2f}$",
                           font_size=18, color=GREY_B),
                     label(rf"${len(r)}$ live of ${int(d['F']):,}$; \ fit-pool FVU ${100 * float(d[f'fvu_{L}']):.0f}\%$".replace(",", "{,}"),
                           font_size=18, color=GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.6, 0.8, 0])
        tag = note(rf"computed: \ BatchTopK, $k = {int(d['k'])}$; \ ${int(d['n_novel']):,}$ novel tokens and "
                   rf"${int(d['n_chat']):,}$ chat tokens".replace(",", "{,}")).to_corner(DR, buff=0.2)
        warn = label(r"L1 can overstate model specificity: \\ Minder et al.\ (2025) found shrinkage and decoupling; "
                     r"\\ BatchTopK mitigated these in their study", font_size=18, color=GREY_A).move_to([4.6, -2.0, 0])
        cv = np.asarray(d[f"curve_{L}"])
        if cv.ndim != 2 or not len(cv) or cv.shape[1] < 3 or not np.isfinite(cv[:, :3]).all() or np.any(cv[:, 2] < 0):
            raise ValueError("Crosscoder training curve must contain finite nonnegative FVU values")
        ftop = max(float(cv[:, 2].max()), 1e-6)
        g0 = axes([0, float(cv[-1, 0])], [0, ftop * 1.05], x_length=7.4, y_length=3.6, xlabel=r"training steps",
                  ylabel=r"variance left unexplained, \ normalized fit batches", xticks=[0, float(cv[-1, 0])],
                  yticks=ticks(0, ftop, 3), center=[-1.8, -0.3, 0])
        c0 = curve(g0.ax, cv[:, 0], cv[:, 2], FEAT, 3)
        verdict = (f"At block {L}, {ns} live latents have norm shares between point three and point seven; "
                   f"{nc} exceed point nine and {nb} are below point one. The other {len(r) - ns - nc - nb} "
                   f"lie outside those bins. The range is {lo:.2f} to {hi:.2f}; at block {L3}, {lo3:.2f} to {hi3:.2f}. "
                   "These thresholds describe this dictionary, not whether fine-tuning created or removed concepts.")
        with self.voiceover(
            f"We trained one after block {L3} and one after block {L}, each on {int(d['n_novel']):,} tokens of novel "
            f"and {int(d['n_chat']):,} of chat transcripts, with {int(d['F']):,} latents; here is the deeper one's "
            f"training, with the full finite FVU range shown. Reconstruction is measured on fitting activations. "
            f"<bookmark mark='a'/> Here is each live latent's normalized decoder-norm share. {verdict} "
            "<bookmark mark='c'/> A warning from 2025: Julian Minder, Clément Dumas and colleagues showed that "
            "L1 crosscoders can misidentify model-specific latents through shrinkage and decoupling. BatchTopK "
            "substantially mitigated these artifacts in their experiments; it does not replace independent validation here."
        ) as vo:
            self.play(FadeIn(g0), FadeIn(tag))
            self.play(Create(c0), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeOut(VGroup(g0, c0)), run_time=0.4)
            self.play(FadeIn(g), run_time=0.6)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars_], lag_ratio=0.03), run_time=2)
            self.play(LaggedStart(*[FadeIn(t_) for t_ in tab], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(warn))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def latents(self):
        d = load("diffing")
        L = [int(v) for v in d["layers"]][-1]
        sh = d[f"show_{L}"]
        chat = list(sh["chat_only"])[:3] or list(sh["chatty"])[:3]
        if not chat:
            raise ValueError("No selected live crosscoder latents are available to display")
        own = bool(sh["chat_only"])
        panels = VGroup()
        for f in chat:
            ctx = VGroup(*[model_text(show_tok(c["text"])[-40:], chars=42, font_size=22, max_lines=1,
                                      color=WHITE if c["chat"] else GREY_B) for c in f["contexts"][:3]])
            ctx.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            hd = label(rf"latent {f['id']}, \ $r = {f['rel']:.2f}$; \ on in ${100 * f['on_chat']:.1f}\%$ of chat tokens, \ "
                       rf"${100 * f['on_novel']:.1f}\%$ of novel", font_size=21, color=CHAT)
            panels.add(VGroup(hd, ctx).arrange(DOWN, aligned_edge=LEFT, buff=0.08))
        panels.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(DOWN * 0.3)
        if panels.height > 6.2:
            panels.scale_to_fit_height(6.2)
        if panels.width > 13.0:
            panels.scale_to_fit_width(13.0)
        head = label((r"selected chat-decoder-dominant latents" if own else r"selected high chat/novel activation ratios") +
                     r" \\ white: chat context; grey: novel context", font_size=24)
        head.to_edge(UP, buff=0.3)
        n_marker = sum(any(str(c["tok"]).startswith("<|") for c in f["contexts"][:3]) for f in chat)
        rs = [float(f["rel"]) for f in chat]
        verdict = (f"{n_marker} of these {len(chat)} have a chat marker as one of the displayed strongest firing "
                   "tokens." if n_marker else "None has a chat marker among the displayed strongest firing tokens.")
        verdict2 = (f"Their normalized decoder-norm shares range from {min(rs):.2f} to {max(rs):.2f}. "
                    "Norm shares and selected contexts do not establish new concepts, aligned decoder directions, "
                    "or their causal use by either model.")
        with self.voiceover(
            "What do the selected latents look like? <bookmark mark='a'/> We prefer the high chat-decoder-norm bin; "
            f"if it is empty, we show eligible latents with the largest chat-to-novel activation-frequency ratios. {verdict} <bookmark mark='b'/>"
            f"{verdict2}"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in panels], lag_ratio=0.4), run_time=3)
            vo.wait_until("b")
            self.play(*[Indicate(p[0], color=CHAT) for p in panels])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def difflens(self):
        d = load("diffing")
        L = [int(v) for v in d["layers"]][-1]
        toks = [show_tok(str(t)) for t in d[f"diff_tokens_{L}"]][:10]
        vals = np.asarray(d[f"diff_logits_{L}"], float)[:10]
        if not len(vals) or len(toks) != len(vals) or not np.isfinite(vals).all():
            raise ValueError("Difference readout requires paired finite token scores")
        vmax = max(float(np.abs(vals).max()), 1e-9)
        rows = VGroup(Line([3.5, -2.7, 0], [3.5, 1.75, 0], color=GREY_D, stroke_width=1.5))
        for i, (t, v) in enumerate(zip(toks, vals)):
            y = 1.45 - i * 0.43
            b = Rectangle(width=max(2.1 * abs(v) / vmax, 0.002), height=0.32, stroke_width=0,
                          fill_color=CHAT if v >= 0 else BASEM, fill_opacity=0.85 if v != 0 else 0)
            b.move_to([3.5, y, 0], aligned_edge=LEFT if v >= 0 else RIGHT)
            tx = data_text(t, font=MONO, font_size=20, color=WHITE)
            if tx.width > 2.2:
                tx.scale_to_fit_width(2.2)
            tx.move_to([1.0, y, 0], aligned_edge=RIGHT)
            value = MathTex(f"{v:+.2f}", font_size=22, color=CHAT if v >= 0 else BASEM).move_to([6.2, y, 0])
            rows.add(VGroup(tx, b, value))
        colors = {r"\Delta": CHAT}
        f = cmath(r"\Delta = \mathbb{E}\big[h_{\text{chat}} - h_{\text{base}}\big] \quad \text{on novel text only}",
                  colors=colors, font_size=30).to_corner(UL, buff=0.4)
        f2 = cmath(r"R(\bar h+\Delta)-R(\bar h),\quad R(z)=\operatorname{head}(\operatorname{norm}(z))",
                   font_size=25).next_to(f, DOWN, buff=0.2)
        f2.align_to(f, LEFT)
        hc = history_card(2025, r"J.~Minder, C.~Dumas et al.", r"narrow fine-tuning leaves readable traces in "
                          r"activation differences, \ even on unrelated text", width=4.8, color=CHAT, font_size=19)
        hc.to_corner(DL, buff=0.4)
        rl = label(rf"top local readout changes after block ${L}$ \ (signed logits)", font_size=20,
                   color=GREY_A).next_to(rows, UP, buff=0.2)
        special = sum("<|" in t for t in toks)
        dn, bn = float(d[f"diff_norm_{L}"]), float(d[f"base_norm_{L}"])
        if not np.isfinite([dn, bn]).all() or dn < 0 or bn <= 0:
            raise ValueError("Difference-length comparison requires finite nonnegative difference and positive base norms")
        verdict = (f"{special} of the top ten local readout tokens are chat markers." if special else
                   "None of these top ten local readout tokens is a chat marker; that alone does not classify the change as style.")
        o_ = np.array([0.6, -2.0, 0])
        ang = 0.9
        hb = np.array([np.cos(ang), np.sin(ang), 0]) * 4.0
        hcv = hb + np.array([np.cos(ang - PI / 2), np.sin(ang - PI / 2), 0]) * 4.0 * dn / bn
        ab = Arrow(o_, o_ + hb, buff=0, color=BASEM, stroke_width=5, max_tip_length_to_length_ratio=0.06)
        ac = Arrow(o_, o_ + hcv, buff=0, color=CHAT, stroke_width=5, max_tip_length_to_length_ratio=0.06)
        ad = Arrow(o_ + hb, o_ + hcv, buff=0, color=WHITE, stroke_width=4, max_tip_length_to_length_ratio=0.35)
        lb_ = label(r"$h_{\text{base}}$", font_size=24, color=BASEM).next_to(ab.get_center(), LEFT, buff=0.25)
        lc_ = label(r"$h_{\text{chat}}$", font_size=24, color=CHAT).next_to(ac.get_center(), RIGHT, buff=0.25)
        ld_ = label(rf"$\Delta$: \ ${100 * dn / bn:.0f}\%$ of the length", font_size=22, color=WHITE).next_to(ad, RIGHT, buff=0.2)
        vec_pic = VGroup(ab, ac, ad, lb_, lc_, ld_)
        schematic = label(r"schematic directions; \ only the relative difference length is measured", font_size=16,
                          color=GREY_B).move_to([2.0, -3.25, 0])
        with self.voiceover(
            "There is an even cheaper diff, from Julian Minder and colleagues in October 2025. <bookmark mark='a'/> "
            "Our local variant averages across the sampled novel positions rather than reproducing their per-position "
            "first-token analysis. Run both models on plain novel text, and "
            f"average the difference between their vectors: it is {100 * dn / bn:.0f} percent of a typical vector's "
            "length. The arrow directions are schematic. <bookmark mark='b'/> Evaluate the base model's final "
            "normalization and output head at the mean base vector plus this difference, and subtract the same "
            "readout at the mean base vector. This is a nonlinear local readout contrast, not the full models' "
            f"prediction difference. <bookmark mark='c'/> {verdict} Narrow fine-tuning can leave readable traces, which is good "
            "news for auditors, the subject of Part 31."
        ) as vo:
            self.play(Write(f))
            vo.wait_until("a")
            self.play(FadeIn(hc), GrowArrow(ab), GrowArrow(ac), FadeIn(lb_), FadeIn(lc_))
            self.play(GrowArrow(ad), FadeIn(ld_), FadeIn(schematic))
            vo.wait_until("b")
            self.play(FadeOut(vec_pic), FadeOut(schematic))
            self.play(FadeIn(f2), FadeIn(rl), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in rows], lag_ratio=0.15))
            vo.wait_until("c")
            self.play(Indicate(rows, color=CHAT, scale_factor=1.03))
        self.wait(0.3)
        self.clear_scene()
