from __future__ import annotations

import numpy as np

from videos.music.music42.common import *  # noqa: F403


class Chains(SoundScene):
    def construct(self):
        chapter(self, 8, r"Chains, \ grammars and evolution", r"Can a program learn a style from examples?")
        self.markov()
        self.quiz()
        self.copying()
        self.grammars()
        self.evolve()
        self.hear_evolved()

    # ------------------------------------------------------------------
    def markov(self):
        d = load("chains")
        items = [
            (rf"read the series' corpus of {d['tunes']} major-key folk and public-domain tunes \ (Part 14)", WHITE),
            (r"order 1: \ count which note follows each note; \ order 4: \ which note follows each run of four", WHITE),
            (r"generate: \ start from a tune's opening, \ then draw each next note from the counts for the last few", WHITE),
            (rf"order 1 has {d['orders']['1']['contexts']} contexts to remember; \ order 4 has {d['orders']['4']['contexts']}", TUNE),
            (r"Hiller and Isaacson's fourth experiment, \ and Brooks, \ Hopkins, \ Neumann and Wright's hymn tunes \ (1957)", GREY_A),
        ]
        rows_scene(self, r"Markov chains learn from examples", items,
                   "A Markov chain learns a style from examples. <bookmark mark='b'/> Read the series' corpus of "
                   f"{say(d['tunes'])} major-key folk and public-domain tunes, from Part 14. <bookmark mark='c'/> A chain of order "
                   "one counts which note follows each note; a chain of order four, which note follows each run of four. "
                   "<bookmark mark='d'/> To generate, start from a tune's opening and draw each next note from the counts for the "
                   f"last few. <bookmark mark='e'/> Order one has {say(d['orders']['1']['contexts'])} contexts to remember; order "
                   f"four has {say(d['orders']['4']['contexts'])}. <bookmark mark='f'/> This was Hiller and Isaacson's fourth "
                   "experiment, and in the same year Brooks, Hopkins, Neumann and Wright trained chains on hymn tunes.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("chains")
        c = clip("chains.two")
        card = listen_card(r"Two melodies walked from Markov chains trained on the same tunes. \ "
                           r"One remembers only the last note, \ the other the last four. \ Which remembers four?", width=10.4)
        with self.voiceover(
            "A question for your ears. Two melodies walked from Markov chains trained on the same tunes. One chain "
            "remembers only the last note; the other remembers the last four. Which one remembers four?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        rolls = VGroup()
        for k in ("first", "second"):
            notes = d["orders"][str(d["order_of"][k])]["notes"]
            mel = [[72 + x, float(i), 1.0] for i, x in enumerate(notes)]
            r = scored(mel, None, width=5.6, height=1.6, lo=62, hi=90, bars=6, beats=4.0)
            rolls.add(VGroup(r, label(k, font_size=22, color=GREY_A)).arrange(DOWN, buff=0.3))
        rolls.arrange(RIGHT, buff=0.8).move_to(UP * 0.4)
        self.play(FadeOut(card), FadeIn(rolls))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"two chains", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for i, k in enumerate(("first", "second")):
                notes = d["orders"][str(d["order_of"][k])]["notes"]
                flash(snd, rolls[i][0].roll.notes, [st[k] + j * 0.32 for j in range(len(notes))], hot=WHITE, base=TUNE)
        ans = VGroup(label(r"first: \ order 1, \ plausible note to note, \ aimless over a phrase", font_size=20, color=GREY_A),
                     label(r"second: \ order 4, \ phrases that sound like real tunes, \ because they are", font_size=20, color=TUNE)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The second. The first chain makes each step plausible but wanders, with no sense of a phrase. The second "
            "sounds like real tunes over longer stretches, and the next chart shows why: because, in places, it is real tunes."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def copying(self):
        d = load("chains")
        o1, o4 = d["orders"]["1"], d["orders"]["4"]
        rows_ = text_rows([
            (r"corpus overlap descriptor: \ the longest run of consecutive notes found verbatim in one corpus tune", WHITE),
            (rf"order 1: \ {o1['mean_copy']:.1f} notes on average over 40 walks \ (this one: \ {o1['copy']['run']}, \ from `{o1['copy']['tune']}')", WHITE),
            (rf"order 4: \ {o4['mean_copy']:.1f} notes on average \ (this one: \ {o4['copy']['run']}, \ from `{o4['copy']['tune']}')", EAR),
            (r"higher-order walks here have longer corpus matches; \\ this is not a universal law or a plagiarism verdict", TUNE),
            (r"the same trade-off haunts today's generative models \ (Parts 65 and 66)", GREY_A),
        ])
        head = label(r"how much does a chain copy?", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            f"Measure the copying: the longest run of consecutive notes that appears, verbatim, in one of the corpus tunes. <bookmark mark='a'/> For order one, about {say(o1['mean_copy'])} notes on average over forty walks; short runs like these are just scales and repeated notes. <bookmark mark='b'/> For order four, about {say(o4['mean_copy'])}: whole phrases lifted from real tunes. <bookmark mark='c'/> In these walks, the higher-order chain produces longer exact corpus matches; this is not a theorem for every corpus or sampling method. This example trades local predictability against longer corpus matches; matching a passage is not by itself a legal or ethical finding of plagiarism. <bookmark mark='d'/> The same trade-off haunts today's generative models, in Parts 65 and 66."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("abcd", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def grammars(self):
        items = [
            (r"a grammar rewrites symbols into strings: \ phrase \ $\to$ \ antecedent consequent, \ chord \ $\to$ \ dominant tonic", WHITE),
            (r"Part 22 grew melodies from skeletons and parsed harmony with a probabilistic grammar", WHITE),
            (r"grammars capture nesting that chains miss: \ a phrase inside a period inside a section", WHITE),
            (r"Steedman \ (1984) \ wrote a grammar for the twelve-bar blues \ (Part 38)", TUNE),
            (r"grammars generate; \ something still has to choose", GREY_A),
        ]
        rows_scene(self, r"grammars", items,
                   "Chains see only the last few notes. Grammars see structure. <bookmark mark='b'/> A grammar rewrites symbols "
                   "into strings: a phrase into an antecedent and a consequent, a chord into a dominant and a tonic. "
                   "<bookmark mark='c'/> Part 22 grew melodies from skeletons that way and parsed harmony with a probabilistic "
                   "grammar. <bookmark mark='d'/> Grammars capture the nesting that chains miss: a phrase inside a period inside "
                   "a section. <bookmark mark='e'/> Mark Steedman wrote one for the twelve-bar blues in 1984. "
                   "<bookmark mark='f'/> But a grammar only generates; something still has to choose.", marks="cdef")

    # ------------------------------------------------------------------
    def evolve(self):
        d = load("evolve")
        b, m = d["best_curve"], d["mean_curve"]
        x0, y0, W, H = -5.8, -1.8, 5.8, 3.4
        def pts(v):
            return [[x0 + W * i / (len(v) - 1), y0 + H * y, 0] for i, y in enumerate(v)]
        ax = VGroup(Line([x0, y0, 0], [x0 + W, y0, 0], color=GREY_B), Line([x0, y0, 0], [x0, y0 + H, 0], color=GREY_B))
        lb = VMobject(color=TUNE, stroke_width=4).set_points_as_corners(pts(b))
        lm = VMobject(color=BLUE, stroke_width=3).set_points_as_corners(pts(m))
        labs = VGroup(label(r"generation", font_size=16, color=GREY_A).move_to([x0 + W / 2, y0 - 0.35, 0]),
                      label(r"0", font_size=14, color=GREY_A).move_to([x0, y0 - 0.25, 0]), label(rf"{len(b) - 1}", font_size=14, color=GREY_A).move_to([x0 + W, y0 - 0.25, 0]),
                      label(r"1", font_size=14, color=GREY_A).move_to([x0 - 0.25, y0 + H, 0]), label(r"0", font_size=14, color=GREY_A).move_to([x0 - 0.25, y0, 0]),
                      label(r"best", font_size=16, color=TUNE).next_to(pts(b)[-1], UP, buff=0.12),
                      label(r"average", font_size=16, color=BLUE).next_to(pts(m)[-1], DOWN, buff=0.12))
        side = VGroup(label(r"a population of 40 plans for eight bars", font_size=19, color=WHITE),
                      label(r"fitness: \ the critics' score, \ 0 if a hard critic refuses", font_size=19, color=WHITE),
                      label(r"children take bars from two parents; \ now and then a bar is redrawn", font_size=19, color=WHITE),
                      label(rf"after {len(b) - 1} generations: \ best {b[-1]:.2f}, \ from {b[0]:.2f}", font_size=19, color=TUNE)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 4.1 + UP * 0.2)
        side.scale_to_fit_width(min(side.width, 5.0)).move_to(RIGHT * 4.1 + UP * 0.2)
        head = label(r"evolution: \ the critics as a fitness", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Evolution is another way to search. <bookmark mark='a'/> Keep a population of forty plans for eight bars. Score "
            "each with chapter nine's critics, zero if a hard critic refuses it. <bookmark mark='b'/> Breed the fitter: "
            "children take bars from two parents, and now and then a bar is redrawn at random. <bookmark mark='c'/> The "
            f"best fitness climbs from {say(b[0], 2)} to {say(b[-1], 2)} in {say(len(b) - 1)} generations, and the "
            "average follows it up. Genetic algorithms have composed jazz solos, in Al Biles's GenJam of 1994, among much else."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(labs[:5]), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(Create(lb), Create(lm), FadeIn(labs[5:]), FadeIn(side[3]), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear_evolved(self):
        d = load("evolve")
        s = load("search")
        c = clip("evolve.best")
        g = scored(d["melody"], s["chords"], width=11.0, height=2.0, lo=57, hi=81).move_to(UP * 0.4)
        head = label(rf"the fittest after {len(d['best_curve']) - 1} generations \ (fitness {d['fitness']:.2f})", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"the same motive, \ chords and critics as chapter 9's searcher", font_size=19, color=GREY_A).to_edge(DOWN, buff=1.0)
        with self.voiceover("Here is the fittest melody after the last generation."):
            self.play(FadeIn(head), FadeIn(g), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"evolved", detail=r"Part 7's piano, \ a plucked bass", corner=DL, tag_corner=DR)
            flash(snd, g.roll.notes, [n[1] * 0.42 for n in d["melody"]], hot=WHITE, base=TUNE)
        self.wait(0.3)
        self.clear_scene()
