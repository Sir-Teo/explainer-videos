from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai8.common import HIST, MEAS, TEST, TRAIN, bars, chapter, curve, load


def _clean(s: str, n=70) -> str:
    s = " ".join(s.replace("\n", " ").split())
    return s if len(s) <= n else s[: n - 1] + "…"


class Memorization(VoiceoverScene):
    def construct(self):
        chapter(self, 17, r"Memorization in language models", r"What does a model remember word for word?",
                "Chapter seventeen. Memorization in language models.", lit=(2019,))
        self.history()
        self.natural()
        self.canary()
        self.law()

    # ------------------------------------------------------------------
    def history(self):
        cards = VGroup(
            history_card(2019, r"N.~Carlini et al., \ \textit{The Secret Sharer}", r"plant a random ``canary'' in the "
                         r"training data, \ measure how exposed it is", width=6.4, font_size=19, color=HIST),
            history_card(2021, r"N.~Carlini et al., \ extracting from GPT-2", r"over $600$ of $1{,}800$ candidate "
                         r"samples were verbatim training text", width=6.4, font_size=19, color=HIST),
            history_card(2023, r"N.~Carlini et al., \ quantifying memorization", r"log-linear in model size, \ "
                         r"repetition and prompt length; \ GPT-J: at least $1\%$ of its data", width=4.3, font_size=16,
                         color=HIST),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_corner(UL, buff=0.35)
        dfn = definition_card(r"extractable with $k$ tokens of context",
                              r"a string $s$ in the training data, \ preceded there by a $k$-token prefix $p$, \ is "
                              r"extractable if greedy decoding from $p$ produces $s$ exactly.",
                              width=5.6, font_size=22).to_corner(UR, buff=0.35).shift(DOWN * 0.8)
        src = note(r"definition: \ Carlini et al.\ (2023)").next_to(dfn, DOWN, buff=0.1)
        ex_ = VGroup(label(r"a prefix from the training text: \ $32$ tokens", font_size=22, color=GREY_B),
                     label(r"$\to$ \ greedy decoding: \ $32$ more tokens", font_size=22, color=C.SURPRISE),
                     label(r"$=$ \ the next $32$ tokens of the training text?", font_size=22, color=MEAS)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        ex_.next_to(src, DOWN, buff=0.4).align_to(dfn, LEFT)
        with self.voiceover(
            "The last chapter is about what a model remembers exactly. Generalizing is not copying, but large "
            "models do both. <bookmark mark='a'/> In 2019 Nicholas Carlini and colleagues planted random secrets in "
            "training data and measured how readily models gave them back. <bookmark mark='b'/> In 2021 they pulled "
            "training text out of GPT-2 by sampling and filtering: over six hundred of eighteen hundred candidates "
            "were verbatim copies of training documents, some with names and contact details. "
            "<bookmark mark='c'/> In 2023 they measured it at scale: memorization grows log-linearly with model "
            "size, with how often a passage is repeated, and with the length of the prompt; the six-billion-"
            "parameter GPT-J had memorized at least one percent of its training data. <bookmark mark='d'/> Their "
            "test: give the model a prefix from the training data, and see whether greedy decoding continues it "
            "exactly."
        ) as vo:
            self.play(FadeIn(dfn, shift=UP * 0.2), FadeIn(src))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
            vo.wait_until("d")
            self.play(Indicate(dfn, color=WHITE, scale_factor=1.03), FadeIn(ex_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def natural(self):
        m = load("memorize")
        rows = [r for r in m["rows"] if r["k"] > 0]
        runs = [float(r["run32"]) for r in rows]
        exact = [float(r["exact32"]) for r in rows]
        labs = [rf"{r['lo']}" if r["lo"] == r["hi"] else rf"{r['lo']}\text{{--}}{r['hi']}" for r in rows]
        nb = len(rows)
        top = max(max(runs), m["valid_run32"]) * 1.25
        G = axes([-0.6, nb + 0.6], [0, top], x_length=7.0, y_length=4.0, xticks=[], yticks=[0, round(top / 2, 1)],
                 ylabel=r"tokens continued correctly before the first miss \ (of $32$)", center=(-2.2, -0.6, 0))
        ax = G.ax
        bs = bars(ax, np.arange(nb), runs, 0.6, MEAS, 0.85)
        vb = bars(ax, [nb], [m["valid_run32"]], 0.6, GREY_B, 0.85)
        xl = VGroup(*[MathTex(t, font_size=22, color=GREY_B).next_to(ax.c2p(i, 0), DOWN, buff=0.12) for i, t in enumerate(labs)])
        xl.add(label(r"held out", font_size=18, color=GREY_B).next_to(ax.c2p(nb, 0), DOWN, buff=0.14))
        xt = label(r"times the $64$-token passage occurs in the training text", font_size=20, color=GREY_A)
        xt.next_to(xl, DOWN, buff=0.15)
        kk = VGroup(*[MathTex(rf"{int(r['k'])}", font_size=18, color=GREY_B).next_to(b_, UP, buff=0.05)
                      for r, b_ in zip(rows, bs)])
        n_ex = sum(int(round(e * r["k"])) for e, r in zip(exact, rows))
        n_tried = sum(int(r["k"]) for r in rows)
        mtok, mmax, vrun = m["train_tokens"] / 1e6, m["max_count"], m["valid_run32"]
        r0, rN, topbin = runs[0], runs[-1], labs[-1].replace(chr(92) + "text{--}", " to ")
        info = VGroup(
            label(r"our novels model: \ $6$ million weights, \ thirty novels", font_size=22),
            label(rf"${m['train_tokens'] / 1e6:.1f}$ million training tokens; \ the most any passage repeats: "
                  rf"${m['max_count']}$", font_size=20, color=GREY_A),
            label(rf"passages extracted exactly: \ ${n_ex}$ of ${sum(int(r['k']) for r in rows)}$ tested", font_size=22,
                  color=MEAS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.35)
        miss = m["miss"]
        ex = VGroup(
            label(r"a passage seen once: \ prompt, \ truth, \ model", font_size=20, color=GREY_A),
            data_text(_clean(miss["prefix"][-40:], 40), font_size=17, color=GREY_B),
            data_text(_clean(miss["truth"], 40), font_size=17, color=MEAS),
            data_text(_clean(miss["model"], 40), font_size=17, color=C.SURPRISE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(info, DOWN, buff=0.5).align_to(info, LEFT)
        if ex.width > 5.4:
            ex.scale_to_fit_width(5.4)
        keep_in_frame(ex)
        rising = runs[-1] > 2 * runs[0]
        further = ("But it gets further before its first mistake on passages it has seen more often: "
                   f"{r0:.1f} tokens on average for passages seen once, {rN:.1f} for those seen {topbin} times, "
                   f"against {vrun:.1f} on text it never saw. " if rising else
                   f"On average it gets {r0:.1f} tokens right before its first mistake, about as many as on text it "
                   f"never saw, {vrun:.1f}. ")
        with self.voiceover(
            f"Run that test on our own novels model. Its training text has {mtok:.1f} million tokens, and long "
            f"passages rarely repeat: no 64-token passage occurs more than {mmax} times. <bookmark mark='a'/> "
            f"Prompted with the first 32 tokens of a training passage, it reproduces the next 32 exactly in {n_ex} "
            f"cases out of {n_tried} tried. <bookmark mark='b'/> " + further
            + "<bookmark mark='c'/> A small model that saw its text a few times stores the style, not the words. "
            "What makes words stick is repetition."
        ) as vo:
            self.play(FadeIn(G), FadeIn(xl), FadeIn(xt), FadeIn(info[0]), FadeIn(info[1]))
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bs], lag_ratio=0.15), FadeIn(kk), run_time=1.6)
            self.play(GrowFromEdge(vb[0], DOWN))
            vo.wait_until("a")
            self.play(FadeIn(info[2]))
            vo.wait_until("b")
            self.play(Indicate(bs, color=MEAS, scale_factor=1.02))
            vo.wait_until("c")
            self.play(FadeIn(ex))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def canary(self):
        c = load("canary")
        groups = [int(g) for g in c["groups"]]
        steps = np.asarray(c["eval_steps"], float)
        ex, rn = np.asarray(c["exact"]), np.asarray(c["run"])
        S = int(c["steps"])
        cols = [interpolate_color(ManimColor(GREY_C), ManimColor(C.SURPRISE), i / max(1, len(groups) - 2))
                for i in range(len(groups) - 1)] + [ManimColor(GREY_B)]
        G = axes([0, S], [0, 1], x_length=5.6, y_length=3.8, xticks=[0, S // 2, S], xfmt=lambda v: fmt_int(v),
                 yticks=[0, 0.5, 1], yfmt=lambda v: rf"{100 * v:.0f}\%", xlabel=r"training steps",
                 ylabel=r"planted passages extracted exactly", center=(-3.5, -0.2, 0), font_size=18)
        ax = G.ax
        lines = VGroup(*[curve(ax, steps, ex[:, j], cols[j], 3.5 if g >= 16 else 2.5) for j, g in enumerate(groups)])
        lk = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.3, color=cols[j], stroke_width=4),
                             label(rf"${g}\times$" if g else r"never", font_size=18, color=cols[j])).arrange(RIGHT, buff=0.1)
                      for j, g in reversed(list(enumerate(groups)))]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        lk.move_to([0.3, -0.2, 0])
        gs = [g for g in groups if g > 0]
        H = axes([0, math.log2(gs[-1])], [0, 1], x_length=4.6, y_length=3.8, xticks=list(range(int(math.log2(gs[-1])) + 1)),
                 xfmt=lambda v: f"{2 ** int(v)}", yticks=[0, 0.5, 1], yfmt=lambda v: rf"{100 * v:.0f}\%",
                 xlabel=r"times planted", center=(3.6, -0.2, 0), font_size=18)
        hx = H.ax
        fin = ex[-1, :len(gs)]
        cf = VGroup(curve(hx, np.log2(gs), fin, C.SURPRISE, 4),
                    *[Dot(hx.c2p(math.log2(g), v), radius=0.07, color=C.SURPRISE) for g, v in zip(gs, fin)])
        ctrl = ex[-1, -1]
        head = label(rf"Trained on: \ its own text, \ plus ${int(c['per'])}$ unseen passages planted $1, 2, 4, \dots, "
                     rf"{gs[-1]}$ times", font_size=24).to_edge(UP, buff=0.3)
        sh = c["shown"]
        k64 = f"g{len(groups) - 2}"
        demo = None
        if k64 in sh:
            d = sh[k64]
            demo = VGroup(
                label(rf"planted ${d['count']}$ times: \ prompt, \ then the model's greedy continuation", font_size=18,
                      color=GREY_A),
                data_text(_clean(d["prefix"], 80), font_size=15, color=GREY_B),
                data_text(_clean(d["model"], 80), font_size=15,
                          color=C.SURPRISE if d["model"] == d["truth"] else MEAS),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).to_edge(DOWN, buff=0.25)
            if demo.width > 13:
                demo.scale_to_fit_width(13)
        j1 = next((j for j, g in enumerate(gs) if fin[j] >= 0.5), None)
        e1, e8, eN, eC = 100 * fin[0], 100 * fin[gs.index(8)], 100 * fin[-1], 100 * ctrl
        gN, per, g_half = gs[-1], int(c["per"]), (gs[j1] if j1 is not None else 0)
        mono = bool(np.all(np.diff(fin) >= -0.07))
        halfway = f"Half or more are extractable from {g_half} repetitions on. " if j1 is not None else ""
        trend = ("Extraction climbs with repetition, as Carlini and colleagues and Kandpal and colleagues found at "
                 "scale; it's why deduplicating training data became standard."
                 if mono else
                 "The trend with repetition is noisy at this scale, but it's the one found at scale by Carlini and "
                 "colleagues and Kandpal and colleagues, and why deduplicating training data became standard.")
        with self.voiceover(
            "To see repetition at work, plant it. Continue training our model on its own text, into which "
            f"{per} passages it has never seen are planted once each, {per} more twice each, and so on up to {gN} "
            f"times, with {per} more never planted, as a control. <bookmark mark='a'/> Through {S} steps of "
            "training, the passages planted most often become extractable first. "
            f"<bookmark mark='b'/> By the end: {e1:.0f} percent of passages seen once, {e8:.0f} percent of those "
            f"planted eight times, and {eN:.0f} percent of those planted {gN} times come back word for word; the "
            f"control, {eC:.0f} percent. " + halfway + "<bookmark mark='c'/> " + trend
        ) as vo:
            self.play(FadeIn(head), FadeIn(G), FadeIn(H), FadeIn(lk))
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.15), run_time=6.0)
            vo.wait_until("a")
            self.play(Indicate(lk, color=WHITE, scale_factor=1.03))
            vo.wait_until("b")
            self.play(Create(cf), run_time=1.5)
            vo.wait_until("c")
            if demo is not None:
                self.play(FadeIn(demo))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def law(self):
        items = [
            (2022, r"N.~Kandpal et al.; \ K.~Lee et al.", r"deduplicating the training data cuts memorization"),
            (2023, r"M.~Nasr et al.", r"a prompt that makes a chat model diverge, \ repeating a word, \ makes it emit "
                   r"training data"),
            (2025, r"A.~F.~Cooper et al.", r"Llama 3.1 70B has memorized large parts of some books, \ the first "
                   r"\textit{Harry Potter} almost entirely"),
            (2025, r"Munich Regional Court, \ GEMA v.\ OpenAI", r"lyrics memorized in a model's weights are a "
                   r"reproduction; \ not yet final"),
            (2025, r"High Court, \ Getty Images v.\ Stability AI", r"the image model's weights are not an infringing "
                   r"copy"),
            (2026, r"A.~Ahmed, A.~F.~Cooper et al.", r"near-complete books extracted from some production chat models"),
        ]
        cards = VGroup(*[history_card(y, w, t, width=4.3, font_size=18, color=HIST) for y, w, t in items])
        cards.arrange_in_grid(rows=2, cols=3, buff=(0.2, 0.35), cell_alignment=UL).move_to(UP * 0.1)
        head = label(r"Memorization, \ 2022--2026", font_size=34).to_edge(UP, buff=0.3)
        foot = note(r"US rulings of June 2025 (Bartz v.\ Anthropic; \ Kadrey v.\ Meta) \ found training itself fair use; "
                    r"\ the law is unsettled").to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Since then, memorization has become a practical and legal question. <bookmark mark='a'/> Deduplicating "
            "training data reduces it. <bookmark mark='b'/> In 2023 Nasr and colleagues found that asking a chat "
            "model to repeat one word forever made it drift into reciting training data. <bookmark mark='c'/> In "
            "2025 Cooper and colleagues showed that some open-weight models have memorized large parts of popular "
            "books. <bookmark mark='d'/> Courts disagree on what that means. In November 2025 a Munich court held "
            "that song lyrics memorized in a model are a copy, a ruling not yet final, <bookmark mark='e'/> while "
            "London's High Court held that an image model's weights were not one. American judges that June had "
            "found training itself to be fair use. <bookmark mark='f'/> And in early 2026 researchers reported "
            "extracting near-complete books from production chat models. Whether a model has learned or copied "
            "is no longer only a question for learning theory."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cards[0]))
            for k, mk in enumerate("abcdef"):
                vo.wait_until(mk)
                if k == 0:
                    self.play(Indicate(cards[0], color=HIST, scale_factor=1.02))
                else:
                    self.play(FadeIn(cards[k], shift=UP * 0.15))
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()
