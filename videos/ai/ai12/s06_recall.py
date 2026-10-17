from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai12.common import ADD, DELTA, K, MONO, V, load

MIXERS = [("softmax", r"softmax attention", C.ATTN), ("linear", r"linear attention \ (add)", ADD),
          ("delta", r"the delta rule", DELTA)]


class Recall(VoiceoverScene):
    def construct(self):
        self.card()
        self.task()
        self.results()

    def card(self):
        card = chapter_card(5, r"A recall test", r"Which memory can look things up?", part=12)
        with self.voiceover("Chapter five. A recall test."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def task(self):
        pairs = [("A", "4"), ("Q", "7"), ("M", "2"), ("D", "9"), ("X", "1")]
        boxes = VGroup()
        for kk, vv in pairs:
            boxes.add(VGroup(Text(kk, font=MONO, font_size=30, color=K), Text(vv, font=MONO, font_size=30, color=V)).arrange(RIGHT, buff=0.12))
        boxes.arrange(RIGHT, buff=0.45).move_to(UP * 1.2 + LEFT * 1.5)
        qs = VGroup(*[Text(c_, font=MONO, font_size=30, color=K) for c_ in ("M", "A", "X")]).arrange(RIGHT, buff=0.45)
        qs.next_to(boxes, RIGHT, buff=0.9)
        ans = VGroup(*[Text(c_, font=MONO, font_size=30, color=C.BITS) for c_ in ("2", "4", "1")])
        for a_, q_ in zip(ans, qs):
            a_.next_to(q_, DOWN, buff=0.35)
        bl = label(r"pairs: \ a key, then its value", font_size=24, color=GREY_A).next_to(boxes, DOWN, buff=0.5)
        ql = label(r"then keys again: \ answer with their values", font_size=24, color=C.BITS).next_to(ans, DOWN, buff=0.3)
        m = load("mqar")
        rule = label(rf"tiny one-layer models, \ each with a memory of ${int(m['d'])}$ numbers per token, \\ "
                     r"trained on this game with up to $48$ pairs", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.7)
        cite_ = cite(r"S.~Arora et al., \textit{Zoology: Measuring and Improving Recall in Efficient Language Models} (2023)",
                     corner=UR)
        with self.voiceover(
            "How much does forgetting cost? Here's a test of pure memory: a list of keys, each followed by its "
            "value; <bookmark mark='a'/> then some of the keys again, and the model must answer with their values. "
            "It's the skill a model needs to quote a name or a number from far back in a document. "
            "<bookmark mark='b'/> We trained tiny one-layer models to play it, with three kinds of memory: softmax "
            "attention, linear attention that only adds, and the delta rule."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(b_) for b_ in boxes], lag_ratio=0.2), FadeIn(bl), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(qs))
            self.play(LaggedStart(*[FadeIn(a_, shift=DOWN * 0.15) for a_ in ans], lag_ratio=0.3), FadeIn(ql))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def results(self):
        m = load("mqar")
        Ns = [int(n) for n in m["Ns"]]
        bw = 0.42
        groups = VGroup()
        base_y, H = -2.0, 4.0
        for j, N in enumerate(Ns):
            x0 = -4.6 + j * 2.6
            g = VGroup()
            for i, (key, _, col) in enumerate(MIXERS):
                v = float(m[key][j])
                bar = Rectangle(width=bw, height=max(H * v, 0.02), stroke_width=0, fill_color=col, fill_opacity=0.85)
                bar.move_to([x0 + i * (bw + 0.08), base_y + H * v / 2, 0])
                val = MathTex(f"{100 * v:.0f}", font_size=20, color=col).next_to(bar, UP, buff=0.06)
                g.add(VGroup(bar, val))
            nl = label(rf"${N}$ pairs", font_size=24, color=GREY_A).next_to(g, DOWN, buff=0.2).set_y(base_y - 0.3)
            groups.add(VGroup(g, nl))
        axis = Line([-5.0, base_y, 0], [5.6, base_y, 0], color=GREY_C, stroke_width=2)
        yl = label(r"answers right, \ \%", font_size=22, color=GREY_A).move_to([-5.0, base_y + H + 0.65, 0], aligned_edge=LEFT)
        # where the lists outgrow the keys: more pairs than a key has numbers
        dk = int(m["d"])
        past = [j for j, N in enumerate(Ns) if N > dk]
        cut = None
        if past and past[0] > 0:
            xc = (groups[past[0] - 1].get_right()[0] + groups[past[0]].get_left()[0]) / 2
            cut = VGroup(DashedLine([xc, base_y, 0], [xc, base_y + H + 0.85, 0], dash_length=0.08, stroke_width=2, color=GREY_B),
                         label(rf"more pairs than a key has numbers \ (${dk}$) \ $\rightarrow$", font_size=20, color=GREY_B))
            cut[1].next_to(cut[0].get_top(), RIGHT, buff=0.12).shift(DOWN * 0.12)
        key = VGroup(*[label(t, font_size=24, color=c_) for _, t, c_ in MIXERS]).arrange(RIGHT, buff=0.7).to_edge(UP, buff=0.35)
        sm, li, de = (np.asarray(m[k_]) for k_, _, _ in MIXERS)
        with self.voiceover(
            f"With {Ns[0]} pairs, all three manage. <bookmark mark='a'/> As the list grows, the adding memory falls "
            f"apart: {100 * li[-1]:.0f} percent right at {Ns[-1]} pairs, as its crosstalk swamps the answers, "
            f"worst once there are more pairs than each key has numbers, {int(m['d'])} here. "
            + (f"The delta rule holds on much longer: {100 * de[-1]:.0f} percent. " if de[-1] > li[-1] + 0.1 else
               f"The delta rule does a little better, {100 * de[-1]:.0f} percent: it can overwrite, but its state is just "
               "as small. " if de[-1] > li[-1] else
               f"The delta rule's state is just as small, and here it fares no better: {100 * de[-1]:.0f} percent. ")
            + f"And softmax attention, which simply keeps every pair, gets {100 * sm[-1]:.0f}. "
            "<bookmark mark='b'/> Exact recall is what attention buys with its "
            "growing cache, and what a fixed memory has to approximate."
        ) as vo:
            self.play(FadeIn(key), Create(axis), FadeIn(yl), FadeIn(groups[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(*[GrowFromEdge(b_[0], DOWN) for b_ in g_[0]], *[FadeIn(b_[1]) for b_ in g_[0]],
                                                   FadeIn(g_[1])) for g_ in groups[1:]], lag_ratio=0.4), run_time=3.0)
            if cut is not None:
                self.play(Create(cut[0]), FadeIn(cut[1]))
            vo.wait_until("b")
        self.wait(0.3)
        self.clear_scene()
