from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai20.common import FEAT, FEATURE_COLORS, MONO, load, show

OUT = C.TRUE_P


class Circuits(VoiceoverScene):
    def construct(self):
        self.card()
        self.graph()
        self.published()

    def card(self):
        card = chapter_card(3, r"Tracing a thought", r"Which features made the model say that?", part=20)
        with self.voiceover("Chapter three. Tracing a thought."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def graph(self):
        a = load("attribution")
        prompt = str(a["prompt"])
        T = len(prompt)
        nv = 20
        vis = prompt[-nv:]
        off = T - nv
        W = 12.4
        step = W / nv
        boxes = VGroup()
        for i, ch in enumerate(vis):
            b = VGroup(RoundedRectangle(width=step * 0.9, height=0.5, corner_radius=0.06, stroke_color=GREY_C, stroke_width=1.2),
                       Text(show(ch), font=MONO, font_size=22, color=GREY_A))
            b[1].move_to(b[0])
            boxes.add(b.move_to([-W / 2 + step * (i + 0.5), -2.9, 0]))
        lead = label(r"\ldots", font_size=24, color=GREY_C).next_to(boxes, LEFT, buff=0.1)
        nodes = sorted(a["nodes"], key=lambda n: (n["pos"], n["feature"]))
        m = len(nodes)
        amax = max(n["attr"] for n in nodes)
        xs = np.linspace(-4.8, 4.8, m)
        fn = VGroup()
        for j, (n, x) in enumerate(zip(nodes, xs)):
            col = FEATURE_COLORS[j % len(FEATURE_COLORS)]
            c = Circle(radius=0.28, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.25).move_to([x, 0.1, 0])
            t = Text(str(n["feature"]), font=MONO, font_size=16, color=WHITE).move_to(c)
            ctx = n["contexts"][0] if n["contexts"] else "?" * 10
            snip = VGroup(Text("".join(show(ch) for ch in ctx[-9:-2]), font=MONO, font_size=14, color=GREY_B),
                          Text(show(ctx[-2]), font=MONO, font_size=14, color=col)).arrange(RIGHT, buff=0.02)
            snip.next_to(c, DOWN, buff=0.1)
            fn.add(VGroup(c, t, snip))
        fl = label(r"features after block $2$ \ (under each: where it fires hardest)", font_size=20, color=FEAT).next_to(fn, UP, buff=0.25)
        out = VGroup(RoundedRectangle(width=1.0, height=0.7, corner_radius=0.1, stroke_color=OUT, stroke_width=3, fill_color=OUT,
                                      fill_opacity=0.2),
                     Text(show(str(a["target"])), font=MONO, font_size=34, color=WHITE)).move_to([0, 2.6, 0])
        out[1].move_to(out[0])
        ol = label(rf"next: \ ${100 * float(a['p_target']):.0f}\%$", font_size=24, color=OUT).next_to(out, RIGHT, buff=0.25)
        # edges: feature -> output (attribution), input -> feature (which characters switched it on)
        e_out = VGroup(*[Line(f[0].get_top(), out[0].get_bottom(), stroke_width=1 + 9 * max(n["attr"], 0) / amax,
                              color=FEATURE_COLORS[j % len(FEATURE_COLORS)]).set_stroke(opacity=0.85)
                         for j, (n, f) in enumerate(zip(nodes, fn))])
        e_in = VGroup()
        for j, (n, f) in enumerate(zip(nodes, fn)):
            src = np.asarray(n["inputs"], float)[off:]
            if src.max() <= 0:
                continue
            for i in np.argsort(-src)[:3]:
                if src[i] <= 0.15 * src.max():
                    continue
                e_in.add(Line(boxes[i].get_top(), f[0].get_bottom(), stroke_width=0.8 + 5 * src[i] / src.max(),
                              color=FEATURE_COLORS[j % len(FEATURE_COLORS)]).set_stroke(opacity=0.6))
        homes = VGroup(*[DashedLine(f[0].get_bottom() + DOWN * 0.45, boxes[n["pos"] - off].get_top(), dash_length=0.06,
                                    stroke_width=1, color=GREY_D) for n, f in zip(nodes, fn) if n["pos"] >= off])
        el = label(rf"line width: \ how much each feature raised \\ the score of `{show(str(a['target']))}'", font_size=20,
                   color=GREY_A).to_corner(UR, buff=0.3)
        cite_ = cite(r"E.~Ameisen et al., \textit{Circuit Tracing} (2025); \ J.~Lindsey et al., \textit{On the Biology of a Large "
                     r"Language Model} (2025)", corner=DL)
        tag = note(r"to first order: \ activation $\times$ gradient").to_corner(DR, buff=0.25)
        with self.voiceover(
            "With features in hand, we can trace a single decision. <bookmark mark='a'/> Our transformer reads: she "
            f"sai, and writes {a['target']}, with {100 * float(a['p_target']):.0f} percent confidence. "
            "<bookmark mark='b'/> Which features pushed it there? For each one, multiply how strongly it's on by how "
            "much the output's score moves when it changes: its attribution. Here are the six strongest. "
            "<bookmark mark='c'/> And for each feature, the same question one step back: which input characters "
            "switched it on? <bookmark mark='d'/> The result is an attribution graph: a map of the computation, from "
            "the text, through features, to the answer."
        ) as vo:
            self.play(FadeIn(lead), LaggedStart(*[FadeIn(b_) for b_ in boxes], lag_ratio=0.03), FadeIn(cite_), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(out), FadeIn(ol))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(f_, scale=0.8) for f_ in fn], lag_ratio=0.12), FadeIn(fl), Create(homes))
            self.play(LaggedStart(*[Create(e_) for e_ in e_out], lag_ratio=0.12), FadeIn(el), run_time=1.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(e_) for e_ in e_in], lag_ratio=0.05), run_time=2.0)
            vo.wait_until("d")
            flashes = [ShowPassingFlash(e_.copy().set_stroke(WHITE, width=e_.get_stroke_width() + 2, opacity=1), time_width=0.5)
                       for e_ in list(e_in) + list(e_out)]
            self.play(LaggedStart(*flashes, lag_ratio=0.03), run_time=2.5)
            self.play(Indicate(out, color=OUT, scale_factor=1.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def published(self):
        def node(text, color):
            t = label(text, font_size=24, color=WHITE)
            box = RoundedRectangle(width=t.width + 0.5, height=0.75, corner_radius=0.12, stroke_color=color, stroke_width=2.5,
                                   fill_color=color, fill_opacity=0.18)
            return VGroup(box, t.move_to(box))

        q = node(r"``the capital of the state containing Dallas is''", GREY_B).move_to([0, -2.4, 0])
        f1 = node(r"Dallas", C.TRUE_P).move_to([-3.0, -0.6, 0])
        f2 = node(r"Texas", C.BITS).move_to([0.0, 0.6, 0])
        f3 = node(r"say a capital", C.INTERVAL).move_to([3.4, -0.6, 0])
        o = node(r"Austin", OUT).move_to([1.6, 2.4, 0])
        arr = lambda a_, b_: Arrow(a_.get_top(), b_.get_bottom(), buff=0.08, stroke_width=4, color=GREY_B,
                                   max_tip_length_to_length_ratio=0.12)
        edges = VGroup(arr(q, f1), arr(q, f3), arr(f1, f2), arr(f2, o), arr(f3, o))
        tag = note(r"published result, redrawn: \ Claude 3.5 Haiku").to_corner(DR, buff=0.25)
        cite_ = cite(r"J.~Lindsey et al., \textit{On the Biology of a Large Language Model} (2025)", corner=DL)
        with self.voiceover(
            "In big models this gets striking. Researchers at Anthropic replaced each layer's MLP with a sparse "
            "transcoder, so the graph is exact for that replacement, and traced Claude 3.5 Haiku. "
            "<bookmark mark='a'/> Asked for the capital of the state containing Dallas, it doesn't jump straight "
            "there: one feature represents Dallas, which activates Texas, and Texas together with a "
            "say-a-capital feature produces Austin. Two steps of reasoning, inside one forward pass. When writing a "
            "rhyming poem, it picks the rhyme before it writes the line that leads to it."
        ) as vo:
            self.play(FadeIn(q), FadeIn(tag), FadeIn(cite_))
            vo.wait_until("a")
            self.play(GrowArrow(edges[0]), FadeIn(f1))
            self.play(GrowArrow(edges[2]), FadeIn(f2))
            self.play(GrowArrow(edges[1]), FadeIn(f3))
            self.play(GrowArrow(edges[3]), GrowArrow(edges[4]), FadeIn(o))
        self.wait(0.3)
        self.clear_scene()
