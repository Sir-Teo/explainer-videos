from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs53.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load


def meter(x, y, color=KERN, size=0.5):
    """A measurement box: a dial with a needle."""
    sq = Square(side_length=size, stroke_color=color, stroke_width=2, fill_color=BG, fill_opacity=1).move_to([x, y, 0])
    arc = Arc(radius=size * 0.32, start_angle=PI / 6, angle=2 * PI / 3, color=color, stroke_width=2).move_to(
        [x, y - size * 0.02, 0])
    needle = Line([x, y - size * 0.2, 0], [x + size * 0.2, y + size * 0.2, 0], color=color, stroke_width=2)
    return VGroup(sq, arc, needle)


def prob_bar(lo, hi, color, text, w=4.4, h=0.34):
    """The interval [0, 1] with the allowed range of the acceptance probability shaded."""
    frame = Rectangle(width=w, height=h, stroke_color=GREY_C, stroke_width=1.5)
    fill = Rectangle(width=w * (hi - lo), height=h, stroke_width=0, fill_color=color, fill_opacity=0.7)
    fill.move_to(frame.get_left() + RIGHT * w * (lo + (hi - lo) / 2))
    ticks = VGroup(*[MathTex(t, font_size=20, color=GREY_B).next_to(frame.get_left() + RIGHT * w * v, DOWN,
                                                                      buff=0.08)
                     for t, v in ((r"0", 0), (r"\tfrac13", 1 / 3), (r"\tfrac23", 2 / 3), (r"1", 1))])
    marks = VGroup(*[Line(frame.get_left() + RIGHT * w * v + UP * h / 2, frame.get_left() + RIGHT * w * v + DOWN * h / 2,
                          color=GREY_B, stroke_width=1.2) for v in (1 / 3, 2 / 3)])
    t = label(text, font_size=19, color=color).next_to(frame, UP, buff=0.12).align_to(frame, LEFT)
    return VGroup(frame, fill, marks, ticks, t)


def event_card(year, text, col, w=4.0):
    body = VGroup(label(year, font_size=22, color=col), wrapped_label(text, w - 0.3, font_size=18, color=GREY_A)).arrange(
        DOWN, buff=0.1, aligned_edge=LEFT)
    fr = RoundedRectangle(width=w, height=body.height + 0.3, corner_radius=0.1, stroke_color=col, stroke_width=1.6,
                          fill_color=BG, fill_opacity=1)
    body.move_to(fr)
    return VGroup(fr, body)


