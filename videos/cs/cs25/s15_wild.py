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
            (r"x86 \texttt{mov}", r"Dolan \ (2013): \ \texttt{mov} alone is \\ Turing complete", CTRL),
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
        note_ = label(r"a type checker, \ a build tool, \ a game engine: \ give it enough power \ and some question "
                      r"about it becomes undecidable", font_size=20, color=NO).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Programmers meet undecidability by accident. <bookmark mark='a'/> C++ templates were meant for generic "
            "containers. In 2003 Todd Veldhuizen showed they form a complete programming language running inside "
            "the compiler, which is why compilers stop at a fixed template depth. <bookmark mark='b'/> In 2017 Radu "
            "Grigore proved that subtyping with Java generics is undecidable: no compiler can always tell whether "
            "one type fits another. TypeScript's type system can run any program too, and its checker gives up at a "
            "depth limit. <bookmark mark='c'/> In 2019 Alex Churchill, Stella Biderman and Austin Herrick built a "
            "Turing machine out of the cards of Magic: the Gathering, so deciding who wins a given position is "
            "undecidable. <bookmark mark='d'/> Stephen Dolan showed that the x86 move instruction, alone, is Turing "
            "complete. <bookmark mark='e'/> And Conway's Game of Life, which Part 1 met, runs Turing machines made of "
            "gliders, like this one, walking diagonally across the grid. <bookmark mark='f'/> The lesson: give any "
            "configuration language, type system or rule set enough power, and some question about it becomes "
            "undecidable. Good designs decide on purpose where to stop."
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
            label(r"gapped or gapless decides how the material behaves \\ (insulator or conductor, \ phases)",
                  font_size=21, color=GREY_A),
            label(r"Cubitt, \ P\'erez-Garc\'ia and Wolf \ (\textit{Nature}, 2015): \\ for 2-D lattices, \ "
                  r"\textbf{undecidable}", font_size=21, color=NO),
            label(r"the ground state tiles the plane \ (Robinson's tiles, \ chapter 6) \\ and runs a Turing machine "
                  r"in each tile", font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(bonds, RIGHT, buff=0.6)
        fit_right(lines)
        with self.voiceover(
            "Undecidability reaches physics too. <bookmark mark='a'/> Model a material as particles on a grid, "
            "each interacting only with its neighbours by the same local rule. <bookmark mark='b'/> Its spectral "
            "gap is the energy it takes to lift the system out of its lowest state, in the limit of a large grid. "
            "<bookmark mark='c'/> Whether there is a gap decides much of how the material behaves. <bookmark "
            "mark='d'/> In 2015 Toby Cubitt, David Pérez-García and Michael Wolf proved that, for two-dimensional "
            "lattices, whether a gap exists is undecidable. <bookmark mark='e'/> Their construction is this part in "
            "miniature: the ground state is built from Robinson's aperiodic tiles, each tile running a Turing "
            "machine, and whether the gap closes depends on whether the machine halts."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bonds), FadeIn(lattice))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
