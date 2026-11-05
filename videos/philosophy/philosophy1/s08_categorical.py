from __future__ import annotations

import numpy as np

from videos.philosophy.philosophy1.common import *  # noqa: F403

FORMS = [("A", r"All $S$ are $P$", r"universal affirmative"), ("E", r"No $S$ are $P$", r"universal negative"),
         ("I", r"Some $S$ are $P$", r"particular affirmative"), ("O", r"Some $S$ are not $P$", r"particular negative")]


def venn2(kind, r=0.62, center=ORIGIN):
    a = Circle(radius=r, stroke_color=S_C, stroke_width=2.5).move_to(np.asarray(center) + LEFT * r * 0.55)
    b = Circle(radius=r, stroke_color=P_C, stroke_width=2.5).move_to(np.asarray(center) + RIGHT * r * 0.55)
    g = VGroup()
    if kind == "A":
        g.add(Difference(a, b, stroke_width=0, fill_color=GREY_D, fill_opacity=0.9))
    elif kind == "E":
        g.add(Intersection(a, b, stroke_width=0, fill_color=GREY_D, fill_opacity=0.9))
    elif kind == "I":
        g.add(Cross(scale_factor=0.09, stroke_color=GOAL, stroke_width=4).move_to(np.asarray(center)))
    else:
        g.add(Cross(scale_factor=0.09, stroke_color=GOAL, stroke_width=4).move_to(a.get_center() + LEFT * r * 0.35))
    g.add(a, b)
    return g


