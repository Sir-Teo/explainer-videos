from __future__ import annotations

import numpy as np

from videos.psychology.psych15.common import *  # noqa: F403


class Smell(VoiceoverScene):
    def construct(self):
        self.card()
        self.code()
        self.flavour()
        self.trillion()
        self.fragile()

    def card(self):
        card = chapter_card(11, r"Smell and taste", r"How many smells are there?",
                            lit={1901: r"Hänig", 1991: r"Buck \& Axel", 2014: r"Bushdid"}, part=PART,
                            scale=("molecule", "mind"), marr=("what", "how"))
        with self.voiceover("Chapter eleven. Smell and taste."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def code(self):
        head = heading(r"A combinatorial code")
        rng = np.random.default_rng(1512)
        grid = VGroup()
        odours = (r"lemon", r"coffee", r"rose")
        pats = [rng.random(12) < p for p in (0.3, 0.45, 0.25)]
        for r, (name, pat) in enumerate(zip(odours, pats)):
            lab = label(name, font_size=24, color=SMELL).move_to([-5.4, 1.4 - 0.9 * r, 0])
            cells = VGroup(*[Square(0.5, stroke_color=GREY_D, stroke_width=1.5, fill_color=SMELL if on else BLACK,
                                    fill_opacity=0.85 if on else 0.2).move_to([-4.2 + 0.6 * k, 1.4 - 0.9 * r, 0])
                             for k, on in enumerate(pat)])
            grid.add(VGroup(lab, cells))
        cap = label(r"receptor types (a dozen of about 400)", font_size=22, color=GREY_B).next_to(grid, UP, buff=0.25)
        rows = rows_of([
            (r"1991: \ Buck and Axel find a family of about a thousand receptor genes in rodents \ (Nobel Prize, \ 2004)", WHITE),
            (r"people have about 400 working types; \ each nose cell carries one", SMELL),
            (r"each odour excites a pattern of types, \ and each type answers to many odours", PRIOR),
            (r"so smell is a code of combinations, \ like colour, \ but with hundreds of dimensions instead of three", TIMING),
        ], 12.6, 26, 0.26).to_edge(DOWN, buff=0.75)
        tag = note(r"drawn: \ the patterns are illustrative").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Smell begins with molecules binding to receptors in the roof of the nose. <bookmark mark='a'/> In 1991, "
            "Linda Buck and Richard Axel found the genes for those receptors: a family that turned out to number "
            "about a thousand in rodents, the largest gene family known at the time. It won them the Nobel Prize in "
            "2004. <bookmark mark='b'/> People have about four hundred working types, and each smell-sensing cell "
            "carries just one. <bookmark mark='c'/> An odour excites a pattern of receptor types, and each type "
            "responds to many different odours. <bookmark mark='d'/> So smell is a combinatorial code, like the three "
            "cones of colour vision in Part 13, but with hundreds of dimensions instead of three."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cap))
            self.play(LaggedStart(*[FadeIn(g) for g in grid], lag_ratio=0.5), run_time=2.5)
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def flavour(self):
        head = heading(r"Taste, \ and the map that never was")
        rows = rows_of([
            (r"taste has five qualities: \ sweet, \ salty, \ sour, \ bitter, \ umami", WHITE),
            (r"most of what we call flavour is smell, \ breathed out from the back of the mouth: \ hold your nose and taste", SMELL),
            (r"1901: \ Hänig measures small differences in sensitivity around the tongue", GREY_A),
            (r"1942: \ redrawn in a history; \ textbooks turn it into zones: \ sweet at the tip, \ bitter at the back", BAD),
            (r"every part of the tongue with taste buds detects every taste \ (Collings, \ 1974)", TIMING),
        ], 12.6, 27, 0.4).move_to([0, -0.1, 0])
        tag = historical_tag(archive.HANIG_1901.cite)
        with self.voiceover(
            "Taste is simpler. <bookmark mark='a'/> The tongue reports five qualities: sweet, salty, sour, bitter, "
            "and umami, the savoury taste of glutamate. <bookmark mark='b'/> Most of what we call flavour is actually "
            "smell, carried from the back of the mouth up into the nose as we breathe out. Hold your nose and eat a "
            "jelly bean, and you'll taste sweet, but not cherry. <bookmark mark='c'/> And then there's the tongue map. "
            "In 1901, David Hänig measured small differences in how sensitive different points around the tongue were "
            "to each taste. <bookmark mark='d'/> In 1942 the Harvard historian of psychology Edwin Boring replotted his "
            "data, and textbooks turned small differences into separate zones: sweet at the tip, bitter at the back. "
            "Generations of schoolchildren were taught it. <bookmark mark='e'/> It isn't true. Virginia Collings "
            "remeasured in 1974: the differences are real but small, and every part of the tongue with taste buds "
            "detects every taste. The finding was fine. The story built on it was not."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def trillion(self):
        head = heading(r"A trillion smells?")
        rows = rows_of([
            (r"2014: \ Bushdid and colleagues: \ mixtures of 10, \ 20 or 30 odorants from 128", WHITE),
            (r"26 people tried to tell pairs of mixtures apart, \ sharing more or fewer components", SMELL),
            (r"from the overlap at which pairs became hard to tell apart, \ they extrapolated: \ at least 1.7 trillion", TIMING),
            (r"2015: \ Gerkin and Castro, \ and Meister, \ reanalyse: \ the count could have come out almost anywhere", BAD),
        ], 12.6, 28, 0.42).move_to([0, -0.1, 0])
        tag = published_tag(archive.BUSHDID_2014.cite)
        with self.voiceover(
            "So how many smells can people tell apart? <bookmark mark='a'/> In 2014, Caroline Bushdid and colleagues "
            "made mixtures of ten, twenty or thirty odorants, chosen from a hundred and twenty-eight. "
            "<bookmark mark='b'/> Twenty-six people tried to tell pairs of mixtures apart, pairs that shared more or "
            "fewer of their components. <bookmark mark='c'/> From how much overlap made pairs hard to distinguish, they "
            "extrapolated to the whole space of possible mixtures, and announced that people can discriminate at least "
            "one trillion smells. It was everywhere in the news. <bookmark mark='d'/> In 2015, two reanalyses, by "
            "Richard Gerkin and Jason Castro, and by Markus Meister, argued that the extrapolation was fragile: the same "
            "method, with tiny changes, could give almost any number. Meister applied it to colour vision and got an "
            "infinite number of colours."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def fragile(self):
        d = load("smell")
        head = heading(r"How fragile is a count like that?")
        A = axes([0.3, 0.95], [0, 26], x_length=7.0, y_length=4.2, xticks=[0.3, 0.5, 0.7, 0.9], xfmt=lambda v: pct(v),
                 yticks=[0, 5, 10, 15, 20, 25], yfmt=lambda v: rf"10^{{{int(v)}}}",
                 xlabel=r"overlap below which two mixtures count as different", ylabel=r"discriminable mixtures",
                 center=[-2.4, -0.3, 0])
        ax = A.ax
        c = curve(ax, d["thr"], d["log10_est"], SMELL, stroke_width=4)
        tri = DashedLine(ax.c2p(0.3, 12), ax.c2p(0.95, 12), color=TIMING, stroke_width=2)
        trl = label(r"a trillion", font_size=22, color=TIMING).next_to(tri, UP, buff=0.05).align_to(tri, LEFT)
        m = d["marks"]
        rows = rows_of([
            (r"mixtures of 30 from 128; \ count how many fit if each needs a private neighbourhood", WHITE),
            (rf"threshold 40\%: \ about {m['0.4']:.0f}; \ 60\%: \ about 2 million; \ 80\%: \ about $10^{{14}}$", SMELL),
            (r"a small change in one estimated number moves the answer by twenty orders of magnitude", BAD),
            (r"the experiments are sound; \ the trillion is not established: \ the Ledger says contested", PRIOR),
        ], 4.8, 25, 0.32).move_to([4.4, -0.2, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ \texttt{hearing.bushdid\_estimate}, \ one natural way to count; \ not the paper's exact formula")
        with self.voiceover(
            "You can see the fragility with a little combinatorics. <bookmark mark='a'/> Take mixtures of thirty "
            "odorants from a hundred and twenty-eight. Suppose two mixtures can be told apart whenever they share less "
            "than some fraction of their components. Then count how many mixtures you could pick, each with its own "
            "private neighbourhood of mixtures too similar to tell from it. <bookmark mark='b'/> If the threshold is "
            "forty percent, the count is about sixty. At sixty percent, about two million. At eighty percent, about a "
            "hundred trillion. <bookmark mark='c'/> A modest change in one estimated quantity moves the answer by twenty "
            "orders of magnitude. This isn't the paper's exact formula, but it shows the problem the reanalyses "
            "describe. <bookmark mark='d'/> The experiments themselves are not in doubt. The trillion is: nobody knows "
            "how many smells people can tell apart, and the Ledger records the claim as contested."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(c), Create(tri), FadeIn(trl), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
