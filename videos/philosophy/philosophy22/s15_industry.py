from __future__ import annotations

from videos.philosophy.philosophy22.common import *  # noqa: F403


class Industry(VoiceoverScene):
    def construct(self):
        card = chapter_card(14, r"Possible worlds at work", r"Where do engineers compute with worlds?",
                            lit=(1995, 2017), part=PART)
        with self.voiceover("Chapter fourteen. Possible worlds at work."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.where()
        self.explain()
        self.ties()
        self.problog()

    def where(self):
        head = label(r"Worlds in the machine room", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"verification", r"the states of a program are worlds; \ `always', \ `eventually' are modal operators "
                              r"\ (Part 4's model checker)", WORLD),
            (r"knowledge", r"distributed protocols reason about what each process knows: \ worlds it cannot tell "
                           r"apart \ (Part 12)", CPT),
            (r"probability", r"a probabilistic program defines a distribution over possible worlds", NAME),
            (r"explanation", r"`you would have got the loan if your income had been higher': \ a counterfactual "
                             r"about the nearest world", DESC),
            (r"fairness", r"Kusner et al. \ (2017): \ a decision is fair if it would be the same in the world where "
                          r"your group were different", GOAL),
        ]
        g = rows_table(rows, top=1.9, gap=0.45, width=8.8, x_text=-2.6, label_size=21)
        with self.voiceover(
            "Possible worlds are not only for metaphysicians. <bookmark mark='a'/>In verification, the states of a "
            "program are worlds, and always and eventually are modal operators: Part 4 built a model checker on "
            "exactly that. <bookmark mark='b'/>Distributed protocols reason about what each process knows, as the "
            "worlds it cannot distinguish from the actual one: the epistemic logic of Part 12. "
            "<bookmark mark='c'/>Probabilistic programming languages define distributions over possible worlds. "
            "<bookmark mark='d'/>Explanations of automated decisions are counterfactuals: you would have been given "
            "the loan if your income had been higher. <bookmark mark='e'/>And one definition of fairness, Matt "
            "Kusner and colleagues' counterfactual fairness, asks whether a decision would have been the same in the "
            "world where your demographic group were different. Two of these are built now."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def explain(self):
        d = load("cfx")
        head = label(r"A counterfactual explanation, \ computed", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        w = d["weights"]
        f = MathTex(rf"\text{{score}} = {w['income']}\,\text{{income}} - {abs(w['debt'])}\,\text{{debt}} + "
                    rf"{w['years']}\,\text{{years}} - {abs(w['bias'])}", font_size=32, color=ABS).next_to(head, DOWN,
                                                                                                    buff=0.35)
        fl = label(r"approve when the score is at least 0", font_size=19, color=GREY_A).next_to(f, DOWN, buff=0.12)
        a = d["applicant"]
        app = island([-4.6, -0.5, 0], w=3.4, h=2.4, seed=210, color=NAME, name=r"actual", font_size=19)
        at = VGroup(label(rf"income {a['income']}k", font_size=19), label(rf"debt {a['debt']}k", font_size=19),
                    label(rf"{a['years']} years employed", font_size=19),
                    label(rf"score ${d['score']}$: \ refused", font_size=19, color=BAD)).arrange(DOWN, buff=0.1).move_to(
            app.shape)
        best = d["closest"][1]
        cw = island([0.4, -0.5, 0], w=3.6, h=2.4, seed=211, color=OK, name=r"a closest world", font_size=19)
        ct = VGroup(label(rf"income {a['income'] + best['income']}k \ (+{best['income']}k)", font_size=19),
                    label(rf"debt {a['debt'] + best['debt']}k \ ({best['debt']}k)", font_size=19),
                    label(rf"{a['years'] + best['years']} years employed", font_size=19),
                    label(r"score $0$: \ approved", font_size=19, color=OK)).arrange(DOWN, buff=0.1).move_to(cw.shape)
        arr = Arrow(app.shape.get_right(), cw.shape.get_left(), buff=0.1, color=GREY_B, stroke_width=3)
        cost = label(rf"distance {d['best_cost']}", font_size=17, color=GREY_A).next_to(arr, UP, buff=0.08)
        rows = stack([(r"search every change on a grid: \ " + f"{d['searched']}" + r" worlds, \ " + f"{d['flips']}" +
                       r" of them flip the decision", WHITE),
                      (r"keep the nearest, \ by a weighted distance: \ Wachter, \ Mittelstadt and Russell \ (2017)",
                       CPT),
                      (r"`had your income been 5k higher, \ your debt 2k lower \ and your job two years longer, \ "
                       r"you would have been approved'", OK)], font_size=19, aligned_edge=LEFT, width=4.6).move_to([4.75, -0.5, 0])
        with self.voiceover(
            "First, an explanation. <bookmark mark='a'/>A toy credit model scores applicants by income, debt and "
            "years employed, and approves when the score is at least zero. <bookmark mark='b'/>An applicant earning "
            "thirty-five thousand, with ten thousand in debt and two years in the job, scores minus one point four, "
            "and is refused. Why? <bookmark mark='c'/>Sandra Wachter, Brent Mittelstadt and Chris Russell proposed "
            "answering with a counterfactual: the smallest change that would have flipped the decision. The Reasoner "
            "searches every change on a grid, four hundred and sixty-two candidate worlds, of which four hundred and "
            "five flip the decision, and keeps the nearest by a weighted distance. <bookmark mark='d'/>Here is one: "
            "had your income been five thousand higher, your debt two thousand lower, and your time in the job two "
            "years longer, you would have been approved. This is Lewis's semantics, run as an algorithm: an explanation is a "
            "counterfactual true at the closest world."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(fl))
            vo.wait_until("b")
            self.play(FadeIn(app), FadeIn(at))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(GrowArrow(arr), FadeIn(cost), FadeIn(cw), FadeIn(ct), FadeIn(rows[2]))
        self.clear_scene()

    def ties(self):
        d = load("cfx")
        head = label(r"No unique closest world", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        hd = [r"\text{income}", r"\text{debt}", r"\text{years}", r"\text{distance}"]
        rows = []
        for c in d["closest"]:
            rows.append([MathTex(rf"+{c['income']}\text{{k}}", font_size=22), MathTex(rf"{c['debt']}\text{{k}}",
                                                                                         font_size=22),
                         MathTex(rf"+{c['years']}", font_size=22), MathTex(str(d["best_cost"]), font_size=22,
                                                                           color=OK)])
        for c in d["next"][:2]:
            rows.append([MathTex(rf"+{c['income']}\text{{k}}", font_size=22, color=GREY_B),
                         MathTex(rf"{c['debt']}\text{{k}}", font_size=22, color=GREY_B),
                         MathTex(rf"+{c['years']}", font_size=22, color=GREY_B),
                         MathTex(str(c["cost"]), font_size=22, color=GREY_B)])
        grid = ValueGrid(hd, rows, col_w=[1.8, 1.8, 1.6, 1.8], cell_h=0.48, font_size=20).move_to([-3.0, -0.3, 0])
        n = len(d["closest"])
        side = stack([(f"{n}" + r" worlds tie for closest", OK),
                      (r"Stalnaker \ (1968): \ there is always a unique closest world; \ Lewis \ (1973): \ not "
                       r"always", ABS),
                      (r"`if Bizet and Verdi had been compatriots, \ Bizet would have been Italian'? \ or Verdi "
                       r"French?", GOAL),
                      (r"for users: \ several explanations, \ and some are not actionable: \ you cannot add three "
                       r"years tonight \ (Ustun et al., \ 2019)", BAD)], font_size=19, aligned_edge=LEFT,
                     width=5.6).move_to([3.7, -0.3, 0])
        with self.voiceover(
            "There is a twist. <bookmark mark='a'/>The search finds not one closest world but four, all at the same "
            "distance: more income and fewer extra years, or less income and more years, each with the same small "
            "cut in debt. <bookmark mark='b'/>Robert Stalnaker's semantics for counterfactuals assumed that there is always a "
            "unique closest world; Lewis denied it. <bookmark mark='c'/>Take an example of Quine's: if Bizet and Verdi had been "
            "compatriots, would Bizet have been Italian, or Verdi French? Neither counterfactual is true, because "
            "the closest worlds tie. <bookmark mark='d'/>For a person who was refused, ties mean several explanations, "
            "and some of them describe worlds they cannot reach: no one can add three years of employment tonight. "
            "Berk Ustun and colleagues call the reachable ones actionable recourse."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(*[FadeIn(c) for c in grid.cell[r]]) for r in range(n)],
                                  lag_ratio=0.3), FadeIn(side[0]))
            self.play(*[FadeIn(c) for r in range(n, len(rows)) for c in grid.cell[r]])
            for mk, r in zip("bcd", side[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def problog(self):
        d = load("problog")
        head = label(r"Probabilities over possible worlds", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        prog = VGroup(*[label(r"\texttt{" + t + "}", font_size=19, color=c) for t, c in (
            (r"0.1 :: burglary.", NAME), (r"0.2 :: earthquake.", NAME), (r"0.7 :: hears(mary).", NAME),
            (r"alarm :- burglary.", WHITE), (r"alarm :- earthquake.", WHITE),
            (r"calls(mary) :- alarm, hears(mary).", WHITE))]).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(
            [-4.3, 1.3, 0])
        box = SurroundingRectangle(prog, buff=0.22, color=GREY_D, corner_radius=0.1)
        cells = VGroup()
        for i, w in enumerate(d["worlds"]):
            c = np.array([0.4 + 1.7 * (i % 4), 1.75 - 1.7 * (i // 4), 0])
            I = island(c, w=1.55, h=1.35, seed=220 + i, color=OK if w["calls"] else WORLD)
            fs = w["facts"]
            t = VGroup(label(("B" if fs["burglary"] else r"$\cdot$") + r" \ " + ("E" if fs["earthquake"] else
                                                                               r"$\cdot$") + r" \ " +
                             ("H" if fs["hears"] else r"$\cdot$"), font_size=18),
                       label(f"{w['p']:.3f}", font_size=16, color=GREY_A),
                       label(r"calls" if w["calls"] else r"\ ", font_size=15, color=OK)).arrange(DOWN, buff=0.05)
            cells.add(VGroup(I, t.move_to(c)))
        key = label(r"B: \ burglary; \ E: \ earthquake; \ H: \ Mary hears", font_size=16, color=GREY_A).move_to(
            [3.0, -0.9, 0])
        rows = stack([(r"each choice of the probabilistic facts is a world: \ $2^3 = 8$, \ with probability the "
                       r"product", WHITE),
                      (rf"$P(\text{{alarm}}) = {d['p_alarm']}$; \ \ $P(\text{{calls}}) = {d['p_calls']}$: \ add the "
                       r"worlds where it holds", OK),
                      (rf"$P(\text{{burglary}} \mid \text{{calls}}) = {d['p_burglary_given_calls']}$: \ inference is "
                       r"renormalizing over the worlds that fit", GOAL),
                      (r"Sato \ (1995); \ ProbLog \ (De Raedt et al., \ 2007): \ Carnap's state descriptions, \ with "
                       r"weights", ABS)], font_size=20, aligned_edge=LEFT, width=12.4).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Second, probabilities. <bookmark mark='a'/>Here is a tiny probabilistic logic program in the style of "
            "ProbLog. A burglary with probability one in ten, an earthquake with probability one in five, and Mary "
            "hearing the alarm with probability seven in ten. Rules say that either a burglary or an earthquake sets "
            "off the alarm, and that Mary calls if there is an alarm and she hears it. <bookmark mark='b'/>Taisuke "
            "Sato's distribution semantics: each choice of the probabilistic facts is a possible world, eight of "
            "them, with probability the product of the choices; the rules then settle everything else in each "
            "world. <bookmark mark='c'/>The probability of a query is the total probability of the worlds where it "
            "holds: the alarm sounds with probability zero point two eight, and Mary calls with probability zero "
            "point one nine six. <bookmark mark='d'/>Conditioning is renormalizing over the worlds that fit the "
            "evidence: given that Mary calls, the probability of a burglary is about thirty-six percent. "
            "<bookmark mark='e'/>Carnap's state descriptions, with weights, running in production."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(box), FadeIn(prog))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.1), FadeIn(key), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(*[Indicate(c[0].shape, color=OK) for c, w in zip(cells, d["worlds"]) if w["calls"]],
                      FadeIn(rows[1]))
            for mk, r in zip("de", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
