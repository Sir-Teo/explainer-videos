from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai14.common import (CONTEXT, DECODER, MONO, PART, PRIOR, SIZE_COLORS, F, human, load, said, take_away)
from videos.ai.ai14.compute import CACHE, EARLY, LATE

NAMES = {"gpt_xs": r"XS", "gpt_s": r"S", "gpt_m": r"M", "gpt_l": r"L", "base": r"the series' model"}


def smooth(y, k=9):
    """A moving average for the later positions; the first ones, where the loss falls fastest (and which a log axis
    spreads out), stay as measured."""
    y = np.asarray(y, float)
    pad = np.pad(y, (k // 2, k // 2), mode="edge")
    out = np.convolve(pad, np.ones(k) / k, mode="valid")
    out[:k // 2] = y[:k // 2]
    return out


def rows_():
    """The family's rows, and the series' base model's when its item is computed (`compute.py` and `make.py` compute
    it, after the novels model: a render never trains the base model)."""
    d = load("icl")
    b = load("icl_base") if CACHE.path("icl_base").exists() else dict(rows=[], base_tokens=None)
    d = dict(d, base_tokens=b["base_tokens"])
    return d, list(d["rows"]) + list(b["rows"])


def tag_of(r):
    return NAMES.get(r["name"], r["name"])


def who_of(r):
    return "the series' model" if r["name"] == "base" else f"model {tag_of(r)}"


def size_word(r):
    p = r["params"]
    return f"{p / 1e6:.1f} million" if p >= 1e6 else f"{p / 1e3:.0f} thousand"


class Emergence(VoiceoverScene):
    def construct(self):
        self.card()
        self.context_curves()
        self.replay()
        self.copying()
        self.few_shot()
        self.verdict()

    def card(self):
        card = chapter_card(14, r"Learning in context, in our own models",
                            r"Does learning from the prompt appear as our models grow?", lit=(2020,), part=PART)
        with self.voiceover("Chapter fourteen. Learning in context, in our own models."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def context_curves(self):
        d, rows = rows_()
        fam = [r for r in rows if r["name"] != "base"]
        has_base = any(r["name"] == "base" for r in rows)
        cols = {r["name"]: SIZE_COLORS[i] for i, r in enumerate(rows)}
        # left: the family
        lst = VGroup()
        for r in rows:
            lst.add(VGroup(Dot(radius=0.09, color=cols[r["name"]]),
                           label(rf"{tag_of(r)}: \ {human(r['params'], 3)} parameters", font_size=22,
                                 color=cols[r["name"]])).arrange(RIGHT, buff=0.15))
        lst.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([-4.9, 0.6, 0])
        lh = label(rf"same ${F_tokens() / 1e6:.0f}$M tokens each", font_size=20, color=GREY_B).next_to(lst, UP, buff=0.3)
        times = (d.get("base_tokens") or 0) / F_tokens()
        bl = (label(rf"the series' model: \\ trained on ${times:.0f}\times$ as many tokens", font_size=18, color=GREY_B)
              .next_to(lst, DOWN, buff=0.25) if has_base else VectorizedPoint())
        allp = np.concatenate([np.asarray(r["pos"]) for r in rows])
        top = math.ceil(float(np.percentile(allp, 99.5)) * 2) / 2
        bot = math.floor(min(min(smooth(r["pos"])[150:]) for r in rows) * 2) / 2 - 0.25
        g = axes([0, math.log10(255)], [bot, top], x_length=7.0, y_length=4.6,
                 xlabel=r"position in the context \ (tokens of context before it; \ log scale)",
                 ylabel=r"loss on held-out text (nats)", xticks=[0, 1, 2], yticks=[bot + 0.25, top],
                 xfmt=lambda v: f"{10 ** v:.0f}", yfmt=lambda v: f"{v:.1f}", center=[2.3, -0.2, 0])
        ax = g.ax
        curves = VGroup()
        for r in rows:
            y = smooth(r["pos"])
            xs = np.log10(np.arange(1, len(y) + 1))
            curves.add(curve(ax, xs, np.clip(y, bot, top), cols[r["name"]], 3.5))
        gains = {r["name"]: r["early"] - r["late"] for r in rows}
        small, large = fam[0], fam[-1]
        falls = ("Every curve falls from left to right: the words before help." if min(gains.values()) > 0.05 else
                 "Not every curve falls: some models barely use the words before.")
        bigger_more = gains[large["name"]] > gains[small["name"]] + 0.05
        tail = (f"the {size_word(large)}-parameter model gains {gains[large['name']]:.2f}: the bigger models learn "
                "more from context." if bigger_more else
                f"the largest of the family gains about the same, {gains[large['name']]:.2f} nats.")
        btail = (f" The series' own model, bigger and trained longer, gains {gains['base']:.2f}." if has_base else "")
        fifth = (f" And, as a fifth, the series' own model, larger and trained on {times:.0f} times as many tokens."
                 if has_base else "")
        tag = note(rf"computed: \ ${rows[0]['windows']}$ held-out windows of $256$ tokens").to_corner(DR, buff=0.2)
        with self.voiceover(
            "GPT-3's surprise was that learning from the prompt appeared with scale. Can we see any of it at our "
            "scale? <bookmark mark='a'/> Four GPT-style models of growing size, all trained on the same text, the "
            "same number of tokens." + fifth + " <bookmark mark='b'/> First, the simplest measure of learning from "
            "context: the loss at each position of a 256-token window. Early positions have almost no context; later "
            "ones have a lot. <bookmark mark='c'/> " + falls + " From one to four tokens of context to more than a "
            f"hundred, the smallest model gains {gains[small['name']]:.2f} nats per token; " + tail + btail
        ) as vo:
            self.play(FadeIn(lh), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.1) for m in lst], lag_ratio=0.3), FadeIn(bl))
            vo.wait_until("b")
            self.play(FadeIn(g))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.3), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        r = load("gpt_l")
        sn = r["snaps"]
        S = float(r["tokens"])
        vals = [s["val"] for s in sn]
        top = math.ceil(max(vals) + 0.2)
        bot = math.floor(min(vals) - 0.3)
        g = axes([0, S], [bot, top], x_length=4.8, y_length=3.4, xlabel=r"tokens read", ylabel=r"held-out loss",
                 xticks=[0, S], yticks=[bot, top], xfmt=lambda v: rf"{v / 1e6:.0f}\text{{M}}" if v else "0",
                 center=[-4.0, 0.2, 0])
        pts = VGroup(*[Dot(g.ax.c2p(s["tokens"], s["val"]), radius=0.06, color=DECODER) for s in sn])
        line = VMobject().set_points_as_corners([g.ax.c2p(s["tokens"], s["val"]) for s in sn]).set_stroke(DECODER, 3)
        allp = np.concatenate([np.asarray(s["pos"]) for s in sn[1:]])
        ptop = math.ceil(float(np.percentile(allp, 99.5)))
        pbot = math.floor(min(min(smooth(s["pos"])[150:]) for s in sn)) - 0.5
        h = axes([0, math.log10(255)], [pbot, ptop], x_length=5.6, y_length=3.8,
                 xlabel=r"position in the context \ (log scale)", ylabel=r"loss at that position",
                 xticks=[0, 1, 2], yticks=[pbot, ptop], xfmt=lambda v: f"{10 ** v:.0f}", yfmt=lambda v: f"{v:.0f}",
                 center=[3.3, 0.2, 0])
        curves = []
        for s in sn:
            y = smooth(s["pos"])
            curves.append(curve(h.ax, np.log10(np.arange(1, len(y) + 1)), np.clip(y, pbot, ptop), DECODER, 4))
        gains = [float(np.mean(s["pos"][EARLY]) - np.mean(s["pos"][LATE])) for s in sn]
        reads = [label(rf"after ${s['tokens'] / 1e6:.2f}$M tokens: \ context gain ${gn:.2f}$ nats", font_size=22,
                       color=CONTEXT).move_to([3.3, -2.6, 0]) for s, gn in zip(sn, gains)]
        final = gains[-1]
        half = next((s for s, gn in zip(sn, gains) if gn >= final / 2), sn[-1])
        tag = note(rf"computed: \ model L, \ {human(r['params']['total'])} parameters").to_corner(DR, buff=0.2)
        grow = (f"As it trains, the whole curve drops, and it tilts. Half of its final gain from context is there after "
                f"{half['tokens'] / 1e6:.2f} million tokens." if final > 0.1 else
                "As it trains, the whole curve drops, but it hardly tilts.")
        with self.voiceover(
            "Now replay the training of the largest of the family, and watch that curve form. On the left, its "
            "held-out loss; on the right, its loss at each position of the context, frozen at each checkpoint. "
            "<bookmark mark='a'/> Untrained, the curve is flat: a model that knows nothing gains nothing from context. "
            "<bookmark mark='b'/> " + grow + " <bookmark mark='c'/> By the end it "
            f"gains {final:.2f} nats per token from the words before."
        ) as vo:
            self.play(FadeIn(g), FadeIn(h), FadeIn(tag), FadeIn(pts[0]), FadeIn(curves[0]), FadeIn(reads[0]))
            vo.wait_until("a")
            self.play(Indicate(curves[0], color=YELLOW))
            vo.wait_until("b")
            cur, rd = curves[0], reads[0]
            per = min(1.2, max(0.5, (vo.until("c") - 1.0) / max(1, len(sn) - 1)))
            for k in range(1, len(sn)):
                self.play(FadeIn(pts[k], scale=1.5), ReplacementTransform(cur, curves[k]),
                          ReplacementTransform(rd, reads[k]), run_time=per)
                cur, rd = curves[k], reads[k]
            self.play(Create(line))
            vo.wait_until("c")
            self.play(Indicate(rd, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def copying(self):
        d, rows = rows_()
        cols = {r["name"]: SIZE_COLORS[i] for i, r in enumerate(rows)}
        ex = data_text("river candle horse ... wheel  |  river candle horse ... wheel", font=MONO, font_size=22,
                       color=GREY_A).move_to(UP * 2.9)
        exl = label(r"$60$ random common words, \ then the same $60$ again", font_size=22, color=GREY_B)
        exl.next_to(ex, DOWN, buff=0.15)
        W = 0.42
        bars = VGroup()
        for i, r in enumerate(rows):
            x = -4.6 + 2.0 * i if len(rows) == 5 else -4.0 + 2.4 * i
            b1 = Rectangle(width=W, height=max(3.0 * r["acc1"], 0.02), stroke_width=0, fill_color=GREY_C,
                           fill_opacity=0.9).move_to([x - 0.24, -2.4, 0], aligned_edge=DOWN)
            b2 = Rectangle(width=W, height=max(3.0 * r["acc2"], 0.02), stroke_width=0, fill_color=cols[r["name"]],
                           fill_opacity=0.95).move_to([x + 0.24, -2.4, 0], aligned_edge=DOWN)
            t1 = label(rf"${100 * r['acc1']:.0f}\%$", font_size=18, color=GREY_B).next_to(b1, UP, buff=0.05)
            t2 = label(rf"${100 * r['acc2']:.0f}\%$", font_size=20, color=cols[r["name"]]).next_to(b2, UP, buff=0.05)
            n_ = label(tag_of(r), font_size=20, color=cols[r["name"]]).move_to([x, -2.75, 0])
            bars.add(VGroup(b1, b2, t1, t2, n_))
        base = Line([-5.6, -2.4, 0], [5.6, -2.4, 0], color=GREY_C, stroke_width=1.5)
        lg = legend([(GREY_C, r"first copy"), (DECODER, r"second copy")], font_size=20).to_corner(UR, buff=0.4)
        lg.shift(DOWN * 1.2)
        yl = label(r"next word guessed right", font_size=20, color=GREY_A).move_to([-4.6, 1.2, 0])
        fam = [r for r in rows if r["name"] != "base"]
        jumps = {r["name"]: r["acc2"] - r["acc1"] for r in rows}
        copiers = [r for r in rows if jumps[r["name"]] > 0.2]
        if copiers:
            first = copiers[0]
            if rows.index(first) == 0:
                lead = "Every one of our models copies."
            elif first["name"] == "base":
                lead = "None of the family copies; only the series' own model, larger and trained longer, does."
            else:
                lead = f"The smaller models don't copy; from model {tag_of(first)} on, they do."
            verdict = (f"For {who_of(first)}, the second copy is far easier: {100 * first['acc2']:.0f} percent of its "
                       f"words guessed right, against {100 * first['acc1']:.0f} the first time. That is copying from the "
                       "context: the induction heads of Part 13.")
        else:
            lead = ""
            verdict = ("None of our models does much better the second time: the best gains "
                       f"{100 * max(jumps.values()):.0f} points. At our scale and training length, the copying circuit, "
                       "the induction heads of Part 13, hasn't formed; Part 13's small transformer couldn't copy either.")
        r_l = load("gpt_l")
        sn = r_l["snaps"]
        acc2 = [s["acc2"] for s in sn]
        on = next((s for s in sn if s["acc2"] - s["acc1"] > 0.2), None)
        when = (f" In model L's training, it switched on between {sn[max(0, sn.index(on) - 1)]['tokens'] / 1e6:.2f} and "
                f"{on['tokens'] / 1e6:.2f} million tokens." if on is not None and sn.index(on) > 0 else "")
        with self.voiceover(
            "A sharper test, the one Part 13 used: a list of sixty random common words, then the same list again. A "
            "model that can copy from its context finds the second copy much easier than the first. "
            "<bookmark mark='a'/> Here is how often each model guesses the next word, on the first copy and on the "
            "second. <bookmark mark='b'/> " + lead + " " + verdict + when
        ) as vo:
            self.play(FadeIn(ex), FadeIn(exl), Create(base), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(lg), LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[2]), FadeIn(b[4]))
                                                for b in bars], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b[1], DOWN), FadeIn(b[3])) for b in bars],
                                  lag_ratio=0.3), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def few_shot(self):
        d, rows = rows_()
        cols = {r["name"]: SIZE_COLORS[i] for i, r in enumerate(rows)}
        shots = d["shots"]
        ex = said(d["example"] + " ...", chars=58, font_size=17, max_lines=4, box_color=CONTEXT).move_to([0, 2.65, 0])
        exl = label(rf"two books, \ $k$ labelled examples, \ then a held-out sentence: \ which title is more likely? \ "
                    rf"(${d['n_items']}$ prompts)", font_size=20, color=GREY_B).next_to(ex, DOWN, buff=0.15)
        lo = 0.4
        hi = max(0.75, max(max(r["fewshot"]) for r in rows) + 0.05)
        g = axes([-0.3, len(shots) - 0.7], [lo, hi], x_length=6.4, y_length=3.6, xlabel=r"examples in the prompt, $k$",
                 ylabel=r"right title chosen", xticks=list(range(len(shots))), yticks=[0.5, round(hi, 1)],
                 xfmt=lambda v: str(shots[int(round(v))]), yfmt=lambda v: rf"{100 * v:.0f}\%", center=[-1.4, -1.3, 0])
        ax = g.ax
        chance = DashedLine(ax.c2p(-0.3, 0.5), ax.c2p(len(shots) - 0.7, 0.5), color=GREY_B, dash_length=0.08)
        cl = label(r"chance", font_size=18, color=GREY_B).next_to(chance, RIGHT, buff=0.08)
        lines = VGroup()
        for r in rows:
            pts = [ax.c2p(i, a) for i, a in enumerate(r["fewshot"])]
            lines.add(VGroup(VMobject().set_points_as_corners(pts).set_stroke(cols[r["name"]], 3.5),
                             *[Dot(p, radius=0.06, color=cols[r["name"]]) for p in pts]))
        lg = legend([(cols[r["name"]], tag_of(r)) for r in rows], font_size=20).move_to([4.6, -1.2, 0])
        big = rows[-1]
        fam = [r for r in rows if r["name"] != "base"]
        gain = big["fewshot"][-1] - big["fewshot"][0]
        who = who_of(big)
        if gain > 0.05:
            v1 = (f"For {who}, examples help: from {100 * big['fewshot'][0]:.0f} percent with none to "
                  f"{100 * big['fewshot'][-1]:.0f} with {shots[-1]}.")
        elif gain < -0.05:
            v1 = (f"For {who}, examples hurt: from {100 * big['fewshot'][0]:.0f} percent with none to "
                  f"{100 * big['fewshot'][-1]:.0f} with {shots[-1]}; a long prompt of other sentences only confuses it.")
        else:
            v1 = (f"For {who}, examples barely matter: {100 * big['fewshot'][0]:.0f} percent with none, "
                  f"{100 * big['fewshot'][-1]:.0f} with {shots[-1]}.")
        best0 = max(r["fewshot"][0] for r in rows)
        v0 = (f"Even with no examples, the models do better than chance, up to {100 * best0:.0f} percent: a title is "
              "often a character's name, and a sentence that mentions the character makes the name more likely."
              if best0 > 0.56 else
              f"With no examples the models are near chance, at most {100 * best0:.0f} percent.")
        sz = fam[-1]["fewshot"][-1] - fam[0]["fewshot"][-1]
        v2 = (f" And with {shots[-1]} examples, the largest of the family beats the smallest by {100 * sz:.0f} points."
              if sz > 0.03 else
              f" With {shots[-1]} examples, the family's sizes are within {100 * abs(sz):.0f} points of each other.")
        with self.voiceover(
            "Finally, GPT-3's own kind of test, built from the novels. Two books; a few labelled examples in the "
            "prompt, each a sentence and the book it is from; then a new sentence from a paragraph the models never "
            "read, and we compare the probabilities they give to the two titles. <bookmark mark='a'/> With zero, one, "
            "two, four and eight examples, for every model. <bookmark mark='b'/> " + v0 + " <bookmark mark='c'/> "
            + v1 + v2
        ) as vo:
            self.play(FadeIn(ex), FadeIn(exl))
            vo.wait_until("a")
            self.play(FadeIn(g), Create(chance), FadeIn(cl), FadeIn(lg))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(l[0]) for l in lines], lag_ratio=0.2),
                      LaggedStart(*[FadeIn(VGroup(*l[1:])) for l in lines], lag_ratio=0.2), run_time=3.0)
            vo.wait_until("c")
            self.play(Indicate(lines[-1], scale_factor=1.04))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def verdict(self):
        d, rows = rows_()
        fam = [r for r in rows if r["name"] != "base"]
        gains = [r["early"] - r["late"] for r in rows]
        grows = gains[len(fam) - 1] > gains[0] + 0.05
        copies = any(r["acc2"] - r["acc1"] > 0.2 for r in rows)
        big = rows[-1]
        fs = big["fewshot"][-1] - big["fewshot"][0] > 0.05
        items = [
            (r"using context grows with size", grows),
            (r"copying from the context", copies),
            (r"learning a task from examples", fs),
        ]
        rows_g = VGroup()
        for t, ok in items:
            mark = MathTex(r"\checkmark" if ok else r"\times", font_size=40, color=C.REWARD if ok else C.PENALTY)
            rows_g.add(VGroup(mark, label(t, font_size=30, color=WHITE)).arrange(RIGHT, buff=0.35))
        rows_g.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(UP * 0.8)
        head = label(r"at our scale, \ million-parameter models:", font_size=30, color=GREY_A).next_to(rows_g, UP, buff=0.5)
        t1 = ("Our models use their context more as they grow." if grows else
              "Our larger models don't use their context much more than the smaller ones.")
        t2 = ("Copying from the context appears with size." if copies else
              "Copying from the context hasn't appeared at our scale.")
        t3 = ("And examples in the prompt help the largest model choose." if fs else
              "But learning a task from examples in the prompt hasn't appeared at our scale.")
        tw = take_away(r"GPT-3 needed billions of parameters for few-shot learning to be useful: \ "
                       r"the mechanism is Part 13's, \ the scale is Part 12's", color=CONTEXT, font_size=24)
        with self.voiceover(
            "So what did our small models show? <bookmark mark='a'/> " + t1 + " " + t2 + " " + t3 + " <bookmark mark='b'/> "
            "In GPT-3's own "
            "plots, few-shot learning became useful only in the billions of parameters. Part 13 showed the "
            "mechanism, heads that find and copy; Part 12, the scaling laws that make larger models worth their cost."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows_g], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(tw))
        self.wait(0.3)
        self.clear_scene()


def F_tokens():
    return load("family")["tokens"]
