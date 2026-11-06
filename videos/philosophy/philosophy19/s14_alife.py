from __future__ import annotations

from videos.philosophy.philosophy19.common import *  # noqa: F403


class Alife(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"Artificial life", r"Can a pattern in a computer be alive?", lit=(1966, 2019),
                            part=PART)
        with self.voiceover("Chapter thirteen. Artificial life."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.neumann()
        self.conway()
        self.lenia_rule()
        self.lenia_movie()
        self.strong()

    def neumann(self):
        hc = history_card(1966, r"John von Neumann \ (ed. Burks)", r"\textit{Theory of Self-Reproducing Automata}",
                          width=7.0, color=HIST).to_corner(UL, buff=0.3)

        def machine(center, kids=True, tape_label=r"\Phi(A + B + C)"):
            g = VGroup()
            for i, (n, c) in enumerate(((r"A", ORG), (r"B", GENE), (r"C", GROUP))):
                box = RoundedRectangle(width=0.9, height=0.7, corner_radius=0.1, color=c, stroke_width=3)
                box.move_to(np.array(center) + np.array([(i - 1) * 1.05, 0.35, 0]))
                g.add(VGroup(box, MathTex(n, font_size=28, color=c).move_to(box)))
            tape = Rectangle(width=3.0, height=0.36, color=GOAL, stroke_width=2.5).move_to(
                np.array(center) + DOWN * 0.45)
            g.add(VGroup(tape, MathTex(tape_label, font_size=20, color=GOAL).move_to(tape)))
            return g

        parent = machine([-3.8, -0.4, 0])
        child = machine([2.2, -0.4, 0])
        a1 = Arrow([-2.1, 0.0, 0], [0.5, 0.0, 0], buff=0.1, color=ORG, stroke_width=3)
        l1 = label(r"$A$ builds from the tape", font_size=16, color=ORG).next_to(a1, UP, buff=0.05)
        a2 = Arrow([-2.1, -0.85, 0], [0.5, -0.85, 0], buff=0.1, color=GENE, stroke_width=3)
        l2 = label(r"$B$ copies the tape", font_size=16, color=GENE).next_to(a2, DOWN, buff=0.05)
        key = label(r"$A$ constructor, \ $B$ copier, \ $C$ controller, \ $\Phi$ a description", font_size=17,
                    color=GREY_A).next_to(VGroup(parent, child), UP, buff=0.5)
        rows = stack([(r"the tape is used twice: \ \textit{interpreted} \ to build, \ \textit{copied} \ to inherit",
                       GOAL),
                      (r"lectures of 1948--49: \ the logic of DNA's double use, \ before DNA's structure was known",
                       GENE),
                      (r"mutations to $\Phi$ are inherited: \ the design can evolve", ALT),
                      (r"realized in a cellular automaton with 29 states per cell", GREY_A)], font_size=19,
                     aligned_edge=LEFT, width=9.0).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Artificial life begins with John von Neumann, who asked in the late 1940s what logical organization a "
            "machine would need to build a copy of itself. <bookmark mark='a'/>His answer has three parts: a "
            "universal constructor A, which builds whatever a description tells it to; a copier B, which duplicates "
            "any description; and a controller C. Give the machine a tape describing A, B and C. "
            "<bookmark mark='b'/>A reads the tape and builds a new machine. <bookmark mark='c'/>B copies the tape and "
            "hands the copy to the offspring. <bookmark mark='d'/>The trick is that the description is used twice: "
            "once interpreted, as instructions, and once copied, uninterpreted, as inheritance. "
            "<bookmark mark='e'/>This is exactly how DNA is used, by transcription and by replication, and von "
            "Neumann worked it out years before the double helix. <bookmark mark='f'/>Because a change to the tape "
            "is copied along with the rest, the design can evolve. <bookmark mark='g'/>Arthur Burks completed and "
            "published the work in 1966, realized in a grid of cells with twenty-nine states each."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(parent), FadeIn(key))
            vo.wait_until("b")
            self.play(GrowArrow(a1), FadeIn(l1), FadeIn(VGroup(*child[:3])))
            vo.wait_until("c")
            self.play(GrowArrow(a2), FadeIn(l2), FadeIn(child[3]))
            for mk, r in zip("defg", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def conway(self):
        d = load("conway")
        hc = history_card(1970, r"John Horton Conway", r"the Game of Life \ (Gardner, \ \textit{Scientific American})",
                          width=7.2, color=HIST).to_corner(UL, buff=0.3)
        rule = label(r"a live cell survives with 2 or 3 live neighbours; \ a dead cell is born with exactly 3",
                     font_size=20, color=WHITE).next_to(hc, DOWN, buff=0.3).to_edge(LEFT, buff=0.5)
        n, s = 7, 0.27
        boards = VGroup()
        for k in range(5):
            f = np.array(d["frames"][k])
            cells = VGroup()
            for y in range(n):
                for x in range(n):
                    on = f[y, x] == 1
                    cells.add(Square(side_length=s * 0.92, stroke_width=0.6, stroke_color=GREY_D,
                                     fill_color=GENE if on else "#10151C", fill_opacity=1).move_to(
                        [x * s, -y * s, 0]))
            t = label(r"$t = " + f"{k}" + r"$", font_size=18, color=GREY_A).next_to(cells, DOWN, buff=0.12)
            boards.add(VGroup(cells, t))
        boards.arrange(RIGHT, buff=0.42).move_to([0, -0.3, 0])
        sh = d["shift"]
        rows = stack([(r"population at every step: \ " + f"{d['population'][0]}", GREY_A),
                      (r"period " + f"{d['period']}" + r", \ shifted by $(" + f"{sh[0]}, {sh[1]}" +
                       r")$: \ speed $c/4$, \ one cell every four steps", GENE),
                      (r"Life is Turing-complete \ (Berlekamp, \ Conway and Guy, \ 1982)", OK),
                      (r"Beer \ (2004): \ is the glider a self-maintaining unity, \ as autopoiesis requires?", ALT)],
                     font_size=19, aligned_edge=LEFT, width=10.0).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "In 1970 John Horton Conway simplified von Neumann's world to two states and one rule, and Martin "
            "Gardner's column made it famous. <bookmark mark='a'/>A live cell survives if two or three of its eight "
            "neighbours are alive; a dead cell comes alive if exactly three are. <bookmark mark='b'/>The Reasoner "
            "runs the most famous pattern, the glider. Five cells change shape, step by step. "
            "<bookmark mark='c'/>After four steps the shape returns, moved one cell down and one across: a thing "
            "that moves, although nothing in the rule mentions motion. <bookmark mark='d'/>Elwyn Berlekamp, Conway "
            "and Richard Guy showed that Life can compute anything a Turing machine can, with gliders as signals. "
            "<bookmark mark='e'/>And Randall Beer asked, seriously, whether a glider is a self-maintaining unity "
            "in Maturana and Varela's sense: it constantly replaces its cells, yet stays the same thing."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(rule))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in boards], lag_ratio=0.35), FadeIn(rows[0]), run_time=2.5)
            vo.wait_until("c")
            self.play(Indicate(boards[0], color=GOAL, scale_factor=1.05),
                      Indicate(boards[4], color=GOAL, scale_factor=1.05), FadeIn(rows[1]))
            for mk, r in zip("de", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def lenia_rule(self):
        d = load("lenia")
        pr = d["params"]
        hc = history_card(2019, r"Bert Wang-Chak Chan", r"Lenia: \ continuous cellular automata", width=6.2,
                          color=HIST).to_corner(UL, buff=0.3)
        eq = MathTex(r"A^{t+\Delta t}", r"=", r"\Big[\, A^t + \Delta t \; G\!\left(K * A^t\right) \Big]_0^1",
                     font_size=40).move_to([3.3, 2.3, 0])
        eq[0].set_color(GENE)
        g_eq = MathTex(r"G(u) = 2\, e^{-(u - \mu)^2 / 2\sigma^2} - 1", font_size=32, color=ORG).move_to([3.6, 1.0, 0])
        k_eq = MathTex(r"K(r) \propto \exp\!\Big(4 - \tfrac{1}{(r/R)(1 - r/R)}\Big)", font_size=30,
                       color=GROUP).move_to([3.6, 0.1, 0])
        ax = Axes(x_range=[0, 1.05, 0.25], y_range=[0, 1.1, 0.5], x_length=3.0, y_length=1.5,
                  axis_config={"color": GREY_B, "include_ticks": False}).move_to([-4.4, 0.4, 0])
        kern = ax.plot(lambda r: float(np.exp(4 - 1 / max(r * (1 - r), 1e-6))) if 0 < r < 1 else 0.0,
                       x_range=[0.001, 0.999, 0.005], color=GROUP, stroke_width=3)
        kl = label(r"the ring kernel, \ $r$ out to $R = " + f"{pr['R']}" + r"$", font_size=16,
                   color=GROUP).next_to(ax, DOWN, buff=0.1)
        ax2 = Axes(x_range=[0, 0.35, 0.1], y_range=[-1.1, 1.1, 1], x_length=3.0, y_length=1.6,
                   axis_config={"color": GREY_B, "include_ticks": False}).move_to([-4.4, -2.2, 0])
        mu, sg = pr["mu"], pr["sigma"]
        grow = ax2.plot(lambda u: 2 * np.exp(-(u - mu) ** 2 / (2 * sg ** 2)) - 1, x_range=[0, 0.35, 0.002],
                        color=ORG, stroke_width=3)
        gl = label(r"growth: \ positive only near $\mu = " + f"{mu:.3f}" + r"$", font_size=16,
                   color=ORG).next_to(ax2, DOWN, buff=0.1)
        rows = stack([(r"each cell holds a number between 0 and 1, \ not just on or off", WHITE),
                      (r"$K * A$: \ a weighted average of the neighbourhood, \ a ring of radius $R$", GROUP),
                      (r"too little or too much around you: \ shrink; \ just right: \ grow", ORG),
                      (r"Chan catalogued over 400 `species' \ by searching parameter space", GENE)],
                     font_size=19, aligned_edge=LEFT, width=6.6).move_to([2.6, -2.0, 0])
        with self.voiceover(
            "Conway's world is digital. In 2019 Bert Chan made it continuous. <bookmark mark='a'/>In Lenia, each "
            "cell holds a number between zero and one, and the whole field updates by one equation. "
            "<bookmark mark='b'/>First, every cell takes a weighted average of its neighbourhood, using a smooth "
            "ring-shaped kernel K of radius R. <bookmark mark='c'/>Then a growth function G turns that average into "
            "a change: if the neighbourhood is too empty or too full, the cell fades; if it is just right, near mu, "
            "the cell grows. <bookmark mark='d'/>Chan searched the space of parameters and catalogued hundreds of "
            "creatures, which he named and classified like a naturalist."
        ) as vo:
            self.play(FadeIn(hc), Write(eq))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(k_eq), Create(ax), Create(kern), FadeIn(kl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(g_eq), Create(ax2), Create(grow), FadeIn(gl), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def lenia_movie(self):
        d = load("lenia")
        film = np.array(d["movie"], dtype=np.uint8)
        every = 5
        mass = d["mass"]
        head = label(r"The Reasoner's own creature", font_size=30, color=CONN).to_edge(UP, buff=0.25)
        com = d["com"]
        size = film.shape[1]
        W = 36

        def crop(i):
            cx, cy = com[min(len(com) - 1, every * i)]
            f = np.roll(np.roll(film[i], W // 2 - int(round(cy)), axis=0), W // 2 - int(round(cx)), axis=1)
            return f[:W, :W]

        img = field_image(film[0], 4.2, color=GENE, scale=255).move_to([-4.6, -0.3, 0])
        frame = SurroundingRectangle(img, buff=0.02, color=GREY_C, stroke_width=1.5)
        zoom = field_image(crop(0), 2.6, color=GENE, scale=255).move_to([-1.0, 0.5, 0])
        zframe = SurroundingRectangle(zoom, buff=0.02, color=GOAL, stroke_width=1.5)
        zl = label(r"close-up, \ following the centre of mass", font_size=14, color=GOAL).next_to(zframe, UP,
                                                                                                 buff=0.08)
        wl = label(r"the whole world: \ " + f"{size}" + r" $\times$ " + f"{size}" + r" cells, \ a torus", font_size=14,
                   color=GREY_A).next_to(frame, UP, buff=0.08)
        k = ValueTracker(0)

        def refresh(m):
            m.pixel_array = field_rgba(film[min(len(film) - 1, int(k.get_value()))], GENE, 255)

        def refresh_zoom(m):
            m.pixel_array = field_rgba(crop(min(len(film) - 1, int(k.get_value()))), GENE, 255)

        img.add_updater(refresh)
        zoom.add_updater(refresh_zoom)
        n_step = Integer(0, font_size=22, color=GREY_A, group_with_commas=False)
        n_mass = Integer(round(mass[0]), font_size=22, color=GENE, group_with_commas=False)
        sl = label(r"step", font_size=18, color=GREY_A).next_to(frame, DOWN, buff=0.15).align_to(frame, LEFT)
        n_step.next_to(sl, RIGHT, buff=0.15)
        ml_ = label(r"mass", font_size=18, color=GREY_A).next_to(frame, DOWN, buff=0.15).shift(RIGHT * 0.6)
        n_mass.next_to(ml_, RIGHT, buff=0.15)
        step = VGroup(sl, n_step, ml_, n_mass)

        def counters(_):
            i = every * min(len(film) - 1, int(k.get_value()))
            n_step.set_value(i)
            n_step.next_to(sl, RIGHT, buff=0.15)
            n_mass.set_value(round(mass[min(len(mass) - 1, i)]))
            n_mass.next_to(ml_, RIGHT, buff=0.15)

        n_step.add_updater(counters)
        ax = Axes(x_range=[0, 1500, 500], y_range=[0, 450, 150], x_length=4.4, y_length=2.0,
                  axis_config={"color": GREY_B, "font_size": 14}, x_axis_config={"include_numbers": True},
                  y_axis_config={"include_numbers": True}).move_to([3.9, 1.3, 0])
        ml = label(r"total mass over 1500 steps", font_size=16, color=GREY_A).next_to(ax, UP, buff=0.08)
        curve = series_plot(ax, mass, GENE, width=2.5)
        rows = stack([(r"start: \ a disc of random noise, \ mass " + f"{d['mass_start']:.0f}", GREY_A),
                      (r"most of it dies; \ one crescent condenses", ORG),
                      (r"then: \ mass " + f"{d['mass_after']:.1f}" + r", \ steady to " +
                       f"{100 * d['mass_spread']:.1f}" + r"\%", GENE),
                      (r"it glides at " + f"{d['speed']:.2f}" + r" cells per step, \ on a torus", GENE),
                      (r"nothing in the equation says `creature', \ `boundary' \ or `move'", GOAL)],
                     font_size=19, aligned_edge=LEFT, width=5.4).move_to([3.7, -1.7, 0])
        with self.voiceover(
            "Here is a creature the Reasoner found for itself, by random search over growth parameters and starting "
            "patterns. <bookmark mark='a'/>It begins as a disc of random noise, with a total mass of four hundred "
            "and thirty. <bookmark mark='b'/>Watch. Most of the noise dies away. What is left draws together into a "
            "single crescent. <bookmark mark='c'/>From then on the crescent keeps an almost constant mass, about "
            "forty-seven, varying by less than one percent. <bookmark mark='d'/>And it moves, at about half a cell "
            "per step, leaving one edge of the world and returning at the other, because the world is a torus. "
            "<bookmark mark='e'/>Nothing in the equation mentions a creature, a boundary or motion. They are "
            "patterns that maintain themselves, which is exactly what made the previous chapter's definitions "
            "argue about them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(img), Create(frame), FadeIn(wl), FadeIn(step), Create(ax), FadeIn(ml),
                      FadeIn(zoom), Create(zframe), FadeIn(zl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(k.animate.set_value(60), Create(curve), FadeIn(rows[1]), run_time=6, rate_func=linear)
            vo.wait_until("c")
            self.play(k.animate.set_value(160), FadeIn(rows[2]), run_time=7, rate_func=linear)
            vo.wait_until("d")
            self.play(k.animate.set_value(260), FadeIn(rows[3]), run_time=7, rate_func=linear)
            vo.wait_until("e")
            self.play(k.animate.set_value(len(film) - 1), FadeIn(rows[4]), run_time=3, rate_func=linear)
        img.clear_updaters()
        zoom.clear_updaters()
        n_step.clear_updaters()
        self.clear_scene()

    def strong(self):
        head = label(r"Life-as-it-could-be", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Langton \ (1987)", r"named the field: \ study life-as-it-could-be, \ not only life-as-we-know-it", GENE),
            (r"Ray's Tierra \ (1991)", r"self-copying programs in computer memory evolved parasites and "
                                       r"hyper-parasites, \ unasked", ORG),
            (r"Avida \ (2003)", r"Lenski, \ Ofria, \ Pennock and Adami: \ a complex function \ (EQU) \ evolved by "
                                r"building on simpler ones", ALT),
            (r"weak vs strong", r"weak: \ software models life; \ strong: \ the right software is alive", GROUP),
            (r"Pattee \ (1989); \ Sober \ (1991)", r"a simulation is not a realization; \ but if life, \ like mind, "
                                                   r"is organization, \ strong alife is coherent", GOAL),
            (r"open-ended evolution", r"no artificial system yet keeps producing new kinds of things \ "
                                      r"(Bedau et al., \ 2000)", BAD),
        ]
        g = rows_table(rows, top=1.6, gap=0.42, width=8.2, x_text=-2.0, label_size=20)
        nxt = label(r"the same question about minds: \ Part 30", font_size=20, color=GOAL).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Christopher Langton gave the field its name in 1987. <bookmark mark='a'/>Biology, he said, studies "
            "life-as-we-know-it; artificial life would study life-as-it-could-be. <bookmark mark='b'/>Thomas Ray's "
            "Tierra let self-copying programs compete for memory and processor time. Without being asked, they "
            "evolved parasites, which borrowed other programs' copying code, and then hosts that resisted them. "
            "<bookmark mark='c'/>In the Avida system, Richard Lenski, Charles Ofria, Robert Pennock and Christoph "
            "Adami watched a complex logical function evolve by building on simpler ones, some of which were "
            "harmful when they first appeared. <bookmark mark='d'/>Weak artificial life uses software to model "
            "living processes; strong artificial life claims that the right software would itself be alive. "
            "<bookmark mark='e'/>Howard Pattee warned that a simulation is not a realization. Elliott Sober replied "
            "that if life, like mind, is a matter of organization rather than stuff, the strong claim is at least "
            "coherent. <bookmark mark='f'/>The great open problem is open-ended evolution: no artificial world yet "
            "keeps producing new kinds of things the way the biosphere has for four billion years. "
            "<bookmark mark='g'/>The same question, whether organization is enough, returns for minds in Part 30."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("g")
            self.play(FadeIn(nxt))
        self.clear_scene()
