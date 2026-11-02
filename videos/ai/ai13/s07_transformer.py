from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai13.common import (A, K, MONO, OURS, PART, Q, V, curve, framed, heat_image, layernorm_picture,
                                  layernorm_stage, load)


def board_rows():
    """Selected historical Part1, KN, neural/mixture and TF reports; distinct target cohorts."""
    from videos.ai.ai1 import compute as c1
    from videos.ai.ai7 import compute as c6
    from videos.ai.ai9 import compute as c8

    t, k, n = load("tf"), c6.load("kn"), c8.load("lm")
    rows = [dict(r) for r in c1.load("scoreboard")["rows"]]
    i = next(j for j, r in enumerate(rows) if r["key"] == "best") + 1
    rows.insert(i, dict(key="kn", label=rf"Kneser--Ney, \ ${k['best']}$ characters", bits=k["best_bits"], part=7, kind="count"))
    rows.insert(i + 1, dict(key="nlm", label=rf"a neural model, \ ${n['n_ctx']}$ characters", bits=n["passage_bits"], part=9,
                            kind="lm"))
    rows.insert(i + 2, dict(key="mix", label=r"the neural model $+$ Kneser--Ney", bits=n["mix_bits"], part=9, kind="lm"))
    rows.insert(i + 3, dict(key="tf", label=rf"our transformer, \ ${t['ctx']}$ characters", bits=t["passage_bits"], part=13,
                            kind="lm"))
    assert int(t["ctx"]) == 256 and int(n["n_ctx"]) == 24 and int(k["best"]) == 7, "Re-audit target annotations if recipe changes"
    scopes = {
        "kn": dict(targets=(7,21405),count=21399,unit="bits per Unicode character"),
        "nlm": dict(targets=(24,21405),count=21382,unit="bits per Unicode character"),
        "mix": dict(targets=(24,21405),count=21382,unit="bits per Unicode character"),
        "tf": dict(targets=(1,21376),count=21376,unit="bits per Unicode character"),
    }
    for row in rows:
        row["cohort"] = scopes.get(row["key"],dict(kind="Part1 historical report; metric and coverage vary"))
        if row["key"] in scopes:
            row["cohort"].update(index_convention="zero-based inclusive")
    return rows, i + 3, n, k


