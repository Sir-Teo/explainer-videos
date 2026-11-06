from __future__ import annotations

from videos.philosophy.philosophy3.common import *  # noqa: F403

MOOD_TEX = {"A": r"\text{All } {a} \text{ are } {b}", "E": r"\text{No } {a} \text{ are } {b}",
            "I": r"\text{Some } {a} \text{ are } {b}", "O": r"\text{Some } {a} \text{ are not } {b}"}


def mood_tex(k, a, b):
    return MOOD_TEX[k].replace("{a}", a).replace("{b}", b)


class Express(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"Saying things exactly", r"What can first-order logic say?", lit=(1905,), part=PART)
        with self.voiceover("Chapter four. Saying things exactly."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.counting()
        self.russell()
        self.scope_table()
        self.aristotle()
        self.lover()

    def counting(self):
        d = load("counting")
        head = label(r"Counting with nothing but $\forall$, $\exists$ and $=$", font_size=32, color=CONN).to_edge(
            UP, buff=0.4)
        rows = VGroup()
        for name, reading in (("at least two", r"at least two $P$s"), ("exactly one", r"exactly one $P$"),
                              ("exactly two", r"exactly two $P$s")):
            rows.add(VGroup(label(reading, font_size=26, color=GOAL),
                            MathTex(d[name]["tex"].replace(r"\mathrm{P}", "P"), font_size=30)))
        for r in rows:
            r.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(head, DOWN, buff=0.45)
        if rows.width > 13:
            rows.width = 13
        chk = label(r"each checked on every structure of sizes 1--4, \ every possible set of $P$s", font_size=24,
                    color=OK).to_edge(DOWN, buff=0.95)
        inf = label(r"but no single sentence says `there are infinitely many $P$s' \ (Chapter 8)", font_size=24,
                    color=BAD).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "With identity, first-order logic can count. <bookmark mark='a'/>'There are at least two Ps': there is an "
            "x and a y, both P, and x is not y. Without that last clause, x and y could be the same thing. "
            "<bookmark mark='b'/>'Exactly one P': there is a P, and every P is identical to it. "
            "<bookmark mark='c'/>'Exactly two': two different Ps, and every P is one of them. Any finite number works "
            "the same way, with as many variables as the number. <bookmark mark='d'/>The Reasoner checked each "
            "formula against every structure with up to four objects and every possible set of Ps. "
            "<bookmark mark='e'/>But there is no single sentence that says 'there are infinitely many Ps'. Chapter "
            "eight will prove it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r[0]), Write(r[1]))
            vo.wait_until("d")
            self.play(FadeIn(chk))
            vo.wait_until("e")
            self.play(FadeIn(inf))
        self.clear_scene()

    def russell(self):
        hc = history_card(1905, r"Bertrand Russell", r"`On Denoting', \textit{Mind}", width=4.6,
                          color=HIST).to_corner(UL, buff=0.4)
        s = label(r"`The present King of France is bald.'", font_size=36).move_to([1.2, 2.2, 0])
        puzzle = label(r"France has no king. \ True? \ False? \ About nothing?", font_size=26, color=GREY_A).next_to(
            s, DOWN, buff=0.25)
        parts = VGroup(
            VGroup(MathTex(r"\exists x\, (\mathrm{K}(x)", font_size=40, color=P.CLAIM),
                   label(r"there is a king", font_size=22, color=P.CLAIM)),
            VGroup(MathTex(r"\land\ \forall y\, (\mathrm{K}(y) \to y = x)", font_size=40, color=P.AGENT),
                   label(r"at most one", font_size=22, color=P.AGENT)),
            VGroup(MathTex(r"\land\ \mathrm{B}(x))", font_size=40, color=GOAL),
                   label(r"he is bald", font_size=22, color=GOAL)))
        for p in parts:
            p[1].next_to(p[0], DOWN, buff=0.2)
        for i in (1, 2):
            parts[i].next_to(parts[i - 1], RIGHT, buff=0.15)
            parts[i].align_to(parts[0], UP)
        parts.move_to([0, -0.2, 0])
        verdict = label(r"no king: \ the first conjunct fails, \ so the sentence is simply \textbf{false}",
                        font_size=26, color=BAD).to_edge(DOWN, buff=0.9)
        moral = label(r"`the King of France' is not a name: \ it vanishes on analysis", font_size=26,
                      color=GOAL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In 1905 Bertrand Russell used this logic to dissolve a philosophical puzzle. <bookmark mark='a'/>'The "
            "present King of France is bald.' France has no king. So is the sentence true, false, or about nothing at "
            "all? And if it is about nothing, how can it mean anything? <bookmark mark='b'/>Russell's answer: the "
            "sentence only looks like it names someone. Its logical form is three claims. There is a king of France; "
            "<bookmark mark='c'/>there is at most one; <bookmark mark='d'/>and he is bald. <bookmark mark='e'/>Since "
            "there is no king, the first claim fails and the whole sentence is plainly false. No mysterious "
            "non-existent king is needed. <bookmark mark='f'/>'The King of France' is not a name at all; it "
            "disappears when the sentence is analysed. Frank Ramsey called this theory a paradigm of philosophy."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(s), FadeIn(puzzle))
            vo.wait_until("b")
            self.play(Write(parts[0][0]), FadeIn(parts[0][1]))
            vo.wait_until("c")
            self.play(Write(parts[1][0]), FadeIn(parts[1][1]))
            vo.wait_until("d")
            self.play(Write(parts[2][0]), FadeIn(parts[2][1]))
            vo.wait_until("e")
            self.play(FadeIn(verdict))
            vo.wait_until("f")
            self.play(FadeIn(moral))
        self.clear_scene()

    def scope_table(self):
        d = load("russell")
        s = label(r"`The King of France is \textit{not} bald.' \ Two readings:", font_size=32).to_edge(UP, buff=0.4)
        wide = VGroup(label(r"(1) \ there is exactly one king, and he is not bald", font_size=24, color=P.CLAIM),
                      MathTex(d["neg_wide"], font_size=30, color=P.CLAIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        narrow = VGroup(label(r"(2) \ it is not the case that exactly one king is bald", font_size=24,
                              color=P.AGENT),
                        MathTex(d["neg_narrow"], font_size=30, color=P.AGENT)).arrange(DOWN, aligned_edge=LEFT,
                                                                                       buff=0.1)
        rd = VGroup(wide, narrow).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(s, DOWN, buff=0.35)
        names = {"no king": r"no king", "one bald king": r"one bald king", "one hairy king": r"one hairy king",
                 "two kings": r"two kings"}
        rows = [[names[r["world"]], r["bald"], r["not_bald_wide"], r["not_bald_narrow"]] for r in d["rows"]]
        hd = [label(r"world", font_size=24, color=P.CLAIM), label(r"`is bald'", font_size=24, color=P.CLAIM),
              label(r"(1)", font_size=24, color=P.CLAIM), label(r"(2)", font_size=24, color=P.CLAIM)]
        grid = ValueGrid(hd, [[label(w, font_size=24)] + [tv(b) for b in vals] for w, *vals in rows],
                         col_w=[3.2, 1.8, 1.4, 1.4],
                         font_size=24).next_to(rd, DOWN, buff=0.4)
        fwd = label(r"Strawson (1950): \ neither true nor false, a failed presupposition \ (Parts 5 and 27)",
                    font_size=22, color=GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The theory also explains an ambiguity. <bookmark mark='a'/>'The King of France is not bald' can mean that "
            "there is exactly one king and he is not bald. <bookmark mark='b'/>Or it can mean: it is not the case "
            "that there is exactly one king who is bald. The difference is the scope of 'not'. "
            "<bookmark mark='c'/>The Reasoner evaluated all three sentences in four small worlds. "
            "<bookmark mark='d'/>With no king, the first two are false, and the second reading of 'not bald' is "
            "true. With two kings, the same. Only in a world with exactly one king do the two readings agree. "
            "<bookmark mark='e'/>In 1950 Peter Strawson objected that, with no king, the sentence is neither true nor "
            "false: it presupposes something that fails. That objection opens Part 5."
        ) as vo:
            self.play(FadeIn(s))
            vo.wait_until("a")
            self.play(FadeIn(wide))
            vo.wait_until("b")
            self.play(FadeIn(narrow))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), FadeIn(grid.rows_bg))
            self.play(LaggedStart(*[FadeIn(grid.row(r)) for r in range(len(rows))], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(Create(grid.row_box(0, color=GOAL)), Create(grid.row_box(3, color=GOAL)))
            vo.wait_until("e")
            self.play(FadeIn(fwd))
        self.clear_scene()

    def aristotle(self):
        d = load("moods")
        head = label(r"Aristotle inside first-order logic", font_size=34, color=CONN).to_edge(UP, buff=0.4)
        tr = VGroup(*[MathTex(mood_tex(k, "S", "P"), r"\ \leadsto\ ", t, font_size=30) for k, t in (
            ("A", r"\forall x\, (S(x) \to P(x))"), ("E", r"\forall x\, (S(x) \to \lnot P(x))"),
            ("I", r"\exists x\, (S(x) \land P(x))"), ("O", r"\exists x\, (S(x) \land \lnot P(x))"))])
        for t in tr:
            t[2].set_color(GOAL)
        tr.arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.8)
        bars = bar_row([256, d["boolean"], d["traditional"]],
                       [r"all moods", r"valid", r"valid, $S, M, P$ inhabited"],
                       [GREY_B, OK, P.AGENT], width=2.6, height=0.36, font_size=22).next_to(tr, RIGHT, buff=0.6)
        if bars.get_right()[0] > 6.9:
            bars.shift(LEFT * (bars.get_right()[0] - 6.9))
        agree = label(r"exactly the 15 and the 24 of Part 1's Venn diagrams", font_size=24, color=OK).next_to(
            bars, DOWN, buff=0.3)
        n3 = d["needs3"]
        prem = VGroup(*[MathTex(mood_tex(k, a, b), font_size=30) for k, a, b in n3["premises"]])
        concl = MathTex(mood_tex(*n3["conclusion"]),
                        font_size=30, color=GOAL)
        arg = VGroup(*prem, Line(LEFT * 1.6, RIGHT * 1.6, color=GREY_B), concl).arrange(DOWN, buff=0.12)
        sz = d["countermodel_sizes"]
        cms = label(rf"smallest countermodels: \ {sz['1']} invalid moods need 1 object, \ {sz['2']} need 2, \ "
                    rf"{sz['3']} needs 3:", font_size=24, color=GREY_A)
        cm = VGroup(*[VGroup(Dot(color=OBJ), label(t, font_size=22, color=OBJ)).arrange(RIGHT, buff=0.12) for t in (
            r"$P$, not $M$", r"$M$, not $S$", r"$S$, not $P$")]).arrange(RIGHT, buff=0.6)
        low = VGroup(cms, VGroup(arg, cm).arrange(RIGHT, buff=1.0)).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Aristotle's logic now becomes a small corner of the new one. <bookmark mark='a'/>Each of the four "
            "categorical forms is one first-order sentence. 'All S are P': for every x, if x is S, x is P. 'Some S "
            "are P': there is an x that is both. <bookmark mark='b'/>The Reasoner translated all two hundred and "
            "fifty-six moods and handed each to its first-order model finder. Fifteen have no countermodel. Add the "
            "three sentences saying that S, M and P each have members, and twenty-four survive. "
            "<bookmark mark='c'/>Exactly the fifteen and the twenty-four that Part 1 found with Venn diagrams: two "
            "different methods, one answer. <bookmark mark='d'/>The countermodels are tiny. Most invalid moods fail "
            "in a world with a single object, and only one needs three: some P is not M, some M is not S, so all S "
            "are P. To refute it you need three different things, one for each premise and one for the failure."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.2) for t in tr], lag_ratio=0.25))
            vo.wait_until("b")
            for r in bars:
                self.play(FadeIn(r.name), GrowFromEdge(r.bar, LEFT), FadeIn(r.value), run_time=0.7)
            vo.wait_until("c")
            self.play(FadeIn(agree))
            vo.wait_until("d")
            self.play(FadeIn(cms), FadeIn(arg))
            self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in cm], lag_ratio=0.3))
        self.clear_scene()

    def lover(self):
        d = load("tableaux")["romeo"]
        prem = VGroup(label(r"Everybody loves a lover.", font_size=30),
                      MathTex(r"\forall x\, \forall y\, (\mathrm{L}(x, y) \to \forall z\, \mathrm{L}(z, x))",
                              font_size=34, color=GREY_A),
                      label(r"Romeo loves Juliet.", font_size=30),
                      label(r"So I love you.", font_size=30, color=GOAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        prem.to_corner(UL, buff=0.5)
        steps = [(r"\mathrm{L}(\mathrm{romeo}, \mathrm{juliet})", r"premise"),
                 (r"\forall z\, \mathrm{L}(z, \mathrm{romeo})", r"Romeo is a lover, so everyone loves him"),
                 (r"\mathrm{L}(\mathrm{you}, \mathrm{romeo})", r"in particular, you love Romeo"),
                 (r"\forall z\, \mathrm{L}(z, \mathrm{you})", r"so you are a lover: everyone loves you"),
                 (r"\mathrm{L}(\mathrm{me}, \mathrm{you})", r"in particular, I do")]
        rows = VGroup()
        for i, (f, j) in enumerate(steps):
            num = MathTex(rf"{i + 1}.", font_size=28, color=GREY_B)
            rows.add(VGroup(num, MathTex(f, font_size=32).next_to(num, RIGHT, buff=0.25)))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to([-1.6, -1.0, 0])
        jx = max(r[1].get_right()[0] for r in rows) + 0.5
        for r, (f, j) in zip(rows, steps):
            lab_ = label(j, font_size=22, color=GREY_A)
            r.add(lab_.move_to([jx + lab_.width / 2, r[1].get_y(), 0]))
        rows[-1][1].set_color(GOAL)
        blind = label(rf"the Reasoner's blind tableau: \ also valid, \ but {d['n_steps']} steps on "
                      rf"{d['branches']} branches", font_size=24, color=CONN).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here is an argument that sounds like a joke and is perfectly valid. <bookmark mark='a'/>Everybody loves a "
            "lover. Romeo loves Juliet. Therefore, I love you. <bookmark mark='b'/>Read 'everybody loves a lover' as: "
            "whenever x loves anyone, everyone loves x. <bookmark mark='c'/>Romeo loves Juliet, so Romeo is a lover, "
            "and everyone loves Romeo. <bookmark mark='d'/>In particular, you love Romeo. So you are a lover, "
            "<bookmark mark='e'/>and everyone loves you, including me. <bookmark mark='f'/>Five lines. The Reasoner's "
            f"tableau proves it too, but blindly: {d['n_steps']} steps, because it tries every person in every "
            "rule. Choosing the right instances is the whole art of proof, and Chapter eleven is about machines that "
            "learned it."
        ) as vo:
            self.play(FadeIn(prem[0]))
            vo.wait_until("a")
            self.play(FadeIn(prem[2]), FadeIn(prem[3]))
            vo.wait_until("b")
            self.play(Write(prem[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
            self.play(Indicate(rows[4][1], color=GOAL))
            vo.wait_until("f")
            self.play(FadeIn(blind))
        self.clear_scene()
