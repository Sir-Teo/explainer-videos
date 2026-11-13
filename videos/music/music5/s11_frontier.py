from __future__ import annotations

import numpy as np

from videos.music.music5.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 10, r"Frontier: \ one model for all of it", r"Can the three layers be put into one calculation?", lit=(2016,),
                extra=((2020, r"a composite model"), (2024, r"235,440 judgments")))
        self.composite()
        self.online()
        self.open()

    # ------------------------------------------------------------------
    def composite(self):
        card = history_card(2020, r"Peter Harrison and Marcus Pearce, \ \textit{Psychological Review}",
                            r"gather a century of models, twenty in all, and test every one against the same listening data and against what composers actually wrote.",
                            width=5.8).to_corner(UL, buff=0.4)
        parts = VGroup(label(r"roughness", font_size=34, color=ROUGH), MathTex(r"+", font_size=40), label(r"harmonicity", font_size=34, color=EAR), MathTex(r"+", font_size=40),
                       label(r"familiarity", font_size=34, color=HIST)).arrange(RIGHT, buff=0.35).move_to(UP * 0.2)
        notes = VGroup(label(r"each of the three adds something the other two cannot", font_size=26, color=GREY_A),
                       label(r"familiarity is measured too: \ how often a chord occurs in 100,000 pieces of music", font_size=26, color=GREY_A),
                       label(r"no single cause wins", font_size=30, color=GOOD)).arrange(DOWN, buff=0.25).move_to(DOWN * 1.6)
        with self.voiceover(
            "Can the three layers be put into one calculation? <bookmark mark='a'/> In 2020 Peter Harrison and "
            "Marcus Pearce collected the models of a century, twenty of them, and ran every one against the same "
            "sets of listeners' judgments. <bookmark mark='b'/> The best account was not any single theory. It "
            "was a sum: a roughness term, a harmonicity term, and a familiarity term. <bookmark mark='c'/> The "
            "third is the new one. They measured familiarity by counting how often each chord occurs in more "
            "than a hundred thousand pieces of written music. Each term explained something that the other two "
            "could not. <bookmark mark='d'/> After twenty-five centuries, the answer to which theory is right "
            "turns out to be: all three, in proportions that can be measured."
        ) as vo:
            ask = label(r"three layers: \ can they be one calculation?", font_size=36, color=LIMIT).to_edge(DOWN, buff=0.6)
            self.play(FadeIn(ask), run_time=0.6)
            vo.wait_until("a")
            self.play(FadeIn(card))
            vo.wait_until("b")
            self.play(FadeOut(ask), LaggedStart(*[FadeIn(p) for p in parts], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(notes[0]), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def online(self):
        d, p = load("stretched"), load("curve")
        card = history_card(2024, r"Raja Marjieh, Peter Harrison and colleagues, \ \textit{Nature Communications}",
                            r"twenty-three experiments online, more than four thousand people in the United States and South Korea, 235,440 judgments.",
                            width=5.8).to_corner(UL, buff=0.4)
        g = ratio_axis(1.0, 2.25, y_hi=1.0, x_length=6.6, y_length=2.4, marks=((1, 1), (5, 4), (3, 2), (2, 1)), font_size=18)
        g.move_to(RIGHT * 3.2 + UP * 1.4)
        a = rcurve(g, p["r"], p["curve"], AIR).set_stroke(opacity=0.6)
        b = rcurve(g, d["r"], d["curve"], TUNE)
        gl = label(r"this part's two curves: \ what they tested, \ on people", font_size=22, color=GREY_B).next_to(g, UP, buff=0.15)
        finds = VGroup(
            label(r"stretch or squeeze the partials, \ and the intervals people prefer move with them", font_size=26, color=GOOD),
            label(r"with the partials of a Javanese gong-chime, \ preferences fall near the steps of a gamelan scale", font_size=26, color=GOOD),
            label(r"a surprise: \ people like a slightly mistuned interval. \ Slow beats are pleasant.", font_size=26, color=TUNE),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(DOWN * 1.9)
        with self.voiceover(
            "And the experiment that this part has been leading to has now been done on people, at a scale no "
            "laboratory could manage. <bookmark mark='a'/> In 2024 Raja Marjieh, Peter Harrison and their "
            "colleagues ran twenty-three experiments online, with more than four thousand participants in the "
            "United States and South Korea, and collected nearly a quarter of a million judgments. Instead of "
            "testing a dozen named intervals, they mapped pleasantness across the whole continuum, for many "
            "different timbres. <bookmark mark='b'/> When the partials were stretched or squeezed, the intervals "
            "people preferred moved with them, as the curves of chapter six predict. <bookmark mark='c'/> When "
            "the tones were given the partials of a bonang, a gong-chime of the Javanese gamelan, people who had "
            "never heard a gamelan preferred intervals close to the steps of a gamelan scale. "
            "<bookmark mark='d'/> And there was a surprise. Listeners liked intervals a little better when they "
            "were slightly out of tune. Slow beats, it seems, are not a flaw. They are pleasant, as every "
            "accordion maker and every string section already knew."
        ) as vo:
            self.play(FadeIn(g), Create(a), Create(b), FadeIn(gl), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(card))
            for mark, f in zip("bcd", finds):
                vo.wait_until(mark)
                self.play(FadeIn(f), run_time=0.6)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def open(self):
        head = label(r"What is not known", font_size=40, color=LIMIT).to_edge(UP, buff=0.4)
        rows = rows_card([
            (r"major and minor", r"harmonicity tells them apart. \ Nothing here explains why, \ in the West, \\ one is heard as bright and the other as dark. \quad $\rightarrow$ Part 46"),
            (r"the augmented chord", r"listeners rank it below the diminished one; \\ roughness and harmonicity both say the opposite."),
            (r"infants", r"do babies prefer consonance before they have heard much music? \\ Early studies said yes; \ later ones, \ controlling for familiarity, \ did not find it."),
            (r"chords in motion", r"the same chord is restful in one place and tense in another. \\ Consonance in context is a different problem. \quad $\rightarrow$ Parts 13 and 18"),
        ], left=-6.4, text_left=-2.9, top=1.75, step=1.4, name_size=28, text_size=23, color=LIMIT)
        with self.voiceover(
            "Here is where the knowledge runs out. <bookmark mark='a'/> Major and minor. Harmonicity separates "
            "them, but nothing in this part explains why Western listeners hear one as bright and the other as "
            "dark. That is a question about emotion, and we will take it up much later. <bookmark mark='b'/> The "
            "augmented chord. Listeners rank it below the diminished one. Roughness and harmonicity both say "
            "the opposite. <bookmark mark='c'/> Infants. If the preference for consonance is learned, babies "
            "should not have it. Early studies found that they did. Later ones, which controlled for what the "
            "babies had just been listening to, did not. It is still argued over. <bookmark mark='d'/> And "
            "chords in motion. Everything in this part was about a chord standing still. In a piece of music "
            "the same chord can be a place of rest or a point of tension, depending on what came before. That "
            "is not a property of the chord at all, and it is where harmony begins."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.4)
        self.clear_scene()
