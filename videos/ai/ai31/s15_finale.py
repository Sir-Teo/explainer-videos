from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai1.s01_hook import sentence_block
from videos.ai.ai31.common import EST, HACK, JUDGE, PART, board_rows, load, stat_card

ACT_CAPTIONS = [
    r"guessing the next character, \ and the mathematics underneath",
    r"learning from data: \ counting, \ fitting, \ networks, \ going downhill",
    r"the transformer, \ and the machinery of scale",
    r"generating and perceiving: \ images, \ sound, \ science",
    r"agency: \ rewards, \ post-training, \ reasoning, \ agents",
    r"looking inside, \ and asking whether to trust it",
]


class Finale(VoiceoverScene):
    def construct(self):
        self.card()
        self.series()
        self.board()
        self.shannon()
        self.last_words()

    def card(self):
        card = chapter_card(14, r"The guessing game, revisited", r"How far has the guessing game come?",
                            lit=(1951, 2026), part=PART)
        with self.voiceover("Chapter fourteen. The guessing game, revisited."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def series(self):
        title = label(r"AI, Built: \ thirty-one parts, \ five acts and a finale", font_size=40).to_edge(UP, buff=0.35)
        smap = series_map(current=None, done=0).scale(0.9).move_to(DOWN * 0.25)
        cap = label(ACT_CAPTIONS[0], font_size=24, color=C.BITS).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Thirty-one parts. <bookmark mark='a'/> We began with a guessing game, and the mathematics underneath it: "
            "information, search and logic, vectors, change and chance. <bookmark mark='b'/> Then learning from data: "
            "counting, fitting, the first networks, seeing and remembering, the long walk downhill, and the "
            "mathematics of scale. <bookmark mark='c'/> Then the transformer, and everything it took to make it big: "
            "memory, sparsity, silicon, pretraining and inference. <bookmark mark='d'/> Then models that generate "
            "and perceive: images and video, every sense as tokens, learning without labels, and science. "
            "<bookmark mark='e'/> Then agency: reinforcement learning, post-training, reasoning and agents. "
            "<bookmark mark='f'/> And the finale: looking inside the model, and asking whether to trust it."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            box = None
            for i, m in enumerate("abcdef"):
                vo.wait_until(m)
                col = smap.cols[i]
                new = label(ACT_CAPTIONS[i], font_size=24, color=C.BITS).to_edge(DOWN, buff=0.3)
                nb = SurroundingRectangle(col, color=C.BITS, buff=0.12, corner_radius=0.1, stroke_width=2)
                self.play(Transform(cap, new) if i else FadeIn(cap), Transform(box, nb) if box else Create(nb),
                          LaggedStart(*[r_.animate.set_color(WHITE) for r_ in col.rows], lag_ratio=0.12),
                          col.head.animate.set_color(C.BITS), run_time=1.5)
                box = box or nb
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def board(self):
        rows, named = board_rows()
        nb = load("novels_bits")
        i_nov = named.get("novels")
        hl = tuple(k for k in (i_nov,) if k is not None)
        board = scoreboard(rows, highlight=hl, max_bits=8.0, row_h=0.36, font_size=20)
        board.scale_to_fit_height(min(board.height, 6.5)).move_to(DOWN * 0.2)
        head = label(r"The scoreboard: \ bits per character on the Falcon passage", font_size=30).to_edge(UP, buff=0.2)

        def mark(key):
            if key in named:
                self.play(Circumscribe(board.rows[named[key]], color=C.NEURAL, buff=0.04), run_time=1.2)

        with self.voiceover(
            "And the scoreboard from Part 1, where it all started: bits per character on one passage of a novel."
        ):
            self.play(FadeIn(head), FadeIn(board), run_time=2.0)
        if "best" in named:
            best = rows[named["best"]]["bits"]
            best_said = f"Counting got us to {best:.2f}."
            with self.voiceover(best_said):
                mark("best")
        if "kn" in named:
            kn = rows[named["kn"]]["bits"]
            kn_said = f"Kneser-Ney smoothing, in Part 7, to {kn:.2f}."
            with self.voiceover(kn_said):
                mark("kn")
        if "tf" in named:
            tf = rows[named["tf"]]["bits"]
            tf_said = f"Our first small transformer, in Part 13, to {tf:.2f}."
            with self.voiceover(tf_said):
                mark("tf")
        lo, hi = nb["ci"]
        mp, bpc, pm = nb["params"] / 1e6, nb["bpc"], (hi - lo) / 2
        ours_said = (f"And the series' own model, {mp:.1f} million parameters trained on thirty novels on this "
                     f"computer, reaches {bpc:.2f}, give or take {pm:.2f}.")
        with self.voiceover(ours_said):
            mark("novels")
        if "top" in named:
            top = rows[named["top"]]["bits"]
            top_said = (f"The large pretrained models of Part 1 reach {top:.2f}; Shannon's readers, guessing letters "
                        "alone, needed between 0.6 and 1.3.")
            with self.voiceover(top_said):
                mark("top")
                mark("human")
        else:
            with self.voiceover("Shannon's readers, guessing letters alone, needed between 0.6 and 1.3."):
                mark("human")
        with self.voiceover("Every row of it is the same idea: a better guess at what comes next."):
            self.play(Indicate(board.unit, color=C.BITS))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def shannon(self):
        d = load("shannon")
        sent = d["sentence"]
        rows1, counts1, _ = sentence_block(sent, d["count_ranks"], font_size=26)
        _, counts2, _ = sentence_block(sent, d["ranks"], font_size=26)
        letters = VGroup(*[m for t in rows1 for m in t])
        grp1 = VGroup(rows1, counts1)
        grp1.shift(UP * 0.5)
        counts2.shift(UP * 0.5)
        who1 = label(rf"Part 1's counting program \ ({d['count_order']} letters of context)", font_size=24,
                     color=C.COUNTING).to_edge(UP, buff=0.35)
        who2 = label(r"our model, \ trained on thirty novels", font_size=24, color=C.NEURAL).to_edge(UP, buff=0.35)
        s1 = stat_card(rf"{d['count_first'] * 100:.0f}\%", r"right at the first guess", C.COUNTING, width=3.4)
        s2 = stat_card(rf"{d['count_total']:.0f}", r"bits for the whole sentence", C.COUNTING, width=3.4)
        t1 = stat_card(rf"{d['first'] * 100:.0f}\%", r"right at the first guess", C.NEURAL, width=3.4)
        t2 = stat_card(rf"{d['total']:.0f}", r"bits for the whole sentence", C.NEURAL, width=3.4)
        VGroup(s1, s2).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.35)
        VGroup(t1, t2).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.35)
        tag = note(r"computed: \ the number under each letter is how many guesses it took", font_size=18)
        tag.to_corner(DR, buff=0.15)
        if d["total"] < d["count_total"]:
            verdict = (f"It needs one guess for {d['first'] * 100:.0f} percent of the letters, and the sentence costs "
                       f"it {d['total']:.0f} bits, against the counting program's {d['count_total']:.0f}.")
        else:
            verdict = (f"It needs one guess for {d['first'] * 100:.0f} percent of the letters, and the sentence costs "
                       f"it {d['total']:.0f} bits, against the counting program's {d['count_total']:.0f}. Shannon's "
                       "sentence has no capitals and no punctuation, the very form the counting program was trained "
                       "on, while our model learned from printed books: here, the counting program wins.")
        with self.voiceover(
            "And back to where we began: Shannon's own sentence. <bookmark mark='a'/> In Part 1 a counting program "
            f"played his game. It guessed {d['count_first'] * 100:.0f} percent of the letters at the first try, and "
            f"the whole sentence cost it {d['count_total']:.0f} bits. <bookmark mark='b'/> Now our model plays. It "
            "reads tokens, not letters, so we add up its probabilities over every way its tokens could spell the next "
            "letter, and let it guess in order. <bookmark mark='c'/> " + verdict
        ) as vo:
            self.play(FadeIn(letters), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(who1), LaggedStart(*[FadeIn(c_) for c_ in counts1], lag_ratio=0.02), FadeIn(s1),
                      FadeIn(s2), run_time=2.5)
            vo.wait_until("b")
            self.play(ReplacementTransform(who1, who2), FadeOut(s1), FadeOut(s2))
            self.play(LaggedStart(*[ReplacementTransform(a_, b_) for a_, b_ in zip(counts1, counts2)], lag_ratio=0.02),
                      run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(t1), FadeIn(t2))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def last_words(self):
        q = label(r"``\dots we had better be quite sure that the purpose put into the machine \\ is the purpose which "
                  r"we really desire and not merely a colorful imitation of it.''", font_size=30)
        who = label(r"Norbert Wiener, \ 1960", font_size=24, color=GREY_B).next_to(q, DOWN, buff=0.3)
        g = VGroup(q, who).move_to(UP * 0.6)
        words = VGroup(label(r"to guess well, \ a model must know a great deal", font_size=28, color=EST),
                       label(r"to trust it, \ we must measure what it does, \ and why", font_size=28, color=JUDGE))
        words.arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Shannon asked how much a reader must know to guess the next letter well. The answer turned out to be: a "
            "great deal, about the world as well as the language, and machines that guess well enough have learned "
            "much of it. <bookmark mark='a'/> That is exactly why they need measuring with care: what they can do, "
            "what we actually asked of them, and what they do when we are not looking. <bookmark mark='b'/> Wiener "
            "put it in one sentence, sixty-six years ago, and it is still the right one."
        ) as vo:
            self.play(FadeIn(words[0]))
            vo.wait_until("a")
            self.play(FadeIn(words[1]))
            vo.wait_until("b")
            self.play(FadeIn(g, shift=UP * 0.1))
        self.wait(1.5)
        self.clear_scene()
