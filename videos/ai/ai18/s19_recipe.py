from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai18.common import (BASE_C, C_COL, D_COL, F, FULL_C, MONO, N_COL, PART, load, said, spoken_int,
                                   take_away)


class Recipe(VoiceoverScene):
    def construct(self):
        self.card()
        self.same_run()
        self.replay()
        self.result()
        self.board()

    def card(self):
        card = chapter_card(18, r"Our own full recipe", r"Does the 2026 recipe beat the 2020 one, at equal "
                            r"compute?", part=PART)
        with self.voiceover("Chapter eighteen. Our own full recipe."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def same_run(self):
        b, f = load("recipe_base"), load("recipe_full")
        sb, sf = b["spec"], f["spec"]
        same = VGroup(
            label(rf"the same model: \ ${sb['d']}$ wide, \ ${sb['layers']}$ layers, \ "
                  rf"${b['counts']['total'] / 1e6:.2f}$M parameters", font_size=24, color=N_COL),
            label(rf"the same ${b['tokens'] / 1e6:.1f}$M tokens of the thirty novels, \ in the same order", font_size=24,
                  color=D_COL),
            label(rf"the same ${sb['steps']}$ steps, \ peak learning rate, \ seed, \ FP32 arithmetic", font_size=24,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(UP, buff=0.5)
        cols = VGroup(
            VGroup(label(r"2020 recipe", font_size=30, color=BASE_C),
                   label(r"AdamW", font_size=24), label(r"cosine schedule", font_size=24),
                   label(r"plain attention", font_size=24), label(r"no z-loss", font_size=24)),
            VGroup(label(r"2026 recipe", font_size=30, color=FULL_C),
                   label(r"Muon for the hidden matrices", font_size=24), label(r"warmup--stable--decay", font_size=24),
                   label(r"QK-norm", font_size=24), label(r"z-loss $10^{-4}$", font_size=24)),
        )
        for c in cols:
            c.arrange(DOWN, buff=0.22)
        cols.arrange(RIGHT, buff=1.8).move_to(DOWN * 1.0)
        boxes = VGroup(*[SurroundingRectangle(c, buff=0.25, corner_radius=0.12, color=col, stroke_width=2)
                         for c, col in zip(cols, (BASE_C, FULL_C))])
        left_out = note(r"not included: \ FP8 and two-token prediction \ (chapters 14 and 16)", font_size=18)
        left_out.to_edge(DOWN, buff=0.3)
        Mt, MC = load("mtp"), load("mtp_cost")
        mfin = Mt["final"]
        mtp_gain = np.mean(mfin["0"]) - np.mean(mfin["0.3"])
        mtp_spread = max(abs(mfin["0"][0] - mfin["0"][1]), abs(mfin["0.3"][0] - mfin["0.3"][1]))
        if mtp_gain > max(mtp_spread, 0.01):  # the same test as chapter sixteen's
            out_ = (f"Two-token prediction stays out although it helped a little in chapter sixteen: it costs "
                    f"{100 * MC['extra_share']:.0f} percent more arithmetic, and the comparison must be at equal "
                    "compute. Eight-bit arithmetic stays out too: on a CPU it only emulates the saving.")
        else:
            out_ = ("Two-token prediction stays out: it gave no gain at our scale in chapter sixteen, and it costs "
                    "extra compute, which would make the comparison unequal. Eight-bit arithmetic stays out too: on a "
                    "CPU it only emulates the saving.")
        with self.voiceover(
            "Now we put the pieces together. Two models of the same shape, trained on the same three million tokens of "
            "the thirty novels, in the same order, from the same starting weights; and the whole comparison again from "
            "a second seed. <bookmark mark='a'/> One with the recipe of 2020: AdamW, a cosine schedule, plain "
            "attention. "
            "<bookmark mark='b'/> One with the recipe of 2026: Muon for the hidden matrices, warmup, stable, decay, "
            "QK-norm and the z-loss. <bookmark mark='c'/> " + out_
        ) as vo:
            self.play(LaggedStart(*[FadeIn(s_) for s_ in same], lag_ratio=0.4), FadeIn(VGroup(cols, boxes).copy().set_opacity(0.15)),
                      run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(cols[0]), Create(boxes[0]))
            vo.wait_until("b")
            self.play(FadeIn(cols[1]), Create(boxes[1]))
            vo.wait_until("c")
            self.play(FadeIn(left_out))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        b, f = load("recipe_base"), load("recipe_full")
        eb, ef = np.asarray(b["evals"]), np.asarray(f["evals"])
        lo = math.floor(min(eb[:, 2].min(), ef[:, 2].min()) * 2) / 2 - 0.25
        hi = 8.5
        steps = b["spec"]["steps"]
        g = axes([0, steps], [lo, hi], x_length=6.0, y_length=4.2, xlabel=r"step",
                 ylabel=r"held-out loss (nats per token)", xticks=[0, steps // 2, steps], yticks=[lo, hi],
                 yfmt=lambda v: f"{v:.1f}", center=[-3.4, -0.3, 0], font_size=18)
        sn_b, sn_f = b["snaps"], f["snaps"]
        steps_ = [s["step"] for s in sn_f]
        pts_b = VGroup(*[Dot(g.ax.c2p(s["step"], min(s["val"], hi)), radius=0.06, color=BASE_C) for s in sn_b])
        pts_f = VGroup(*[Dot(g.ax.c2p(s["step"], min(s["val"], hi)), radius=0.06, color=FULL_C) for s in sn_f])
        cb = curve(g.ax, eb[:, 0], np.minimum(eb[:, 2], hi), BASE_C, 2.5)
        cf = curve(g.ax, ef[:, 0], np.minimum(ef[:, 2], hi), FULL_C, 2.5)
        S1 = load("recipe_seed1")  # the second seed of each recipe, dashed
        s1 = VGroup(*[DashedVMobject(curve(g.ax, np.asarray(S1[k]["evals"])[:, 0],
                                           np.minimum(np.asarray(S1[k]["evals"])[:, 2], hi), col, 2), num_dashes=40)
                      for k, col in (("base", BASE_C), ("full", FULL_C)) if S1[k].get("evals")])
        s1n = note(r"dashed: \ the second seed", font_size=16).next_to(g, DOWN, buff=0.05).align_to(g, RIGHT)
        prompt = data_text("The door opened, and", font=MONO, font_size=20, color=GREY_A).move_to([3.4, 3.1, 0])

        def clean(t):  # bytes the tokenizer can't decode show as '?'
            return "".join(c if c.isprintable() and c != "\ufffd" else "?" for c in t)

        def boxes(sn, col, y):
            return [said(clean(s["sample"]), chars=36, font_size=17, max_lines=3, box_color=col).move_to([3.4, y, 0])
                    for s in sn]

        bx_b, bx_f = boxes(sn_b, BASE_C, 1.55), boxes(sn_f, FULL_C, -0.6)
        lb = label(r"2020 recipe", font_size=20, color=BASE_C).next_to(bx_b[-1], UP, buff=0.08)
        lf = label(r"2026 recipe", font_size=20, color=FULL_C).next_to(bx_f[-1], UP, buff=0.08)
        stp = [label(rf"after ${s['step']}$ steps \ (${s['tokens'] / 1e6:.2f}$M tokens)", font_size=20,
                     color=GREY_A).move_to([3.4, -2.4, 0]) for s in sn_f]
        tag = note(r"computed: \ the same seed for every sample", font_size=18).to_corner(DR, buff=0.2)
        first = sn_f[0]
        with self.voiceover(
            "Watch them learn. On the left, each model's loss on text it never trains on; on the right, what each "
            "writes after the words 'The door opened, and', frozen at the same steps, with the same random seed. "
            f"<bookmark mark='a'/> At the start both write noise, at a loss of about {first['val']:.1f} nats. "
            "<bookmark mark='b'/> Let them read. <bookmark mark='c'/> By the end, compare what they write; the curves "
            "tell which learned faster."
        ) as vo:
            self.play(FadeIn(g), FadeIn(prompt), FadeIn(lb), FadeIn(lf), FadeIn(tag))
            self.play(FadeIn(pts_b[0]), FadeIn(pts_f[0]), FadeIn(bx_b[0]), FadeIn(bx_f[0]), FadeIn(stp[0]))
            vo.wait_until("a")
            self.play(Indicate(VGroup(pts_b[0], pts_f[0]), color=YELLOW))
            vo.wait_until("b")
            per = max(0.8, vo.until("c") / max(1, len(steps_) - 1))
            cur = [bx_b[0], bx_f[0], stp[0]]
            for k in range(1, len(steps_)):
                self.play(FadeIn(pts_b[k], scale=1.5), FadeIn(pts_f[k], scale=1.5),
                          ReplacementTransform(cur[0], bx_b[k]), ReplacementTransform(cur[1], bx_f[k]),
                          ReplacementTransform(cur[2], stp[k]), run_time=0.6 * per)
                cur = [bx_b[k], bx_f[k], stp[k]]
                self.wait(0.4 * per)
            vo.wait_until("c")
            self.play(Create(cb), Create(cf), run_time=1.5)
            if len(s1):
                self.play(Create(s1), FadeIn(s1n), run_time=1.2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def result(self):
        R, M = load("recipe"), load("mfu")
        b, f = R["base"], R["full"]
        mb, mf = float(np.mean(b["seeds_bits"])), float(np.mean(f["seeds_bits"]))
        sp = max(abs(b["seeds_bits"][0] - b["seeds_bits"][1]), abs(f["seeds_bits"][0] - f["seeds_bits"][1]))
        bl_, fl_ = max(b["seeds_max_logit"]), max(f["seeds_max_logit"])
        two = lambda v, k: rf"{v[0]:.{k}f} \ / \ {v[1]:.{k}f}"  # noqa: E731
        rows = [(r"held-out loss (nats per token)", two(b["seeds_val"], 3), two(f["seeds_val"], 3)),
                (r"bits per character, \ the scoreboard's passage", two(b["seeds_bits"], 3), two(f["seeds_bits"], 3)),
                (r"largest attention logit", two(b["seeds_max_logit"], 0), two(f["seeds_max_logit"], 0)),
                (r"training time on this computer (min)", f"{b['seconds'] / 60:.0f}", f"{f['seconds'] / 60:.0f}")]
        xs = [-3.3, 1.6, 4.9]
        hd = VGroup(label(r"2020 recipe", font_size=24, color=BASE_C).move_to([xs[1], 2.4, 0]),
                    label(r"2026 recipe", font_size=24, color=FULL_C).move_to([xs[2], 2.4, 0]))
        body = VGroup()
        for i, (nm, a, c) in enumerate(rows):
            y = 1.6 - 0.75 * i
            body.add(VGroup(label(nm, font_size=22, color=GREY_A).move_to([xs[0], y, 0]),
                            label(f"${a}$", font_size=23, color=BASE_C).move_to([xs[1], y, 0]),
                            label(f"${c}$", font_size=23, color=FULL_C).move_to([xs[2], y, 0])))
        d = mb - mf
        rel = d / mb
        if d > max(sp, 0.01):
            verdict = (f"The 2026 recipe wins: {mf:.3f} bits per character on the scoreboard's passage, against "
                       f"{mb:.3f}, the mean of two seeds each: {100 * rel:.1f} percent better with exactly the same "
                       f"model, data and steps, and more than the {sp:.3f} between seeds.")
        elif -d > max(sp, 0.01):
            verdict = (f"The 2020 recipe wins here: {mb:.3f} bits per character against {mf:.3f}, the mean of two "
                       "seeds each. At our scale, and with one untuned learning rate for both, the new recipe's "
                       "advantages don't show.")
        else:
            verdict = (f"They tie: {mb:.3f} and {mf:.3f} bits per character, the mean of two seeds each, closer than "
                       f"the {sp:.3f} between seeds. At our scale the new recipe neither helps nor hurts.")
        if fl_ < 0.5 * bl_:
            stab = (f"And the 2026 recipe's attention stayed tamer: its largest logit was {fl_:.0f}, against "
                    f"{bl_:.0f}.")
        else:
            stab = (f"Its largest attention logit was {fl_:.0f}, against {bl_:.0f}: at this learning rate neither "
                    "model's attention ran away.")
        tag = note(rf"computed: \ ${b['tokens'] / 1e6:.1f}$M tokens each; \ seed $0$ \ / \ seed $1$",
                   font_size=18).to_corner(DR, buff=0.2)
        with self.voiceover(
            "The scores. <bookmark mark='a'/> " + verdict + " <bookmark mark='b'/> " + stab
        ) as vo:
            self.play(FadeIn(hd), FadeIn(tag), FadeIn(body[0]))
            vo.wait_until("a")
            self.play(FadeIn(body[1]), FadeIn(body[3]))
            vo.wait_until("b")
            self.play(FadeIn(body[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def board(self):
        S, R = load("scoreboard"), load("recipe")
        names = {"recipe_base": rf"our 2020 recipe, \ ${R['base']['params'] / 1e6:.1f}$M",
                 "recipe_full": rf"our 2026 recipe, \ ${R['full']['params'] / 1e6:.1f}$M"}
        rows = []
        for r in S["rows"]:
            lab = names.get(r.get("name"), r["label"])
            if r.get("name") == "base":
                lab = rf"the series' model, \ ${r['params'] / 1e6:.1f}$M"
            elif r.get("name", "").startswith("gpt_"):
                lab = rf"Part 14, \ {r['label'].split('model ')[-1]}, \ ${r['params'] / 1e6:.1f}$M"
            rows.append(dict(label=lab, bits=r["bits"], kind=r["kind"]))
        hl = tuple(i for i, r in enumerate(S["rows"]) if r.get("part") == 18)
        rh = min(0.46, 5.0 / len(rows))
        board = scoreboard(rows, highlight=hl, max_bits=4.0, row_h=rh, font_size=20 if rh > 0.42 else 18,
                           bar_width=5.6, label_width=4.6).scale(0.92).move_to([0, 0.2, 0])
        bl = label(r"bits per character on the scoreboard's passage", font_size=22, color=GREY_B)
        bl.next_to(board, UP, buff=0.15)
        base_row = next(r for r in S["rows"] if r.get("name") == "base")
        from explainer.ai.novels import BASE_RUN

        times = BASE_RUN["tokens"] / R["full"]["tokens"]
        gm = next(r for r in S["rows"] if r.get("name") == "gpt_m")
        f = R["full"]
        sp = abs(f["seeds_bits"][0] - f["seeds_bits"][1])  # the board shows seed 0; better only beyond the seeds' gap
        if f["bits"] < gm["bits"] - max(sp, 0.01):
            vs14 = (f"Our 2026 model scores {f['bits']:.2f}, better than Part 14's model of the same size, "
                    f"{gm['bits']:.2f}, which read the same number of tokens.")
        else:
            vs14 = (f"Our 2026 model scores {f['bits']:.2f}, against {gm['bits']:.2f} for Part 14's model of the same "
                    "size, which read the same number of tokens.")
        tw = take_away(r"the recipe is the lab's craft; \ the scale is what it buys", color=FULL_C, font_size=26)
        if any(r.get("name", "").startswith("p1_") for r in S["rows"]):
            top_rows = ("Part 1's compressors and counts at the top, then the published models Part 1 measured, "
                        "GPT-2 and Qwen3, then Part 14's family")
        else:
            top_rows = "Part 1's compressors and counts at the top, then Part 14's family"
        with self.voiceover(
            "And on the series' scoreboard, the bits per character each model needs for chapter two of The Maltese "
            "Falcon. <bookmark mark='a'/> " + top_rows + ", and the "
            f"series' own model of {base_row['params'] / 1e6:.1f} million parameters, trained on {times:.0f} times our "
            f"tokens, at {base_row['bits']:.2f}. <bookmark mark='b'/> " + vs14 + " <bookmark mark='c'/> A recipe "
            "buys efficiency: the same quality for less compute. The frontier labs spend that saving on scale."
        ) as vo:
            self.play(FadeIn(bl), FadeIn(board.axis), *[FadeIn(board.rows[i].name) for i in range(len(board.rows))
                                                         if i not in hl])
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for i, r_ in enumerate(board.rows) if i not in hl], lag_ratio=0.15),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(board.rows[i], shift=RIGHT * 0.1) for i in hl], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(tw, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