class Categorical(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"Aristotle: all, no, some", r"What did the first formal logic look like?",
                            lit=(-350,), part=PART)
        with self.voiceover("Chapter seven. Aristotle: all, no, some."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.letters()
        self.forms()
        self.square_()
        self.conversion()

    def letters(self):
        hc = history_card(r"c.\ 350 BCE", r"Aristotle", r"\textit{Prior Analytics}: the first formal logic",
                          width=5.2, color=HIST).to_corner(UL, buff=0.4)
        q = quote_card(r"A deduction is a discourse in which, certain things being stated, something other than what "
                       r"is stated follows of necessity from their being so.", r"Aristotle, \textit{Prior Analytics} "
                       r"I.2, 24b18", r"trans.\ Jenkinson", width=10.0, font_size=28).move_to([0, 0.0, 0])
        var = label(r"the great invention: \ letters for terms, \ so a form can be stated once, for all subjects",
                    font_size=26, color=GOAL).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Aristotle, a student of Plato's Academy, wrote the first systematic logic: the Prior Analytics, around "
            "350 before our era. <bookmark mark='a'/>Its definition of deduction still holds: a discourse in which, "
            "certain things being stated, something other than what is stated follows of necessity from their being "
            "so. <bookmark mark='b'/>And it contains a quiet revolution. Aristotle uses letters for terms, A, B, C, "
            "so that a form of argument can be stated once and for all, whatever it is about. Variables were born in "
            "logic before they were born in algebra."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(var))
        self.clear_scene()

    def forms(self):
        cards = VGroup()
        for k, txt, nm in FORMS:
            v = venn2(k)
            t = VGroup(MathTex(k, font_size=44, color=GOAL), label(txt, font_size=28), label(nm, font_size=20,
                                                                                            color=GREY_A))
            t.arrange(DOWN, buff=0.12)
            cards.add(VGroup(t, v).arrange(DOWN, buff=0.35))
        cards.arrange(RIGHT, buff=0.7).move_to([0, -0.1, 0])
        leg = label(r"grey: \ empty region \qquad $\times$: \ inhabited region", font_size=24, color=GREY_A)
        leg.to_edge(DOWN, buff=0.45)
        names = label(r"A and I from \textit{AffIrmo}; \ E and O from \textit{nEgO} (medieval mnemonics)",
                      font_size=22, color=GREY_B).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Aristotle's logic is built from four kinds of sentence, each joining a subject term to a predicate "
            "term. <bookmark mark='a'/>All S are P. No S are P. Some S are P. Some S are not P. <bookmark mark='b'/>"
            "Medieval logicians named them A, E, I and O, from the Latin affirmo, I affirm, and nego, I deny. "
            "<bookmark mark='c'/>Draw S and P as circles. 'All S are P' says the part of S outside P is empty: grey "
            "it out. 'No S are P' empties the overlap. 'Some S are P' puts a mark in the overlap: something is there. "
            "'Some S are not P' puts a mark in S outside P. This picture, from John Venn in 1880, will let us check "
            "Aristotle's logic by machine."
        ) as vo:
            self.play(FadeIn(cards[0][0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c[0], shift=UP * 0.2) for c in cards[1:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(names))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c[1]) for c in cards], lag_ratio=0.4), FadeIn(leg), run_time=3)
        self.clear_scene()

    def square_(self):
        pos = {"A": [-3.0, 1.8, 0], "E": [3.0, 1.8, 0], "I": [-3.0, -1.8, 0], "O": [3.0, -1.8, 0]}
        nodes = {k: VGroup(MathTex(k, font_size=48, color=GOAL), label(t, font_size=22)).arrange(DOWN, buff=0.1)
                 .move_to(pos[k]) for k, t, _ in FORMS}
        rel = [("A", "E", r"contraries: not both true", P.AGENT), ("I", "O", r"subcontraries: not both false", P.TRUE),
               ("A", "O", r"contradictories", BAD), ("E", "I", r"contradictories", BAD),
               ("A", "I", r"subalternation: A implies I", P.CLAIM), ("E", "O", r"subalternation: E implies O", P.CLAIM)]
        lines, labs = VGroup(), VGroup()
        for a, b, t, c in rel:
            ln = Line(nodes[a].get_center(), nodes[b].get_center(), buff=0.75, color=c, stroke_width=3)
            lines.add(ln)
            lab = label(t, font_size=20, color=c)
            if a in "AE" and b in "AE":
                lab.next_to(ln, UP, buff=0.1)
            elif a in "IO" and b in "IO":
                lab.next_to(ln, DOWN, buff=0.1)
            elif (a, b) in (("A", "I"), ("E", "O")):
                lab.rotate(PI / 2).next_to(ln, LEFT if a == "A" else RIGHT, buff=0.1)
            else:
                lab.move_to(ln.get_center() + UP * 0.3)
                if a == "E":
                    lab.set_opacity(0)
            labs.add(lab)
        warn = label(r"subalternation needs $S$ to be inhabited: \ Chapter 9", font_size=24, color=BAD)
        warn.to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "The four forms sit at the corners of the square of opposition. <bookmark mark='a'/>A and O contradict "
            "each other, as do E and I: exactly one of each pair is true. <bookmark mark='b'/>A and E are contraries: "
            "they can both be false, but not both true. I and O are subcontraries: both can be true, not both false. "
            "<bookmark mark='c'/>And down each side, subalternation: all S are P implies some S are P. "
            "<bookmark mark='d'/>That last step looks harmless. It is the one the unicorns will break."
        ) as vo:
            self.play(*[FadeIn(n) for n in nodes.values()])
            vo.wait_until("a")
            self.play(Create(lines[2]), Create(lines[3]), FadeIn(labs[2]), FadeIn(labs[3]))
            vo.wait_until("b")
            self.play(Create(lines[0]), Create(lines[1]), FadeIn(labs[0]), FadeIn(labs[1]))
            vo.wait_until("c")
            self.play(Create(lines[4]), Create(lines[5]), FadeIn(labs[4]), FadeIn(labs[5]))
            vo.wait_until("d")
            self.play(FadeIn(warn), Indicate(lines[4], color=BAD), Indicate(lines[5], color=BAD))
        self.clear_scene()

    def conversion(self):
        d = load("conversion")
        conv = {(o["kind"], o["import"]): o["converts"] for o in d["simple"]}
        head = label(r"conversion: \ swap subject and predicate", font_size=32, color=GOAL).to_edge(UP, buff=0.4)
        rows = VGroup()
        words = {"A": (r"All $S$ are $P$", r"All $P$ are $S$"), "E": (r"No $S$ are $P$", r"No $P$ are $S$"),
                 "I": (r"Some $S$ are $P$", r"Some $P$ are $S$"), "O": (r"Some $S$ are not $P$", r"Some $P$ are not $S$")}
        for k in "AEIO":
            ok = conv[(k, False)]
            rows.add(VGroup(MathTex(k, font_size=36, color=GOAL), label(words[k][0], font_size=28),
                            MathTex(r"\Rightarrow", font_size=32, color=GREY_C), label(words[k][1], font_size=28),
                            MathTex(r"\checkmark" if ok else r"\times", font_size=36, color=OK if ok else BAD)).arrange(
                RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 0.3, 0])
        ce = label(r"all dogs are animals; \ not all animals are dogs", font_size=24, color=BAD).next_to(rows[0], RIGHT,
                                                                                                 buff=0.4)
        if ce.get_right()[0] > 6.9:
            ce.next_to(rows, DOWN, buff=0.3)
        lim = d["limitation"]
        assert lim["True"] and not lim["False"]
        lm = label(r"by limitation: \ all $S$ are $P$, so some $P$ are $S$ \ --- valid only if $S$ is inhabited",
                   font_size=26, color=P.AGENT).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Aristotle's first theorems are about single sentences. Conversion swaps subject and predicate. Which "
            "sentences survive it? <bookmark mark='a'/>The machine checks every Venn arrangement. 'No S are P' "
            "converts: if no dog is a cat, no cat is a dog. 'Some S are P' converts too. <bookmark mark='b'/>'All S "
            "are P' does not: all dogs are animals, but not all animals are dogs. Nor does 'some S are not P'. "
            "<bookmark mark='c'/>Aristotle allowed one more step, conversion by limitation: from 'all S are P', infer "
            "'some P are S'. The machine accepts it only when S is inhabited: existential import again. These "
            "conversions are the tools Aristotle used to prove the moods, as the next chapter shows."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(rows[3]), FadeIn(ce))
            vo.wait_until("c")
            self.play(FadeIn(lm))
        self.clear_scene()
