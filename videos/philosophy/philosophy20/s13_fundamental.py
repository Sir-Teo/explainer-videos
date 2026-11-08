from __future__ import annotations

from videos.philosophy.philosophy20.common import *  # noqa: F403


class Fundamental(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"Is there a bottom level?", r"Must every chain of grounds come to an end?",
                            lit=(2003, 2010), part=PART)
        with self.voiceover("Chapter twelve. Is there a bottom level?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.gunk()
        self.options()
        self.monism()

    def gunk(self):
        d = load("gunk")
        head = label(r"Gunk: \ parts all the way down", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        L = d["levels"]
        bars = VGroup()
        x0, w = -6.4, 6.0
        for k, lev in enumerate(L):
            y = 2.0 - 0.62 * k
            row = VGroup()
            for i, (a, b) in enumerate(lev):
                r = Rectangle(width=w * (b - a) * 0.96, height=0.34, stroke_width=1,
                              stroke_color=GREY_B, fill_color=interpolate_color(ManimColor(PARTC), ManimColor(ABS),
                                                                                k / max(1, len(L) - 1)),
                              fill_opacity=0.7)
                r.move_to([x0 + w * (a + b) / 2, y, 0])
                row.add(r)
            bars.add(row)
        labels = VGroup(*[label(r"depth " + f"{k}" + r": \ " + f"{d['atoms_at_depth'][k]}" +
                                (r" atom" if d['atoms_at_depth'][k] == 1 else r" atoms"), font_size=15,
                                color=GREY_A).move_to([1.0, 2.0 - 0.62 * k, 0]) for k in range(len(L))])
        rows = stack([(r"stop at any depth, \ and the smallest pieces are atoms", WHITE),
                      (r"but each has a proper part one level down: \ the limit has no atoms", GOAL),
                      (r"every finite model of mereology is atomic \ (chapter 6); \ gunk needs infinity", UNIV),
                      (r"Whitehead; \ Sider \ (1993): \ gunk is at least possible, \ so atomism is not necessary", ABS)],
                     font_size=19, aligned_edge=LEFT, width=4.6).move_to([4.4, 0.4, 0])
        with self.voiceover(
            "Is there a bottom level of reality, made of things with no parts? <bookmark mark='a'/>Picture a stick, "
            "and divide it in half, and each half in half again. <bookmark mark='b'/>Stop at any depth and the "
            "smallest pieces are atoms of that stage: one, two, four, up to sixty-four. <bookmark mark='c'/>But each "
            "piece has a proper part one level further down, so in the limit there are no atoms at all. "
            "Philosophers call such stuff gunk. <bookmark mark='d'/>Chapter six showed why: every finite model of "
            "classical mereology has atoms, so gunk needs infinitely many parts. <bookmark mark='e'/>Alfred North "
            "Whitehead built a theory of space from gunky regions, and Ted Sider argued that gunk is at least "
            "possible, so that atomism, if true, is not necessary."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bars[0]), FadeIn(labels[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(b, l)) for b, l in zip(bars[1:], labels[1:])], lag_ratio=0.3),
                      FadeIn(rows[0]), run_time=2.5)
            for mk, r in zip("cde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def options(self):
        head = label(r"Four shapes for reality", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        shapes = VGroup()
        titles = [(r"well-founded", OK), (r"infinite descent", ABS), (r"no top \ (junky)", WHOLE),
                  (r"a single top", UNIV)]
        for k, (t, col) in enumerate(titles):
            cx = -5.1 + 3.4 * k
            g = VGroup()
            if k == 0:
                for i in range(4):
                    g.add(Dot([cx - 0.75 + 0.5 * i, -1.6, 0], radius=0.08, color=OK))
                for j in range(3):
                    g.add(Line([cx - 0.75 + 0.5 * j, -1.6, 0], [cx - 0.5 + 0.5 * j, -0.6, 0], color=GREY_B))
                    g.add(Line([cx - 0.25 + 0.5 * j, -1.6, 0], [cx - 0.5 + 0.5 * j, -0.6, 0], color=GREY_B))
                g.add(label(r"a bottom of fundamental facts", font_size=14, color=GREY_A).move_to([cx, -2.1, 0]))
            elif k == 1:
                for i in range(6):
                    g.add(Dot([cx, 0.6 - 0.45 * i, 0], radius=0.07 * (1 - i / 8), color=ABS))
                g.add(label(r"$\vdots$", font_size=28, color=ABS).move_to([cx, -2.1, 0]))
            elif k == 2:
                for i in range(6):
                    g.add(Dot([cx, -1.6 + 0.45 * i, 0], radius=0.07, color=WHOLE))
                g.add(label(r"$\vdots$", font_size=28, color=WHOLE).move_to([cx, 1.2, 0]))
            else:
                g.add(Circle(radius=0.5, color=UNIV, fill_opacity=0.3).move_to([cx, 0.6, 0]))
                g.add(label(r"the cosmos", font_size=15, color=UNIV).move_to([cx, 0.6, 0]))
                for i in range(4):
                    g.add(Line([cx, 0.1, 0], [cx - 0.75 + 0.5 * i, -1.2, 0], color=GREY_B))
                    g.add(Dot([cx - 0.75 + 0.5 * i, -1.2, 0], radius=0.07, color=GREY_A))
                g.add(label(r"parts are derivative", font_size=14, color=GREY_A).move_to([cx, -2.1, 0]))
            tl = label(t, font_size=19, color=col).move_to([cx, 1.9, 0])
            shapes.add(VGroup(tl, g))
        rows = stack([(r"Schaffer \ (2003): \ `Is There a Fundamental Level?' \ the evidence of physics is open", GOAL),
                      (r"metaphysical infinitism \ (Bohn; \ Morganti): \ grounding without a bottom", ABS)],
                     font_size=19, width=12.4).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "There are four shapes reality might take. <bookmark mark='a'/>Well-founded: every chain of grounds or "
            "parts ends in a bottom of fundamental facts, the standard view. <bookmark mark='b'/>Infinite descent: "
            "every level rests on a lower one, forever, as with gunk. <bookmark mark='c'/>No top: everything is part "
            "of something bigger, which Einar Bohn calls junk. <bookmark mark='d'/>Or a single top on which everything "
            "else depends. <bookmark mark='e'/>Jonathan Schaffer asked whether physics gives any evidence of a "
            "fundamental level, and found it open: the history of physics is a history of finding new levels. "
            "<bookmark mark='f'/>Metaphysical infinitists accept grounding without a bottom."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcd", shapes):
                vo.wait_until(mk)
                self.play(FadeIn(s))
            for mk, r in zip("ef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def monism(self):
        head = label(r"Priority monism", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Schaffer \ (2010)", r"`Monism: \ the Priority of the Whole': \ there are many things, \ but only one "
                                   r"is fundamental, \ the cosmos", UNIV),
            (r"existence monism", r"Horgan and Potrč: \ there is only one thing at all; \ `blobjectivism'", BAD),
            (r"the argument", r"quantum entanglement: \ the state of the whole is not fixed by the states of its "
                              r"parts \ (Part 26)", GOAL),
            (r"against it", r"common sense, \ and the explanatory priority of particles in physics", NOM),
            (r"Spinoza returns", r"one substance, \ many modes \ (Part 10), \ rebuilt with grounding", HIST),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.8, x_text=-2.4, label_size=21)
        with self.voiceover(
            "The last shape has a modern defender. <bookmark mark='a'/>Jonathan Schaffer's priority monism: there "
            "are many things, but only one is fundamental, the cosmos as a whole, and its parts depend on it. "
            "<bookmark mark='b'/>Terry Horgan and Matjaž Potrč go further, to existence monism: there is only one "
            "thing at all, which they call the blobject. <bookmark mark='c'/>Schaffer's main argument is quantum "
            "entanglement: the state of an entangled whole is not fixed by the states of its parts, as Part 26 will "
            "show. <bookmark mark='d'/>Against it stand common sense and the explanatory priority physics seems to "
            "give to particles. <bookmark mark='e'/>Either way, Spinoza's one substance with many modes, from Part 10, "
            "has returned, rebuilt with the tools of grounding."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
