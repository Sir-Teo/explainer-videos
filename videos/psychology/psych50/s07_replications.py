from __future__ import annotations

from videos.psychology.psych50.common import *  # noqa: F403


class Replications(VoiceoverScene):
    def construct(self):
        self.card()
        self.kvarven()
        self.lesson()

    def card(self):
        card = chapter_card(6, r"Meta-analyses against replications", r"What happens when the filter is removed?",
                            lit=(), part=PART, scale=("society",), marr=("what",))
        with self.voiceover("Chapter six. Meta-analyses against replications."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def kvarven(self):
        d = load("kvarven")
        head = heading(r"Ten effects, \ measured twice")
        A = axes([0, 0.5], [0, 0.5], x_length=3.8, y_length=3.8, xticks=[0, 0.25, 0.5], yticks=[0, 0.25, 0.5],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"large preregistered replication",
                 ylabel=r"meta-analysis of the published", center=[-4.0, 0.1, 0], font_size=12)
        diag = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(0.5, 0.5), color=GREY_B, stroke_width=1.5)
        dots = VGroup(*[Dot(A.ax.c2p(r, m), radius=0.08, color=AUTH) for r, m in zip(d["rep"], d["meta"])])
        rows = rows_of([
            (r"Psyche: \ ten small true effects; \ for each, \ a filtered literature of 60 studies and one replication "
             r"with 1,500 people per group", WHITE),
            (rf"every dot sits above the diagonal: \ the meta-analyses average about {d['ratio']:.1f} times the "
             rf"replications", AUTH),
            (r"Kvarven, \ Str\o mland and Johannesson, \ 2020: \ fifteen real effects with both a meta-analysis and a "
             r"multi-site preregistered replication; \ the meta-analyses were about three times larger", PERSON),
            (r"correction methods shrank the gap but did not close it, \ as chapter five predicts", MODEL),
        ], 7.4, 19, 0.36).move_to([2.6, -0.1, 0])
        tag = psyche_tag(r"\texttt{meta.literature}, \ \texttt{random\_effects}")
        tag2 = published_tag(r"Kvarven et al.\ (2020)").to_corner(DL, buff=0.3)
        with self.voiceover(
            "What happens when the same effect is measured both ways? <bookmark mark='a'/> Psyche makes ten small "
            "true effects. For each, a filtered literature of sixty studies, and one replication with fifteen "
            "hundred people per group. <bookmark mark='b'/> Every dot sits above the diagonal. The meta-analyses "
            "average about two and a half times the replications. <bookmark mark='c'/> In 2020 Amanda Kvarven, Eirik "
            "Stromland and Magnus Johannesson found fifteen real effects with both a meta-analysis and a multi-site "
            "preregistered replication. The meta-analyses were about three times larger. <bookmark mark='d'/> "
            "Correction methods shrank the gap, but didn't close it, just as the last chapter predicts."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tag2), FadeIn(A), FadeIn(diag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[FadeIn(x, scale=1.5) for x in dots], lag_ratio=0.15))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def lesson(self):
        head = heading(r"Precise, \ and wrong")
        rows = rows_of([
            (r"pooling more filtered studies narrows the interval around the wrong number", AUTH),
            (r"a meta-analysis cannot be better than the literature it pools: \ garbage in, \ precise garbage out", WHITE),
            (r"a single large registered study can outweigh a hundred small unregistered ones", GOOD),
            (r"that is why the Ledger's records are mostly multi-site replications, \ not meta-analyses", YOU),
        ], 12.4, 23, 0.46).move_to([0, -0.3, 0])
        with self.voiceover(
            "So a meta-analysis can be precise and wrong. <bookmark mark='a'/> Pooling more filtered studies narrows "
            "the interval around the wrong number. <bookmark mark='b'/> A meta-analysis can't be better than the "
            "literature it pools. <bookmark mark='c'/> A single large registered study can outweigh a hundred small "
            "unregistered ones. <bookmark mark='d'/> That's why the Ledger's records are mostly multi-site "
            "replications, not meta-analyses."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