class Bqp(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.inclusions()
        self.np_complete()
        self.supremacy()
        self.limits()

    def card(self):
        card = chapter_card(11, r"What quantum computers cannot do", r"Where does BQP sit among the classes?",
                            lit=(1993, 2019), extra=((1993, r"Bernstein and Vazirani: \ BQP"),
                                                     (2019, r"a first supremacy claim")), part=PART)
        with self.voiceover("Chapter eleven. What quantum computers cannot do. Where does BQP sit among the "
                            "classes?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ the definition
    def definition(self):
        head = label(r"BQP: \ bounded-error quantum polynomial time", font_size=36).to_edge(UP, buff=0.3)
        ys = [2.0 - 0.42 * i for i in range(6)]
        x0, x1 = -4.3, 0.6
        wires = VGroup(*[Line([x0, y, 0], [x1 if i == 0 else -0.2, y, 0], color=GREY_B, stroke_width=1.8)
                         for i, y in enumerate(ys)])
        kets = VGroup(*[MathTex(r"|x_{%d}\rangle" % (i + 1) if i < 3 else r"|0\rangle", font_size=22,
                                color=DATA if i < 3 else GREY_A).next_to([x0, y, 0], LEFT, buff=0.08)
                        for i, y in enumerate(ys)])
        b1 = Brace(VGroup(*kets[:3]), LEFT, buff=0.08, color=DATA)
        b1l = label(r"input, \ $n$ bits", font_size=17, color=DATA).next_to(b1, LEFT, buff=0.08)
        b2 = Brace(VGroup(*kets[3:]), LEFT, buff=0.08, color=GREY_B)
        b2l = label(r"poly$(n)$ \ work qubits", font_size=17, color=GREY_B).next_to(b2, LEFT, buff=0.08)
        box = Rectangle(width=2.7, height=ys[0] - ys[-1] + 0.6, stroke_color=HEAD, stroke_width=2, fill_color=BG,
                        fill_opacity=1).move_to([-1.75, (ys[0] + ys[-1]) / 2, 0])
        bt = VGroup(label(r"poly$(n)$ gates", font_size=21, color=HEAD),
                    label(r"$H$, \ $T$, \ CNOT \ (chapter 4)", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.12)
        bt.move_to(box)
        m = meter(0.55, ys[0])
        acc = label(r"accept?", font_size=20, color=KERN).next_to(m, RIGHT, buff=0.15)
        uni = wrapped_label(r"\textit{uniform}: \ a classical program writes the circuit for each $n$ in polynomial "
                            r"time", 6.0, font_size=18, color=GREY_B).next_to(box, DOWN, buff=0.35).set_x(-2.6)
        yes_ = prob_bar(2 / 3, 1, YES, r"$x$ a yes-instance: \ $P(\text{accept}) \ge \tfrac23$", w=3.9)
        no_ = prob_bar(0, 1 / 3, NO, r"$x$ a no-instance: \ $P(\text{accept}) \le \tfrac13$", w=3.9)
        VGroup(yes_, no_).arrange(DOWN, buff=0.55).move_to([4.75, 0.95, 0])
        notes = VGroup(
            wrapped_label(r"the thirds are arbitrary: \ the majority of $k$ runs errs with probability "
                          r"$e^{-\Omega(k)}$ \ (Chernoff, \ as for Part 27's BPP)", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"$\mathrm{BPP} \subseteq \mathrm{BQP}$: \ chapter 1's Toffoli gates make any classical "
                          r"circuit reversible, \ and $H$ on a fresh qubit is a fair coin", 12.4, font_size=20,
                          color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "What exactly can a quantum computer do efficiently? <bookmark mark='a'/> The class is BQP, defined by "
            "Bernstein and Vazirani in 1993. A problem is in it if, for inputs of n bits, a classical program can "
            "write down in polynomial time a circuit of polynomially many gates from chapter four's set, ending in "
            "the measurement of one qubit. <bookmark mark='b'/> On yes-instances it accepts with probability at "
            "least two thirds; on no-instances, at most one third. <bookmark mark='c'/> The thirds are arbitrary: "
            "run it k times and take the majority, and the error falls exponentially in k, as for Part 27's BPP. "
            "<bookmark mark='d'/> And BQP contains BPP: chapter one's Toffoli gates make any classical circuit "
            "reversible, and a Hadamard on a fresh qubit is a fair coin."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(wires), FadeIn(kets), FadeIn(b1), FadeIn(b1l), FadeIn(b2), FadeIn(b2l))
            self.play(FadeIn(box), FadeIn(bt))
            self.play(FadeIn(m), FadeIn(acc), FadeIn(uni))
            vo.wait_until("b")
            self.play(FadeIn(yes_))
            self.play(FadeIn(no_))
            vo.wait_until("c")
            self.play(FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ BPP ⊆ BQP ⊆ PP ⊆ PSPACE
    def inclusions(self):
        head = label(r"$\mathrm{BPP} \subseteq \mathrm{BQP} \subseteq \mathrm{PP} \subseteq \mathrm{PSPACE}$",
                     font_size=36).to_edge(UP, buff=0.3)
        c = np.array([-3.9, -0.35, 0])
        sets = VGroup()
        for i, (name, col) in enumerate(((r"BPP", DATA), (r"BQP", YES), (r"PP", LAM), (r"PSPACE", KERN))):
            w, h = 1.7 + 1.25 * i, 1.0 + 1.05 * i
            e = Ellipse(width=w, height=h, color=col, stroke_width=2.4).move_to(c + UP * (h / 2 - 0.5))
            t = label(name, font_size=22, color=col).move_to(e.get_top() + DOWN * 0.27)
            sets.add(VGroup(e, t))
        fs = 26
        rows = VGroup(
            MathTex(r"\langle y|U_T\cdots U_1|x\rangle", r"=",
                    r"\sum_{z_1,\dots,z_{T-1}} \langle y|U_T|z_{T-1}\rangle \cdots \langle z_1|U_1|x\rangle",
                    font_size=fs),
            MathTex(r"\langle y|U_T\cdots U_1|x\rangle", r"=", r"\sum_{\text{paths}} \pm 2^{-h/2}", font_size=fs),
            MathTex(r"\langle y|U_T\cdots U_1|x\rangle", r"=", r"\frac{N_+(y) - N_-(y)}{2^{h/2}}", font_size=fs),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.55)
        rows.move_to([3.4, 1.0, 0]).align_to([-0.7, 0, 0], LEFT)
        rows[2][2].set_color(YES)
        whys = VGroup(label(r"Feynman's sum over paths: \ multiply along a path, \ add across \ (chapter 5)",
                            font_size=18, color=GREY_B),
                      label(r"with only $H$ and Toffoli, \ which suffice, \ every path weighs $\pm 2^{-h/2}$",
                            font_size=18, color=GREY_B),
                      label(r"$N_\pm$: \ the numbers of positive and negative paths", font_size=18, color=GREY_B))
        for w_, r in zip(whys, rows):
            w_.next_to(r, DOWN, buff=0.1).align_to(r, LEFT).shift(RIGHT * 0.1)
        notes = VGroup(
            wrapped_label(r"\textbf{PSPACE}: \ add the paths one at a time, \ reusing memory \ (Bernstein and "
                          r"Vazirani, \ 1993)", 7.3, font_size=19, color=KERN),
            wrapped_label(r"\textbf{PP}: \ deciding whether $\sum_y |\langle y|U|x\rangle|^2 > \tfrac12$ compares "
                          r"counts of paths \ (Adleman, \ DeMarrais and Huang, \ 1997)", 7.3, font_size=19, color=LAM),
            wrapped_label(r"no inclusion is known to be strict: \ even $\mathrm{P} \ne \mathrm{PSPACE}$ is unproved",
                          7.3, font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(whys[2], DOWN, buff=0.4).align_to(rows, LEFT)
        with self.voiceover(
            "Where does BQP sit among the classical classes? <bookmark mark='a'/> It contains BPP, as we saw. "
            "<bookmark mark='b'/> For an upper bound, write the amplitude of an outcome as Feynman did: a sum over "
            "every path through the intermediate basis states, multiplying along each path and adding across "
            "paths, as in chapter five. <bookmark mark='c'/> With only Hadamard and Toffoli "
            "gates, which suffice for any quantum computation, every path weighs plus or minus the same small "
            "number. The amplitude is the count of positive paths minus the count of negative ones, scaled. "
            "<bookmark mark='d'/> A classical machine can add the paths one at a time, reusing its memory: "
            "exponential time, but polynomial space. And comparing the counts puts BQP inside PP, as Adleman, "
            "DeMarrais and Huang showed in 1997. <bookmark mark='e'/> None of these inclusions is known to be "
            "strict."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(sets[0][0]), FadeIn(sets[0][1]))
            self.play(Create(sets[1][0]), FadeIn(sets[1][1]))
            vo.wait_until("b")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(Create(sets[3][0]), FadeIn(sets[3][1]), FadeIn(notes[0]))
            self.play(Create(sets[2][0]), FadeIn(sets[2][1]), FadeIn(notes[1]))
            vo.wait_until("e")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ NP-complete problems
    def np_complete(self):
        gs = load("gscale")["rows"][-1]
        head = label(r"NP-complete problems: \ no known quantum shortcut", font_size=36).to_edge(UP, buff=0.3)
        np_box = RoundedRectangle(width=6.6, height=4.6, corner_radius=0.2, stroke_color=DATA, stroke_width=2.4)
        np_box.move_to([-3.1, -0.4, 0])
        npl = label(r"NP", font_size=24, color=DATA).move_to([-1.75, 1.5, 0])
        npc = Rectangle(width=1.6, height=4.6 - 0.04, stroke_width=0, fill_color=NO, fill_opacity=0.22).move_to(
            np_box.get_right() + LEFT * 0.82)
        npcl = VGroup(label(r"NP-complete", font_size=18, color=NO),
                      label(r"SAT", font_size=17, color=GREY_A), label(r"colouring", font_size=17, color=GREY_A),
                      label(r"TSP", font_size=17, color=GREY_A)).arrange(DOWN, buff=0.18).move_to(npc)
        bqp = Ellipse(width=4.0, height=4.6, color=YES, stroke_width=2.4).move_to([-4.2, 0.1, 0])
        bqpl = label(r"BQP", font_size=24, color=YES).move_to([-4.2, 2.05, 0])
        p_ = Ellipse(width=1.8, height=1.3, color=GREY_A, stroke_width=2).move_to([-4.6, -1.0, 0])
        pl = label(r"P", font_size=22, color=GREY_A).move_to(p_)
        fac = VGroup(label(r"factoring", font_size=18, color=YES), label(r"discrete log", font_size=18,
                                                                         color=YES)).arrange(DOWN, buff=0.1)
        fac.move_to([-3.35, 0.55, 0])
        warn = note(r"the believed picture: \ none of it is proved", font_size=17).next_to(np_box, DOWN, buff=0.15)
        notes = VGroup(
            wrapped_label(r"factoring and discrete log: \ in BQP and in NP, \ not believed NP-complete", 5.6,
                          font_size=19, color=YES),
            wrapped_label(rf"brute force gains only a square root: \ $2^{{16}} = {format(gs['N'], ',').replace(',', '{,}')}$ assignments, \ "
                          rf"{gs['iterations']} Grover rounds \ (chapter 10); \ relative to a random oracle, \ "
                          r"$\mathrm{NP} \not\subseteq \mathrm{BQP}$ \ (Bennett et al., \ 1997)", 5.6, font_size=19,
                          color=NO),
            wrapped_label(r"a fast algorithm would have to exploit structure, \ as Shor's does; \ none is known", 5.6,
                          font_size=19, color=WHITE),
            wrapped_label(r"relative to an oracle, \ BQP escapes the whole polynomial hierarchy \ (Raz and Tal, \ "
                          r"2018)", 5.6, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([3.9, -0.3, 0])
        with self.voiceover(
            "Does BQP contain the NP-complete problems? Nobody knows, but the evidence says no. "
            "<bookmark mark='a'/> Here is the picture most researchers believe, though none of it is proved. "
            "Factoring and discrete logarithms lie in BQP and in NP, and are not thought to be NP-complete. "
            "<bookmark mark='b'/> The NP-complete problems sit outside BQP. Brute force gains only a square root: "
            "sixty-five thousand assignments of sixteen variables still need two hundred and one Grover rounds. And "
            "relative to a random oracle, Bennett, Bernstein, Brassard and Vazirani showed that NP is not inside "
            "BQP. <bookmark mark='c'/> A fast quantum algorithm would have to exploit structure, as Shor's does. "
            "<bookmark mark='d'/> BQP may also reach outside NP: relative to an oracle, Raz and "
            "Tal showed in 2018 that it escapes the whole polynomial hierarchy."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(np_box), FadeIn(npl), Create(p_), FadeIn(pl), FadeIn(warn))
            self.play(Create(bqp), FadeIn(bqpl))
            self.play(FadeIn(fac), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(npc), FadeIn(npcl), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]), Indicate(bqpl, color=HEAD))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ supremacy claims and replies
    def supremacy(self):
        head = label(r"Supremacy claims, \ and the classical replies", font_size=36).to_edge(UP, buff=0.3)
        y0, ya, yb = 0.05, 1.45, -1.35
        x_of = (lambda yr: -6.0 + (yr - 2010) / 13 * 12)
        axis = Line([-6.2, y0, 0], [6.2, y0, 0], color=GREY_C, stroke_width=2)
        yl = VGroup(*[label(f"{yr}", font_size=16, color=GREY_B).next_to([x_of(yr), y0, 0], DOWN, buff=0.08)
                      for yr in (2010, 2015, 2020)])
        ev = [("2011", r"Aaronson and Arkhipov; \ Bremner, \ Jozsa and Shepherd: \ an efficient exact classical "
                       r"sampler would collapse the polynomial hierarchy", 2011, DATA, -4.5, ya),
              ("2019", r"Google \ (Arute et al.): \ random circuits on 53 qubits sampled in about 200 seconds; \ "
                       r"estimated 10{,}000 years classically", 2019, YES, -2.25, yb),
              ("2019", r"IBM \ (Pednault et al.): \ the same task in about 2.5 days on a supercomputer using its "
                       r"disk storage, \ by their estimate", 2019.3, NO, 0.0, ya),
              ("2020", r"USTC \ (Zhong et al.): \ boson sampling with photons", 2020, YES, 2.25, yb),
              ("2022", r"Pan, \ Chen and Zhang: \ tensor networks simulate the 2019 task classically", 2022, NO,
               4.5, ya)]
        cards, links, dots = VGroup(), VGroup(), VGroup()
        for yr, text, x, col, sx, sy in ev:
            cd = event_card(yr, text, col, w=4.1 if sy > 0 else 4.2)
            cd.move_to([sx, sy + (cd.height / 2 if sy > 0 else -cd.height / 2) - (0.45 if sy > 0 else -0.45), 0])
            d = Dot([x_of(x), y0, 0], radius=0.08, color=col)
            edge = cd.get_bottom() if sy > 0 else cd.get_top()
            links.add(Line(d.get_center(), edge, color=col, stroke_width=1.5))
            cards.add(cd)
            dots.add(d)
        for cd in cards:
            if cd.get_right()[0] > 6.85:
                cd.shift(LEFT * (cd.get_right()[0] - 6.85))
            if cd.get_left()[0] < -6.85:
                cd.shift(RIGHT * (-6.85 - cd.get_left()[0]))
        for ln, cd, (_, _, _, col, _, sy) in zip(links, cards, ev):
            ln.put_start_and_end_on(ln.get_start(), cd.get_bottom() if sy > 0 else cd.get_top())
        foot = wrapped_label(r"the extended Church--Turing thesis is being contested in the laboratory: \ the "
                             r"sampling tasks have no known use, \ and checking their output classically is itself "
                             r"expensive", 12.4, font_size=19, color=HEAD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "If quantum computers are more powerful, an experiment should show it. <bookmark mark='a'/> "
            "In 2011 Scott Aaronson and Alex Arkhipov, and independently Bremner, Jozsa and Shepherd, identified "
            "sampling tasks natural for quantum hardware and, under complexity assumptions, hard for classical "
            "machines: an efficient exact classical sampler would collapse the polynomial hierarchy. "
            "<bookmark mark='b'/> In 2019 Google's team reported sampling from random circuits on fifty-three "
            "qubits in about two hundred seconds, and estimated ten thousand years for a supercomputer. "
            "<bookmark mark='c'/> IBM replied that, with better use of disk storage, a supercomputer would need "
            "about two and a half days. <bookmark mark='d'/> In 2020 a team in China reported a photonic version. "
            "<bookmark mark='e'/> By 2022, tensor-network methods had simulated the 2019 task. The contest goes on, "
            "and the extended Church–Turing thesis is now being tested in the laboratory."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(yl))
            for mk, cd, ln, d in zip("abcde", cards, links, dots):
                vo.wait_until(mk)
                self.play(FadeIn(d), Create(ln), FadeIn(cd, shift=UP * 0.1 if cd.get_y() > 0 else DOWN * 0.1))
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ limits on every quantum algorithm
    def limits(self):
        head = label(r"Limits that bind every quantum algorithm", font_size=36).to_edge(UP, buff=0.3)
        tab = grid_table([r"problem", r"classical queries", r"quantum queries"],
                         [[r"search \ (OR of $N$ bits)", r"$N$", r"$\Theta(\sqrt N)$ \ (chapter 10)"],
                          [r"parity of $N$ bits", r"$N$", r"$N/2$"],
                          [r"Simon \ (a promise)", r"$\Omega(2^{n/2})$", r"$O(n)$ \ (chapter 6)"]],
                         widths=[2.8, 1.9, 2.4], row_h=0.62, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.35)
        for r in range(1, 4):
            tab.cells[r][1].set_color(NO)
            tab.cells[r][2].set_color(YES)
        tl = wrapped_label(r"without a promise, \ quantum queries save at most a polynomial: \ $D(f) = O(Q(f)^6)$ "
                           r"\ (Beals, \ Buhrman, \ Cleve, \ Mosca and de Wolf, \ 1998)", 7.0, font_size=20,
                           color=HEAD).next_to(tab, DOWN, buff=0.3).align_to(tab, LEFT)
        fs = 31
        rows = VGroup(
            MathTex(r"\alpha_y(x)", r":\ \deg", r"\le", r"T", font_size=fs),
            MathTex(r"P_{\text{acc}}(x) = \sum_y |\alpha_y(x)|^2", r":\ \deg", r"\le", r"2T", font_size=fs),
            MathTex(r"\text{parity}", r":\ \deg", r"\ge", r"N", r"\;\Rightarrow\; T \ge N/2", font_size=fs),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.75)
        rows.next_to(head, DOWN, buff=0.6).align_to([1.0, 0, 0], LEFT)
        rows[2][4].set_color(YES)
        whys = VGroup(
            wrapped_label(r"each query multiplies by $(-1)^{x_i} = 1 - 2x_i$: \ after $T$ queries, \ amplitudes are "
                          r"polynomials of degree $\le T$ in the input bits", 5.6, font_size=19, color=GREY_B),
            label(r"squaring doubles the degree", font_size=19, color=GREY_B),
            wrapped_label(r"parity flips with every bit: \ any approximation has degree $N$; \ Deutsch's trick on "
                          r"pairs \ (chapter 5) \ meets the bound", 5.6, font_size=19, color=GREY_B))
        for w_, r in zip(whys, rows):
            w_.next_to(r, DOWN, buff=0.1).align_to(r, LEFT).shift(RIGHT * 0.1)
        n6 = 6
        pax = Axes(x_range=[0, n6, 1], y_range=[0, 1, 0.5], x_length=4.6, y_length=1.5,
                   axis_config={"color": GREY_D, "include_numbers": False, "include_ticks": True})
        pax.next_to(tl, DOWN, buff=0.75).align_to(tab, LEFT).shift(RIGHT * 0.5)
        pxt = VGroup(*[label(f"{k}", font_size=16, color=GREY_B).next_to(pax.c2p(k, 0), DOWN, buff=0.08)
                       for k in range(n6 + 1)])
        pxl = label(r"number of ones in $x$", font_size=17, color=GREY_B).next_to(pxt, DOWN, buff=0.08)
        half = DashedLine(pax.c2p(0, 0.5), pax.c2p(n6, 0.5), color=GREY_C, dash_length=0.06)
        hl = MathTex(r"\tfrac12", font_size=20, color=GREY_B).next_to(pax.c2p(0, 0.5), LEFT, buff=0.1)
        pdots = VGroup(*[Dot(pax.c2p(k, 0.15 if k % 2 == 0 else 0.85), radius=0.07, color=NO if k % 2 == 0 else YES)
                         for k in range(n6 + 1)])
        pcurve = pax.plot(lambda t: 0.5 - 0.35 * math.cos(PI * t), x_range=[0, n6, 0.02], color=LAM,
                          stroke_width=2.5)
        xmarks = VGroup(*[Dot(pax.c2p(k + 0.5, 0.5), radius=0.05, color=KERN) for k in range(n6)])
        pcap = wrapped_label(r"$P_{\text{acc}}$ must sit below $\tfrac13$ on even parity and above $\tfrac23$ on "
                             r"odd, \ so it crosses $\tfrac12$ at least $N$ times: \ degree $\ge N$", 5.6,
                             font_size=18, color=GREY_A)
        pill = note(rf"illustrative: \ $N = {n6}$, \ after averaging over inputs with the same number of ones",
                    font_size=16).next_to(pxl, DOWN, buff=0.08).align_to(pax, LEFT)
        pcap.next_to(whys[2], DOWN, buff=0.45).align_to(rows, LEFT)
        hol = wrapped_label(r"\textbf{Holevo} \ (1973): \ $n$ qubits carry at most $n$ classical bits; \ the $2^n$ "
                            r"amplitudes are real, \ but a measurement yields $n$ bits", 12.4, font_size=20,
                            color=LAM).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Two limits bind every quantum algorithm. <bookmark mark='a'/> The first is the polynomial "
            "method of Beals, Buhrman, Cleve, Mosca and de Wolf, from 1998. Each query multiplies amplitudes by "
            "something linear in one input bit, so after T queries every amplitude is a polynomial of degree at most "
            "T in the input bits, <bookmark mark='b'/> and the acceptance probability has degree at most two T. "
            "<bookmark mark='c'/> Parity flips with every bit, so approximating it needs degree N, and computing "
            "the parity of N bits needs N over two queries. Deutsch's trick from chapter five achieves exactly that. "
            "<bookmark mark='d'/> Without a promise, quantum queries save at most a polynomial factor. Exponential "
            "speedups, like Simon's and Shor's, need structure. <bookmark mark='e'/> The second is Holevo's bound: n "
            "qubits carry at most n classical bits."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])),
                      LaggedStart(*[FadeIn(VGroup(*c)) for c in tab.cells[1:]], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            self.play(Create(pax), FadeIn(pxt), FadeIn(pxl), Create(half), FadeIn(hl), FadeIn(pdots), FadeIn(pill))
            self.play(Create(pcurve), run_time=1.5)
            self.play(LaggedStart(*[FadeIn(m_) for m_ in xmarks], lag_ratio=0.2), FadeIn(pcap))
            vo.wait_until("d")
            self.play(FadeIn(tl))
            vo.wait_until("e")
            self.play(FadeIn(hol))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
