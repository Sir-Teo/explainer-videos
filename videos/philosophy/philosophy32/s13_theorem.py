from __future__ import annotations

from videos.philosophy.philosophy32.common import *  # noqa: F403


class Theorem(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"The free will theorem", r"If we are free, \ must electrons be too?", lit=(2006,),
                            part=PART)
        with self.voiceover("Chapter twelve. The free will theorem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.axioms()
        self.fixed()
        self.reading()

    def axioms(self):
        hc = history_card(2006, r"John Conway and Simon Kochen", r"`The Free Will Theorem'", width=6.2,
                          color=HIST).to_corner(UL, buff=0.3)
        rows = [(r"SPIN", r"squared spin components of a spin-1 particle along three orthogonal axes are 1, \ 0, \ 1 "
                          r"in some order \ (Kochen--Specker, \ Part 26)", LAW),
                (r"TWIN", r"two entangled particles, \ measured along the same axis, \ give the same answer", LAW),
                (r"MIN", r"two distant experimenters choose their axes independently: \ relativity forbids one "
                         r"choice influencing the other", WILL),
                (r"the theorem", r"if the experimenters' choices are not functions of the past, \ neither are the "
                                 r"particles' responses", GOAL)]
        g = rows_table(rows, top=1.4, gap=0.5)
        with self.voiceover(
            "Physics entered the debate in 2006, with a theorem by John Conway and Simon Kochen. "
            "<bookmark mark='a'/>Its first axiom, SPIN, is a prediction of quantum mechanics: measure the squared "
            "spin of a spin-one particle along three perpendicular axes, and you get one, zero and one in some "
            "order, the structure behind the Kochen–Specker theorem of Part 26. <bookmark mark='b'/>TWIN: two "
            "entangled particles measured along the same axis give the same answer. <bookmark mark='c'/>MIN: two "
            "experimenters far apart choose their axes independently; relativity forbids one choice from "
            "influencing the other. <bookmark mark='d'/>From these, they proved that if the experimenters' choices "
            "are not functions of the past, then neither are the particles' responses. As they put it, if "
            "experimenters have even a modicum of free will, elementary particles have their own share of it."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def fixed(self):
        d = load("chsh")
        head = label(r"Answers fixed in advance, \ checked", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["strategies"] == 16 and d["values"] == [-2, 2] and d["tsirelson"] == 2.8284
        f = MathTex(r"S \;=\; E(0,0) + E(0,1) + E(1,0) - E(1,1)", font_size=34, color=FUNC).move_to([0, 2.1, 0])
        ax = NumberLine(x_range=[-3, 3, 1], length=10.0, include_numbers=True, font_size=22,
                        color=GREY_B).move_to([0, 0.2, 0])
        band = Rectangle(width=ax.unit_size * 4, height=0.5, fill_color=LAW, fill_opacity=0.25,
                         stroke_width=0).move_to(ax.n2p(0))
        dots = VGroup(*[Dot(ax.n2p(v), radius=0.12, color=LAW) for v in d["values"]])
        q = VGroup(Triangle(color=CHANCE, fill_opacity=1).scale(0.15).rotate(PI).next_to(ax.n2p(d["tsirelson"]), UP,
                                                                                          buff=0.05),
                   label(r"quantum: \ $2\sqrt{2} \approx 2.83$", font_size=19, color=CHANCE).next_to(
                       ax.n2p(d["tsirelson"]), UP, buff=0.4))
        bl = label(r"all 16 local strategies: \ $S = \pm 2$; \ their mixtures stay inside", font_size=19,
                   color=LAW).next_to(ax, DOWN, buff=0.5)
        foot = label(r"answers fixed in advance, \ plus independent settings, \ cannot reach what experiments see",
                     font_size=20, color=GOAL).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The theorem rests on the same logic as Bell's, which the Reasoner can check in a few lines. "
            "<bookmark mark='a'/>Two particles each answer one of two questions, chosen independently, with plus or "
            "minus one. Combine the correlations into this sum, S. <bookmark mark='b'/>If each particle's answers "
            "were fixed in advance, there are sixteen ways to fix them, and every one gives S equal to plus or minus "
            "two; any mixture of them stays in between. <bookmark mark='c'/>Quantum mechanics predicts, and "
            "experiments find, about two point eight three. <bookmark mark='d'/>So answers fixed in advance, with "
            "independent settings, cannot reproduce what is observed, and Conway and Kochen's theorem sharpens the "
            "same conclusion."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(band), LaggedStart(*[GrowFromCenter(x) for x in dots]), FadeIn(bl))
            vo.wait_until("c")
            self.play(FadeIn(q))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def reading(self):
        head = label(r"What it shows, \ and what it does not", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"it shows", r"no local deterministic theory can fix the outcomes in advance, \ given independent "
                              r"settings: \ a cousin of Bell's theorem \ (Part 26)", OK),
                (r"free, \ here", r"means only: \ not a function of the past light cone", GREY_A),
                (r"it does not show", r"that we are free in any sense the consequence argument is about", BAD),
                (r"superdeterminism", r"denies MIN: \ the choices and outcomes share a common cause; \ few accept "
                                      r"it", CHANCE),
                (r"the lesson", r"indeterminism is cheap; \ the question is whether any of it is up to us", GOAL)]
        g = rows_table(rows, top=1.6, gap=0.45)
        with self.voiceover(
            "The theorem is real mathematics, and easy to oversell. <bookmark mark='a'/>What it shows is that no "
            "local deterministic theory can fix the outcomes in advance, if the settings are chosen independently: "
            "it is a cousin of Bell's theorem from Part 26. <bookmark mark='b'/>Free, in the theorem, means only "
            "not a function of what lies in the past light cone. <bookmark mark='c'/>It does not show that we are "
            "free in the sense the consequence argument is about, or that a particle's indeterminism is a choice. "
            "<bookmark mark='d'/>It can be escaped by superdeterminism, which denies the independence of the "
            "settings, at a cost to the whole of experimental science that few accept. <bookmark mark='e'/>The "
            "lesson for free will is the one from chapter one: indeterminism is cheap. The question is whether any "
            "of it is up to us."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
