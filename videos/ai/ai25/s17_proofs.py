from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai25.common import (HIST, LEAN_C, PAIR_C, PART, PLAIN, PRED_C, SEARCH_C, STRUCT, SYM, TRUE_C, node_box,
                                   take_away, takeaway_anims)


def score_bars(rows, total, W=6.0, x0=-1.0, y0=1.6, dy=0.75, font_size=21):
    g = VGroup()
    for i, (t, v, c) in enumerate(rows):
        y = y0 - i * dy
        name = label(t, font_size=font_size, color=GREY_A)
        name.move_to([x0 - 0.2 - name.width / 2, y, 0])
        bar = Rectangle(width=max(W * v / total, 0.02), height=0.45, stroke_width=0, fill_color=c, fill_opacity=0.85)
        bar.move_to([x0 + bar.width / 2, y, 0])
        val = label(rf"${v:g}$", font_size=font_size + 2, color=c).next_to(bar, RIGHT, buff=0.12)
        g.add(VGroup(name, bar, val))
    return g


class Proofs(VoiceoverScene):
    def construct(self):
        self.card()
        self.checkers()
        self.alphageometry()
        self.olympiad()
        self.research()

    def card(self):
        card = chapter_card(16, r"Geometry and proofs", r"What changes when the checker is perfect?", lit=(),
                            part=PART)
        with self.voiceover("Chapter sixteen. Geometry and proofs."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def checkers(self):
        code = code_block([
            "theorem two_dvd (n : ℕ) : 2 ∣ n * (n + 1) :=",
            "  (Nat.even_mul_succ_self n).two_dvd",
        ], font_size=22, color=WHITE)
        box = SurroundingRectangle(code, color=LEAN_C, buff=0.3, corner_radius=0.12, stroke_width=2)
        lean = VGroup(box, code).move_to([0, 2.3, 0])
        ll = note(r"illustrative: \ Lean 4 with Mathlib; \ the kernel checks every step", font_size=20)
        ll.next_to(lean, DOWN, buff=0.12)
        ok_ = VGroup(MathTex(r"\checkmark", font_size=48, color=STRUCT), label(r"the kernel: \ accepted \ (every step checked)",
                                                                 font_size=26, color=STRUCT)).arrange(RIGHT, buff=0.2)
        ok_.next_to(ll, DOWN, buff=0.35)
        cards = VGroup(
            history_card(1976, r"Appel \& Haken", r"the four-colour theorem, \ by computer; \ checked in Coq in "
                         r"2005 (Gonthier)", width=4.2, color=HIST),
            history_card(2014, r"Flyspeck \ (Hales et al.)", r"the Kepler conjecture on packing spheres, \ "
                         r"formally verified", width=4.2, color=HIST),
            history_card(2022, r"the Liquid Tensor Experiment", r"a hard theorem of Clausen and Scholze, \ "
                         r"formalized in Lean in about eighteen months", width=4.2, color=HIST),
        ).arrange(RIGHT, buff=0.25).move_to([0, -0.3, 0])
        cards.width = min(cards.width * 1.08, 13.4)
        cards.move_to([0, -0.4, 0])
        ml = label(r"Mathlib, \ October 2026: \ $291{,}099$ theorems, \ $139{,}563$ definitions, \ $772$ "
                   r"contributors", font_size=24, color=LEAN_C).to_edge(DOWN, buff=0.45)
        mc = note(r"leanprover-community.github.io, \ Mathlib statistics", font_size=18).next_to(ml, DOWN, buff=0.08)
        with self.voiceover(
            "Mathematics has something no other science has: a checker that cannot be fooled. <bookmark mark='a'/> In a "
            "proof assistant such as Lean, a theorem and its proof are code, and a small kernel checks every inference; this "
            "one says that n times n plus one is even. <bookmark mark='b'/> Computers entered proofs in 1976 with Appel and "
            "Haken's four-colour theorem, which Georges Gonthier checked formally in 2005. <bookmark mark='c'/> Thomas "
            "Hales's proof of the Kepler conjecture was formally verified in 2014, <bookmark mark='d'/> and in 2022 Lean's "
            "community formalized a hard new theorem of Dustin Clausen and Peter Scholze. <bookmark mark='e'/> Lean's "
            "library, Mathlib, now holds about two hundred and ninety thousand theorems; Part 28 shows what reinforcement "
            "learning does with such a checker."
        ) as vo:
            self.play(FadeIn(lean), FadeIn(ll))
            vo.wait_until("a")
            self.play(Indicate(lean, color=LEAN_C, scale_factor=1.02))
            self.play(FadeIn(ok_, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeOut(ok_))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(ml), FadeIn(mc))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def alphageometry(self):
        steps = [(r"random premises \\ (points, lines, circles)", GREY_A), (r"deduce everything: \\ symbolic engine",
                                                                         LEAN_C),
                 (r"trace back each fact \\ to what it needed", SYM), (r"$100$ million \\ theorems with proofs",
                                                                         PAIR_C)]
        boxes = VGroup(*[node_box(t, c, font_size=24, height=1.25) for t, c in steps]).arrange(RIGHT, buff=0.45)
        boxes.width = min(boxes.width, 13.2)
        boxes.to_edge(UP, buff=0.55)
        arr = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.06, color=GREY_B, stroke_width=2.5)
                       for a, b in zip(boxes, boxes[1:])])
        aux = label(r"$9\%$ of them need an extra point the statement never mentions: \ an \textit{auxiliary "
                    r"construction}, \\ which a $151$-million-weight language model learns to propose",
                    font_size=24, color=PRED_C).next_to(boxes, DOWN, buff=0.35)
        aux.width = min(aux.width, 13.0)
        rows = [(r"GPT-4", 0, PLAIN), (r"Wu's method \ (1978)", 10, GREY_B), (r"the symbolic engine alone", 14, LEAN_C),
                (r"AlphaGeometry", 25, PAIR_C), (r"average IMO gold medallist", 25.9, HIST)]
        bars = score_bars(rows, 30, W=5.6, x0=-0.4, y0=0.25, dy=0.62)
        bl = label(r"olympiad geometry problems solved, \ of $30$ \ (IMO 2000--2022)", font_size=20, color=GREY_A)
        bl.next_to(bars, UP, buff=0.15)
        ag2 = label(r"AlphaGeometry 2 (2025): \ $84\%$ of all IMO geometry problems of 2000--2024, \ up from $54\%$",
                    font_size=22, color=PAIR_C).to_edge(DOWN, buff=0.75)
        cite_ = cite(r"Trinh et al., \textit{Nature} (2024); \ Chervonyi et al.\ (2025)", corner=DR)
        with self.voiceover(
            "Olympiad geometry fell first. In January 2024 Trieu Trinh, Thang Luong and colleagues at Google DeepMind "
            "published AlphaGeometry. <bookmark mark='a'/> With no human proofs to learn from, they made their own: random "
            "premises, a symbolic engine deducing all that follows, and a traceback from each new fact to what it needed: a "
            "hundred million theorems with proofs. <bookmark mark='b'/> Nine percent need a point the statement never "
            "mentions, an auxiliary construction, the creative step; a language model learned to propose them, and the "
            "engine does the rest. <bookmark mark='c'/> On thirty olympiad problems it solved twenty-five, against ten for "
            "the best earlier method, fourteen for its engine alone and none for GPT-4; the average gold medallist solves "
            "25.9. <bookmark mark='d'/> A year later AlphaGeometry 2 solved eighty-four percent of the olympiad's geometry "
            "problems since 2000."
        ) as vo:
            self.play(FadeIn(boxes[0]), FadeIn(cite_))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(b)) for a, b in zip(arr, boxes[1:])],
                                  lag_ratio=0.5), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(aux))
            vo.wait_until("c")
            self.play(FadeIn(bl), LaggedStart(*[FadeIn(r_) for r_ in bars], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(ag2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def olympiad(self):
        rows = [(r"2024 \ AlphaProof + AlphaGeometry 2 \ (Lean)", 28, LEAN_C),
                (r"2025 \ Gemini Deep Think; \ OpenAI's model \ (words)", 35, PAIR_C),
                (r"2026 \ two systems, \ graded via the organizers", 42, SEARCH_C)]
        bars = score_bars(rows, 42, W=6.0, x0=-0.2, y0=1.4, dy=1.0, font_size=22)
        gold = VGroup()
        for v, i in ((29, 0), (35, 1)):
            x = -0.2 + 6.0 * v / 42
            y = 1.4 - i * 1.0
            gold.add(DashedLine([x, y + 0.35, 0], [x, y - 0.35, 0], color=C.BITS, dash_length=0.05))
        gl = label(r"dashed: \ the gold-medal line, \ 2024 and 2025", font_size=18, color=C.BITS).next_to(bars, DOWN, buff=0.3)
        head = label(r"points of $42$ at the International Mathematical Olympiad", font_size=26, color=GREY_A)
        head.to_edge(UP, buff=0.45)
        notes = VGroup(
            label(r"2024 and 2025: \ Part 28, \ chapter 13", font_size=22, color=GREY_B),
            label(r"2026, Shanghai: \ Huawei's Celia and Xiaohongshu's dots-note-3.0 reported $42$ of $42$, \\ "
                  r"solutions submitted to the organizers for grading \ (AFP, 23 July 2026); \\ seven of $666$ "
                  r"students also scored $42$", font_size=22, color=SEARCH_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.4)
        for n_ in notes:
            if n_.width > 13.0:
                n_.width = 13.0
        with self.voiceover(
            "Then the olympiad itself, which Part 28 follows in detail. <bookmark mark='a'/> In 2024 AlphaProof, AlphaZero's "
            "method working in Lean, with AlphaGeometry 2 for the geometry, scored twenty-eight of forty-two, one point short "
            "of gold. <bookmark mark='b'/> In 2025 Google's Gemini Deep Think and an experimental OpenAI model each scored "
            "thirty-five, exactly gold, writing proofs in plain language. <bookmark mark='c'/> And in July 2026, in "
            "Shanghai, Huawei and Xiaohongshu reported perfect scores, forty-two of forty-two, with solutions submitted to "
            "the organizers for grading, as AFP reported; seven of the six hundred and sixty-six students also scored "
            "forty-two. As a test for machines, the olympiad is nearly saturated."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bars[0]), Create(gold[0]), FadeIn(gl))
            vo.wait_until("b")
            self.play(FadeIn(bars[1]), Create(gold[1]), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(bars[2]), FadeIn(notes[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def research(self):
        cards = VGroup(
            history_card(2025, r"Gauss \ (Math Inc.)", r"autoformalization: \ the strong prime number theorem, \ "
                         r"about $25{,}000$ lines of Lean in about three weeks, \ by the company's account", width=4.3,
                         color=HIST),
            history_card(2026, r"Erd\H{o}s problem \#728", r"GPT-5.2 Pro and Harmonic's Aristotle: \ an open problem "
                         r"resolved, \ ending in a Lean proof \ (January)", width=4.3, color=HIST),
            history_card(2026, r"Feng et al.\ (Google DeepMind)", r"Gemini on $700$ Erd\H{o}s problems marked open: "
                         r"\ $13$ settled, \ $5$ by seemingly new arguments, \ $8$ already solved in the literature",
                         width=4.3, color=HIST),
        ).arrange(RIGHT, buff=0.25).move_to(UP * 0.8)
        caveats = VGroup(
            label(r"a formal proof is only as good as its statement: \ mistranslate the problem, \ and you prove the "
                  r"wrong thing", font_size=22, color=PLAIN),
            label(r"the easier open problems fall first; \ the experts still choose, \ check and explain",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.6)
        cite_ = cite(r"Math Inc.\ (2025); \ Sothanaphan (2026); \ Feng et al.\ (2026)", corner=DR)
        head = label(r"research mathematics", font_size=34, color=LEAN_C).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Beyond contests, the frontier is research mathematics. <bookmark mark='a'/> Autoformalization, translating "
            "informal mathematics into Lean, sped up sharply: in September 2025 the start-up Math Inc. reported that its "
            "agent Gauss had formalized the strong prime number theorem, about twenty-five thousand lines of Lean, in roughly "
            "three weeks. <bookmark mark='b'/> In January 2026 OpenAI's GPT-5.2 Pro and Harmonic's prover Aristotle resolved "
            "Erdős problem 728, with a proof that ends in Lean. <bookmark mark='c'/> A Google DeepMind team ran Gemini over "
            "seven hundred open Erdős problems: thirteen were settled, five by seemingly new arguments, eight because the "
            "answer was already in the literature. <bookmark mark='d'/> Two cautions: a formal proof proves exactly its "
            "statement, so a mistranslated statement proves the wrong thing; and the problems falling first are the easier "
            "ones."
        ) as vo:
            self.play(FadeIn(cite_), FadeIn(head))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(caveats))
        self.wait(0.6)
        tk = take_away(r"mathematics: \ a perfect checker, \ so search can be trusted")
        with self.voiceover(
            "With a perfect checker, search can be trusted: generate freely, keep only what checks. The last chapter "
            "is about exactly that."
        ):
            self.play(FadeOut(caveats), FadeIn(tk, shift=UP * 0.1), *takeaway_anims(self, tk))
        self.wait(0.3)
        self.clear_scene()
