from __future__ import annotations

import numpy as np

from videos.music.music13.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 11, r"Frontier: \ what makes a chord sound as it does?", r"Can a model hear a chord the way you do?", extra=((2020, r"three ingredients of consonance"),),
                spoken="Frontier: what makes a chord sound as it does?")
        self.four()
        self.listener()
        self.fails()
        self.open()

    # ------------------------------------------------------------------
    def four(self):
        d = load("frontier")
        cols = VGroup()
        for j, (title, order, col) in enumerate(((r"listeners", d["listeners"], WHITE), (r"roughness \ (Part 5)", d["by_roughness"], GREY_A), (r"fusion into one pitch \ (Part 4)", d["by_fusion"], GREY_A))):
            head = label(title, font_size=28, color=col)
            items = VGroup(*[label(rf"{i + 1}. \ {k}", font_size=30, color=KIND_COLOR[k]) for i, k in enumerate(order)]).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
            cols.add(VGroup(head, items).arrange(DOWN, buff=0.4))
        cols.arrange(RIGHT, buff=1.2, aligned_edge=UP).move_to(UP * 0.6)
        head = label(r"the four triads, \ most consonant first", font_size=30, color=GREY_A).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Which triad is the most consonant? Ask listeners, and study after study gives the same "
            "order: major, minor, diminished, augmented. <bookmark mark='a'/> Now ask the two models we "
            "built. Part 5's roughness says: major, minor, augmented, diminished. <bookmark mark='b'/> "
            "Part 4's fusion into one pitch says the same. Both models put the augmented triad above "
            "the diminished. Listeners put it last."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cols[0]))
            vo.wait_until("a")
            self.play(FadeIn(cols[1]))
            vo.wait_until("b")
            self.play(FadeIn(cols[2]))
            self.play(Indicate(cols[0][1][3], color=AUG_C), Indicate(cols[1][1][2], color=AUG_C), Indicate(cols[2][1][2], color=AUG_C))
        three = VGroup(label(r"interference between partials", font_size=28, color=WHITE), label(r"harmonicity", font_size=28, color=WHITE), label(r"familiarity", font_size=28, color=TUNE)).arrange(RIGHT, buff=0.9)
        cite = label(r"P. Harrison and M. Pearce, \ \textit{Psychological Review} \ (2020)", font_size=22, color=GREY_B)
        g = VGroup(three, cite).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "So something is missing. In 2020 Peter Harrison and Marcus Pearce tested some twenty "
            "published models of consonance against listeners' ratings, and concluded that it takes "
            "three ingredients together. <bookmark mark='a'/> Interference between partials, which is "
            "our roughness. Harmonicity, which is our fusion. <bookmark mark='b'/> And plain "
            "familiarity: how often a listener has heard the chord. The augmented triad is smooth, and "
            "it is rare; and nobody yet has a model that predicts the ratings of every chord, in every "
            "spacing, for every listener."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(three[0]), FadeIn(three[1]), FadeIn(cite))
            vo.wait_until("b")
            self.play(FadeIn(three[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def listener(self):
        d = load("frontier")
        bars = note_bars(d["chroma"], d["chroma_names"], width=7.0, height=2.2, color=WEAK, hot=(0, 4, 7), hot_color=MAJOR_C, fmt="{:.2f}", font_size=20).move_to(LEFT * 2.9 + DOWN * 0.6)
        bh = label(r"a C major triad on the piano, \ folded onto twelve notes", font_size=24, color=GREY_A).next_to(bars, UP, buff=0.35)
        acc = d["accuracy"]
        rows = VGroup(*[VGroup(label(nm, font_size=24, color=GREY_A), label(rf"{acc[key]['4']} of 24", font_size=26, color=TUNE)).arrange(RIGHT, buff=0.3) for key, nm in
                        (("root position, middle", r"root position"), ("first inversion", r"first inversion"), ("second inversion", r"second inversion"), ("close, two octaves down", r"low and close"))]).arrange(DOWN, buff=0.3, aligned_edge=RIGHT).move_to(RIGHT * 4.3 + DOWN * 0.4)
        head = label(r"a listener: \ spectrum $\rightarrow$ twelve notes $\rightarrow$ the nearest of 24 templates", font_size=28, color=GREY_A).to_edge(UP, buff=0.5)
        total = sum(acc[k]["4"] for k in acc)
        with self.voiceover(
            "Now turn the question round. Can a machine name a chord from its sound? Monochord has a "
            "small listener. It takes the spectrum, Part 3's Fourier transform once more, folds it onto "
            "the twelve notes, and compares the result with a template for each of the twenty-four "
            "major and minor triads. <bookmark mark='a'/> Here is what it sees in a C major triad on "
            "the piano: C, E and G, and a trace of B and D, which are harmonics of the E and the G. "
            f"<bookmark mark='b'/> On clean piano chords it is right every time: {say(total)} out of "
            f"{say(4 * 24)}, in every inversion, even low and close in the mud."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bars), FadeIn(bh))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fails(self):
        d = load("frontier")
        v = d["variation"]
        g = VGroup()
        for j, ph in enumerate(v):
            y = 1.9 - 0.72 * j
            cells = VGroup(*[label(tex(r["heard"]), font_size=30, color=WHITE if r["ok"] else EAR).move_to([0.6 + 1.1 * i, y, 0]) for i, r in enumerate(ph["rows"])])
            g.add(VGroup(label(ph["name"], font_size=24, color=GREY_A).move_to([-5.9, y, 0], aligned_edge=LEFT), cells, label(rf"{ph['right']} of {ph['of']}", font_size=24, color=GREY_B).move_to([5.6, y, 0])))
        head = label(rf"the listener on this part's Variation, \ half a bar at a time: \ {d['variation_right']} of {d['variation_of']}", font_size=28, color=GREY_A).to_edge(UP, buff=0.5)
        cap = VGroup(label(r"C major heard as A minor: \ two notes shared; \ neighbours on Euler's map", font_size=28, color=EAR),
                     label(r"the hard part is not hearing the notes. \ It is deciding which notes are the chord.", font_size=28, color=TUNE)).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.45)
        wrong = d["variation_of"] - d["variation_right"]
        with self.voiceover(
            "So we gave it something harder: this part's Variation, the Tune with its accompaniment, "
            f"half a bar at a time. It names {say(d['variation_right'])} chords out of "
            f"{say(d['variation_of'])}. <bookmark mark='a'/> And {say(wrong - 1)} of its {say(wrong)} "
            "mistakes are the same mistake. It hears C major as A minor, just after the melody or the "
            "chord before has sounded an A that is still ringing. C major and A minor share two notes; "
            "they are neighbours on Euler's map."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in g], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(cap[0]))
        with self.voiceover(
            "That is the real difficulty of chord recognition. It is not hearing the notes. It is "
            "deciding which notes count as the chord, when the answer depends on what came before and "
            "what comes next. Human experts disagree too: in one study, four annotators labelling the "
            "same fifty songs agreed on the root of the chord only about three quarters of the time."
        ):
            self.play(FadeIn(cap[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def open(self):
        star = VGroup(label(r"$\bigstar$ \ open", font_size=30, color=LIMIT),
                      label(r"from chord names to Roman numerals: \ which key, \ and what job does each chord do in it?", font_size=28, color=WHITE),
                      label(r"the best published systems match an expert's full analysis on about half the chords", font_size=26, color=GREY_A),
                      label(r"harmony is not in the sound at one moment. \ It is in how moments follow one another.", font_size=30, color=TUNE)).arrange(DOWN, buff=0.4).move_to(UP * 0.2)
        with self.voiceover(
            "Harder still is the step from chord names to Roman numerals: deciding the key, and the job "
            "each chord does in it. <bookmark mark='a'/> On classical pieces, the best published "
            "systems agree with an expert's complete analysis on only about half the chords. "
            "<bookmark mark='b'/> And that tells us where the subject really lives. Harmony is not in "
            "the sound at any one moment. It is in how moments follow one another, and that is where "
            "the next parts of this series go."
        ) as vo:
            self.play(FadeIn(star[0]), FadeIn(star[1]))
            vo.wait_until("a")
            self.play(FadeIn(star[2]))
            vo.wait_until("b")
            self.play(FadeIn(star[3]))
        self.wait(0.4)
        self.clear_scene()
