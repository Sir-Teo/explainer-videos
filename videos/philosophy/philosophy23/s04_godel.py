from __future__ import annotations

from videos.philosophy.philosophy23.common import *  # noqa: F403


class Godel(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"Gödel's proof, \ checked", r"What happens when a machine reads the proof?",
                            lit=(1987, 2016), part=PART)
        with self.voiceover("Chapter three. Gödel's proof, checked."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.axioms()
        self.model()
        self.search()
        self.brick()

    def axioms(self):
        head = label(r"Gödel's ontological proof \ (1970 notes; \ published 1987)", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        ax = [
            (r"A1", r"P(\lnot\varphi) \leftrightarrow \lnot P(\varphi)", r"of a property and its negation, \ exactly "
                                                                         r"one is positive"),
            (r"A2", r"P(\varphi) \land \Box \forall x(\varphi x \to \psi x) \to P(\psi)", r"what a positive property "
                                                                                       r"necessarily entails is positive"),
            (r"D1", r"G(x) \leftrightarrow \forall \varphi\,(P(\varphi) \to \varphi x)", r"God-like: \ having every "
                                                                                       r"positive property"),
            (r"A3", r"P(G)", r"being God-like is positive"),
            (r"D2", r"\varphi \text{ ess } x \leftrightarrow \forall \psi\,(\psi x \to \Box \forall y(\varphi y \to "
                    r"\psi y))", r"an essence entails every property of $x$"),
            (r"D3", r"NE(x) \leftrightarrow \forall \varphi\,(\varphi \text{ ess } x \to \Box \exists y\, \varphi y)",
             r"necessary existence: \ every essence is necessarily exemplified"),
            (r"A5", r"P(NE)", r"necessary existence is positive"),
        ]
        rows = VGroup()
        for i, (k, f, gl) in enumerate(ax):
            y = 2.2 - 0.66 * i
            a = label(k, font_size=21, color=DIV).move_to([-6.3, y, 0])
            b = MathTex(f, font_size=26, color=ABS)
            if b.width > 6.6:
                b.width = 6.6
            b.move_to([-5.8 + b.width / 2, y, 0])
            c = wrapped_label(gl, 4.6, 17, GREY_A)
            c.move_to([1.9 + c.width / 2, y, 0])
            rows.add(VGroup(a, b, c))
        concl = MathTex(r"\therefore\ \Box\, \exists x\, G(x)", font_size=36, color=DIV).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Kurt Gödel worked on an ontological proof for decades; a two-page note of 1970 was published only in "
            "1987, after his death. It is a proof in higher-order modal logic, about properties. "
            "<bookmark mark='a'/>The undefined notion is a positive property. Of a property and its negation, exactly "
            "one is positive. <bookmark mark='b'/>Whatever a positive property necessarily entails is positive. "
            "<bookmark mark='c'/>Something is God-like if it has every positive property, and being God-like is "
            "itself positive. <bookmark mark='d'/>An essence of a thing is a property that necessarily entails every "
            "property the thing has. A thing exists necessarily if every essence of it is necessarily exemplified; "
            "and necessary existence is positive. <bookmark mark='e'/>From these Gödel derived that, necessarily, a "
            "God-like being exists."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]), FadeIn(rows[5]), FadeIn(rows[6]))
            vo.wait_until("e")
            self.play(Write(concl))
        self.clear_scene()

    def model(self):
        head = label(r"A finite model of higher-order modal logic", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        cells = VGroup()
        for w in range(2):
            for d in range(2):
                sq = Square(side_length=1.1, color=GREY_B, stroke_width=2).move_to([-4.6 + 1.2 * d, 1.0 - 1.2 * w, 0])
                t = MathTex(rf"(w_{w}, d_{d})", font_size=20).move_to(sq)
                cells.add(VGroup(sq, t))
        wl = VGroup(*[label(rf"world $w_{w}$", font_size=18, color=ARG).next_to(cells[2 * w], LEFT, buff=0.15)
                      for w in range(2)])
        dl = VGroup(*[label(rf"individual $d_{d}$", font_size=16, color=HUM).next_to(cells[d], UP, buff=0.12)
                      for d in range(2)])
        phi = VGroup(cells[0].copy(), cells[3].copy()).set_color(DIV)
        rows = stack([(r"a property: \ any set of (world, individual) cells: \ $2^4 = 16$ of them", WHITE),
                      (r"positiveness $P$: \ a set of properties; \ A1 forces one of each complementary pair: \ "
                       r"$2^8 = 256$ choices", ABS),
                      (r"$\Box$: \ at every world \ (S5); \ $\exists x$: \ some individual", ARG),
                      (r"the Reasoner tests every axiom on every choice of $P$, \ for every small model", OK)],
                     font_size=21, aligned_edge=LEFT, width=7.6).move_to([2.6, 0.2, 0])
        with self.voiceover(
            "Can the Reasoner check a proof in higher-order logic? On finite models it can. <bookmark mark='a'/>Take "
            "two worlds and two individuals: four cells, each an individual at a world. A property is any set of "
            "cells, which says which individuals have it at which worlds; there are sixteen. "
            "<bookmark mark='b'/>Positiveness is a set of properties. Axiom one forces it to contain exactly one "
            "property from each complementary pair, so there are two hundred and fifty-six candidates. "
            "<bookmark mark='c'/>Necessity is truth at every world; the quantifier ranges over the individuals. "
            "<bookmark mark='d'/>Then the Reasoner tests every axiom, on every candidate, for every small model: "
            "one world or several, one individual or several."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells), FadeIn(wl), FadeIn(dl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(phi))
            for mk, r in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def search(self):
        d = load("godel")
        head = label(r"Every model, \ searched", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"\text{worlds}", r"\text{individuals}", r"\text{candidates}", r"\text{Gödel's axioms}",
              r"\text{Scott's axioms}", r"\text{one God}"]
        rows = []
        for g, s in zip(d["godel"], d["scott"]):
            rows.append([MathTex(str(g["worlds"]), font_size=21), MathTex(str(g["individuals"]), font_size=21),
                         MathTex(str(g["candidates"]), font_size=21),
                         MathTex(str(g["models"]), font_size=21, color=BAD),
                         MathTex(str(s["models"]), font_size=21, color=OK if s["models"] else GREY_B),
                         MathTex(str(s["one_god"]) if s["models"] else r"\text{--}", font_size=21, color=DIV)])
        grid = ValueGrid(hd, rows, col_w=[1.3, 1.6, 1.7, 2.1, 2.1, 1.4], cell_h=0.42, font_size=18).move_to(
            [-1.95, -0.25, 0])
        side = stack([(r"Gödel's own axioms: \ no model at all", BAD),
                      (r"his essence lacks `$\varphi x$': \ the empty property is an essence of everything, \ so "
                       r"nothing has necessary existence", GREY_A),
                      (r"Scott's repair: \ models exist, \ each with one God", OK),
                      (r"but only with \textit{one world}", DIV)], font_size=20, aligned_edge=LEFT, width=3.3).move_to(
            [5.3, -0.2, 0])
        with self.voiceover(
            "Here is the search. <bookmark mark='a'/>Gödel's axioms, exactly as in his note: across every model with "
            "up to four cells, not a single one satisfies them. They are inconsistent. <bookmark mark='b'/>The reason "
            "is a missing clause. Gödel's definition of essence does not require the thing to have the property, so "
            "the empty property counts as an essence of everything; nothing exemplifies it, so nothing exists "
            "necessarily; and then necessary existence is the empty property, which cannot be positive. "
            "Christoph Benzmüller and Bruno Woltzenlogel Paleo found this in 2016 with automated theorem provers. "
            "<bookmark mark='c'/>Dana Scott's version adds the clause. Now models exist, and in each there is "
            "exactly one God-like being. <bookmark mark='d'/>But look at the worlds column. Every model the Reasoner finds for Scott's "
            "axioms has a single world."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule),
                      *[FadeIn(grid.cell[r][c]) for r in range(len(rows)) for c in range(3)])
            vo.wait_until("a")
            self.play(*[FadeIn(grid.cell[r][3]) for r in range(len(rows))], FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(*[FadeIn(grid.cell[r][c]) for r in range(len(rows)) for c in (4, 5)], FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), *[Indicate(grid.cell[r][0], color=DIV) for r in range(len(rows))
                                         if d["scott"][r]["models"]])
        self.clear_scene()

    def brick(self):
        w = wall(upto=23, current=23).scale(0.44).to_edge(LEFT, buff=0.3).shift(DOWN * 0.3)
        card = wall_card(23, width=6.2, font_size=22).to_edge(RIGHT, buff=0.3)
        rows = card[1][1]
        f = MathTex(r"\forall p\,(p \to \Box p)", font_size=40, color=BAD).next_to(card, DOWN, buff=0.3)
        fl = label(r"modal collapse \ (Sobel, \ 1987)", font_size=18, color=GREY_A).next_to(f, DOWN, buff=0.1)
        with self.voiceover(
            "A single world means that whatever is true is necessary. That is modal collapse, and Jordan Howard Sobel "
            "proved it from Scott's axioms in 1987: this is the twenty-third brick in the Wall. "
            "<bookmark mark='a'/>The dream: a proof of God from the mere possibility of perfection. "
            "<bookmark mark='b'/>The wall: the axioms that deliver God also deliver that every truth is necessary. "
            "Nothing could have been otherwise: not your birth, not this sentence. <bookmark mark='c'/>What it "
            "forces: weaken the axioms, as Anderson and Fitting did, and lose some of the proof's power; or accept "
            "that everything true is necessary, which almost no one, theist or atheist, will do."
        ) as vo:
            self.play(FadeIn(w), Write(f), FadeIn(fl))
            vo.wait_until("a")
            self.play(Indicate(w.brick[23], color=P.CONCL, scale_factor=1.08), FadeIn(card[0]), FadeIn(card[1][0]),
                      FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
