from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs25.common import (fit_right, BG, CODE, CTRL, DATA, HEAD, LAM, NO, PART, YES, mono)


def life_step(cells):
    from collections import Counter
    cnt = Counter((x + dx, y + dy) for x, y in cells for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy)
    return {p for p, k in cnt.items() if k == 3 or (k == 2 and p in cells)}


class Wild(VoiceoverScene):
    def construct(self):
        self.card()
        self.accidents()
        self.physics()

    def card(self):
        card = chapter_card(14, r"Undecidability in the wild", r"Where do working programmers meet it?",
                            lit=(2003, 2019), extra=((2003, r"C++ templates"), (2017, r"Java generics"),
                                                    (2019, r"Magic: the Gathering")), part=PART)
        with self.voiceover("Chapter fourteen. Undecidability in the wild."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def accidents(self):
        head = label(r"Accidentally Turing complete", font_size=34).to_edge(UP, buff=0.3)
        items = [
            (r"C++ templates", r"Veldhuizen \ (2003): \ type-level programs; \\ compilers cap the depth \ "
                               r"(\texttt{-ftemplate-depth})", CODE),
            (r"Java generics", r"Grigore \ (2017): \ subtyping is undecidable; \\ no checker can always "
                               r"answer", DATA),
            (r"TypeScript types", r"conditional and recursive types: \\ the checker gives up at a depth limit",
             LAM),
            (r"Magic: the Gathering", r"Churchill, \ Biderman, \ Herrick \ (2019): \\ who wins a given position "
                                      r"is undecidable", HEAD),
            (r"x86 \texttt{mov}", 'Dolan (2013): move operations \\\\ with a repeating control-flow convention', CTRL),
            (r"Conway's Life", r"a Turing machine built of gliders \\ (Rendell, \ 2000)", YES),
        ]
        cards = VGroup()
        for name, desc, col in items:
            box_ = RoundedRectangle(width=4.1, height=1.55, corner_radius=0.12, stroke_color=col, stroke_width=2,
                                    fill_color=BG, fill_opacity=1)
            t = label(name, font_size=22, color=col).move_to(box_.get_top() + DOWN * 0.3)
            d = label(desc, font_size=17, color=GREY_A).next_to(t, DOWN, buff=0.12)
            if d.width > 3.9:
                d.width = 3.9
            cards.add(VGroup(box_, t, d))
        cards.arrange_in_grid(rows=2, cols=3, buff=(0.25, 0.3)).next_to(head, DOWN, buff=0.4)
        glider = {(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)}
        gens = [glider]
        for _ in range(4):
            gens.append(life_step(gens[-1]))
        frames = VGroup()
        for gi, g in enumerate(gens):
            fr = VGroup(*[Square(side_length=0.16, stroke_color=GREY_D, stroke_width=0.5,
                                 fill_color=YES if (x, y) in g else BG, fill_opacity=1)
                          .move_to([x * 0.16, -y * 0.16, 0]) for x in range(5) for y in range(5)])
            frames.add(fr)
        frames.arrange(RIGHT, buff=0.18).next_to(cards, DOWN, buff=0.3)
        fl = label(r"a glider: \ four generations later, \ the same shape, \ one cell down and right", font_size=17,
                   color=GREY_A).next_to(frames, DOWN, buff=0.1)
        note_ = label('ideal unbounded resources; finite implementation limits change the decision problem', font_size=20, color=NO).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Universality can appear in unexpected rule systems under IDEAL UNBOUNDED resources. <bookmark mark='a'/> C++ template metaprograms encode computation; real compilers impose depth and memory limits. <bookmark mark='b'/> Grigore's Java-generics result concerns the formal unbounded subtyping problem. Recursive type-level systems likewise differ from finite implementations with cutoffs. <bookmark mark='c'/> The Magic construction uses a precise idealized game model; finite hardware limits are not part of its universality theorem. <bookmark mark='d'/> Dolan's move-instruction construction requires a repeating control-flow convention as well as unbounded storage. A finite straight-line list of moves alone is not universal. <bookmark mark='e'/> Life uses an unbounded grid; the displayed finite glider merely illustrates local dynamics. <bookmark mark='f'/> Choose restrictions for a particular decision problem. Being less than Turing complete by itself does not prove all semantic questions decidable."
        ) as vo:
            self.play(FadeIn(head))
            for mk, k in zip("abcde", [[0], [1, 2], [3], [4], [5]]):
                vo.wait_until(mk)
                self.play(*[FadeIn(cards[i], shift=UP * 0.1) for i in k])
                if mk == "e":
                    self.play(LaggedStart(*[FadeIn(f_) for f_ in frames], lag_ratio=0.3), FadeIn(fl))
            vo.wait_until("f")
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    def physics(self):
        head = label(r"Even physics", font_size=34).to_edge(UP, buff=0.35)
        lattice = VGroup(*[Dot([x * 0.5, y * 0.5, 0], radius=0.07, color=DATA) for x in range(-4, 5)
                           for y in range(-3, 4)]).shift(LEFT * 4.4 + DOWN * 0.3)
        bonds = VGroup(*[Line([x * 0.5, y * 0.5, 0], [(x + 1) * 0.5, y * 0.5, 0], color=GREY_D, stroke_width=1.2)
                         for x in range(-4, 4) for y in range(-3, 4)],
                       *[Line([x * 0.5, y * 0.5, 0], [x * 0.5, (y + 1) * 0.5, 0], color=GREY_D, stroke_width=1.2)
                         for x in range(-4, 5) for y in range(-3, 3)]).shift(LEFT * 4.4 + DOWN * 0.3)
        lines = VGroup(
            label(r"a material, \ modelled as particles on a grid, \\ each interacting with its neighbours",
                  font_size=21, color=WHITE),
            label(r"the \textbf{spectral gap}: \ the energy needed to leave \\ the ground state, \ as the grid grows",
                  font_size=21, color=DATA),
            label('gap structure influences phases; \\\\ this is not a general finite-material conductor test',
                  font_size=21, color=GREY_A),
            label('2-D translation-invariant nearest-neighbor families; \\\\ fixed local dimension; robust thermodynamic promise', font_size=21, color=NO),
            label(r"the ground state tiles the plane \ (Robinson's tiles, \ chapter 6) \\ and runs a Turing machine "
                  r"in each tile", font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(bonds, RIGHT, buff=0.6)
        fit_right(lines)
        with self.voiceover(
            "The spectral-gap theorem has a precise thermodynamic scope. <bookmark mark='a'/> Consider a computably specified family of two-dimensional translation-invariant nearest-neighbor Hamiltonians with fixed local dimension. <bookmark mark='b'/> Ask about the spectral gap in the growing-lattice limit. <bookmark mark='c'/> The promise separates robust gapped and gapless cases; gap structure influences phases, but is not a universal finite-material conductor test. <bookmark mark='d'/> Cubitt, Perez-Garcia and Wolf proved this promised family problem undecidable. It is not a claim that a particular finite Hamiltonian's eigenvalues cannot be approximated. <bookmark mark='e'/> Their construction combines aperiodic forcing and computation so that halting controls the limiting gap. Finite experimental evidence and the ideal limit are different questions."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bonds), FadeIn(lattice))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
