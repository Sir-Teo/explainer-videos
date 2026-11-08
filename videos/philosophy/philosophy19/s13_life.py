from __future__ import annotations

from videos.philosophy.philosophy19.common import *  # noqa: F403


def sci(x: float, digits: int = 1) -> str:
    """``x`` as TeX scientific notation, for use inside inline math."""
    e = int(np.floor(np.log10(abs(x))))
    m = x / 10 ** e
    return f"{m:.{digits}f}" + r" \times 10^{" + f"{e}" + "}"


class Life(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"What is life?", r"Can life be defined, \ with only one example?", lit=(1944, 1994),
                            part=PART)
        with self.voiceover("Chapter twelve. What is life?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.schrodinger()
        self.budget()
        self.matrix()
        self.one()

    def schrodinger(self):
        hc = history_card(1944, r"Erwin Schrödinger", r"\textit{What Is Life?} \ (Dublin lectures, \ 1943)",
                          width=6.4, color=HIST).to_corner(UL, buff=0.3)
        rows = stack([(r"order from order: \ heredity needs a stable molecular store", GENE),
                      (r"the gene as an \textit{aperiodic crystal}: \ a code-script in its arrangement", GENE),
                      (r"order from disorder? \ no: \ an organism feeds on `negative entropy'", ORG),
                      (r"read by Crick, \ Watson and Wilkins: \ the structure was found in 1953", OK)],
                     font_size=21, aligned_edge=LEFT, width=7.2).move_to([2.6, -0.2, 0])
        dna = VGroup()
        for i in range(14):
            y = 1.6 - i * 0.28
            a = 0.55 * np.sin(i * 0.65)
            dna.add(Dot([-4.8 + a, y, 0], radius=0.06, color=GENE), Dot([-4.8 - a, y, 0], radius=0.06, color=ORG),
                    Line([-4.8 + a, y, 0], [-4.8 - a, y, 0], color=GREY_C, stroke_width=1.5))
        dna.shift(DOWN * 0.6)
        with self.voiceover(
            "In 1943 the physicist Erwin Schrödinger gave public lectures in Dublin, published the next year as What "
            "Is Life? <bookmark mark='a'/>He asked how heredity could be so stable when molecular motion is so "
            "disordered, and answered that the hereditary material must be a stable molecule. "
            "<bookmark mark='b'/>He called it an aperiodic crystal, whose arrangement is a code-script for the "
            "organism. <bookmark mark='c'/>And he asked how organisms keep themselves ordered when the second law "
            "says disorder grows. His answer: an organism feeds on negative entropy, taking in order and giving back "
            "disorder. <bookmark mark='d'/>Francis Crick, James Watson and Maurice Wilkins all said the book had "
            "drawn them to biology; the aperiodic crystal turned out to be the double helix."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in dna], lag_ratio=0.02), FadeIn(rows[0]), run_time=2)
            for mk, r in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def budget(self):
        d = load("entropy")
        pr = d["params"]
        head = label(r"Negative entropy, \ counted", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        law = MathTex(r"dS", r"=", r"d_eS", r"+", r"d_iS", r",\qquad", r"d_iS \ge 0", font_size=40).next_to(
            head, DOWN, buff=0.35)
        law[2].set_color(GENE)
        law[4].set_color(BAD)
        law[6].set_color(BAD)
        notes = VGroup(label(r"exchanged with the outside", font_size=16, color=GENE).next_to(law[2], DOWN, buff=0.25),
                       label(r"produced inside", font_size=16, color=BAD).next_to(law[4], DOWN, buff=0.25))
        notes[0].shift(LEFT * 0.6)
        notes[1].shift(RIGHT * 0.6)
        body = Circle(radius=0.8, color=ORG, fill_opacity=0.2).move_to([-4.6, -1.3, 0])
        bl = label(r"a body, \ " + f"{pr['t_body']:.0f}" + r" K", font_size=16, color=ORG).move_to(body)
        food = Arrow(body.get_left() + LEFT * 1.4, body.get_left(), buff=0.05, color=GENE, stroke_width=3)
        fl = label(r"food", font_size=16, color=GENE).next_to(food, UP, buff=0.05)
        heat = Arrow(body.get_right(), body.get_right() + RIGHT * 1.4, buff=0.05, color=BAD, stroke_width=3)
        hl = label(f"{pr['power']:.0f}" + r" W of heat", font_size=16, color=BAD).next_to(heat, UP, buff=0.05)
        rows_b = stack([(r"heat leaves at " + f"{pr['t_body']:.0f}" + r" K: \ $" + f"{d['body_in']:.3f}" +
                         r"$ W/K", GREY_A),
                        (r"the room receives it at " + f"{pr['t_env']:.0f}" + r" K: \ $" + f"{d['body_out']:.3f}" +
                         r"$ W/K", GREY_A),
                        (r"net: \ the world gains $" + f"{d['body']:.4f}" + r"$ W/K \ while the body stays ordered",
                         BAD)], font_size=18, aligned_edge=LEFT, width=6.2).move_to([-3.0, -3.0, 0])
        sun = Circle(radius=0.45, color=GOAL, fill_opacity=0.5).move_to([1.6, -1.2, 0])
        earth = Circle(radius=0.35, color=GROUP, fill_opacity=0.5).move_to([4.2, -1.2, 0])
        rays = Arrow(sun.get_right(), earth.get_left(), buff=0.08, color=GOAL, stroke_width=3)
        back = VGroup(*[Arrow(earth.get_right(), earth.get_right() + np.array([1.0 * np.cos(a), 1.0 * np.sin(a), 0]),
                              buff=0.05, color=BAD, stroke_width=2, max_tip_length_to_length_ratio=0.2)
                        for a in (-0.7, -0.25, 0.25, 0.7)])
        rows_e = stack([(r"sunlight in, \ at $" + f"{pr['t_sun']:.0f}" + r"$ K: \ $" + sci(d["earth_in"]) +
                         r"$ W/K", GOAL),
                        (r"infrared out, \ at $" + f"{pr['t_earth']:.0f}" + r"$ K: \ $" + sci(d["earth_out"]) +
                         r"$ W/K", BAD),
                        (r"one visible photon in, \ about " + f"{d['photon_ratio']:.0f}" + r" infrared photons out",
                         WHITE),
                        (r"the Earth lives on low entropy, \ not on energy", OK)], font_size=18, aligned_edge=LEFT,
                       width=6.0).move_to([3.6, -3.0, 0])
        with self.voiceover(
            "Ilya Prigogine made Schrödinger's phrase precise. <bookmark mark='a'/>The entropy change of an open "
            "system has two parts: entropy exchanged with the outside, and entropy produced inside, which by the "
            "second law is never negative. A living thing can stay ordered only by exporting entropy faster than it "
            "makes it. <bookmark mark='b'/>The Reasoner counts. A resting body turns food into a hundred watts of "
            "heat. <bookmark mark='c'/>The heat leaves at body temperature, and the cooler room receives it, so the "
            "entropy of the world rises by about two hundredths of a watt per kelvin, every second the body is "
            "alive. <bookmark mark='d'/>The same holds for the planet. Sunlight arrives at the temperature of the "
            "Sun's surface, and the Earth radiates the same energy back at two hundred and fifty-five kelvin. "
            "<bookmark mark='e'/>For every visible photon that comes in, about twenty-three infrared photons go out. "
            "<bookmark mark='f'/>As Roger Penrose put it, the Earth does not live on the Sun's energy, which it gives "
            "back in full, but on its low entropy."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(law), FadeIn(notes))
            vo.wait_until("b")
            self.play(FadeIn(body), FadeIn(bl), GrowArrow(food), FadeIn(fl), GrowArrow(heat), FadeIn(hl))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in rows_b], lag_ratio=0.4))
            vo.wait_until("d")
            self.play(FadeIn(sun), FadeIn(earth), GrowArrow(rays), FadeIn(rows_e[0]), FadeIn(rows_e[1]))
            vo.wait_until("e")
            self.play(LaggedStart(*[GrowArrow(a) for a in back], lag_ratio=0.15), FadeIn(rows_e[2]))
            vo.wait_until("f")
            self.play(FadeIn(rows_e[3]))
        self.clear_scene()

    def matrix(self):
        d = load("lifedef")
        head = label(r"Five definitions, \ seven cases", font_size=30, color=CONN).to_edge(UP, buff=0.25)
        defs = d["defs"]
        cases = d["cases"]
        hd = [r""] + [r"\text{" + x + "}" for x in defs]
        rows = []
        for c in cases:
            row = [MathTex(r"\text{" + c + "}", font_size=22, color=GOAL if c in d["contested"] else OK)]
            for x in defs:
                ok = d["table"][c][x]
                row.append(MathTex(r"\checkmark" if ok else r"\times", font_size=26, color=OK if ok else BAD))
            rows.append(row)
        grid = ValueGrid(hd, rows, col_w=[2.6, 1.8, 1.8, 1.8, 1.8, 2.1], cell_h=0.52, font_size=20).move_to(
            [0, 0.3, 0])
        key = label(r"needs: \ reproduces $\{R\}$, \ metabolizes $\{M\}$, \ autopoietic $\{A\}$, \ Darwinian "
                    r"$\{R, H, E\}$, \ NASA $\{C, M, E\}$", font_size=16, color=GREY_A).next_to(grid, DOWN, buff=0.2)
        verdict = label(r"only the bacterium is alive on every definition; \ every other case is contested",
                        font_size=20, color=GOAL).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Suppose we try to define life. The Reasoner tabulates five definitions against seven cases, each "
            "definition a set of properties a case must have. <bookmark mark='a'/>The cases: a bacterium; a mule, "
            "which cannot breed; a virus, which has no metabolism of its own; a fire, which feeds, grows and "
            "spreads; a salt crystal, which seeds copies of itself; a Lenia glider, from the next chapter; and a "
            "self-copying program in Thomas Ray's Tierra. <bookmark mark='b'/>Reproduction counts fire and crystals "
            "as alive, and the mule as dead. <bookmark mark='c'/>Metabolism counts the fire. Autopoiesis, Humberto "
            "Maturana and Francisco Varela's self-producing, self-bounding system, counts the glider. "
            "<bookmark mark='d'/>Darwinian definitions count the virus and the program. NASA's working definition, "
            "from Gerald Joyce, a self-sustaining chemical system capable of Darwinian evolution, counts only the "
            "bacterium. <bookmark mark='e'/>Only the bacterium is alive on every definition. Every other case is "
            "contested."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(grid.cell[r][0]) for r in range(len(cases))], lag_ratio=0.15))
            for mk, cols in zip("bcd", ((1,), (2, 3), (4, 5))):
                vo.wait_until(mk)
                self.play(*[FadeIn(grid.cell[r][c]) for r in range(len(cases)) for c in cols])
            vo.wait_until("e")
            self.play(FadeIn(key), FadeIn(verdict), Create(grid.row_box(0, OK)))
        self.clear_scene()

    def one(self):
        head = label(r"The problem of one example", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Cleland \ (2012)", r"defining life now is like defining water before molecular chemistry: \ we need "
                                  r"a theory, \ not a definition", GENE),
            (r"$N = 1$", r"all known life shares one ancestry: \ we cannot tell the essential from the accidental",
             BAD),
            (r"Machery \ (2012)", r"stop worrying: \ each science has its own useful concept; \ none is `the' "
                                  r"definition", ORG),
            (r"cluster views", r"life as a family resemblance of metabolism, \ boundary, \ heredity and evolution",
             GROUP),
            (r"Bedau \ (1996)", r"life as \textit{supple adaptation}: \ open-ended evolution is the core, \ organisms "
                                r"derive from it", ALT),
            (r"the test", r"a second origin \ (on Mars, \ Enceladus, \ or in a computer) \ would decide", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.42, width=8.6, x_text=-2.6, label_size=21)
        with self.voiceover(
            "Carol Cleland draws a lesson from the failure of definitions. <bookmark mark='a'/>Defining life today, "
            "she argues, is like defining water before molecular chemistry: we would list wetness and transparency, "
            "and miss the point. What we need is a theory of life, not a definition. <bookmark mark='b'/>And we "
            "cannot have one yet, because all known life descends from a single ancestor. With one example, we "
            "cannot tell which of its features are essential and which are accidents of history. "
            "<bookmark mark='c'/>Edouard Machery recommends that we stop worrying: biochemists, ecologists and "
            "astrobiologists each have a useful concept, and none of them needs to be the definition. "
            "<bookmark mark='d'/>Cluster views treat life as a family resemblance of metabolism, boundary, heredity "
            "and evolution. <bookmark mark='e'/>Mark Bedau puts evolution at the centre: life is supple, open-ended "
            "adaptation, and organisms count as alive by belonging to such a process. <bookmark mark='f'/>The "
            "decisive test would be a second example: life found on Mars or Enceladus, or made in a computer, which "
            "is the next chapter."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
