from __future__ import annotations

import numpy as np

from videos.psychology.psych8.common import *  # noqa: F403


class Erp(VoiceoverScene):
    def construct(self):
        self.card()
        self.buried()
        self.root_n()
        self.n400()

    def card(self):
        card = chapter_card(3, r"Averaging out the noise", r"How do you find a signal a quarter the size of the noise?",
                            lit={1980: r"the N400"}, part=PART, scale=("brain", "mind"), marr=("what", "how"))
        with self.voiceover(
            "Chapter three. Averaging out the noise."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def _axes(self, center, y=(-45, 45), yticks=(-40, 0, 40), x_length=6.0, y_length=2.0, xlabel=r""):
        return axes([-100, 800], list(y), x_length=x_length, y_length=y_length, xticks=[0, 200, 400, 600, 800],
                    yticks=list(yticks), xlabel=xlabel, ylabel=r"", center=center)

    def buried(self):
        e = load("erp")
        head = heading(r"One word, one trial: \ the answer is in there, and you cannot see it")
        A = self._axes([-3.4, 1.45, 0], y_length=1.8, xlabel=r"")
        B = self._axes([-3.4, -1.75, 0], y=(-9, 9), yticks=(-5, 0, 5), y_length=1.6, xlabel=r"time after the word (ms)")
        singles = VGroup(*[curve(A.ax, e["t"], np.clip(s, -45, 45), EEGC, stroke_width=2) for s in e["singles"]])
        hidden = curve(B.ax, e["t"], e["template"], MODEL, stroke_width=4)
        la = label(r"three single trials (microvolts)", font_size=24, color=EEGC).next_to(A, UP, buff=0.1)
        lb = label(r"what the word added to each, \ enlarged", font_size=24, color=MODEL).next_to(B, UP, buff=0.3)
        rows = rows_of([
            (rf"the brain's ongoing activity: \ about {e['noise_sd']:.0f} microvolts", EEGC),
            (rf"the response to one word: \ about {e['component_uv']:.0f}", MODEL),
            (r"the response is locked to the word; \ the rest is not", THRESH),
        ], 5.2, 30).move_to([4.2, -0.2, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"simulated trials (Psyche)")
        with self.voiceover(
            "Now use that millisecond timing to ask a question about the mind. Show someone a word, and "
            "record the EEG for the next second. <bookmark mark='a'/> Here are three such trials. They "
            "look like noise, and mostly they are: the brain's own ongoing activity, about "
            f"{e['noise_sd']:.0f} millionths of a volt. <bookmark mark='b'/> Hidden in each one is what "
            f"the word added. In this model that's a wave of about {e['component_uv']:.0f} microvolts, a "
            "quarter the size of the noise. It's drawn below, enlarged. You can't find it in any single "
            "trial. <bookmark mark='c'/> But it has one property the noise doesn't. It's locked to the "
            "word. It comes at the same moment after every word, with the same shape. The ongoing activity "
            "has no idea when the word appeared. So line the trials up on the word, and average."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(la))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(s) for s in singles], lag_ratio=0.5), FadeIn(rows[0]), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(B), FadeIn(lb), Create(hidden), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2], shift=UP * 0.1))
        self.clear_scene()

    def root_n(self):
        e = load("erp")
        head = heading(r"Averaging: \ the noise falls as $1/\sqrt{n}$")
        panels = VGroup()
        for i, (n, key) in enumerate(((10, "avg_10"), (50, "avg_50"), (200, "avg_200"))):
            A = self._axes([-4.6, 1.75 - 1.95 * i, 0], y=(-16, 16), yticks=(-10, 0, 10), x_length=4.2, y_length=1.45,
                           xlabel=r"time after the word (ms)" if i == 2 else r"")
            c = curve(A.ax, e["t"], np.clip(e[key], -16, 16), EEGC, stroke_width=2.5)
            m = curve(A.ax, e["t"], e["template"], MODEL, stroke_width=2)
            lab = label(rf"average of {n}", font_size=27, color=EEGC).next_to(A.ax.c2p(800, 0), RIGHT, buff=0.2)
            panels.add(VGroup(A, m, c, lab))
        Bx = axes([0, 200], [0, 21], x_length=4.4, y_length=3.0, xticks=[0, 50, 100, 150, 200], yticks=[0, 10, 20],
                  xlabel=r"trials averaged, $n$", ylabel=r"noise left (microvolts)", center=[4.1, 0.9, 0])
        bx = Bx.ax
        nn = np.linspace(1, 200, 200)
        th = curve(bx, nn, 20.0 / np.sqrt(nn), MODEL, stroke_width=3)
        pts = VGroup(*[Dot(bx.c2p(float(n), float(v)), radius=0.07, color=EEGC) for n, v in zip(e["ns"], e["left"])])
        lg = legend([(EEGC, r"measured"), (MODEL, r"$20/\sqrt{n}$")], font_size=27)
        lg.next_to(bx.c2p(200, 15), DL, buff=0.1)
        rows = rows_of([
            (r"four times the trials for half the noise", THRESH),
            (rf"to bring 20 microvolts down to 1: \ {e['trials_for_1uv']} trials", WHITE),
        ], 5.4, 30, 0.25).move_to([4.0, -2.35, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"simulated trials (Psyche)")
        with self.voiceover(
            "Average ten trials, and the wave begins to show. <bookmark mark='a'/> Fifty, and it's clear. "
            "<bookmark mark='b'/> Two hundred, and the average lies almost on the hidden wave. The noise "
            "hasn't been removed from any trial. It's been cancelled against itself. <bookmark mark='c'/> "
            "And it cancels at a rate you can calculate, the same rate as every average in this series. "
            "The noise left after n trials is the noise in one trial, divided by the square root of n. "
            "The dots are measured on the simulated trials. The line is the formula. "
            "<bookmark mark='d'/> That square root is the economics of the whole method. To halve the "
            "noise you need four times the trials. To bring twenty microvolts down to one, you need "
            f"{e['trials_for_1uv']}. That's why an experiment of this kind shows people hundreds of words, "
            "and why its result is called an event-related potential: a potential that only exists as an "
            "average over events."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(panels[0]))
            vo.wait_until("a")
            self.play(FadeIn(panels[1]))
            vo.wait_until("b")
            self.play(FadeIn(panels[2]))
            vo.wait_until("c")
            self.play(FadeIn(Bx), Create(th), FadeIn(pts, lag_ratio=0.2), FadeIn(lg), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
        self.clear_scene()

    def n400(self):
        k = archive.KUTAS_HILLYARD_1980.data
        e = load("erp")
        head = heading(r"1980: \ a wave that answers to meaning")
        s1 = VGroup(label(r"He spread the warm bread with", font_size=34), label(r"butter.", font_size=34, color=MODEL)
                    ).arrange(RIGHT, buff=0.15, aligned_edge=DOWN)
        s2 = VGroup(label(r"He spread the warm bread with", font_size=34), label(r"socks.", font_size=34, color=BAD)
                    ).arrange(RIGHT, buff=0.15, aligned_edge=DOWN)
        sents = VGroup(s1, s2).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(head, DOWN, buff=0.4)
        A = axes([-100, 800], [-8, 6], x_length=7.0, y_length=2.6, xticks=[0, 200, 400, 600, 800], yticks=[-5, 0, 5],
                 xlabel=r"time after the last word (ms)", ylabel=r"microvolts", center=[-3.0, -1.1, 0])
        ax = A.ax
        cu = curve(ax, e["t"], e["usual_200"], MODEL, stroke_width=3.5)
        co = curve(ax, e["t"], e["avg_200"], BAD, stroke_width=3.5)
        mark = VGroup(DashedLine(ax.c2p(400, -8), ax.c2p(400, 6), color=THRESH, stroke_width=2),
                      label(r"400 ms", font_size=24, color=THRESH).next_to(ax.c2p(400, 6), UP, buff=0.04))
        rows = rows_of([
            (r"a word that does not fit: \ a negative wave, \ largest near 400 ms", BAD),
            (r"they had expected the positive wave that follows any surprise", GREY_A),
            (r"it grows with how unexpected the word's \emph{meaning} is", WHITE),
            (r"a number, read off a scalp, \ that follows understanding as it happens", P.ACCENT),
        ], 5.0, 28, 0.28).move_to([4.5, -1.2, 0])
        keep_in_frame(rows)
        src = historical_tag(archive.KUTAS_HILLYARD_1980.cite)
        tag = psyche_tag(r"curves: a model (Psyche), not their data")
        with self.voiceover(
            "Here's the most famous use. In 1980 Marta Kutas and Steven Hillyard showed people sentences, "
            "one word at a time. <bookmark mark='a'/> Most ended sensibly. He spread the warm bread with "
            "butter. <bookmark mark='b'/> Some didn't. He spread the warm bread with socks. "
            "<bookmark mark='c'/> They averaged the EEG after the last word, separately for the two kinds "
            "of ending. After socks there's a negative wave that butter doesn't produce, largest about "
            "four hundred milliseconds after the word. It was named the N400. <bookmark mark='d'/> They "
            "had expected something else: the positive wave that follows any surprising event, like a rare "
            "tone, which is called the P300. A word printed in larger type produced a wave of that kind. A "
            "word with the wrong meaning produced this. <bookmark mark='e'/> And it's graded. The less expected the "
            "meaning, the larger the wave. So here's a quantity read off the scalp that follows "
            "understanding while it's happening, four tenths of a second after the word, long before the "
            "person could tell you anything. It goes on the Ledger today."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag))
            self.play(Write(s1[0]), run_time=3.5)
            vo.wait_until("a")
            self.wait(1.5)
            self.play(FadeIn(s1[1], scale=1.2))
            vo.wait_until("b")
            self.play(FadeIn(s2, lag_ratio=0.3), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(A), Create(cu), Create(co), run_time=3.0)
            self.play(FadeIn(mark), FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
        self.clear_scene()
