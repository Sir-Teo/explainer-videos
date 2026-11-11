from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs24.common import (COST, CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


class TheJob(VoiceoverScene):
    def construct(self):
        self.card()
        self.engineered()
        self.breakdown()
        self.ledger()

    def card(self):
        card = chapter_card(14, r"The Job, \ engineered", r"How fast can the word count go on this machine?",
                            lit=(2017,), extra=((2017, r"Swiss tables"),), part=PART)
        with self.voiceover("Chapter fourteen. The Job, engineered."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def engineered(self):
        d = load("job")
        tb, en = d["textbook"], d["engineered"]
        head = label(r"Part 17's hash table, \ engineered for this machine", font_size=32).to_edge(UP, buff=0.3)
        changes = VGroup(
            label(r"\textbf{1.} \ words found 32 bytes at a time \ (chapter 10's AVX2 scan)", font_size=22, color=DATA),
            label('\\textbf{2.} \\ hash letter blocks; retain exact key equality', font_size=22, color=LAM),
            label(r"\textbf{3.} \ a Swiss-style table: \ 16 control bytes per group, \ one SSE2 compare", font_size=22,
                  color=HEAD),
            label(r"\textbf{4.} \ the first 8 letters, \ the length and the count live \textbf{in the slot}: \ a short "
                  r"word never leaves the table", font_size=22, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(head, DOWN, buff=0.45)
        rows = [[r"Part 17's open addressing", f"{tb['best'] * 1000:.0f} ms", f"{tb['median'] * 1000:.0f} ms",
                 f"{tb['best'] * 1e9 / d['bytes']:.1f}"],
                [r"engineered", f"{en['best'] * 1000:.0f} ms", f"{en['median'] * 1000:.0f} ms",
                 f"{d['ns_per_byte']:.1f}"]]
        tab = grid_table([r"C, \ the 30 novels", r"best of 7", r"median", r"ns per byte"], rows,
                         widths=[4.6, 2.0, 2.0, 2.2], row_h=0.48, font_size=22, mono_cols=(),
                         colors=[[GREY_A] * 4, [YES] * 4])
        tab.next_to(changes, DOWN, buff=0.45).set_x(0)
        notes = VGroup(
            label(rf"{words(d['words'])} words, \ {words(d['distinct'])} distinct; \ both print the same twenty lines, "
                  r"byte for byte, \ as the Python reference", font_size=21, color=WHITE),
            label(rf"{d['speedup']:.1f}$\times$ by best time; \ the engineered runs spread widely \ (chapter 12: "
                  r"this machine is shared)", font_size=21, color=YES),
            label('fixed-capacity corpus experiment; no measured cache-miss floor', font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.2).next_to(tab, DOWN, buff=0.35)
        with self.voiceover(
            'The Job counts the words of the fixed thirty-novel corpus and selects the twenty most common. '
            "<bookmark mark='a'/> The engineered version classifies ASCII bytes with AVX2. <bookmark mark='b'/> "
            "It hashes letter blocks while retaining exact key comparisons. <bookmark mark='c'/> A teaching "
            "Swiss-style table filters sixteen control bytes at once. <bookmark mark='d'/> The first eight "
            'letters, length and count live in the slot; longer words also consult their stored bytes. Its fixed '
            "table, pool and word-length bounds are checked against this corpus. <bookmark mark='e'/> Seven "
            'whole-program runs retain both minimum and median times, exact top-twenty output and every distinct '
            "word count, independently checked against Python. <bookmark mark='f'/> The comparison is empirical "
            'for these two programs on the same host. No hardware counters were collected, so we make no claim '
            'of one cache miss per word or a proven performance floor.'
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", changes):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.4), FadeIn(notes[0]))
            vo.wait_until("f")
            self.play(FadeIn(notes[1]), FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    def breakdown(self):
        head=label('Amdahl model: assumed phase fraction, not a Job profile',font_size=30).to_edge(UP,buff=0.35)
        def bar(y,phase,caption):
            x=-3.8;g=VGroup()
            for value,color in [(70,NO),(phase,DATA)]:
                if value:
                    rect=Rectangle(width=value*0.075,height=0.6,stroke_width=0).set_fill(color,0.8)
                    rect.move_to([x+value*0.075/2,y,0]);g.add(rect);x+=value*0.075
            g.add(label(caption,font_size=19).next_to(g,LEFT,buff=0.2))
            g.add(label(rf"{70+phase:g} units",font_size=18,color=WHITE).move_to([4.7,y,0]))
            return g
        b1=bar(1.4,30,'baseline');b2=bar(0.2,3,'phase10x');b3=bar(-1.0,0,'phase infinite')
        notes=VGroup(*[label(s,font_size=21,color=c) for s,c in [('assume $f=0.30$ of 100 baseline units; phase acceleration $s=10$',DATA),('$T_{new}/T_{old}=(1-f)+f/s=0.73$; speedup $\\approx1.37$',HEAD),('isolated tokenizer times do not identify whole-program phases',YES)]]).arrange(DOWN,buff=0.22).to_edge(DOWN,buff=0.4)
        with self.voiceover("Amdahl's law is a model for a specified phase fraction. <bookmark mark='a'/> In this counterfactual example, suppose thirty percent of a program's baseline time belongs to a phase that can be accelerated. This fraction is an assumption, not a profile of our Job. <bookmark mark='b'/> Making that phase ten times faster gives a total cost of seventy plus three units, or speedup one over zero point seven three. Even an infinitely fast phase leaves seventy units. <bookmark mark='c'/> The isolated tokenizer timings cannot be subtracted from a different complete program to recover its phases. Measure phases in a consistent program and workload before using them for a prediction; evaluate the actual whole-program change separately.") as vo:
            self.play(FadeIn(head),FadeIn(b1))
            vo.wait_until('a');self.play(FadeIn(notes[0]))
            vo.wait_until('b');self.play(FadeIn(b2),FadeIn(notes[1]))
            vo.wait_until('c');self.play(FadeIn(b3),FadeIn(notes[2]))
        self.wait(0.3);self.clear_scene()

    def ledger(self):
        d = load("job")
        led = d["ledger"]
        row = led[-1]
        head = label(r"Ledger row 10", font_size=36).to_edge(UP, buff=0.35)
        tab = ledger_table(led, shown=len(led), highlight=(len(led) - 1,), font_size=20, row_h=0.34,
                           label_width=4.8).scale(0.92).move_to(UP * 1.0)
        notes=VGroup(label('rows1--9: modeled Pebble costs; native row: measured host wall time',font_size=21,color=WHITE),label('model/native ratios are not empirical cross-processor speedups',font_size=21,color=WHITE),label('same-host native comparison: identical corpus, complete checked counts',font_size=21,color=WHITE),label('seven observations per native program; minimum and median retained',font_size=21,color=WHITE)).arrange(DOWN,buff=0.22).to_edge(DOWN,buff=0.4)
        with self.voiceover(
            "The ledger now contains two kinds of quantity. <bookmark mark='a'/> Earlier Pebble rows are modeled "
            'costs under their stated machine and clock assumptions. The native row is measured wall time on the '
            "current host. <bookmark mark='b'/> Their numeric ratio is not an empirical speedup between two "
            'physical processors. Input conventions, implementations and modeled costs must be checked before '
            "making a cross-system claim. <bookmark mark='c'/> We do have a same-host comparison: Part 17's "
            'native C program and the engineered program process the same bytes with identical output and '
            "complete counts. Their seven observations are retained. <bookmark mark='d'/> Keep the modeled "
            'teaching ledger and the measured native experiment visibly distinguished; they answer different '
            'questions about the tower we built.'
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.axis), FadeIn(tab.rows[:-1]))
            self.play(FadeIn(tab.rows[-1]))
            for mk, n_ in zip("abcd", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()