class Transformer(VoiceoverScene):
    def construct(self):
        self.card()
        self.block()
        self.train()
        self.replay()
        self.board()

    def card(self):
        card = chapter_card(6, r"Our own transformer", r"What does a whole transformer look like, and how does it learn?",
                            part=PART, lit=(2017,))
        with self.voiceover("Chapter six. Our own transformer."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def block(self):
        t = load("tf")
        word = "Spade"
        n = len(word)
        xs = np.linspace(-4.6, -0.6, n)
        cells = 8
        g = np.random.default_rng(1)

        def column(x, seed_shift=0.0):
            vals = g.normal(size=cells)
            return VGroup(*[Square(0.26, stroke_width=0.8, stroke_color=GREY_D, fill_color=C.EMBED,
                                   fill_opacity=float(0.2 + 0.6 * min(abs(v) / 2, 1))) for v in vals]).arrange(DOWN, buff=0)
        cols = VGroup(*[column(x).move_to([x, 0.2, 0]) for x in xs])
        chars = VGroup(*[Text(ch, font=MONO, font_size=30, color=GREY_A).next_to(c_, DOWN, buff=0.25) for ch, c_ in zip(word, cols)])
        stream = label(r"each character: \ a vector of $" + str(t["d"]) + r"$ numbers \ (the residual stream)",
                       font_size=24, color=C.EMBED).to_edge(UP, buff=0.4)
        # attention: arrows between columns (later reads earlier)
        att = VGroup(*[CurvedArrow(cols[j].get_top() + UP * 0.1, cols[i].get_top() + UP * 0.1, angle=-PI / 3, color=A,
                                   stroke_width=2.5, tip_length=0.14)
                       for i in range(1, n) for j in range(i) if (i - j) <= 2])
        at_l = label(r"attention: \ moves information \\ between positions", font_size=26, color=A).move_to([3.6, 1.6, 0])
        mlp = VGroup(*[RoundedRectangle(width=0.5, height=0.5, corner_radius=0.08, stroke_color=C.BITS, stroke_width=2.5)
                       .move_to(c_.get_center()) for c_ in cols])
        ml_l = label(r"MLP \ (multilayer perceptron): \\ Part 9's small network, \\ on each position on its own", font_size=26,
                     color=C.BITS).move_to([3.6, -0.1, 0])
        colors = {r"\mathrm{Attn}": A, r"\mathrm{MLP}": C.BITS}
        eqs = VGroup(cmath(r"x \leftarrow x +", r"\mathrm{Attn}", r"(\mathrm{LN}(x))", colors=colors, font_size=34),
                     cmath(r"x \leftarrow x +", r"\mathrm{MLP}", r"(\mathrm{LN}(x))", colors=colors, font_size=34))
        eqs.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.6, -1.9, 0])
        rep = label(rf"one block; \ ours stacks ${t['layers']}$", font_size=24, color=GREY_A).next_to(eqs, DOWN, buff=0.2)
        cite_ = cite(r"A.~Vaswani et al., \textit{Attention Is All You Need} (2017)", corner=DL)
        lnc = gloss(r"LN, \ layer normalization", r"shift a vector's numbers to average $0$, \\ then rescale them to a "
                    r"standard spread of $1$ \ (Part 9)", layernorm_picture(), width=4.6, color=C.TRUE_P).move_to([3.6, 0.85, 0])
        lnp = lnc[1][-1]
        with self.voiceover(
            f"Now build one. Each character enters as a vector, Part 3's idea, {t['d']} numbers here. "
            "The column of vectors is the residual stream from Part 9: every layer reads from it and adds back "
            "to it. <bookmark mark='a'/> A transformer block has two halves. Attention moves information between "
            "positions: each character gathers from the ones before it. <bookmark mark='b'/> Then an MLP, a "
            "multilayer perceptron: Part 9's small network of weighted sums and bends, applied to each position "
            "on its own, like thinking over what was gathered. "
            "<bookmark mark='c'/> Each half first normalizes its input, with Part 9's layer norm: "
            "<bookmark mark='n'/> it shifts the vector's numbers to an average of zero, and rescales them to a standard "
            "size. Then the half adds its output back to the stream. Stack four blocks, read off a guess for the next "
            "character, and that is the whole machine: the mask from chapter five, the heads from chapter four."
        ) as vo:
            self.play(FadeIn(stream), LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cols], lag_ratio=0.15),
                      FadeIn(chars), FadeIn(cite_))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(a_) for a_ in att], lag_ratio=0.1), FadeIn(at_l), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeOut(att), LaggedStart(*[Create(m) for m in mlp], lag_ratio=0.1), FadeIn(ml_l))
            self.play(*[Indicate(c_, color=C.BITS, scale_factor=1.05) for c_ in cols])
            vo.wait_until("c")
            self.play(FadeOut(mlp), FadeOut(at_l), FadeOut(ml_l), Write(eqs), FadeIn(rep))
            self.play(FadeIn(lnc, shift=UP * 0.2))
            vo.wait_until("n")
            self.play(Transform(lnp[2], layernorm_stage(lnp, 1)), run_time=1.2)
            self.play(Transform(lnp[2], layernorm_stage(lnp, 2)), run_time=1.2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def train(self):
        t = load("tf")
        cv = np.asarray(t["curve"])
        lo = float(np.floor(cv[:, 1:].min() * 4) / 4 - 0.25)
        hi = float(np.ceil(cv[:, 1:].max()))
        ax = Axes(x_range=[0, float(t["steps"]), float(t["steps"]) / 4], y_range=[lo, hi, 0.5], x_length=7.6, y_length=4.4,
                  tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05})
        ax.move_to([-2.2, -0.5, 0])
        yt = VGroup(*[MathTex(f"{v:.1f}", font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in np.arange(np.ceil(lo * 2) / 2, hi + 0.01, 0.5)])
        xt = VGroup(*[MathTex(f"{int(v):,}".replace(",", "{,}"), font_size=22, color=GREY_B).next_to(ax.c2p(v, lo), DOWN, buff=0.1)
                      for v in np.linspace(0, float(t["steps"]), 5)])
        xn = label(r"training steps", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        yn = label(r"bits per character", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        steps = cv[:, 0]
        key = VGroup(label(r"held-out novels \\ first $60{,}000$ source characters \\ $59{,}904$ scored targets",
                           font_size=19, color=GREY_B),
                     label(r"passage \\ targets $1$--$21{,}376$ \\ $21{,}376$ scored targets",
                           font_size=19, color=OURS))
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.6, 2.1, 0])
        facts = VGroup(label(rf"${t['n_params'] / 1e6:.1f}$ million numbers", font_size=26, color=WHITE),
                       label(rf"${t['tokens'] / 1e6:.0f}$ million training positions", font_size=26, color=WHITE),
                       label(rf"${t['ctx']}$ characters of context", font_size=26, color=WHITE),
                       label(r"trained on a CPU", font_size=24, color=GREY_B),
                       label(rf"final validation: ${float(t['valid_bits']):.2f}$ bits \\ first $400{{,}}000$ source characters \\ "
                             r"$399{,}872$ scored targets", font_size=18, color=GREY_B))
        facts.arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(key, DOWN, buff=0.5).align_to(key, LEFT)
        keep_in_frame(facts)  # clear of the reference lines' names, which sit at the end of the curves
        index_note = note(r"target indices are zero-based and inclusive").to_edge(DOWN, buff=0.15)
        pb = float(t["passage_bits"])
        verdict = (f"It reports {pb:.2f} bits a character over 21,376 passage targets. The checkpoint validation "
                   "curve uses the first sixty thousand source characters; the final validation report uses the "
                   "first four hundred thousand. These original measurements use different targets from the "
                   "historical counting and neural scores, so they do not establish a ranking between models.")
        with self.voiceover(
            f"Ours has {t['layers']} blocks, {t['heads']} heads in each and {t['n_params'] / 1e6:.1f} million numbers, and "
            f"reads {t['ctx']} characters at a time. We trained it on the thirty novels, with about "
            f"{t['tokens'] / 1e6:.0f} million sampled character targets, on an ordinary processor, without a graphics card. "
            f"<bookmark mark='a'/> {verdict}"
        ) as vo:
            self.play(Create(ax), FadeIn(yt), FadeIn(xt), FadeIn(xn), FadeIn(yn), FadeIn(facts), FadeIn(index_note))
            self.play(FadeIn(key))
            # training, replayed: both curves draw as a step counter runs, the passage's bits riding on its curve
            tk = ValueTracker(float(steps[0]))

            def upto(col, color, sw):
                def build():
                    s_ = tk.get_value()
                    xs_ = [float(steps[0])] + [x_ for x_ in steps[1:] if x_ < s_] + [max(s_, float(steps[0]) + 1.0)]
                    ys_ = np.interp(xs_, steps, cv[:, col])
                    return VMobject(color=color, stroke_width=sw).set_points_as_corners([ax.c2p(a_, b_) for a_, b_ in zip(xs_, ys_)])
                return always_redraw(build)

            def head_at(col):
                return ax.c2p(tk.get_value(), float(np.interp(tk.get_value(), steps, cv[:, col])))

            lv, lp = upto(1, GREY_B, 3), upto(2, OURS, 4)
            hd = always_redraw(lambda: Dot(head_at(2), radius=0.08, color=OURS))
            sc = always_redraw(lambda: MathTex(rf"\text{{step }}{int(round(tk.get_value())):,}".replace(",", "{,}"), font_size=30,
                                               color=OURS).move_to(ax.c2p(0.72 * float(t["steps"]), hi - 0.2)))
            rl = label(r"the passage", font_size=24, color=OURS).move_to(ax.c2p(0.72 * float(t["steps"]), hi - 0.2) + DOWN * 0.45)
            rl.shift(LEFT * 0.35)
            rd = always_redraw(lambda: DecimalNumber(float(np.interp(tk.get_value(), steps, cv[:, 2])), num_decimal_places=2,
                                                     font_size=28, color=OURS).next_to(rl, RIGHT, buff=0.15))
            self.add(lv, lp, hd, sc, rl, rd)
            self.play(tk.animate.set_value(float(steps[-1])), run_time=5.0, rate_func=linear)
            for m_ in (lv, lp, hd, rd, sc):
                m_.clear_updaters()
            self.remove(hd)
            vo.wait_until("a")
            end = glow_dot(lp.get_end(), color=OURS, radius=0.09)
            self.play(FadeIn(end, scale=0.5), Indicate(key[1], color=OURS))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        t, w = load("tf"), load("tfwords")
        steps = [int(s_) for s_ in t["snap_steps"]]
        bits = np.asarray(t["snap_bits"], float)
        smp = [str(x) for x in t["snap_samples"]]
        M = np.asarray(t["snap_maps"], float)  # checkpoint, layer, head, query, key
        real = np.asarray(w["real"], float)
        L, H = M.shape[1], M.shape[2]
        K_ = int(t["K"])
        # the bits at each checkpoint, with a dot that walks along them
        hi = math.ceil(bits.max())
        lo = math.floor(bits.min() * 2) / 2
        ax = Axes(x_range=[0, steps[-1], steps[-1] / 3], y_range=[lo, hi, 1], x_length=4.6, y_length=2.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-4.3, 1.75, 0])
        yl = label(r"bits per character, \ on the passage", font_size=18, color=GREY_A).next_to(ax, UP, buff=0.1)
        yl.align_to(ax, LEFT)
        yt = VGroup(*[MathTex(str(v), font_size=18, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.08)
                      for v in range(int(lo + 0.99), hi + 1, max(1, (hi - int(lo)) // 3))])
        cv = curve(ax, steps, bits, OURS, 3)
        tk = ValueTracker(0)

        def at():
            return float(np.interp(tk.get_value(), steps, bits))

        dot = always_redraw(lambda: Dot(ax.c2p(tk.get_value(), at()), radius=0.08, color=OURS))
        cnt = always_redraw(lambda: MathTex(rf"\text{{step }}{int(round(tk.get_value())):,}".replace(",", "{,}"),
                                            font_size=28, color=OURS).next_to(ax, DOWN, buff=0.25))

        def text_at(k):
            body = " ".join(smp[k].replace("\n", " ").split())
            lines = [body[i:i + 40] for i in range(0, min(len(body), 120), 40)]
            g = VGroup(data_text(str(t["prompt"]).strip(), font="DejaVu Serif", font_size=18, color=GREY_B),
                       *[data_text(ln, font="DejaVu Serif", font_size=18, color=WHITE) for ln in lines])
            g.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([1.0, 1.85, 0], aligned_edge=LEFT)
            if g.get_right()[0] > 6.8:
                g.scale((6.8 - g.get_left()[0]) / g.width, about_edge=LEFT)
            return g

        def real_at(k):
            return label(rf"real words: \ ${100 * real[k]:.0f}\%$", font_size=24, color=C.TRUE_P).move_to([5.4, 0.35, 0])

        S = 0.76

        def maps_at(k):
            groups = Group()
            for l_ in range(L):
                groups.add(Group(*[heat_image(M[k, l_, h], S, S, color=A, gamma=0.35, mask_upper=True) for h in range(H)])
                           .arrange(RIGHT, buff=0.06))
            return groups.arrange(RIGHT, buff=0.35).move_to([0, -2.05, 0])

        maps = maps_at(0)
        lls = VGroup(*[label(rf"layer {l_ + 1}", font_size=18, color=GREY_B).next_to(maps[l_], UP, buff=0.1)
                       for l_ in range(L)])
        mcap = note(r"every head's attention on a sentence of the passage, \ at the same moment of training")
        mcap.next_to(maps, DOWN, buff=0.12)
        txt, rw = text_at(0), real_at(0)
        wh = label(r"what it writes:", font_size=20, color=GREY_A).next_to(txt, UP, buff=0.15).align_to(txt, LEFT)
        idx = {s_: i for i, s_ in enumerate(steps)}
        k1 = idx.get(250, 3)
        k2 = idx.get(1000, len(steps) // 2)
        half = bits[0] - 0.5 * (bits[0] - bits[-1])
        s_half = next(s_ for s_, b in zip(steps, bits) if b <= half)
        u = math.log2(K_)
        with self.voiceover(
            "Here is what it knows at each moment of its training: its score on the passage, what it writes after "
            "the same opening words, and where all sixteen heads look. <bookmark mark='a'/> At the start its "
            f"guesses are random, {bits[0]:.1f} bits a character, a little worse than a uniform guess over its "
            f"{K_} characters, {u:.1f}. It writes noise, and its attention is a blur. <bookmark mark='b'/> By step "
            f"{steps[k1]}, {bits[k1]:.2f} bits; {real[k1]:.0%} of the words it writes are real words, and the "
            f"heads have begun to differ. <bookmark mark='c'/> By step {steps[k2]:,}, {bits[k2]:.2f} bits and "
            f"{real[k2]:.0%} real words. <bookmark mark='d'/> At the end, after {steps[-1]:,} steps, "
            f"{bits[-1]:.2f} bits and {real[-1]:.0%} real words. Half of the whole improvement came in the first "
            f"{s_half:,} steps; the rest is slow polish."
        ) as vo:
            self.play(Create(ax), FadeIn(yl), FadeIn(yt), FadeIn(maps), FadeIn(lls), FadeIn(mcap), FadeIn(txt),
                      FadeIn(wh), FadeIn(rw))
            self.add(dot, cnt)
            vo.wait_until("a")
            self.play(Create(cv), run_time=1.0)
            for k in range(1, len(steps)):
                mark = {k1: "b", k2: "c", len(steps) - 1: "d"}.get(k)
                if mark:
                    vo.wait_until(mark)
                nm, nt, nr = maps_at(k), text_at(k), real_at(k)
                self.play(tk.animate.set_value(steps[k]), FadeOut(maps), FadeIn(nm), FadeOut(txt), FadeIn(nt),
                          FadeOut(rw), FadeIn(nr), run_time=0.9)
                maps, txt, rw = nm, nt, nr
        for m_ in (dot, cnt):
            m_.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def board(self):
        t = load("tf")
        rows, i, n, k = board_rows()
        # Preserve original values and separate their audited target cohorts in presentation.
        historical = [r for r in rows if r["key"] not in ("kn", "nlm", "mix", "tf")]
        legacy = scoreboard(historical, max_bits=8.0)
        legacy.scale_to_fit_width(6.4)
        if legacy.height > 5.1:
            legacy.scale_to_fit_height(5.1)
        legacy.move_to([-3.5, -0.25, 0])
        legacy_cap = label(r"Part 1: historical reports \\ mixed metrics and coverage", font_size=20,
                           color=GREY_B).next_to(legacy, UP, buff=0.2)
        title = label(r"Selected reports by target coverage", font_size=30).to_edge(UP, buff=0.25)

        def report(title_text, score_rows, scope, y):
            box = RoundedRectangle(width=6.1, height=1.65, corner_radius=0.1, stroke_color=GREY_D,
                                   stroke_width=1.5).move_to([3.55, y, 0])
            title_ = label(title_text, font_size=23, color=OURS).move_to(box.get_top()+DOWN*0.25)
            body = VGroup(*[VGroup(label(name, font_size=20), MathTex(f"{value:.2f}", font_size=25, color=col))
                            .arrange(RIGHT, buff=0.25) for name,value,col in score_rows])
            body.arrange(RIGHT, buff=0.45).move_to([3.55, y+0.03, 0])
            scope_ = label(scope, font_size=17, color=GREY_B).move_to(box.get_bottom()+UP*0.25)
            return VGroup(box,title_,body,scope_)

        tf_report = report(r"Part 13: our transformer", [(r"bits/character",float(t["passage_bits"]),OURS)],
                           r"targets $1$--$21{,}376$; $21{,}376$ scored", 1.95)
        kn_report = report(r"Part 7: Kneser--Ney", [(r"bits/character",float(k["best_bits"]),C.TRUE_P)],
                           r"targets $7$--$21{,}405$; $21{,}399$ scored", 0.15)
        neural_report = report(r"Part 9: neural and mixture",
                               [(r"neural",float(n["passage_bits"]),C.NEURAL),
                                (r"neural $+$ KN",float(n["mix_bits"]),C.NEURAL)],
                               r"targets $24$--$21{,}405$; $21{,}382$ scored", -1.65)
        scope_note = note(r"target indices: zero-based, inclusive; different contexts \\ no common-target ranking")
        scope_note.to_edge(DOWN,buff=0.15)
        glow = SurroundingRectangle(tf_report, color=OURS, buff=0.06, corner_radius=0.08)
        gpt = next((r for r in historical if "GPT-2 small" in r["label"]), None)
        more = (f"GPT-2 small, at {gpt['bits']:.2f}, is also a stack of attention blocks, about "
                f"{round(124e6 / t['n_params'], -1):.0f} times bigger. Its report covers the full tokenized passage. "
                "Its training data, position design and compute budget also differ; this is historical context, "
                "not a controlled measure of scale alone." if gpt else
                "The large models of Part 1 also stack attention blocks, with different training data, position "
                "designs, budgets and score coverage. These reports do not isolate the effect of scale.")
        with self.voiceover(
            f"On the scoreboard, a new row: our transformer, {float(t['passage_bits']):.2f}. "
            "The reports are separated here because they score different target sets. <bookmark mark='a'/> "+more
        ) as vo:
            self.play(FadeIn(legacy),FadeIn(legacy_cap),FadeIn(title),FadeIn(tf_report),FadeIn(kn_report),
                      FadeIn(neural_report),FadeIn(scope_note))
            self.play(Create(glow))
            vo.wait_until("a")
            if gpt:
                self.play(Indicate(legacy.rows[next(j for j,r in enumerate(historical) if r is gpt)],color=C.NEURAL))
        self.wait(0.6)
        self.clear_scene()
