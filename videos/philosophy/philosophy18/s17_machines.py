from __future__ import annotations

from videos.philosophy.philosophy18.common import *  # noqa: F403


class Machines(VoiceoverScene):
    def construct(self):
        card = chapter_card(16, r"AI scientists", r"Can a machine discover, \ and can it explain?", lit=(1978, 2021),
                            part=PART)
        with self.voiceover("Chapter sixteen. AI scientists."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.bacon()
        self.discovery()
        self.blackbox()

    def bacon(self):
        d = load("bacon")
        hc = history_card(1978, r"Pat Langley", r"BACON, \ with Herbert Simon", width=5.0,
                          color=HIST).to_corner(UL, buff=0.3)
        hd = [r"\text{planet}", r"a\ (\text{AU})", r"T\ (\text{years})", r"a^3 / T^2"]
        rows = [[label(n, font_size=18), MathTex(f"{a:.3f}", font_size=22), MathTex(f"{t:.3f}", font_size=22),
                 MathTex(f"{a ** 3 / t ** 2:.4f}", font_size=22, color=OK)] for n, a, t in d["planets"]]
        grid = ValueGrid(hd, rows, col_w=[1.8, 1.6, 1.8, 1.8], cell_h=0.46, font_size=20).move_to([-2.4, -0.6, 0])
        f = d["found"][0]
        side = stack([(r"search the products $a^i T^j$, \ $|i|, |j| \le 3$: \ " + f"{d['tried']}" + r" terms", WHITE),
                      (r"keep one that is constant across the planets", WHITE),
                      (r"found: \ $a^{" + f"{f['i']}" + r"} T^{" + f"{f['j']}" + r"}$, \ spread " +
                       f"{100 * f['cv']:.2f}" + r"\%; \ the next best varies by " + f"{100 * d['best_cv_other']:.0f}"
                       + r"\%", OK),
                      (r"Kepler's third law \ (1619), \ rediscovered from the data", GOAL),
                      (r"but the variables, \ and the idea of looking, \ were supplied", BAD)], font_size=20,
                     aligned_edge=LEFT, width=5.6).move_to([3.8, -0.6, 0])
        with self.voiceover(
            "Can a machine make a scientific discovery? <bookmark mark='a'/>In 1978 Pat Langley and Herbert Simon's "
            "program BACON was given planetary data: each planet's distance from the Sun and its period. "
            "<bookmark mark='b'/>The Reasoner runs a miniature version. It forms products of small powers of "
            "distance and period, forty-eight in all, and looks for one that stays constant across the planets. "
            "<bookmark mark='c'/>It finds the cube of the distance over the square of the period, constant to a "
            "tenth of a percent, while every other term varies by half its size or more. "
            "<bookmark mark='d'/>That is Kepler's third law, which Kepler found in 1618 after years of searching. "
            "<bookmark mark='e'/>Critics "
            "noted that the hard part had been done for the machine: someone chose the variables, cleaned the data, "
            "and decided that a constant was worth looking for."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(VGroup(*r[:3])) for r in grid.cell])
            vo.wait_until("b")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(*[FadeIn(r[3]) for r in grid.cell], FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def discovery(self):
        head = label(r"Discovery by machine, \ now", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"AlphaFold \ (2020--21)", r"predicts protein structures near experimental accuracy; \ the 2024 Nobel "
                                        r"Prize in Chemistry \ (Hassabis, \ Jumper; \ with Baker)", OK),
            (r"FunSearch \ (2023)", r"a language model proposes programs, \ an evaluator scores them: \ new cap-set "
                                    r"constructions in combinatorics", THEORY),
            (r"AlphaEvolve \ (2025)", r"evolved algorithms, \ including a $4\times 4$ complex matrix product with 48 "
                                      r"multiplications", THEORY),
            (r"automated papers \ (2024--)", r"systems that propose, \ run and write up experiments; \ quality "
                                             r"contested", BAD),
            (r"Reichenbach \ (1938)", r"the context of discovery and the context of justification: \ machines enter "
                                      r"the first, \ evidence still governs the second", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.6, x_text=-2.6)
        with self.voiceover(
            "Machine discovery is no longer a toy. <bookmark mark='a'/>DeepMind's AlphaFold predicts the three-"
            "dimensional structures of proteins close to experimental accuracy; Demis Hassabis and John Jumper "
            "shared the 2024 Nobel Prize in Chemistry for it, with David Baker. <bookmark mark='b'/>FunSearch paired "
            "a language model that proposes programs with an evaluator that scores them, and found new "
            "constructions in a problem of combinatorics. <bookmark mark='c'/>AlphaEvolve extended the approach to "
            "algorithms, including a way of multiplying four by four complex matrices with forty-eight "
            "multiplications. <bookmark mark='d'/>Systems now propose, run and write up experiments of their own, "
            "with contested quality. <bookmark mark='e'/>Hans Reichenbach distinguished the context of discovery "
            "from the context of justification. Machines have entered the first; evidence still governs the second."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def blackbox(self):
        head = label(r"Explanation from a black box?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"epistemic opacity", r"Humphreys \ (2009): \ no human can survey the steps by which the model reached "
                                   r"its output", BAD),
            (r"prediction is not understanding", r"de Regt \ (2017): \ understanding needs an intelligible theory, \ "
                                                 r"one we can use to reason qualitatively", REAL),
            (r"link uncertainty", r"Sullivan \ (2022): \ opacity matters less than whether we know how the model's "
                                  r"features connect to the world", OK),
            (r"this part's tools", r"a model that predicts can still be asked: \ does it unify? \ track causes? \ "
                                   r"survive intervention? \ show invariance?", GOAL),
        ]
        g = rows_table(rows, top=1.5, gap=0.55, width=8.0, x_label=-6.4, x_text=-2.0)
        with self.voiceover(
            "Does a model that predicts explain? <bookmark mark='a'/>Paul Humphreys called the problem epistemic "
            "opacity: no human can survey the steps by which a large computation reached its output. "
            "<bookmark mark='b'/>Henk de Regt argued that understanding requires an intelligible theory, one we can "
            "use to reason about consequences without calculating. <bookmark mark='c'/>Emily Sullivan replied that "
            "opacity matters less than link uncertainty: whether we know how the model's features connect to the "
            "phenomena. <bookmark mark='d'/>The accounts of this part become tests. Does the model unify? Does it "
            "track causes? Do its relations survive intervention? Are they invariant across environments? A model "
            "that passes them explains, whoever, or whatever, built it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
