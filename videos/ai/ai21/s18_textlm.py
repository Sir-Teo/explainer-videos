from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai21.common import AR_C, HIST, MDM_C, MONO, PART, legend, load, take_away


def board_rows():
    """Part 1's scoreboard, Part 13's transformer, and this chapter's two models (seed 0)."""
    from videos.ai.ai1 import compute as c1
    from videos.ai.ai13 import compute as c13

    t, tf = load("textlm"), c13.load("tf")
    T = int(t["T"])
    rows = [dict(r) for r in c1.load("scoreboard")["rows"]]
    i = next(j for j, r in enumerate(rows) if r["key"] == "best") + 1
    rows.insert(i, dict(key="tf", label=rf"Part 13's transformer, \ ${int(tf['ctx'])}$ characters", bits=float(tf["passage_bits"]),
                        part=13, kind="lm"))
    rows.insert(i + 1, dict(key="ar21", label=rf"autoregressive, \ ${T}$-character blocks", bits=float(t["ar0_passage"]), part=21,
                            kind="lm"))
    rows.insert(i + 2, dict(key="mdm21", label=rf"masked diffusion, \ ${T}$-character blocks \ (a bound)",
                            bits=float(t["mdm0_passage"]), part=21, kind="lm"))
    return rows, i + 1, i + 2


