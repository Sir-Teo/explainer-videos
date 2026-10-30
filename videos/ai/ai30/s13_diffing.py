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
        d = load("diffing")
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
                    MathTex(r"\hat h_{\text{base}} = f\, D_{\text{base}}", font_size=26, color=BASEM)).move_to([3.2, 1.3, 0])
        db[1].move_to(db[0])
        dc = VGroup(RoundedRectangle(width=2.2, height=0.8, corner_radius=0.12, stroke_color=CHAT, stroke_width=2.5),
                    MathTex(r"\hat h_{\text{chat}} = f\, D_{\text{chat}}", font_size=26, color=CHAT)).move_to([3.2, -1.3, 0])
        dc[1].move_to(dc[0])
        for b in (db, dc):
            b[0].stretch_to_fit_width(b[1].width + 0.4)
        ar = VGroup(Arrow(hb.get_right(), code.get_left() + UP * 0.6, buff=0.1, color=BASEM),
                    Arrow(hc.get_right(), code.get_left() + DOWN * 0.6, buff=0.1, color=CHAT),
                    Arrow(code.get_right() + UP * 0.6, db.get_left(), buff=0.1, color=BASEM),
                    Arrow(code.get_right() + DOWN * 0.6, dc.get_left(), buff=0.1, color=CHAT))
        rel = cmath(r"r_j = \frac{\|d^{\text{chat}}_j\|}{\|d^{\text{base}}_j\| + \|d^{\text{chat}}_j\|}", font_size=34).to_edge(DOWN, buff=0.55)
        rl = label(r"$0$: \ only in the base model \quad $\tfrac12$: \ in both \quad $1$: \ only after fine-tuning",
                   font_size=20, color=GREY_A).next_to(rel, UP, buff=0.15)
        head = label(r"the same tokens through both models, \ their residual streams", font_size=22,
                     color=RESID).to_edge(UP, buff=0.35)
        cite_ = cite(r"Lindsey et al., \textit{Sparse Crosscoders} (2024); \ Minder et al.\ (2025)", corner=UR).shift(DOWN * 0.5)
        with self.voiceover(
            "Part 27 turned the novels model into an assistant with a few minutes of fine-tuning. What changed inside? "
            "Comparing two models this way is called model diffing. <bookmark mark='a'/> The tool is a crosscoder, "
            "introduced by Jack Lindsey and colleagues in 2024: one dictionary that reads both models' vectors on the "
            "same tokens, and writes them back through a decoder for each. <bookmark mark='b'/> A latent that exists "
            "in both models has two decoders of similar size. One that the fine-tune created has a decoder only on the "
            "chat side. <bookmark mark='c'/> So each latent gets a number between zero and one, the share of its "
            "decoder that belongs to the chat model."
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
                     label(rf"in both \ ($0.3 < r < 0.7$): \ ${ns}$", font_size=22, color=SHARED),
                     label(rf"only after fine-tuning \ ($r > 0.9$): \ ${nc}$", font_size=22, color=CHAT),
                     label(rf"only before \ ($r < 0.1$): \ ${nb}$", font_size=22, color=BASEM),
                     label(rf"$r$ from ${lo:.2f}$ to ${hi:.2f}$; \ after block ${L3}$: \ ${lo3:.2f}$ to ${hi3:.2f}$",
                           font_size=18, color=GREY_B),
                     label(rf"of ${int(d['F']):,}$ latents; \ unexplained ${100 * float(d[f'fvu_{L}']):.0f}\%$".replace(",", "{,}"),
                           font_size=18, color=GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.6, 0.8, 0])
        tag = note(rf"computed: \ BatchTopK, $k = {int(d['k'])}$; \ ${int(d['n_novel']):,}$ novel tokens and "
                   rf"${int(d['n_chat']):,}$ chat tokens".replace(",", "{,}")).to_corner(DR, buff=0.2)
        warn = label(r"an L1 crosscoder invents chat-only latents: \\ Minder et al.\ (2025) found shrinkage and decoupling, "
                     r"\\ and recommend BatchTopK, \ as here", font_size=18, color=GREY_A).move_to([4.6, -2.0, 0])
        cv = np.asarray(d[f"curve_{L}"])
        ftop = float(min(cv[:, 2].max(), 1.0))
        g0 = axes([0, float(cv[-1, 0])], [0, ftop * 1.05], x_length=7.4, y_length=3.6, xlabel=r"training steps",
                  ylabel=r"variance left unexplained, \ both models", xticks=[0, float(cv[-1, 0])],
                  yticks=ticks(0, ftop, 3), center=[-1.8, -0.3, 0])
        c0 = curve(g0.ax, cv[:, 0], np.clip(cv[:, 2], 0, ftop * 1.05), FEAT, 3)
        if nc + nb + nc3 + nb3 == 0:
            verdict = (f"Every latent is shared: r runs only from {lo:.2f} to {hi:.2f}, and after block {L3} from "
                       f"{lo3:.2f} to {hi3:.2f}. Our fine-tune made no features of its own. It changed how the model "
                       "uses the features it had.")
        else:
            verdict = (f"Most are shared, {ns} of them; {nc} belong to the fine-tune alone and {nb} to the base model "
                       f"alone, and after block {L3}, {nc3} and {nb3}.")
        with self.voiceover(
            f"We trained one after block {L3} and one after block {L}, each on {int(d['n_novel']):,} tokens of novel "
            f"and {int(d['n_chat']):,} of chat transcripts, with {int(d['F']):,} latents; here is the deeper one's "
            f"training. <bookmark mark='a'/> And here is each latent's share of the decoder. {verdict} "
            "<bookmark mark='c'/> A warning from 2025: Julian Minder, Clément Dumas and colleagues showed that "
            "crosscoders trained with an L1 penalty manufacture chat-only latents that the base model actually has "
            "too; they recommend BatchTopK, which is what we used."
        ) as vo:
            self.play(FadeIn(g0), FadeIn(tag))
            self.play(Create(c0), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeOut(VGroup(g0, c0)), FadeIn(g))
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
        own = bool(sh["chat_only"])
        panels = VGroup()
        for f in chat:
            ctx = VGroup(*[model_text(show_tok(c["text"])[-46:], chars=48, font_size=15, max_lines=1,
                                      color=WHITE if c["chat"] else GREY_B) for c in f["contexts"][:3]])
            ctx.arrange(DOWN, aligned_edge=LEFT, buff=0.06)
            hd = label(rf"latent {f['id']}, \ $r = {f['rel']:.2f}$; \ on in ${100 * f['on_chat']:.1f}\%$ of chat tokens, \ "
                       rf"${100 * f['on_novel']:.1f}\%$ of novel", font_size=16, color=CHAT)
            panels.add(VGroup(hd, ctx).arrange(DOWN, aligned_edge=LEFT, buff=0.08))
        panels.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(DOWN * 0.3)
        if panels.height > 6.2:
            panels.scale_to_fit_height(6.2)
        if panels.width > 13.0:
            panels.scale_to_fit_width(13.0)
        head = label(r"the latents that fire most on chat transcripts \ (white: \ chat; \ grey: \ novel)", font_size=24)
        head.to_edge(UP, buff=0.3)
        n_marker = sum(any("<|" in c["text"] for c in f["contexts"][:3]) for f in chat)
        rs = [float(f["rel"]) for f in chat]
        verdict = (f"{n_marker} of these {len(chat)} fire on the chat format itself, the markers that open and close "
                   "a turn, and on what follows them." if n_marker else
                   "They fire on the questions and answers of the chat transcripts.")
        verdict2 = ("And their decoders belong to the chat model alone: the fine-tune's new features." if own else
                    f"Yet their decoders are split evenly, r between {min(rs):.2f} and {max(rs):.2f}: the base "
                    "model reads the same directions. It had the features; fine-tuning taught it when to use them.")
        with self.voiceover(
            "So what does chat-specific look like here? <bookmark mark='a'/> These are the latents that fire most "
            f"on chat transcripts rather than novels, at their strongest moments. {verdict} <bookmark mark='b'/>"
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
        vals = np.asarray(d[f"diff_logits_{L}"])[:10]
        rows = VGroup()
        for t, v in zip(toks, vals):
            b = Rectangle(width=max(3.0 * v / vals.max(), 0.02), height=0.32, stroke_width=0, fill_color=CHAT, fill_opacity=0.85)
            tx = data_text(t, font=MONO, font_size=20, color=WHITE)
            rows.add(VGroup(tx, b, MathTex(f"{v:+.2f}", font_size=22, color=CHAT)))
        for r_ in rows:
            r_[0].move_to([1.0, 0, 0], aligned_edge=RIGHT)
            r_[1].next_to(r_[0], RIGHT, buff=0.2)
            r_[2].next_to(r_[1], RIGHT, buff=0.12)
        rows.arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to([2.6, -0.4, 0])
        colors = {r"\Delta": CHAT}
        f = cmath(r"\Delta = \mathbb{E}\big[h_{\text{chat}} - h_{\text{base}}\big] \quad \text{on novel text only}",
                  colors=colors, font_size=30).to_corner(UL, buff=0.4)
        f2 = cmath(r"\text{read } \Delta \text{ through the base model's unembedding}", font_size=26).next_to(f, DOWN, buff=0.2)
        f2.align_to(f, LEFT)
        hc = history_card(2025, r"J.~Minder, C.~Dumas et al.", r"narrow fine-tuning leaves readable traces in "
                          r"activation differences, \ even on unrelated text", width=4.8, color=CHAT, font_size=19)
        hc.to_corner(DL, buff=0.4)
        rl = label(rf"tokens the difference after block ${L}$ promotes most \ (logit change)", font_size=20,
                   color=GREY_A).next_to(rows, UP, buff=0.2)
        special = sum("<|" in t for t in toks)
        dn, bn = float(d[f"diff_norm_{L}"]), float(d[f"base_norm_{L}"])
        verdict = (f"{special} of the top ten are the chat markers themselves: run on nothing but novels, the "
                   "fine-tuned model still leans toward its new format." if special else
                   "None of the top ten is a chat marker: here the difference reads mostly as a shift of style.")
        with self.voiceover(
            "There is an even cheaper diff, from Julian Minder and colleagues in October 2025. <bookmark mark='a'/> "
            "Run both models on ordinary text that has nothing to do with the fine-tune, here plain novel text, and "
            f"average the difference between their vectors: it is {100 * dn / bn:.0f} percent of a typical vector's "
            "length. <bookmark mark='b'/> Then read that difference through the unembedding, as a logit lens would. "
            f"<bookmark mark='c'/> {verdict} Narrow fine-tuning can leave traces that are easy to read, which is good "
            "news for auditors, the subject of Part 31."
        ) as vo:
            self.play(Write(f))
            vo.wait_until("a")
            self.play(FadeIn(hc))
            vo.wait_until("b")
            self.play(FadeIn(f2))
            vo.wait_until("c")
            self.play(FadeIn(rl), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in rows], lag_ratio=0.15))
        self.wait(0.3)
        self.clear_scene()
