from __future__ import annotations

from videos.philosophy.philosophy6.common import *  # noqa: F403

X0, L = -6.0, 12.0


def pos(a: int, b: int) -> float:
    """Where ω·a + b sits when ω² is squeezed into [0, 1): each copy of ω takes half the remaining room."""
    return (1 - 2.0 ** -a) + 2.0 ** -a * (1 - 2.0 ** -b)


def tick(a, b, y, h, color):
    x = X0 + L * pos(a, b)
    s = h * 2.0 ** -(a + b * 0.35)
    return Line([x, y - s / 2, 0], [x, y + s / 2, 0], color=color, stroke_width=max(1.0, 3.2 * 2.0 ** -(0.5 * a)))


class Ordinals(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"Counting past infinity", r"What comes after all the natural numbers?", lit=(1883,),
                            part=PART)
        with self.voiceover("Chapter nine. Counting past infinity."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.omega()
        self.ticks()
        self.arithmetic()
        self.epsilon()

    def omega(self):
        hc = history_card(1883, r"Georg Cantor, \textit{Grundlagen}", r"the transfinite numbers: \ counting goes on",
                          width=6.4, color=HIST).to_corner(UL, buff=0.35)
        seq = MathTex(r"0,\ 1,\ 2,\ 3,\ \dots,\ ", r"\omega", r",\ \omega+1,\ \omega+2,\ \dots,\ ", r"\omega\cdot 2",
                      r",\ \dots", font_size=44).move_to([0, 0.6, 0])
        seq[1].set_color(ORD)
        seq[3].set_color(ORD)
        defs = VGroup(MathTex(r"\omega = \{0, 1, 2, \dots\}", font_size=36, color=ORD),
                      MathTex(r"\omega + 1 = \omega \cup \{\omega\} = \{0, 1, 2, \dots, \omega\}", font_size=36),
                      label(r"an ordinal is the set of the ordinals before it: \ von Neumann again", font_size=24,
                            color=GREY_A)).arrange(DOWN, buff=0.3).next_to(seq, DOWN, buff=0.6)
        with self.voiceover(
            "Cantor discovered a second kind of infinite number while studying trigonometric series. "
            "<bookmark mark='a'/>Count zero, one, two, three. After all of them comes a first infinite number, "
            "omega. Then omega plus one, omega plus two, and after all of those, omega times two. "
            "<bookmark mark='b'/>With von Neumann's definition they are sets like the finite numbers. Omega is the "
            "set of all natural numbers. Omega plus one is omega together with omega itself. Each ordinal is the set "
            "of the ordinals before it, and every set of ordinals has a least member: they are well-ordered."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(seq), run_time=3)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in defs], lag_ratio=0.4))
        self.clear_scene()

    def ticks(self):
        head = label(r"All the ordinals below $\omega^2$, \ squeezed onto one line", font_size=30,
                     color=CONN).to_edge(UP, buff=0.5)
        axis = Line([X0, -0.2, 0], [X0 + L, -0.2, 0], color=GREY_D, stroke_width=1.5)
        first = VGroup(*[tick(0, b, -0.2, 1.4, SETC) for b in range(40)])
        rest = VGroup(*[tick(a, b, -0.2, 1.4, interpolate_color(ManimColor(SETC), ManimColor(ORD), min(a / 6, 1)))
                        for a in range(1, 12) for b in range(40)])
        lab = VGroup(MathTex("0", font_size=26).next_to([X0, -1.0, 0], DOWN, buff=0.1),
                     MathTex(r"\omega", font_size=30, color=ORD).next_to([X0 + L * pos(1, 0), -1.0, 0], DOWN, buff=0.1),
                     MathTex(r"\omega\cdot 2", font_size=26, color=ORD).next_to([X0 + L * pos(2, 0), -1.0, 0], DOWN,
                                                                               buff=0.1),
                     MathTex(r"\omega\cdot 3", font_size=22, color=ORD).next_to([X0 + L * pos(3, 0), -1.0, 0], DOWN,
                                                                               buff=0.1),
                     MathTex(r"\omega^2", font_size=30, color=CARD).next_to([X0 + L, -1.0, 0], DOWN, buff=0.1))
        end = Dot([X0 + L, -0.2, 0], color=CARD, radius=0.07)
        cap = label(r"each copy of $\omega$ is a run of ticks piling up against the next limit", font_size=24,
                    color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Here is a way to see them. <bookmark mark='a'/>Put zero at the left, and each next number halfway to "
            "the mark for omega: the ticks pile up, infinitely many, against a limit. <bookmark mark='b'/>Then omega, "
            "and after it a second, smaller copy of the same pile, up to omega times two. Then a third, smaller "
            "still. <bookmark mark='c'/>Infinitely many copies, shrinking, fill the line up to omega squared. Every "
            "ordinal below omega squared is one tick. <bookmark mark='d'/>Each tick has a next tick, but the limits, "
            "like omega and omega times two, have no tick just before them."
        ) as vo:
            self.play(FadeIn(head), Create(axis))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(t) for t in first], lag_ratio=0.03), FadeIn(lab[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(lab[1]), LaggedStart(*[Create(t) for t in rest[:80]], lag_ratio=0.01), FadeIn(lab[2:4]),
                      run_time=2.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(t) for t in rest[80:]], lag_ratio=0.002), FadeIn(end), FadeIn(lab[4]),
                      run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(cap))
        self.clear_scene()

    def arithmetic(self):
        d = load("ordinals")
        head = label(r"Ordinal arithmetic is not commutative", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        rows = VGroup(
            VGroup(MathTex(r"1 + \omega = \omega", font_size=40, color=GOAL),
                   label(r"one tick in front of a pile: \ still just a pile", font_size=24, color=GREY_A)).arrange(
                RIGHT, buff=0.5),
            VGroup(MathTex(r"\omega + 1 > \omega", font_size=40, color=GOAL),
                   label(r"a pile with a tick after it: \ a new last element", font_size=24, color=GREY_A)).arrange(
                RIGHT, buff=0.5),
            VGroup(MathTex(r"2 \cdot \omega = \omega", font_size=40, color=GOAL),
                   label(r"$\omega$ copies of two ticks", font_size=24, color=GREY_A)).arrange(RIGHT, buff=0.5),
            VGroup(MathTex(r"\omega \cdot 2 = \omega + \omega", font_size=40, color=GOAL),
                   label(r"two copies of $\omega$", font_size=24, color=GREY_A)).arrange(RIGHT, buff=0.5)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.1, 0])
        cnf = VGroup(label(r"Cantor normal form: \ every ordinal below $\varepsilon_0$ is", font_size=24),
                     MathTex(r"\omega^{\beta_1} c_1 + \omega^{\beta_2} c_2 + \dots + \omega^{\beta_k} c_k, \quad "
                             r"\beta_1 > \dots > \beta_k", font_size=32, color=ORD)).arrange(DOWN, buff=0.2).to_edge(
            DOWN, buff=0.45)
        chk = label(r"computed exactly by the Reasoner \ $\checkmark$", font_size=24, color=OK).next_to(rows, DOWN,
                                                                                                  buff=0.45)
        assert all(d["facts"].values())
        with self.voiceover(
            "Arithmetic on these numbers holds surprises. <bookmark mark='a'/>One plus omega is omega: put one tick "
            "in front of an infinite pile, and you still have just a pile, the same shape. <bookmark mark='b'/>But "
            "omega plus one is bigger than omega, because now the pile has a last element. <bookmark mark='c'/>Two "
            "times omega, omega copies of a pair, is omega again. Omega times two, two copies of omega, is omega "
            "plus omega. <bookmark mark='d'/>The Reasoner's new module computes with these exactly, writing each "
            "ordinal below epsilon zero in Cantor's normal form, a finite sum of powers of omega."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", rows[:3]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            self.play(FadeIn(rows[3], shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(cnf), FadeIn(chk))
        self.clear_scene()

    def epsilon(self):
        d = load("ordinals")
        ladder = VGroup(*[MathTex(t, font_size=30, color=interpolate_color(ManimColor(SETC), ManimColor(CARD), i / 16))
                          for i, t in enumerate(d["ladder"])])
        ladder.arrange_in_grid(3, 6, buff=(0.7, 0.55)).move_to([0, 1.0, 0])
        if ladder.width > 13.0:
            ladder.width = 13.0
        lts = label(r"in increasing order, \ each checked by the Reasoner's comparison", font_size=22,
                    color=GREY_A).next_to(ladder, DOWN, buff=0.35)
        eps = MathTex(r"\varepsilon_0 = \omega^{\omega^{\omega^{\cdot^{\cdot^{\cdot}}}}} \quad\text{the least } "
                      r"\varepsilon \text{ with } \omega^\varepsilon = \varepsilon", font_size=36, color=CARD).next_to(
            lts, DOWN, buff=0.55)
        ind = VGroup(label(r"transfinite induction:", font_size=26, color=GOAL),
                     label(r"if a property passes from all ordinals below $\alpha$ to $\alpha$, \ it holds for every "
                           r"ordinal", font_size=24)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Climb further. <bookmark mark='a'/>Omega squared, omega cubed, omega to the omega, omega to the omega to "
            "the omega. The Reasoner puts these in order and checks every comparison. <bookmark mark='b'/>The limit "
            "of the tower, omega to the omega to the omega forever, is called epsilon zero: the first ordinal that "
            "omega to its power cannot exceed. It will matter in a moment, and again in Part 7, as the measure of "
            "how strong arithmetic is. <bookmark mark='c'/>Ordinals support a powerful method of proof: transfinite "
            "induction. If a property passes from all the ordinals below any given one to that one, it holds for "
            "all of them, because a least counterexample cannot exist."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in ladder], lag_ratio=0.12), FadeIn(lts),
                      run_time=3.5)
            vo.wait_until("b")
            self.play(Write(eps))
            vo.wait_until("c")
            self.play(FadeIn(ind))
        self.clear_scene()
