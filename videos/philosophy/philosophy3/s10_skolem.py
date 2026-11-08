from __future__ import annotations

from videos.philosophy.philosophy3.common import *  # noqa: F403


class Skolem(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"Löwenheim, Skolem and the paradox", r"Can a countable model believe in the "
                            r"uncountable?", lit=(1915, 1980), part=PART)
        with self.voiceover("Chapter nine. Löwenheim, Skolem, and the paradox."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.theorem()
        self.hull()
        self.cantor()
        self.paradox()
        self.price()
        self.putnam()

    def theorem(self):
        hcs = VGroup(history_card(1915, r"Leopold Löwenheim", r"a satisfiable sentence has a countable model",
                                  width=4.6, color=HIST, font_size=20),
                     history_card(1920, r"Thoralf Skolem", r"the same for any countable set of sentences",
                                  width=4.6, color=HIST, font_size=20)).arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.4)
        down = theorem_card(r"Downward Löwenheim--Skolem", r"a countable set of sentences with an infinite model has "
                            r"a \textit{countable} model", width=6.2, font_size=22).move_to([-3.4, -0.6, 0])
        up = theorem_card(r"Upward Löwenheim--Skolem", r"\dots\ and a model of every larger infinite size",
                          who=r"Tarski, Mal'tsev, Vaught", width=6.0, font_size=22).move_to([3.4, -0.6, 0])
        moral = label(r"first-order logic cannot tell one infinite size from another", font_size=28,
                      color=GOAL).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The third consequence is the strangest. <bookmark mark='a'/>In 1915 Leopold Löwenheim proved that a "
            "satisfiable first-order sentence always has a countable model, one whose objects can be listed "
            "first, second, third. Thoralf Skolem extended it to any countable set of sentences. "
            "<bookmark mark='b'/>So if a theory has an infinite model, it has a countable one. "
            "<bookmark mark='c'/>And going up instead of down, if it has an infinite model, it has models of every "
            "larger infinite size too. <bookmark mark='d'/>Put together: no first-order theory with an infinite "
            "model can fix how big its models are."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(h, shift=DOWN * 0.2) for h in hcs], lag_ratio=0.3))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(down, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(up, shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(moral))
        self.clear_scene()

    def hull(self):
        rng = np.random.default_rng(7)
        cloud = Ellipse(width=10.0, height=5.0, stroke_color=GREY_C, stroke_width=2, fill_color=GREY_E,
                        fill_opacity=0.25).move_to([0, -0.4, 0])
        cl = label(r"a huge model: \ uncountably many objects", font_size=24, color=GREY_A).next_to(cloud, UP,
                                                                                                  buff=0.15)
        haze = VGroup(*[Dot(cloud.get_center() + np.array([rng.uniform(-4.6, 4.6), rng.uniform(-2.1, 2.1), 0]),
                            radius=0.025, color=GREY_B) for _ in range(500)])
        haze = VGroup(*[d for d in haze if ((d.get_x() / 4.8) ** 2 + ((d.get_y() + 0.4) / 2.35) ** 2) < 1])
        layers = []
        pts = [np.array([0.0, -0.4, 0])]
        cols = [P.CLAIM, P.AGENT, GOAL, OK]
        for k in range(4):
            new = []
            for p in pts:
                for _ in range(2):
                    q = p + np.array([rng.uniform(-1.4, 1.4), rng.uniform(-0.8, 0.8), 0]) * (1 + 0.4 * k)
                    c0 = np.array([0.0, -0.4, 0])
                    r = np.hypot((q[0] - c0[0]) / 4.6, (q[1] - c0[1]) / 2.25)
                    if r > 0.92:
                        q = c0 + (q - c0) * 0.92 / r
                    new.append(q)
            layers.append(VGroup(*[Dot(q, radius=0.07, color=cols[k]) for q in new]))
            pts = new
        seed = Dot(np.array([0.0, -0.4, 0]), radius=0.09, color=WHITE)
        steps = VGroup(label(r"start from the named objects", font_size=22, color=WHITE),
                       label(r"add a witness for every `there exists' they make true", font_size=22, color=P.CLAIM),
                       label(r"and witnesses for those, \ and so on: \ countably many steps", font_size=22,
                             color=GOAL),
                       label(r"the result is a countable model, \ true to every sentence", font_size=22,
                             color=OK)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Why is the downward theorem true? <bookmark mark='a'/>Start with any model, however huge. "
            "<bookmark mark='b'/>Pick out the objects the sentences name. <bookmark mark='c'/>Every existential "
            "sentence that is true about them needs a witness, so add one witness for each. There are only "
            "countably many formulas, so this adds only countably many objects. <bookmark mark='d'/>Then add "
            "witnesses for the new objects, and witnesses for those, layer after layer. <bookmark mark='e'/>After "
            "countably many layers, the collected objects form a smaller model in which exactly the same sentences "
            "are true. Logicians call it a Skolem hull. Everything a first-order sentence can demand, a countable "
            "world can supply."
        ) as vo:
            self.play(FadeIn(cloud), FadeIn(haze), FadeIn(cl))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(seed, scale=2), FadeIn(steps[0]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(d, scale=2) for d in layers[0]], lag_ratio=0.2), FadeIn(steps[1]))
            vo.wait_until("d")
            for L in layers[1:]:
                self.play(LaggedStart(*[FadeIn(d, scale=2) for d in L], lag_ratio=0.05), run_time=1.0)
            self.play(FadeIn(steps[2]))
            vo.wait_until("e")
            self.play(haze.animate.set_opacity(0.15), FadeIn(steps[3]))
        self.clear_scene()

    def cantor(self):
        rows = VGroup()
        digits = ["1415926", "7182818", "4142135", "6180339", "3025850"]
        for i, ds in enumerate(digits):
            r = VGroup(MathTex(rf"r_{{{i + 1}}} = 0.", font_size=32))
            for j, ch in enumerate(ds):
                t = MathTex(ch, font_size=32, color=GOAL if i == j else WHITE)
                r.add(t)
            r.arrange(RIGHT, buff=0.08)
            rows.add(r)
        rows.add(MathTex(r"\vdots", font_size=32))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-2.8, 0.4, 0])
        new_d = "".join(str((int(digits[i][i]) + 1) % 10) for i in range(5))
        diag = MathTex(r"d = 0.", *list(new_d), r"\dots", font_size=34, color=OK).next_to(rows, DOWN, buff=0.4)
        diag.align_to(rows, LEFT)
        txt = VGroup(label(r"change the $n$th digit of the $n$th number:", font_size=24, color=GREY_A),
                     label(r"$d$ differs from every $r_n$, \ so no list contains every real", font_size=24,
                           color=OK),
                     label(r"Cantor 1891; \ a theorem of ZFC, the standard axioms for sets", font_size=24,
                           color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.4, 0.0, 0])
        with self.voiceover(
            "Now recall Cantor's theorem, which says that the real numbers cannot be listed. "
            "<bookmark mark='a'/>Given any list of reals, build a new number d whose n-th digit differs from the "
            "n-th digit of the n-th number on the list. <bookmark mark='b'/>Then d differs from every number on the "
            "list, so the list missed it. No list contains every real: there are uncountably many. "
            "<bookmark mark='c'/>This is a theorem of ZFC, the axioms of set theory on which almost all of "
            "mathematics is built, and ZFC is a first-order theory."
        ) as vo:
            self.play(FadeIn(rows))
            vo.wait_until("a")
            self.play(FadeIn(txt[0]), *[Indicate(rows[i][1 + i], color=GOAL) for i in range(5)])
            self.play(Write(diag))
            vo.wait_until("b")
            self.play(FadeIn(txt[1]))
            vo.wait_until("c")
            self.play(FadeIn(txt[2]))
        self.clear_scene()

    def paradox(self):
        M = Circle(radius=2.4, stroke_color=P.CLAIM, stroke_width=3).move_to([-2.2, -0.3, 0])
        ml = label(r"$M$: \ a countable model of ZFC", font_size=24, color=P.CLAIM).next_to(M, UP, buff=0.15)
        R = Ellipse(width=2.4, height=1.4, stroke_color=GOAL, stroke_width=2.5).move_to(M.get_center() + DOWN * 0.3)
        rl = MathTex(r"\mathbb{R}^M", font_size=34, color=GOAL).move_to(R)
        inside = label(r"$M \models$ `$\mathbb{R}$ is uncountable'", font_size=24, color=GOAL).next_to(R, UP,
                                                                                                     buff=0.35)
        nat = VGroup(*[MathTex(str(i), font_size=26, color=OBJ) for i in range(4)], MathTex(r"\dots", font_size=26))
        nat.arrange(DOWN, buff=0.3).move_to([4.6, -0.3, 0])
        arrows = VGroup(*[Arrow(nat[i].get_left(), R.point_from_proportion(0.05 + 0.1 * i), buff=0.15,
                                color=OK, stroke_width=2.5, max_tip_length_to_length_ratio=0.06) for i in range(4)])
        out = label(r"outside: \ $M$ is countable, \ so $\mathbb{R}^M$ can be listed", font_size=24,
                    color=OK).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Put the two theorems together. <bookmark mark='a'/>If ZFC is consistent, Löwenheim and Skolem give it a "
            "countable model, M. <bookmark mark='b'/>M satisfies every theorem of ZFC, including Cantor's. So inside "
            "M there is an object that M takes to be the set of real numbers, <bookmark mark='c'/>and M satisfies "
            "the sentence 'this set is uncountable'. <bookmark mark='d'/>But M is countable, so from the outside its "
            "'set of reals' has only countably many members, and we can list them. A model that believes in the "
            "uncountable, built from countably many things. This is Skolem's paradox."
        ) as vo:
            self.play(Create(M), FadeIn(ml))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Create(R), FadeIn(rl))
            vo.wait_until("c")
            self.play(FadeIn(inside))
            vo.wait_until("d")
            self.play(FadeIn(nat), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), FadeIn(out))
        self.clear_scene()

    def price(self):
        d = load("skolem")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        assert d["mus"] == [["C", "U", "T", "A"]] and len(d["mcs"]) == 4
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.65, width=3.8, font_size=22,
                       center=[0, -0.45, 0], title=r"The Price List: \ Skolem's paradox")
        with self.voiceover(
            "As a Price List: four claims that cannot all be true. <bookmark mark='a'/>ZFC has a countable model. "
            "ZFC proves the reals are uncountable. What ZFC proves is true in every model of it. And 'uncountable' "
            "means the same inside a model as outside. <bookmark mark='b'/>The Reasoner finds one minimal conflict, "
            "all four together, and so four exits, one per claim. Three of them cost a theorem: Löwenheim and "
            "Skolem's, Cantor's, or soundness. <bookmark mark='c'/>The fourth is the standard resolution, and it "
            "was Skolem's own. 'Uncountable' means 'no list of it exists'. The list we drew from outside is not a "
            "set in M. Inside M, there is no such list, so M is right, by its own lights, to call its reals "
            "uncountable. Skolem concluded that set-theoretic notions are relative to a model."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            vo.wait_until("c")
            anims, centre = pl.position(("A",), r"Relativity", r"Skolem 1922: \ the list exists outside $M$, "
                                        r"not inside it; \ the standard view", width=3.0)
            self.play(*anims)
        self.clear_scene()

    def putnam(self):
        hc = history_card(1980, r"Hilary Putnam", r"`Models and Reality'", width=5.0, color=HIST).to_corner(
            UL, buff=0.4)
        arg = VGroup(
            label(r"our whole theory of the world, \ plus everything we could ever observe, \ is a set of sentences",
                  font_size=24),
            label(r"it has many models, \ of different sizes, \ that make all of it true", font_size=24),
            label(r"so what makes our words refer to \textit{this} world, \ and not to one of the others?",
                  font_size=26, color=GOAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 0.0, 0])
        fwd = label(r"the model-theoretic argument against metaphysical realism: \ Parts 18 and 27", font_size=24,
                    color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "In 1980 Hilary Putnam turned the paradox into an argument about language itself. "
            "<bookmark mark='a'/>Take our best total theory of the world, together with every observation we "
            "could ever make, and write it as a set of sentences. <bookmark mark='b'/>By the theorems of this "
            "chapter it has many models, of different sizes, all making every sentence true. "
            "<bookmark mark='c'/>So what makes our words pick out this world, rather than one of the others? Putnam "
            "concluded that a certain picture of truth, as correspondence to a world fixed independently of us, "
            "cannot be right. <bookmark mark='d'/>Philosophers still argue about what this argument proves. We come "
            "back to it in Parts 18 and 27."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, a in zip("abc", arg):
                vo.wait_until(mk)
                self.play(FadeIn(a, shift=RIGHT * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(fwd))
        self.clear_scene()
