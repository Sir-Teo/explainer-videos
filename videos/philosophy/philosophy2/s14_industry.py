from __future__ import annotations

from videos.philosophy.philosophy2.common import *  # noqa: F403
from explainer.philosophy.reasoner import prop


def box(text, color, w=1.4, h=0.8, font_size=24):
    b = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=color, stroke_width=2.2,
                         fill_color=color, fill_opacity=0.1)
    return VGroup(b, label(text, font_size=font_size, color=color).move_to(b))


class Industry(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"SAT at work", r"Where does logic earn its keep?", lit=(2016,), part=PART)
        with self.voiceover("Chapter thirteen. SAT at work."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.chips()
        self.cloud()
        self.packages()
        self.maths()

    def chips(self):
        hc = history_card(1994, r"Thomas Nicely", r"the Pentium divides wrongly in rare cases; Intel takes a "
                          r"\$475 million charge to replace the chips", width=5.6, color=HIST).to_corner(UL, buff=0.4)
        k = 4
        steps = VGroup(*[box(rf"$T$", CONN, w=1.0, h=0.8) for _ in range(k)]).arrange(RIGHT, buff=0.55)
        init = box(r"$I$", ATOM, w=0.9, h=0.8)
        bad = box(r"$\lnot P$", BAD, w=1.0, h=0.8)
        row = VGroup(init, steps, bad).arrange(RIGHT, buff=0.55).move_to([0.4, -0.9, 0])
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.05, color=GREY_B, stroke_width=3)
                          for a, b in zip([init] + list(steps), list(steps) + [bad])])
        states = VGroup(*[MathTex(rf"s_{i}", font_size=26, color=P.WORLD).next_to(arrows[i], UP, buff=0.08)
                          for i in range(k + 1)])
        q = label(r"is there an input sequence that breaks property $P$ within $k$ steps? \ one SAT question",
                  font_size=26, color=GOAL).next_to(row, DOWN, buff=0.5)
        hc2 = history_card(1999, r"Biere, Cimatti, Clarke \& Zhu", r"bounded model checking", width=4.6,
                           color=HIST).to_corner(UR, buff=0.4)
        with self.voiceover(
            "In 1994 the mathematician Thomas Nicely noticed that Intel's new Pentium processor got certain "
            "divisions wrong. Intel estimated about one random division in nine billion. It replaced the chips, at "
            "a cost of four hundred and seventy-five million dollars. <bookmark mark='a'/>After that, chip makers "
            "turned to proof: write the chip's logic as formulas, and check it against its specification for every "
            "input, not a sample. <bookmark mark='b'/>One method, bounded model checking, from 1999, unrolls a "
            "circuit over k clock cycles: a copy of its transition logic for each step, the starting state at one "
            "end, and the failure of a property at the other. <bookmark mark='c'/>Is there an input sequence that "
            "reaches the failure? One SAT question. If the answer is no, no input can break the chip within k steps."
        ) as vo:
            self.play(FadeIn(hc, shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(init), FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(hc2), LaggedStart(*[FadeIn(x) for x in list(steps[1:]) + [bad]], lag_ratio=0.2),
                      LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), FadeIn(states))
            vo.wait_until("c")
            self.play(FadeIn(q))
        self.clear_scene()

    def cloud(self):
        pol = code_block(['{"Effect": "Allow",', ' "Principal": "*",', ' "Action": "s3:GetObject",',
                          ' "Resource": "arn:aws:s3:::bucket/*",', ' "Condition": {"IpAddress": ...}}'],
                         font_size=20)
        if pol.width > 5.0:
            pol.width = 5.0
        pol.to_edge(LEFT, buff=0.4).set_y(0.0)
        arrow1 = Arrow(pol.get_right() + RIGHT * 0.1, pol.get_right() + RIGHT * 0.9, color=GREY_B)
        fml = MathTex(r"\exists\, r:\ \mathrm{Allowed}(r) \land \mathrm{Public}(r)\ ?", font_size=34)
        fml.next_to(arrow1, RIGHT, buff=0.15)
        ans = VGroup(label(r"unsatisfiable", font_size=26, color=OK), label(r"no public access", font_size=22,
                                                                          color=GREY_A)).arrange(DOWN, buff=0.1)
        ans.next_to(fml, DOWN, buff=0.7)
        arrow2 = Arrow(fml.get_bottom() + DOWN * 0.05, ans.get_top() + UP * 0.05, color=GREY_B, buff=0.05)
        cite_ = cite(r"Backes et al., `Semantic-based automated reasoning for AWS access policies' (2018); "
                     r"Rungta, `A billion SMT queries a day' (CAV 2022)")
        hc = history_card(2018, r"Amazon Web Services", r"Zelkova: access policies, translated into logic and "
                          r"checked by SMT solvers", width=5.8, color=HIST).to_edge(UP, buff=0.4)
        with self.voiceover(
            "In the cloud, the same idea guards data. Amazon's tool Zelkova translates the access policies that "
            "customers write into logic, <bookmark mark='a'/>and asks a solver whether some request could be allowed "
            "that would expose the data to the public. <bookmark mark='b'/>The solvers here are SMT solvers: SAT "
            "solvers extended with arithmetic, strings and other theories. <bookmark mark='c'/>In 2022 Amazon's Neha "
            "Rungta reported that such checks were running about a billion times a day."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(pol))
            vo.wait_until("a")
            self.play(GrowArrow(arrow1), Write(fml))
            vo.wait_until("b")
            self.play(GrowArrow(arrow2), FadeIn(ans))
            vo.wait_until("c")
            self.play(FadeIn(cite_))
        self.clear_scene()

    def packages(self):
        # a tiny dependency problem, solved by the Reasoner
        cons = [("A1", "A1 -> (B2 | B3)", r"$A_1$ needs $B \geq 2$"),
                ("C1", "C1 -> ~B3", r"$C_1$ conflicts with $B_3$"),
                ("one", "~(B2 & B3)", r"at most one version of $B$"),
                ("want", "A1 & C1", r"install $A_1$ and $C_1$")]
        fs = [prop.parse(c[1]) for c in cons]
        v = prop.solve(fs)
        assert v is not None and v["B2"] and not v["B3"]
        rows = VGroup()
        for _, f, w in cons:
            rows.add(VGroup(fmath(f, font_size=32), label(w, font_size=24, color=GREY_A)).arrange(RIGHT, buff=0.5))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-2.2, 0.4, 0])
        sol = label(rf"solver: \ install $B_2$; \ $B_3$ stays out", font_size=30, color=OK).next_to(rows, DOWN,
                                                                                               buff=0.5)
        fact = VGroup(label(r"installability is NP-complete", font_size=26, color=GOAL),
                      label(r"(Mancinelli et al.\ 2006)", font_size=20, color=GREY_B),
                      label(r"package managers: libsolv, conda, \dots", font_size=24, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Installing software is a logic problem too. <bookmark mark='a'/>Each package demands certain versions "
            "of others and conflicts with some: clauses. Here, A one needs version two or three of B, C one cannot "
            "live with B three, and only one version of B can be installed. <bookmark mark='b'/>The Reasoner's solver "
            "picks B two. <bookmark mark='c'/>With thousands of packages this is a real search: deciding whether a "
            "package can be installed at all is NP-complete, and package managers, from Linux distributions to the "
            "scientific Python installer conda, hand it to SAT-style solvers."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(sol))
            vo.wait_until("c")
            self.play(FadeIn(fact))
        self.clear_scene()

    def maths(self):
        hcs = VGroup(
            history_card(2016, r"Heule, Kullmann \& Marek", r"Pythagorean triples: 7,825; a 200-terabyte proof",
                         width=4.2, color=HIST, font_size=20),
            history_card(2017, r"Marijn Heule", r"the fifth Schur number is 160; a 2-petabyte proof", width=4.2,
                         color=HIST, font_size=20),
            history_card(2020, r"Brakensiek, Heule, Mackey \& Narváez", r"Keller's conjecture in dimension 7",
                         width=4.2, color=HIST, font_size=20)).arrange(RIGHT, buff=0.3).to_edge(UP, buff=0.45)
        q = quote_card(r"If we accept the four-colour theorem as a theorem, then we are committed to changing the "
                       r"sense of `theorem', or, more to the point, to changing the sense of the underlying concept "
                       r"of `proof'.", r"Thomas Tymoczko, 1979", r"`The Four-Color Problem and its Philosophical "
                       r"Significance', \textit{Journal of Philosophy}", width=10.6, font_size=26)
        q.move_to([0, -1.3, 0])
        fc = label(r"1976: Appel \& Haken prove the four-colour theorem by computer. \ (Wolfgang Haken was Armin "
                   r"Haken's father.)", font_size=22, color=GREY_A).next_to(hcs, DOWN, buff=0.35)
        pd = load("pythag")
        n, colour = pd["n"], pd["colour"]
        strip = VGroup()
        for i in range(n):
            r, c = divmod(i, 40)
            strip.add(Square(0.24, stroke_width=0, fill_color=P.CLAIM if colour[i] else P.AGENT,
                             fill_opacity=0.85).move_to([(c - 19.5) * 0.27, -r * 0.27, 0]))
        strip.move_to([0, -1.4, 0])
        sl = label(rf"the 2016 problem, up to {n}: \ solved here in {pd['seconds']:.2f} s; \ up to 7,825: a "
                   r"200-terabyte refutation", font_size=22, color=GREY_A).next_to(strip, DOWN, buff=0.25)
        with self.voiceover(
            "And in mathematics. <bookmark mark='a'/>The Pythagorean triples of the opening, in 2016. The fifth "
            "Schur number, 160, the next year, with a proof of two petabytes. Keller's conjecture about tilings by "
            "cubes, in dimension seven, in 2020. Each is a theorem that no person has checked line by line, "
            "certified instead by a proof checker small enough to verify on its own."
        ) as vo:
            self.play(FadeIn(hcs[0], shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(h, shift=DOWN * 0.2) for h in hcs[1:]], lag_ratio=0.3))
            self.play(LaggedStart(*[FadeIn(x) for x in strip], lag_ratio=0.003), FadeIn(sl), run_time=2)
        self.play(FadeOut(strip), FadeOut(sl))
        with self.voiceover(
            "Is a two-hundred-terabyte certificate a proof? The question is older than these solvers. "
            "<bookmark mark='a'/>In 1976 Kenneth Appel and Wolfgang Haken proved the four-colour theorem with a "
            "computer, and three years later the philosopher Thomas Tymoczko argued that accepting it meant changing "
            "what we mean by proof: <bookmark mark='b'/>that mathematics had admitted experiment. Today the standard "
            "answer is formal: a certificate is a proof if a small, trusted program checks it. Part 9 asks what such a "
            "check shows, and what it leaves out."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(fc))
            vo.wait_until("b")
            self.play(FadeIn(q, shift=UP * 0.2))
        self.clear_scene()
