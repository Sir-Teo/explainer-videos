from __future__ import annotations

from videos.philosophy.philosophy22.common import *  # noqa: F403


class DeRe(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"De re and de dicto", r"Is the necessity in the sentence, or in the thing?",
                            lit=(1953, 1960), part=PART)
        with self.voiceover("Chapter one. De re and de dicto."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.planets()
        self.grades()
        self.cyclist()
        self.reply()

    def planets(self):
        head = label(r"One sentence, \ two readings", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        sent = label(r"`The number of planets is necessarily greater than 7'", font_size=24).next_to(head, DOWN,
                                                                                                    buff=0.3)
        dd = MathTex(r"\text{de dicto:}\quad \Box\,(\text{the number of planets} > 7)", font_size=30, color=DESC)
        dr = MathTex(r"\text{de re:}\quad \exists x\,\big(x = \text{the number of planets} \land \Box\,(x > 7)\big)",
                     font_size=30, color=NAME)
        fs = VGroup(dd, dr).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(sent, DOWN, buff=0.3)
        counts = [8, 5, 9]
        names = [r"actual", r"$w_1$", r"$w_2$"]
        isl = VGroup()
        for i, (n, nm) in enumerate(zip(counts, names)):
            c = np.array([-4.2 + 4.2 * i, -1.25, 0])
            I = island(c, w=2.6, h=1.1, seed=10 + i, color=NAME if i == 0 else WORLD)
            dots = VGroup(*[Dot(c + np.array([-1.0 + 2.0 * k / max(1, n - 1), 0.1 * np.sin(k * 1.7), 0]),
                                radius=0.07, color=GREY_A) for k in range(n)])
            t = label(nm + r": \ " + f"{n}" + r" planets", font_size=19, color=NAME if i == 0 else WORLD).next_to(
                I, UP, buff=0.08)
            isl.add(VGroup(I, dots, t))
        ev_dd = VGroup(*[label(rf"${n} > 7$", font_size=22, color=OK if n > 7 else BAD).next_to(isl[i], DOWN,
                                                                                               buff=0.15)
                         for i, n in enumerate(counts)])
        ev_dr = VGroup(*[label(r"$8 > 7$", font_size=22, color=OK).next_to(ev_dd[i], DOWN, buff=0.12)
                         for i in range(3)])
        res = VGroup(label(r"de dicto: \ the number of planets at each world: \ false", font_size=21,
                           color=DESC).move_to([0, -3.15, 0]),
                     label(r"de re: \ the actual number, \ 8, \ at each world: \ true", font_size=21,
                           color=NAME).move_to([0, -3.6, 0]))
        with self.voiceover(
            "Quine's example. <bookmark mark='a'/>The number of planets is necessarily greater than seven. True or "
            "false? <bookmark mark='b'/>Read one way, the necessity applies to the whole sentence: necessarily, "
            "whatever number the planets come to, it exceeds seven. That is the reading de dicto, about what is said. "
            "<bookmark mark='c'/>Read the other way, we pick out a number, the number of planets, and say of that "
            "number that it is necessarily greater than seven. That is the reading de re, about the thing. "
            "<bookmark mark='d'/>Look at three worlds. Ours has eight planets; in one there are five; in another, "
            "nine. <bookmark mark='e'/>De dicto, we check the number of planets at each world: eight, five, nine. "
            "Five fails, so the de dicto claim is false. <bookmark mark='f'/>De re, we take the actual number, "
            "eight, and check eight at every world. Eight exceeds seven everywhere, so the de re claim is true. The "
            "difference is only where the box sits, relative to the description."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(sent))
            vo.wait_until("b")
            self.play(Write(dd))
            vo.wait_until("c")
            self.play(Write(dr))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(g) for g in isl], lag_ratio=0.3))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(e) for e in ev_dd], lag_ratio=0.3), FadeIn(res[0]))
            vo.wait_until("f")
            self.play(LaggedStart(*[FadeIn(e) for e in ev_dr], lag_ratio=0.3), FadeIn(res[1]))
        self.clear_scene()

    def grades(self):
        hc = history_card(1953, r"W. V. O. Quine", r"`Three Grades of Modal Involvement'", width=6.4,
                          color=HIST).to_corner(UL, buff=0.3)
        rows = [
            (r"grade 1", r"`necessary' as a predicate of sentences: \ \texttt{Nec}(`$9 > 7$'): \ fine, \ it means "
                         r"analytic", OK),
            (r"grade 2", r"a sentence operator: \ $\Box(9 > 7)$: \ tolerable, \ if it is grade 1 in disguise", GOAL),
            (r"grade 3", r"quantifying in: \ $\exists x\, \Box(x > 7)$: \ which object is necessarily greater than 7?",
             BAD),
            (r"the trouble", r"`9' and `the number of planets' name the same object, \ but substituting one for the "
                             r"other changes the truth value", DESC),
            (r"the verdict", r"quantifying in commits you to `Aristotelian essentialism': \ objects with "
                             r"necessary properties, \ however they are described", ABS),
        ]
        g = rows_table(rows, top=1.4, gap=0.42, width=8.8, x_text=-2.6, label_size=21)
        with self.voiceover(
            "Quine thought the de re reading was in deep trouble, and he said why in a paper on three grades of modal "
            "involvement. <bookmark mark='a'/>At the first grade, necessary is a predicate of sentences: the "
            "sentence nine is greater than seven is necessary. Quine could live with that, if it meant analytic, true "
            "by virtue of meaning. <bookmark mark='b'/>At the second grade, necessarily is an operator on sentences. "
            "Tolerable, if it is only the first grade in disguise. <bookmark mark='c'/>The third grade quantifies "
            "into a modal context: there is an x such that necessarily x is greater than seven. Which object is "
            "that? <bookmark mark='d'/>Nine is, under the name nine. But nine is the number of planets, and the "
            "number of planets is not necessarily greater than seven. Substituting one name of the object for "
            "another changes the truth value. <bookmark mark='e'/>So, Quine concluded, quantifying in makes sense only "
            "if objects themselves, however described, have some properties necessarily and others contingently. He "
            "called that Aristotelian essentialism, and he did not mean it as praise."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def cyclist(self):
        d = load("cyclist")
        head = label(r"Quine's mathematical cyclist \ (\textit{Word and Object}, \ 1960)", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        tags = {"Math": r"mathematician", "Cyc": r"cyclist", "Rat": r"rational", "Two": r"two-legged"}
        isl = VGroup()
        for i, w in enumerate(["@", "u", "v"]):
            c = np.array([-5.05 + 2.75 * i, 1.0, 0])
            I = island(c, w=2.4, h=1.7, seed=30 + i, color=NAME if w == "@" else WORLD,
                       name=r"actual" if w == "@" else rf"${w}$")
            j = person(c + UP * 0.35, color=DESC, name=r"John", font_size=16)
            facts = d["facts"][w]
            t = label(r", \ ".join(tags[k] for k in ("Math", "Cyc", "Rat", "Two") if k in facts), font_size=15,
                      color=GREY_A)
            if t.width > 2.0:
                t = wrapped_label(r", \ ".join(tags[k] for k in ("Math", "Cyc", "Rat", "Two") if k in facts), 2.0,
                                  15, GREY_A)
            t.move_to(c + DOWN * 0.4)
            isl.add(VGroup(I, j, t))
        hd = [r"\text{claim}", r"\text{reading}", r"\text{on this model}"]
        rows = []
        for r in d["rows"]:
            rows.append([MathTex(r["formula"].strip("$"), font_size=22),
                         MathTex(r"\text{" + r["reading"] + "}", font_size=20, color=GREY_A), tf(r["value"])])
        grid = ValueGrid(hd, rows, col_w=[4.6, 1.6, 1.8], cell_h=0.44, font_size=19).move_to([-2.0, -2.1, 0])
        side = stack([(r"necessarily, \ mathematicians are rational; \ cyclists are two-legged", WHITE),
                      (r"John is both: \ is \textit{he} necessarily rational? \ necessarily two-legged?", GOAL),
                      (r"Quine: \ there is no answer, \ only answers relative to a description", BAD)],
                     font_size=20, aligned_edge=LEFT, width=3.9).move_to([4.95, 0.9, 0])
        with self.voiceover(
            "Quine pressed the point with a famous example. <bookmark mark='a'/>Mathematicians are necessarily "
            "rational and not necessarily two-legged; cyclists are necessarily two-legged and not necessarily "
            "rational. <bookmark mark='b'/>John is a mathematician and a cyclist. Is John, the man himself, "
            "necessarily rational? Necessarily two-legged? Considered as a mathematician, it seems yes to the first; "
            "considered as a cyclist, yes to the second; and neither consideration has a better claim. "
            "<bookmark mark='c'/>The Reasoner builds a model. Three worlds. At ours, John is both, and rational and "
            "two-legged. At u he cycles but does no mathematics, and is not rational. At v he does mathematics but "
            "not cycling, and has one leg. <bookmark mark='d'/>Both de dicto claims come out true: at every world, "
            "every mathematician is rational, and every cyclist two-legged. But neither de re claim is true of John. "
            "<bookmark mark='e'/>Quine took the lesson to be that there is no fact about which of John's properties "
            "are necessary, only facts relative to how he is described."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(g) for g in isl], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(rows)):
                self.play(*[FadeIn(grid.cell[r][c]) for c in range(3)], run_time=0.6)
            vo.wait_until("e")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def reply(self):
        q = quote_card(r"A possible world isn't a distant country that we are coming across, \ or viewing through a "
                       r"telescope. \ \ldots\ `Possible worlds' are stipulated, \ not discovered by powerful "
                       r"telescopes.", r"Saul Kripke", r"\textit{Naming and Necessity} \ (1980), \ pp. 44--5",
                       width=10.4, font_size=24).to_edge(UP, buff=0.5)
        rows = stack([(r"Marcus \ (1961): \ names are tags; \ substituting co-referring tags is safe", NAME),
                      (r"Kripke: \ we do not find John in another world and then ask who he is; \ we say "
                       r"`suppose \textit{John} had not cycled'", WORLD),
                      (r"so de re modality is about the thing, \ however we happen to describe it", OK),
                      (r"`9' is a name, \ `the number of planets' a description: \ the next chapter", GOAL)],
                     font_size=22, aligned_edge=LEFT, width=12.0, buff=0.32).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "The answer to Quine came from two directions. <bookmark mark='a'/>Kripke's: we do not peer at another "
            "world through a telescope, find a man there, and wonder whether he is John. Possible worlds are "
            "stipulated, not discovered. <bookmark mark='b'/>Ruth Barcan Marcus had argued that proper names are "
            "tags, attached to a thing without describing it; substituting one tag for another of the same thing is "
            "always safe. <bookmark mark='c'/>And Kripke: when we consider whether John might have been irrational, "
            "we consider a situation of which we say: suppose John, this man, had never studied mathematics. "
            "<bookmark mark='d'/>De re modality is then about the thing itself, however we describe it. Whether John "
            "could have been irrational is a question about John, and it may have a definite answer. "
            "<bookmark mark='e'/>Everything turns on the difference between a name, like nine, and a description, "
            "like the number of planets. That is the next chapter."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(q))
            for mk, r in zip("bcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
