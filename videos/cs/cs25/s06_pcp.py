from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs25.common import (fit_right, BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


def domino(top, bot, w=None, color=DATA, font=22):
    """One domino: the top string over the bottom one, in a rounded box."""
    w = w or max(0.62, 0.2 + 0.21 * max(len(top), len(bot)))
    box_ = RoundedRectangle(width=w, height=1.0, corner_radius=0.08, stroke_color=color, stroke_width=2.2,
                            fill_color=BG, fill_opacity=1.0)
    rule = Line(box_.get_left() + RIGHT * 0.06, box_.get_right() + LEFT * 0.06, stroke_width=1.0, color=GREY_B)
    t = mono(top or " ", font, WHITE).move_to(box_.get_center() + UP * 0.25)
    b = mono(bot or " ", font, WHITE).move_to(box_.get_center() + DOWN * 0.25)
    return VGroup(box_, rule, t, b)


class Pcp(VoiceoverScene):
    def construct(self):
        self.card()
        self.game()
        self.histories()
        self.search()
        self.grammars()

    def card(self):
        card = chapter_card(5, r"Post's correspondence problem", r"Can a puzzle with dominoes be undecidable?",
                            lit=(1946,), extra=((1946, r"Post"),), part=PART)
        with self.voiceover("Chapter five. Post's correspondence problem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def game(self):
        p = load("pcp")
        head = label(r"Make the top string equal the bottom string", font_size=32).to_edge(UP, buff=0.35)
        ds = VGroup(*[domino(t, b) for t, b in p["sipser"]]).arrange(RIGHT, buff=0.35).next_to(head, DOWN, buff=0.45)
        names = VGroup(*[mono(str(i + 1), 16, GREY_B).next_to(d, DOWN, buff=0.08) for i, d in enumerate(ds)])
        rule = label('use a NONEMPTY sequence; any order; repetitions allowed', font_size=21,
                     color=GREY_A).next_to(names, DOWN, buff=0.2)
        seq = p["sipser_match"]
        row = VGroup(*[domino(*p["sipser"][i], color=HEAD) for i in seq]).arrange(RIGHT, buff=0.06)
        row.next_to(rule, DOWN, buff=0.5)
        top = "".join(p["sipser"][i][0] for i in seq)
        bot = "".join(p["sipser"][i][1] for i in seq)
        res = VGroup(mono(f"top:    {top}", 22, YES), mono(f"bottom: {bot}", 22, YES)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).next_to(row, DOWN, buff=0.35)
        notes = VGroup(
            label(r"\textbf{PCP}: \ given a finite set of dominoes, \ is there a match?", font_size=22, color=WHITE),
            label('Post (1946): no total general decider; individual no-match instances can have proofs', font_size=22, color=NO),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Post's correspondence problem uses a NONEMPTY sequence of dominoes. <bookmark mark='a'/> Each has a top and bottom string; repetitions are allowed. <bookmark mark='b'/> For these four, the sequence two, one, three, two, four is a match. <bookmark mark='c'/> Concatenating each row gives the same string. <bookmark mark='d'/> The general question asks whether any nonempty match exists. <bookmark mark='e'/> Post proved it undecidable. Matches are finite certificates. Some no-match instances also have finite proofs, including exhausted finite residual graphs. What fails is a total general decider; the full no-match set is not recognizable."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.2) for d in ds], lag_ratio=0.15), FadeIn(names),
                      FadeIn(rule))
            vo.wait_until("b")
            self.play(LaggedStart(*[TransformFromCopy(ds[i], row[k]) for k, i in enumerate(seq)], lag_ratio=0.3),
                      run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(res))
            vo.wait_until("d")
            self.play(FadeIn(notes[0]))
            vo.wait_until("e")
            self.play(FadeIn(notes[1]))
        self.wait(0.3)
        self.clear_scene()

    def histories(self):
        p = load("pcp")
        head = label(r"Dominoes that run a Turing machine", font_size=32).to_edge(UP, buff=0.3)
        tm = VGroup(
            label(r"the machine: \ in state $q$ reading 1, \ write 1, \ move right, \ go to $p$", font_size=19,
                  color=GREY_A),
            label(r"in $p$ reading 0, \ write 0, \ move right, \ \textbf{accept} \ ($a$)", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(head, DOWN, buff=0.25).to_edge(LEFT, buff=0.6)
        kinds = [(r"start", [0], HEAD), (r"steps", [1, 2], CTRL), (r"copy", [7, 8, 10, 11], DATA),
                 (r"clean-up", [12, 14], LAM), (r"finish", [18], YES)]
        groups = VGroup()
        for name, idx, col in kinds:
            g = VGroup(*[domino(*p["tm_dominoes"][i], color=col, font=18) for i in idx]).arrange(RIGHT, buff=0.08)
            groups.add(VGroup(g, label(name, font_size=17, color=col).next_to(g, DOWN, buff=0.08)))
        groups.arrange(RIGHT, buff=0.35).next_to(tm, DOWN, buff=0.3).set_x(0)
        if groups.width > 13.2:
            groups.width = 13.2
        top = p["tm_top"]
        rows = VGroup(mono(r"top:    " + top, 20, WHITE), mono(r"bottom: " + top, 20, WHITE)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).next_to(groups, DOWN, buff=0.4)
        hist = mono(p["history"], 22, HEAD).next_to(rows, DOWN, buff=0.25)
        hl = label(r"$\uparrow$ \ the accepting computation history: \ one configuration between each pair of "
                   r"\#", font_size=19, color=HEAD).next_to(hist, DOWN, buff=0.1)
        notes = VGroup(
            label(rf"the search finds the {len(p['tm_match'])}-domino match in {p['tm_nodes']} steps; \ "
                  r"the bottom always runs one configuration ahead", font_size=20, color=WHITE),
            label('forced-first MPCP encodes acceptance; a separate reduction yields ordinary PCP',
                  font_size=21, color=NO),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Computation histories explain the reduction. <bookmark mark='a'/> Our example moves right twice and accepts input one zero. The didactic tape model rejects a left move off its first cell; it never clamps the head. <bookmark mark='b'/> Start, transition, copying, cleanup and closing dominoes encode successive configurations. The start domino is REQUIRED first: this is modified PCP. <bookmark mark='c'/> The bottom row leads the top by one configuration, until accepting cleanup lets the rows close. <bookmark mark='d'/> We check the full concatenated top and bottom for equality, and retain the complete accepting trace. <bookmark mark='e'/> The standard construction reduces acceptance to modified PCP. A separate transformation converts modified PCP to ordinary PCP. The displayed witness illustrates the construction under its stated alphabet and boundary conventions."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tm))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.15) for g in groups], lag_ratio=0.35), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(rows))
            vo.wait_until("d")
            self.play(FadeIn(notes[0]), FadeIn(hist), FadeIn(hl))
            vo.wait_until("e")
            self.play(FadeIn(notes[1]))
        self.wait(0.3)
        self.clear_scene()

    def search(self):
        p = load("pcp")
        head = label(r"How long can the shortest match be?", font_size=32).to_edge(UP, buff=0.35)
        hist = p["len_hist"]
        ks = sorted(int(k) for k in hist)
        rows = [[str(k), words(hist[str(k)])] for k in ks]
        tab = grid_table([r"shortest match", r"instances"], rows, widths=[2.6, 2.0], row_h=0.3, font_size=19,
                         mono_cols=(), colors=[[WHITE, DATA]] * len(rows))
        tab.next_to(head, DOWN, buff=0.35).to_edge(LEFT, buff=0.8)
        tl = label(rf"{words(p['tried'])} random 3-domino sets \ (strings of 1--3 bits): \ {words(p['solved'])} "
                   r"solved", font_size=19, color=GREY_A).next_to(tab, DOWN, buff=0.15).align_to(tab, LEFT)
        hard = p["hard"][0]
        ds = VGroup(*[domino(t, b, color=HEAD, font=20) for t, b in hard["dominoes"]]).arrange(RIGHT, buff=0.25)
        dl = label(rf"the hardest we drew: \ shortest match \ {hard['len']} dominoes", font_size=20, color=HEAD)
        g1 = VGroup(ds, dl).arrange(DOWN, buff=0.15)
        four = [("1000", "0"), ("01", "0"), ("1", "101"), ("00", "001")]
        ds4 = VGroup(*[domino(t, b, color=NO, font=20) for t, b in four]).arrange(RIGHT, buff=0.2)
        dl4 = label(r"four dominoes: \ the shortest match uses \textbf{206} \ (checked by our search)", font_size=20,
                    color=NO)
        g2 = VGroup(ds4, dl4).arrange(DOWN, buff=0.15)
        VGroup(g1, g2).arrange(DOWN, buff=0.5).next_to(tab, RIGHT, buff=0.9).align_to(tab, UP)
        notes = VGroup(
            label(r"2 dominoes: \ decidable \ (Ehrenfeucht, \ Karhum\"aki, \ Rozenberg, \ 1982); \ 5 or more: \ "
                  r"undecidable \ (Neary, \ 2015)", font_size=21, color=WHITE),
            label(r"3 and 4: \ open", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Our search uses fixed budgets and retains every sampled instance. <bookmark mark='a'/> We draw twenty thousand three-domino sets with one-to-three-bit words. Every result says matched, exhausted, depth limit or node limit; an unfinished search is not a no-match proof. <bookmark mark='b'/> The longest shortest match among the solved sample instances has fifteen dominoes. <bookmark mark='c'/> The displayed four-domino instance really has shortest match length two hundred and six. We execute the search, check the full strings and retain a residual-graph distance certificate excluding shorter matches. No computable shortest-match bound exists for UNRESTRICTED PCP. This does not settle the fixed four-domino case. <bookmark mark='d'/> Two dominoes are decidable. Neary's published 2015 theorem proves undecidability for five. <bookmark mark='e'/> That published theorem leaves three and four open; its five-pair result supersedes a conflicting earlier preprint."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.1), FadeIn(tl))
            vo.wait_until("b")
            self.play(FadeIn(g1))
            vo.wait_until("c")
            self.play(FadeIn(g2))
            vo.wait_until("d")
            self.play(FadeIn(notes[0]))
            vo.wait_until("e")
            self.play(FadeIn(notes[1]))
        self.wait(0.3)
        self.clear_scene()

    def grammars(self):
        head = label(r"Ambiguity is undecidable \ (the promise from Part 12)", font_size=32).to_edge(UP, buff=0.35)
        g = VGroup(
            MathTex(r"S \to T \mid B", font_size=34, color=WHITE),
            MathTex(r"T \to t_i\, T\, i \;\mid\; t_i\, i", font_size=34, color=DATA),
            MathTex(r"B \to b_i\, B\, i \;\mid\; b_i\, i", font_size=34, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=1.0)
        gl = label('one rule pair per domino; index markers use a DISJOINT terminal alphabet', font_size=19,
                   color=GREY_A).next_to(g, DOWN, buff=0.2).align_to(g, LEFT)
        ex = VGroup(
            mono("T => t2 t1 t3 ... 3 1 2", 20, DATA),
            mono("B => b2 b1 b3 ... 3 1 2", 20, HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(g, RIGHT, buff=1.0)
        notes = VGroup(
            label(r"$T$ derives the tops of a sequence followed by the sequence reversed; \ $B$ does the same with "
                  r"bottoms", font_size=21, color=WHITE),
            label(r"each half alone is unambiguous: \ the markers spell out which dominoes were used", font_size=21,
                  color=GREY_A),
            label(r"a string with two trees \ (one via $T$, \ one via $B$) \ $=$ a sequence whose tops equal its "
                  r"bottoms", font_size=21, color=YES),
            label(r"grammar ambiguous $\iff$ the dominoes have a match: \ undecidable \ (Cantor; \ Floyd; \ Chomsky "
                  r"and Sch\"utzenberger, \ 1962--63)", font_size=21, color=NO),
            label('nonempty CFG intersection follows here; CFG universality needs a different reduction', font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.22).next_to(gl, DOWN, buff=0.4).set_x(0)
        with self.voiceover(
            "Here is the promised ambiguity reduction. <bookmark mark='a'/> For each domino, the T rules generate its top string, and the B rules its bottom, followed by distinct index markers in reverse sequence order. Markers use a disjoint terminal alphabet. <bookmark mark='b'/> Each half is unambiguous because the markers determine every rule choice. <bookmark mark='c'/> A string has parses through both halves precisely when the same nonempty index sequence makes equal top and bottom strings. <bookmark mark='d'/> Thus grammar ambiguity, and nonempty intersection of two context-free languages, are undecidable. <bookmark mark='e'/> Context-free grammar universality is also undecidable, but needs another reduction; this construction alone does not prove it. Parser conflicts concern particular parsing methods and are not a general ambiguity decider."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(gl))
            vo.wait_until("a")
            self.play(FadeIn(ex), FadeIn(notes[0]))
            for mk, n_ in zip("bcde", notes[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()
