from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai2.common import FAIL, FCOL, GCOST, HEUR, HIST, LEARN, MONO, PART, PATH, SYMBOL, load


class Winters(VoiceoverScene):
    def construct(self):
        self.card()
        self.first()
        self.boom()
        self.moravec()
        self.tail()

    def card(self):
        card = chapter_card(13, r"The winters", r"Why did the symbolic era stall, twice?", lit=(1973, 1987), part=PART)
        with self.voiceover("Chapter thirteen. The winters."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def first(self):
        cards = VGroup(
            history_card(1966, r"the ALPAC report", r"machine translation: \ slower, less accurate and dearer than "
                         r"people; \ US funding for it dries up", width=4.2, color=FAIL, font_size=18),
            history_card(1969, r"Minsky \& Papert, \textit{Perceptrons}", r"the limits of one-layer networks: \ "
                         r"neural research goes quiet \ (Part 9)", width=4.2, color=FAIL, font_size=18),
            history_card(1973, r"Sir James Lighthill's report", r"to Britain's Science Research Council: \ outside "
                         r"toy domains, \ the combinatorial explosion defeats it", width=4.2, color=FAIL, font_size=18),
        ).arrange(RIGHT, buff=0.25).move_to(UP * 1.4)
        if cards.width > 13.4:
            cards.width = 13.4
        debate = label(r"$1973$: \ Lighthill debates Michie, McCarthy and Gregory on BBC television", font_size=22,
                       color=GREY_A).next_to(cards, DOWN, buff=0.35)
        cut = VGroup(label(r"Britain: \ AI funding cut back to a few universities", font_size=24, color=HIST),
                     label(r"United States: \ DARPA moves to mission-directed projects", font_size=24, color=HIST))
        cut.arrange(DOWN, buff=0.15).next_to(debate, DOWN, buff=0.4)
        w = label(r"the first AI winter: \ roughly $1974$--$1980$", font_size=30, color="#9DB8E0").to_edge(DOWN,
                                                                                                     buff=0.45)
        promise = VGroup(label(r"promised, $1958$: \ a computer chess champion within ten years", font_size=32,
                               color=HIST),
                         note(r"Simon \& Newell: \ the forecast from the opening", font_size=22),
                         label(r"by the late $1960$s: \ the bills came due", font_size=30, color=FAIL))
        promise.arrange(DOWN, buff=0.3).move_to(UP * 0.3)
        with self.voiceover(
            "The founders had promised a great deal, soon. By the late sixties the bills came due. <bookmark mark='a'/> In 1966 "
            "an advisory committee told the US government that machine translation was slower, less accurate and costlier than "
            "human translators, and its funding dried up. <bookmark mark='b'/> In 1969 Minsky and Papert's book Perceptrons laid "
            "out the limits of one-layer neural networks, and that line went quiet for a decade. <bookmark mark='c'/> In 1973 "
            "the mathematician James Lighthill told Britain's Science Research Council that outside toy problems, AI was "
            "defeated by the combinatorial explosion: the very search spaces we have been counting. <bookmark mark='d'/> He "
            "defended his report on television against Donald Michie, John McCarthy and Richard Gregory. "
            "<bookmark mark='e'/> British funding shrank to a few centres; in America, DARPA turned to military goals. The first "
            "winter lasted until about 1980."
        ) as vo:
            self.play(FadeIn(promise[0]), FadeIn(promise[1]))
            self.play(FadeIn(promise[2], shift=UP * 0.1))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                if k == 0:
                    self.play(FadeOut(promise), run_time=0.5)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(debate))
            vo.wait_until("e")
            self.play(FadeIn(cut), FadeIn(w))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def boom(self):
        up = VGroup(
            history_card(1980, r"expert systems sell", r"XCON at Digital; \ companies build their own", width=4.2,
                         color=PATH, font_size=18),
            history_card(1982, r"Japan's Fifth Generation project", r"computers built around logic programming, "
                         r"\ ten years", width=4.2, color=PATH, font_size=18),
            history_card(1983, r"DARPA's Strategic Computing; \ Britain's Alvey", r"the West answers", width=4.2,
                         color=PATH, font_size=18),
        ).arrange(RIGHT, buff=0.25).move_to(UP * 2.0)
        if up.width > 13.4:
            up.width = 13.4
        lisp = VGroup(label(r"Lisp machines:", font_size=24, color=SYMBOL),
                      label(r"workstations built to run AI software \ (Symbolics, LMI, Xerox, Texas Instruments)",
                            font_size=22, color=GREY_A)).arrange(RIGHT, buff=0.2).next_to(up, DOWN, buff=0.4)
        if lisp.width > 13.0:
            lisp.width = 13.0
        down = VGroup(
            history_card(1984, r"AAAI: \ ``AI winter'' named", r"Roger Schank and Marvin Minsky warn the boom will bust",
                         width=4.2, color=FAIL, font_size=18),
            history_card(1987, r"the Lisp-machine market collapses", r"general workstations and PCs run Lisp well "
                         r"enough, \ far cheaper", width=4.2, color=FAIL, font_size=18),
            history_card(1992, r"Fifth Generation ends", r"its goals unmet; \ expert systems prove costly to keep "
                         r"up and brittle", width=4.2, color=FAIL, font_size=18),
        ).arrange(RIGHT, buff=0.25).next_to(lisp, DOWN, buff=0.4)
        if down.width > 13.4:
            down.width = 13.4
            down.set_x(0)
        w = label(r"the second winter: \ late $1980$s to early $1990$s", font_size=30, color="#9DB8E0").to_edge(DOWN,
                                                                                                          buff=0.3)
        with self.voiceover(
            "Expert systems brought the money back. <bookmark mark='a'/> Companies built their own; in 1982 Japan launched a "
            "ten-year Fifth Generation project around logic programming, and America and Britain answered. "
            "<bookmark mark='b'/> A small industry sold Lisp machines, workstations built to run AI software. "
            "<bookmark mark='c'/> In 1984 Roger Schank and Marvin Minsky warned the American AI association that enthusiasm had "
            "outrun results, and named what would follow: an AI winter. <bookmark mark='d'/> In 1987 the Lisp-machine market "
            "collapsed, undercut by ordinary workstations; expert systems proved costly to maintain and brittle; the Fifth "
            "Generation project ended in 1992 short of its goals. <bookmark mark='e'/> The second winter set in, and for years "
            "researchers avoided the words artificial intelligence."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in up], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(lisp))
            vo.wait_until("c")
            self.play(FadeIn(down[0], shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(down[1], shift=UP * 0.15))
            self.play(FadeIn(down[2], shift=UP * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(w))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def moravec(self):
        left = VGroup(label(r"hard for us, \ done by $1990$s machines", font_size=26, color=PATH),
                      *[label(t, font_size=24, color=WHITE) for t in (r"chess at world-champion level",
                                                                       r"proving theorems of logic",
                                                                       r"integrals and algebra", r"checkers",
                                                                       r"configuring computer orders")])
        right = VGroup(label(r"easy for a toddler, \ out of reach", font_size=26, color=FAIL),
                       *[label(t, font_size=24, color=WHITE) for t in (r"recognizing a face in a crowd",
                                                                        r"walking over rough ground",
                                                                        r"picking up a cup",
                                                                        r"understanding a spoken sentence",
                                                                        r"common sense about everyday things")])
        for g in (left, right):
            g.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        left.move_to([-3.4, 0.5, 0])
        right.move_to([3.4, 0.5, 0])
        div = DashedLine([0, 2.6, 0], [0, -1.8, 0], color=GREY_C)
        src = label(r"Hans Moravec, \textit{Mind Children} (1988): \ what we find hard, \ evolution polished least",
                    font_size=22, color=GREY_A).to_edge(DOWN, buff=0.5)
        head = label(r"under the funding story: \ a scientific surprise", font_size=32, color=GREY_A)
        head.to_edge(UP, buff=0.35)
        name = label(r"Moravec's paradox", font_size=36, color=FCOL).move_to(head)
        with self.voiceover(
            "Beneath the funding story lay a scientific surprise. <bookmark mark='a'/> Symbolic programs did best at what "
            "people find hard: logic, algebra, chess. <bookmark mark='b'/> They did worst at what any child does without effort: "
            "seeing, walking, grasping, understanding speech, common sense. <bookmark mark='c'/> Hans Moravec observed in 1988 "
            "that it is comparatively easy to make computers match adults on intelligence tests or at checkers, and hard or "
            "impossible to give them the perception and mobility of a one-year-old. Evolution, he argued, spent hundreds of "
            "millions of years on perception and movement; abstract reasoning is a thin, recent layer. This is Moravec's "
            "paradox."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left[0]), LaggedStart(*[FadeIn(t) for t in left[1:]], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(Create(div), FadeIn(right[0]), LaggedStart(*[FadeIn(t) for t in right[1:]], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(src), FadeTransform(head, name))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tail(self):
        d = load("tail")
        k = np.asarray(d["coverage_k"], float)
        cov = np.asarray(d["coverage"], float)
        top = np.log10(d["n_types"])
        g = axes([0, np.ceil(top)], [0, 1], x_length=6.4, y_length=4.0, xlabel=r"distinct words, \ most common first "
                 r"(log scale)", ylabel=r"share of all the words in the novels", xticks=[0, 1, 2, 3, 4],
                 yticks=[0, 0.5, 0.9, 1], yfmt=lambda v: rf"{int(round(100 * v))}\%", xfmt=lambda v: rf"10^{{{int(v)}}}",
                 center=[-3.0, -0.3, 0])
        cl = curve(g.ax, np.log10(k), cov, GCOST, 4)
        need = d["need"]
        marks = VGroup()
        for q, col in (("0.5", GREY_A), ("0.9", FCOL), ("0.99", HEUR), ("0.999", FAIL)):
            x = np.log10(need[q])
            marks.add(VGroup(DashedLine(g.ax.c2p(x, 0), g.ax.c2p(x, float(q)), color=col, dash_length=0.06),
                             Dot(g.ax.c2p(x, float(q)), radius=0.06, color=col)))
        rows = VGroup(*[label(rf"{int(round(100 * float(q) * 10)) / 10:g}\% of the text: \ ${need[q]:,}$ words"
                              .replace(",", "{,}"), font_size=21, color=col)
                        for q, col in (("0.5", GREY_A), ("0.9", FCOL), ("0.99", HEUR), ("0.999", FAIL))])
        rows.arrange(DOWN, buff=0.14, aligned_edge=LEFT).move_to([3.9, 1.9, 0])
        once = label(rf"${d['once']:,}$ of the ${d['n_types']:,}$ words \\ appear exactly once".replace(",", "{,}"),
                     font_size=21, color=GREY_A).move_to([3.9, 0.3, 0])
        fresh = 100 * d["unseen_passage"][-1]
        pas = VGroup(label(rf"and in the scoreboard passage \ (Hammett, \ Part 1):", font_size=21, color=GREY_A),
                     label(rf"${fresh:.1f}\%$ of its words never occur \\ in ${d['n_tokens'] / 1e6:.1f}$ million words "
                           r"of novels", font_size=21, color=FAIL)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        pas.move_to([3.9, -1.1, 0])
        ex = d["passage_new"]
        pick = [w for w in ex if "'" not in w][:6]
        exm = data_text(", ".join(pick), font=MONO, font_size=18, color=FAIL).next_to(pas, DOWN, buff=0.15)
        if exm.width > 5.6:
            exm.width = 5.6
        tag = note(r"computed: \ Part 1's thirty novels").to_corner(DR, buff=0.15)
        with self.voiceover(
            "There is a measurable reason hand-written knowledge kept running out, and we can see it in the thirty novels of "
            "Part 1. <bookmark mark='a'/> Rank their words from most to least common. <bookmark mark='b'/> The top "
            f"{need['0.5']} words make up half the text. Ninety percent takes {need['0.9']:,}; ninety-nine, {need['0.99']:,}; "
            f"ninety-nine point nine, {need['0.999']:,}. <bookmark mark='c'/> {d['once']:,} of the {d['n_types']:,} different "
            "words occur exactly once. <bookmark mark='d'/> And fresh text brings new ones: in the series' test passage, "
            f"{fresh:.1f} percent of the words never appear in {d['n_tokens'] / 1e6:.1f} million words of novels. Language, "
            "vision and the physical world all have this shape: a few common cases, and an endless tail of rare ones. A rule "
            "for each case never finishes. <bookmark mark='e'/> What finishes is a method that learns from data, and "
            "generalizes to cases nobody wrote down. That is where this course goes next."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(cl), run_time=2.0)
            vo.wait_until("b")
            for m, r in zip(marks, rows):
                self.play(Create(m[0]), FadeIn(m[1]), FadeIn(r), run_time=0.7)
            vo.wait_until("c")
            self.play(FadeIn(once))
            vo.wait_until("d")
            self.play(FadeIn(pas), FadeIn(exm))
            vo.wait_until("e")
            self.play(Indicate(cl, color=PATH))
        self.wait(0.3)
        self.clear_scene()
