from __future__ import annotations

import math

from videos.philosophy.philosophy18.common import *  # noqa: F403


class Miracles(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"No miracles", r"Does success show that a theory is true?", lit=(1975, 2004),
                            part=PART)
        with self.voiceover("Chapter seven. No miracles."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.argument()
        self.bayes()
        self.retail()

    def argument(self):
        hc = history_card(1975, r"Hilary Putnam", r"`What is Mathematical Truth?'", width=5.4,
                          color=HIST).to_corner(UL, buff=0.35)
        rows = [
            (r"the datum", r"our best theories predict novel phenomena with astonishing accuracy", THEORY),
            (r"the explanation", r"they are approximately true, \ and their central terms refer", REAL),
            (r"the alternative", r"success would be a cosmic coincidence: \ `a miracle'", BAD),
            (r"the form", r"inference to the best explanation \ (Part 15), \ applied to science itself", GOAL),
            (r"the circle", r"anti-realists doubt IBE for unobservables, \ so cannot be moved by an IBE for realism",
             ANTI),
        ]
        g = rows_table(rows, top=1.3, gap=0.5, width=8.6, x_text=-2.6)
        with self.voiceover(
            "The main argument for scientific realism is the no-miracles argument. <bookmark mark='a'/>The datum: "
            "our best theories predict new phenomena, which no one had seen, with astonishing accuracy. "
            "<bookmark mark='b'/>The best explanation of this success is that the theories are approximately true, "
            "and the entities they posit exist. <bookmark mark='c'/>Otherwise the success is a cosmic coincidence: a "
            "miracle. <bookmark mark='d'/>The argument is an inference to the best explanation, the pattern of Part "
            "fifteen, applied to science as a whole. <bookmark mark='e'/>Which is its first problem: an anti-"
            "realist already doubts inferences to the best explanation about unobservables, and so will not be "
            "moved by one about realism."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def bayes(self):
        d = load("miracles")
        head = label(r"The base-rate fallacy in the no-miracles argument", font_size=28, color=CONN).to_edge(
            UP, buff=0.3)
        eq = MathTex(r"P(T \mid S) = \frac{P(S \mid T)\, P(T)}{P(S \mid T)\, P(T) + P(S \mid \lnot T)\, P(\lnot T)}",
                     font_size=32, color=THEORY).next_to(head, DOWN, buff=0.35)
        ex = label(r"$P(S \mid T) = 0.95$: \ true theories usually succeed; \ \ $P(S \mid \lnot T) = 0.05$: \ false "
                   r"ones rarely do", font_size=19, color=GREY_A).next_to(eq, DOWN, buff=0.2)
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 1, 0.25], x_length=5.6, y_length=2.8,
                  axis_config={"color": GREY_B, "font_size": 18},
                  x_axis_config={"numbers_to_include": []},
                  y_axis_config={"numbers_to_include": [0, 0.5, 1]}).move_to([-3.6, -1.5, 0])
        ticks = VGroup(*[label(t, font_size=16, color=GREY_A).next_to(ax.c2p(k + 4, 0), DOWN, buff=0.12)
                         for k, t in ((-4, r"$10^{-4}$"), (-3, r"$10^{-3}$"), (-2, r"$10^{-2}$"), (-1, r"$0.1$"),
                                      (0, r"$1$"))])
        curve = series_plot(ax, [y for _, y in d["curve"]], REAL, xs=[x + 4 for x, _ in d["curve"]], width=4)
        xl = label(r"base rate $P(T)$: \ the share of candidate theories that are true", font_size=17,
                   color=GREY_A).next_to(ticks, DOWN, buff=0.15)
        yl = label(r"$P(T \mid S)$", font_size=18, color=REAL).next_to(ax, UP, buff=0.05).shift(LEFT * 2.5)
        hd = [r"P(T)", r"P(T \mid S)"]
        rows = [[MathTex(f"{r['base_rate']:g}", font_size=24), MathTex(f"{r['posterior']:.2f}", font_size=24,
                                                                      color=OK if r["posterior"] > 0.5 else BAD)]
                for r in d["table"]]
        grid = ValueGrid(hd, rows, col_w=[1.5, 1.7], cell_h=0.45, font_size=20).move_to([1.4, -1.4, 0])
        note = stack([(r"Magnus and Callender \ (2004):", WHITE),
                      (r"the base rate decides,", BAD),
                      (r"and no one knows it", BAD),
                      (r"`wholesale' arguments fail;", GOAL),
                      (r"go `retail', \ theory by theory", GOAL)], font_size=19, aligned_edge=LEFT,
                     width=3.6).move_to([5.0, -1.4, 0])
        with self.voiceover(
            "P. D. Magnus and Craig Callender pointed out that the no-miracles argument has the structure of Part "
            "16's medical test. <bookmark mark='a'/>We want the probability that a theory is true, given that it is "
            "successful. <bookmark mark='b'/>Grant that true theories usually succeed, and false theories rarely do. "
            "<bookmark mark='c'/>The answer still depends on the base rate: what fraction of the candidate theories "
            "scientists consider are true. <bookmark mark='d'/>If half are, success is strong evidence: ninety-five "
            "percent. If one in a hundred is, success leaves the theory more likely false than true: sixteen percent. "
            "<bookmark mark='e'/>Realists ignore the base rate; anti-realists assume it is low; and no one knows "
            "what it is. Magnus and Callender concluded that wholesale arguments about all of science are hopeless, "
            "and that the debate must go retail, theory by theory."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(FadeIn(ex))
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(ticks), FadeIn(xl), FadeIn(yl), Create(curve), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(grid.head), Create(grid.rule), LaggedStart(*[FadeIn(VGroup(*r)) for r in grid.cell],
                                                                        lag_ratio=0.2))
            vo.wait_until("e")
            self.play(FadeIn(note))
        self.clear_scene()

    def retail(self):
        head = label(r"Going retail", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"novel prediction", r"Fresnel's wave theory predicted a bright spot at the centre of a disc's shadow "
                                  r"\ (Poisson's objection, \ 1818); \ Arago saw it", OK),
            (r"Perrin \ (1913)", r"thirteen independent methods gave the same Avogadro number: \ a coincidence, \ "
                                 r"unless atoms are real", OK),
            (r"Hacking \ (1983)", r"`if you can spray them, \ then they are real': \ electrons as tools", REAL),
            (r"the counter", r"the base rate returns: \ how often did such successes come from false theories?", BAD),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.6, x_text=-2.8)
        with self.voiceover(
            "Retail arguments look at particular episodes. <bookmark mark='a'/>Augustin Fresnel's wave theory of "
            "light implied, as Siméon Poisson pointed out in order to refute it, that a bright spot should appear "
            "at the centre of a disc's shadow. François Arago looked, and saw it. <bookmark mark='b'/>Jean Perrin, "
            "in 1913, listed thirteen independent ways of measuring Avogadro's number, from Brownian motion to the "
            "blue of the sky, all agreeing. Either atoms are real, or the agreement is a coincidence. "
            "<bookmark mark='c'/>Ian Hacking added an argument from practice: if you can spray electrons at a "
            "target to change its charge, they are real. <bookmark mark='d'/>The opponent's reply is historical: "
            "how often have such successes come from theories that were false? The next chapter counts."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