class TextLM(VoiceoverScene):
    def construct(self):
        self.card()
        self.setup()
        self.replay()
        self.writing()
        self.compare()
        self.board()
        self.speed()
        self.frontier()

    def card(self):
        card = chapter_card(17, r"Diffusion language models", r"Can text be written all at once?", part=PART)
        with self.voiceover("Chapter seventeen. Diffusion language models."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def setup(self):
        t = load("textlm")
        card = history_card(2025, r"Nie et al.: \ LLaDA", r"$8$ billion parameters, \ trained from scratch on $2.3$ trillion "
                            r"tokens by masked diffusion; \ competitive with LLaMA 3 8B; \ beats GPT-4o at completing "
                            r"poems backwards", color=HIST, width=6.4, font_size=19).move_to([-3.5, 1.2, 0])
        n = int(t["n_params"])
        ours = VGroup(label(r"ours, \ two models of exactly the same size:", font_size=24, color=GREY_A),
                      label(rf"${n / 1e6:.2f}$ million parameters, \ ${int(t['layers'])}$ blocks, \ the novels' characters", font_size=22),
                      label(r"masked diffusion: \ attention both ways, \ guess the blanks", font_size=22, color=MDM_C),
                      label(r"autoregressive: \ attention backwards only, \ guess the next character", font_size=22, color=AR_C),
                      label(rf"the same initial weights, \ batches, \ and ${int(t['steps']):,}$ steps; \ ${len(t['seeds'])}$ seeds".replace(",", "{,}"),
                            font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.0, -1.4, 0])
        if ours.width > 7.8:
            ours.width = 7.8
        with self.voiceover(
            "In February 2025 Shen Nie, Chongxuan Li and colleagues trained LLaDA, an eight-billion-parameter "
            "language model, entirely by masked diffusion: two point three trillion tokens, every training example a "
            "passage with a random fraction of it blanked. It was competitive with LLaMA 3 of the same size, and "
            "beat GPT-4o at completing a poem backwards, line before line, a task left-to-right models find hard. "
            "<bookmark mark='a'/> We built a pair to compare: a masked-diffusion model and an autoregressive model "
            "of exactly the same size, trained on the novels with the same initial weights, the same batches and "
            "the same number of steps. The only differences are the attention mask and the task."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(o_, shift=UP * 0.1) for o_ in ours], lag_ratio=0.25), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        t = load("textlm")
        seeds = [int(s) for s in t["seeds"]]
        C_ = {f"{k}{s}": np.asarray(t[f"{k}{s}_curve"]) for k in ("mdm", "ar") for s in seeds}
        steps = int(t["steps"])
        allv = np.concatenate([c[1:, 1] for c in C_.values()])
        hi = float(np.ceil(allv.max() * 2) / 2)
        lo = float(np.floor(allv.min() * 2) / 2)
        g = axes([0, steps], [lo, hi], x_length=5.6, y_length=3.2, xlabel=r"training step",
                 ylabel=r"held-out bits per character", xticks=[0, steps // 2, steps], yticks=[lo, hi], center=[-3.4, 0.8, 0])
        series = []  # (points from step eval_at[1] on, colour, width, opacity)
        for k, col in (("mdm", MDM_C), ("ar", AR_C)):
            for s in seeds:
                c = C_[f"{k}{s}"][1:]
                series.append(([g.ax.c2p(a, min(max(b, lo), hi)) for a, b in c], col, 3 if s == seeds[0] else 1.5,
                               1 if s == seeds[0] else 0.5))
        lg = legend([(MDM_C, r"masked diffusion: \ the bound"), (AR_C, r"autoregressive: \ exact")], font_size=19).next_to(g, DOWN, buff=0.15)
        rep_m, rep_a = t[f"mdm{seeds[0]}_replay"], t[f"ar{seeds[0]}_replay"]
        src = str(t["fill_src"])
        fm = np.asarray(t["fill_mask"]).astype(bool)
        half = len(src) // 2

        def two_lines(s_, col):
            return VGroup(data_text(s_[:half].replace(" ", "·"), font=MONO, font_size=20, color=col),
                          data_text(s_[half:].replace(" ", "·"), font=MONO, font_size=20, color=col)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.08)

        blanked = "".join("_" if m else ch for ch, m in zip(src, fm))
        b_m = two_lines(blanked, GREY_B).move_to([3.4, 2.5, 0])
        bl = label(r"a line of the passage, \ half its characters blanked:", font_size=18, color=GREY_A).next_to(b_m, UP, buff=0.1)

        def fill_at(k):
            r = rep_m[k]
            return VGroup(two_lines(str(r["fill"]), MDM_C),
                          label(rf"step ${int(r['step']):,}$: \ ${100 * float(r['fill_right']):.0f}\%$ of blanks right".replace(",", "{,}"),
                                font_size=18, color=MDM_C)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([3.4, 0.9, 0])

        def write_at(k):
            r = rep_a[k]
            return VGroup(label(rf"the autoregressive model writes, \ step ${int(r['step']):,}$".replace(",", "{,}"), font_size=18,
                                color=AR_C), two_lines(str(r["write"]), AR_C)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([3.4, -1.0, 0])

        cur_f, cur_w = fill_at(0), write_at(0)
        m0, a0 = float(C_[f"mdm{seeds[0]}"][-1, 1]), float(C_[f"ar{seeds[0]}"][-1, 1])
        gap = m0 - a0
        fr = float(rep_m[-1]["fill_right"])
        if gap > 0:
            gap_note = (f"Its bound ends at {m0:.2f} bits per character; the autoregressive model at {a0:.2f}, "
                        f"{gap:.2f} lower.")
        else:
            gap_note = (f"Its bound ends at {m0:.2f} bits per character, below the autoregressive model's {a0:.2f}.")
        ks = [k for k in range(1, len(rep_m))]
        with self.voiceover(
            "Here they are learning. On held-out text, the autoregressive model's exact bits per character, and the "
            "diffusion model's bound, both falling. <bookmark mark='a'/> Above, the diffusion model fills in a "
            "line of the passage with half its characters blanked, at each checkpoint; below, the other model writes "
            f"on its own. <bookmark mark='b'/> By the end the diffusion model gets {100 * fr:.0f} percent of the blanks "
            f"right. {gap_note}"
        ) as vo:
            self.play(FadeIn(g), FadeIn(lg), FadeIn(bl), FadeIn(b_m), FadeIn(cur_f), FadeIn(cur_w))
            vo.wait_until("a")
            per = max(0.4, min(1.2, (vo.until("b") - 0.5) / max(1, len(ks))))
            for j, k in enumerate(ks):
                nf, nw = fill_at(k), write_at(min(k, len(rep_a) - 1))
                segs = [Line(P[k - 2], P[k - 1], color=col, stroke_width=w).set_opacity(op) for P, col, w, op in series
                        if k >= 2 and k - 1 < len(P)]
                self.play(FadeOut(cur_f), FadeIn(nf), FadeOut(cur_w), FadeIn(nw), *[Create(x) for x in segs], run_time=per)
                cur_f, cur_w = nf, nw
            vo.wait_until("b")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def writing(self):
        t = load("textlm")
        frames = [str(f_) for f_ in t["frames"][0]]
        T = len(frames[0])
        half = T // 2
        step = 12.0 / half

        def at(i):
            row, col = divmod(i, half)
            return np.array([-6.0 + step * (col + 0.5), 0.9 - 1.0 * row, 0])

        def cell(ch, i, fresh=False):  # fixed character cells, so that every round lines up with the next
            if ch == " ":
                m = Dot(radius=0.025, color=GREY_B)
            elif ch == "_":
                return Line(LEFT * step * 0.3, RIGHT * step * 0.3, color=GREY_B, stroke_width=2.5).move_to(at(i) + DOWN * 0.2)
            else:
                m = data_text(ch, font=MONO, font_size=28, color=MDM_C if fresh else WHITE)
            return m.move_to(at(i))

        slots = VGroup(*[RoundedRectangle(width=step * 0.84, height=0.62, corner_radius=0.05, stroke_color=GREY_C, stroke_width=1.2,
                                          fill_color="#151B27", fill_opacity=1).move_to(at(i)) for i in range(T)])
        cur = VGroup(*[cell(ch, i) for i, ch in enumerate(frames[0])])
        counter = VGroup(label(r"round", font_size=26, color=GREY_A), Integer(0, font_size=30, color=MDM_C)).arrange(RIGHT, buff=0.2)
        counter.to_edge(UP, buff=0.5)
        rule = label(r"each round: \ guess every blank, \ keep only the surest guesses \ (LLaDA's rule)", font_size=24,
                     color=MDM_C).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            f"And here is ours writing {T} characters, from all blanks, in {len(frames) - 1} rounds. "
            "<bookmark mark='a'/> Each round it guesses every blank, keeps the guesses it is surest of, and leaves "
            "the rest blank, LLaDA's rule. <bookmark mark='b'/> Words appear wherever the model is confident first, "
            "and the rest fills in around them: written all at once, then refined, rather than left to right."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(VGroup(b_, c_)) for b_, c_ in zip(slots, cur)], lag_ratio=0.01), FadeIn(counter),
                      run_time=1.2)
            vo.wait_until("a")
            self.play(FadeIn(rule))
            vo.wait_until("b")
            fresh = []
            for r, fr in enumerate(frames[1:], start=1):
                prev = frames[r - 1]
                changed = [i for i in range(T) if prev[i] != fr[i]]
                anims = [Transform(cur[i], cell(fr[i], i, fresh=True)) for i in changed]
                anims += [cur[i].animate.set_color(WHITE) for i in fresh if i not in changed and fr[i] != " "]
                self.play(*anims, counter[1].animate.set_value(r), run_time=0.45)
                fresh = changed
            last = [cur[i].animate.set_color(WHITE) for i in fresh if frames[-1][i] != " "]
            if last:
                self.play(*last, run_time=0.3)
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compare(self):
        t = load("textlm")
        seeds = [int(s) for s in t["seeds"]]
        T = int(t["T"])
        rows = [[r"held-out, \ bits per character", *[rf"seed ${s}$" for s in seeds]],
                [r"masked diffusion \ (bound)", *[rf"${float(t[f'mdm{s}_valid']):.3f} \pm {float(t[f'mdm{s}_valid_se']):.3f}$" for s in seeds]],
                [r"autoregressive \ (exact)", *[rf"${float(t[f'ar{s}_valid']):.3f} \pm {float(t[f'ar{s}_valid_se']):.3f}$" for s in seeds]]]
        tab = VGroup(*[VGroup(*[label(c, font_size=21, color=(GREY_A if i == 0 else [WHITE, MDM_C, AR_C][i]))
                                for c in r]) for i, r in enumerate(rows)])
        xs = [-4.2, -0.6, 2.4]
        for i, r in enumerate(tab):
            for j, c in enumerate(r):
                c.move_to([xs[j], 2.6 - 0.5 * i, 0])
        ests = VGroup(label(r"three estimates of the same bound \ (seed $0$, $256$ held-out blocks):", font_size=21, color=GREY_A),
                      label(rf"blanks with probability $t$, \ weighted $1/t$: \ ${float(t['est_t']):.3f} \pm {float(t['est_t_se']):.3f}$",
                            font_size=20, color=MDM_C),
                      label(rf"exactly $k$ blanks, \ weighted $1/k$: \ ${float(t['est_k']):.3f} \pm {float(t['est_k_se']):.3f}$",
                            font_size=20, color=MDM_C),
                      label(rf"one random order, \ one blank at a time: \ ${float(t['est_order']):.3f} \pm {float(t['est_order_se']):.3f}$",
                            font_size=20, color=MDM_C),
                      label(rf"read left to right: \ ${float(t['l2r']):.3f}$ \qquad the autoregressive model: \ "
                            rf"${float(t['ar0_vb2']):.3f}$", font_size=20, color=WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        ests.move_to([-1.0, -1.2, 0])
        mv = [float(t[f"mdm{s}_valid"]) for s in seeds]
        av = [float(t[f"ar{s}_valid"]) for s in seeds]
        sep = max(av) < min(mv)
        e = [float(t[k]) for k in ("est_t", "est_k", "est_order")]
        se = max(float(t[k + "_se"]) for k in ("est_t", "est_k", "est_order"))
        agree = (max(e) - min(e)) < 3 * se
        l2r, b0 = float(t["l2r"]), float(t["est_k"])
        winner = ("the autoregressive model wins in both seeds" if sep else "the two overlap across seeds")
        agree_note = ("agree within their error bars" if agree else "come close, though not within their error bars")
        if l2r < b0:
            l2r_note = (f"Read strictly left to right, the diffusion model scores {l2r:.3f}, better than its own bound: "
                        "most orders of revealing are harder than reading in order, and the bound pays for all of them.")
        else:
            l2r_note = (f"Read strictly left to right, the diffusion model scores {l2r:.3f}, no better than its bound: it "
                        "was never trained to favour that order.")
        cite_ = cite(r"Prabhudesai et al., \textit{Diffusion Beats Autoregressive in Data-Constrained Settings} (2025)",
                     corner=DR, font_size=18)
        with self.voiceover(
            f"At equal size, data and steps, on held-out blocks of {T} characters, {winner}: the bound is "
            f"{np.mean(mv):.3f} bits per character against {np.mean(av):.3f}. <bookmark mark='a'/> Three different "
            f"estimates of the bound, which the derivation says are equal in expectation, {agree_note}. "
            f"<bookmark mark='b'/> {l2r_note} <bookmark mark='c'/> The gap is not the end of the story: in 2025 Mihir "
            "Prabhudesai and colleagues found that when data is scarce and must be repeated for many epochs, "
            "diffusion models keep improving after autoregressive ones overfit."
        ) as vo:
            self.play(FadeIn(tab))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in ests[:4]], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(ests[4]))
            vo.wait_until("c")
            self.play(FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def board(self):
        t = load("textlm")
        rows, i_ar, i_md = board_rows()
        board = scoreboard(rows, highlight=(i_ar, i_md), max_bits=8.0, row_h=0.38, font_size=20)
        board.scale_to_fit_height(min(board.height, 6.8)).move_to(DOWN * 0.1)
        m, se, a = float(t["mdm0_passage"]), float(t["mdm0_passage_se"]), float(t["ar0_passage"])
        tf = next(r for r in rows if r["key"] == "tf")
        from videos.ai.ai13 import compute as c13

        ratio = int(c13.load("tf")["ctx"]) // int(t["T"])
        with self.voiceover(
            f"On the scoreboard's passage, in blocks of {int(t['T'])} characters: the masked-diffusion model's bound, "
            f"{m:.2f} bits per character, give or take {se:.2f}, and the autoregressive twin, {a:.2f}. "
            f"<bookmark mark='a'/> Part 13's transformer, with {ratio} times the context, "
            f"is at {tf['bits']:.2f}. A bound is an upper limit: the diffusion model's true code length could only be lower."
        ) as vo:
            self.play(FadeIn(board))
            vo.wait_until("a")
            self.play(Indicate(board.rows[i_md], color=MDM_C))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def speed(self):
        t = load("textlm")
        W = t["writes"]
        conf = [w for w in W if w["order"] == "confidence" and int(w["blocks"]) == 1]
        rnd = [w for w in W if w["order"] == "random"]
        blk = [w for w in W if int(w["blocks"]) > 1]
        judge_real = float(t["judge_real"])
        arw = t["ar_write"]
        allj = [w["judge"] for w in W] + [judge_real, arw["judge"]]
        lo, hi = math.floor(min(allj) * 2) / 2, math.ceil(max(allj) * 2) / 2
        T = int(t["T"])
        g = axes([0, math.log2(T)], [lo, hi], x_length=6.0, y_length=3.6, xlabel=r"rounds of unmasking",
                 ylabel=r"bits per character, \ judged by another model", xticks=[], yticks=[lo, hi], center=[-3.0, 0.0, 0])
        g.add(*[MathTex(str(2 ** k), font_size=18, color=GREY_B).next_to(g.ax.c2p(k, lo), DOWN, buff=0.12) for k in range(int(math.log2(T)) + 1)])
        lx = lambda ws: [math.log2(int(w["steps"])) for w in ws]
        cc = VGroup(curve(g.ax, lx(conf), [w["judge"] for w in conf], MDM_C, 3),
                    *[Dot(g.ax.c2p(a, b), radius=0.05, color=MDM_C) for a, b in zip(lx(conf), [w["judge"] for w in conf])])
        cr = VGroup(curve(g.ax, lx(rnd), [w["judge"] for w in rnd], C.SURPRISE, 3),
                    *[Dot(g.ax.c2p(a, b), radius=0.05, color=C.SURPRISE) for a, b in zip(lx(rnd), [w["judge"] for w in rnd])])
        cb = VGroup(*[Square(0.14, color=C.BITS, fill_opacity=1).move_to(g.ax.c2p(math.log2(int(w["steps"])), w["judge"])) for w in blk])
        rl = DashedLine(g.ax.c2p(0, judge_real), g.ax.c2p(math.log2(T), judge_real), color=WHITE, stroke_width=1.5)
        al = DashedLine(g.ax.c2p(0, arw["judge"]), g.ax.c2p(math.log2(T), arw["judge"]), color=AR_C, stroke_width=1.5)
        lg = legend([(MDM_C, r"surest first"), (C.SURPRISE, r"at random"), (C.BITS, rf"in $4$ blocks, left to right"),
                     (AR_C, r"the autoregressive model's own samples"), (WHITE, r"real held-out text")], font_size=18)
        lg.move_to([3.9, 1.8, 0])
        # the cost: network evaluations to write T characters
        sams = VGroup(*[VGroup(label(rf"${int(w['steps'])}$ rounds:", font_size=17, color=GREY_A),
                               data_text(str(w["sample"])[:40], font=MONO, font_size=16, color=MDM_C)).arrange(RIGHT, buff=0.15)
                        for w in conf if int(w["steps"]) in (64, 8, 1)]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        sams.move_to([3.6, -1.4, 0])
        if sams.width > 6.4:
            sams.width = 6.4
        c64 = next(w for w in conf if int(w["steps"]) == T)
        c8 = next(w for w in conf if int(w["steps"]) == 8)
        c1 = next(w for w in conf if int(w["steps"]) == 1)
        r64 = next(w for w in rnd if int(w["steps"]) == T)
        conf_better = c64["judge"] < r64["judge"]
        order_note = (f"Revealing the surest guesses first reads better than revealing at random, {c64['judge']:.2f} "
                      f"against {r64['judge']:.2f} bits, though at random is what the bound describes." if conf_better
                      else f"Revealing at random reads as well as the surest-first rule, {r64['judge']:.2f} against "
                      f"{c64['judge']:.2f}.")
        b16 = next((w for w in blk if int(w["steps"]) == 16), None)
        w16 = next(w for w in conf if int(w["steps"]) == 16)
        blk_note = (f"Writing in four blocks, left to right, with sixteen rounds in all, scores {b16['judge']:.2f}, against "
                    f"{w16['judge']:.2f} for the whole string at once." if b16 else "")
        with self.voiceover(
            f"Writing {T} characters one round per character costs {T} network evaluations, like an autoregressive "
            "model. The promise of diffusion is fewer rounds, several characters each. How much does it cost in "
            "quality? Judge each sample by an autoregressive model of the other seed: lower reads more like the "
            f"novels; real text scores {judge_real:.2f}. <bookmark mark='a'/> With {T} rounds, {c64['judge']:.2f}; "
            f"with eight, {c8['judge']:.2f}; all at once, {c1['judge']:.2f}: guessing many characters independently, "
            "in one go, makes them disagree with each other. <bookmark mark='b'/> " + order_note
            + " <bookmark mark='c'/> " + blk_note
        ) as vo:
            self.play(FadeIn(g), FadeIn(lg), Create(rl), Create(al))
            vo.wait_until("a")
            self.play(Create(cc[0]), FadeIn(cc[1:]), FadeIn(sams))
            vo.wait_until("b")
            self.play(Create(cr[0]), FadeIn(cr[1:]))
            vo.wait_until("c")
            self.play(FadeIn(cb))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def frontier(self):
        cards = VGroup(
            history_card(2025, r"Arriola et al.: \ block diffusion", r"left to right across blocks, \ diffusion within each: \ "
                         r"any length, \ a key-value cache", color=HIST, width=4.3, font_size=17),
            history_card(2025, r"Inception Labs: \ Mercury", r"billed as the first commercial diffusion language models: \ "
                         r"$1{,}109$ tokens a second on an H100", color=HIST, width=4.3, font_size=17),
            history_card(2025, r"Google DeepMind: \ Gemini Diffusion", r"$1{,}479$ tokens a second, \ about the quality "
                         r"of Gemini 2.0 Flash-Lite on code", color=HIST, width=4.3, font_size=17),
            history_card(2025, r"Wu et al.: \ Fast-dLLM", r"an approximate cache, \ and decoding many tokens only when "
                         r"confident: \ up to $27.6\times$ faster", color=HIST, width=4.3, font_size=17),
            history_card(2025, r"Ant Group et al.: \ LLaDA2.0", r"$100$ billion parameters, \ converted from an "
                         r"autoregressive model", color=HIST, width=4.3, font_size=17),
            history_card(2026, r"Google: \ DiffusionGemma", r"open weights, \ $26$B (3.8B active), \ $256$ tokens per "
                         r"block, \ over $1{,}000$ tokens a second; \ below Gemma 4 in quality", color=HIST, width=4.3,
                         font_size=17),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.22, 0.25)).move_to(UP * 0.35)
        if cards.width > 13.4:
            cards.width = 13.4
        ta = take_away(r"Diffusion language models trade a little quality per parameter for writing many tokens at once.")
        with self.voiceover(
            "Fixed-length writing has a cost: nothing can be cached, and the length is set in advance. Marianne "
            "Arriola and colleagues' block diffusion splits the difference: blocks left to right, like an "
            "autoregressive model, diffusion inside each block. <bookmark mark='a'/> In 2025 Inception Labs launched "
            "Mercury, billed as the first commercial diffusion language models, at over a thousand tokens a second "
            "on one GPU; "
            "<bookmark mark='b'/> Google's Gemini Diffusion reported nearly fifteen hundred, at about the coding quality of "
            "a small Gemini; <bookmark mark='c'/> Fast-dLLM added caching and confident parallel decoding to open "
            "models, up to twenty-seven times faster; <bookmark mark='d'/> LLaDA two point oh reached a hundred "
            "billion parameters by converting an autoregressive model. <bookmark mark='e'/> And in June 2026 Google "
            "released DiffusionGemma with open weights: 256 tokens a block, over a thousand tokens a second on one "
            "GPU, and, in Google's own words, lower in quality than the standard Gemma 4. The trade is speed for a "
            "little quality, the one our two small models measured."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.1))
            for k, mk in enumerate("abcde", 1):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.1), run_time=0.7)
            self.play(FadeIn(ta, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()
