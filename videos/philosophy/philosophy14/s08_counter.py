from __future__ import annotations

from videos.philosophy.philosophy14.common import *  # noqa: F403

ORDER = ["strengthening", "transitivity", "contraposition", "excluded middle", "disjunctive antecedents"]
TITLES = {"strengthening": r"Strengthening the antecedent", "transitivity": r"Transitivity",
          "contraposition": r"Contraposition", "excluded middle": r"Conditional excluded middle",
          "disjunctive antecedents": r"Simplifying disjunctive antecedents"}
FORMS = {"strengthening": (r"A > C", r"(A \land B) > C"), "transitivity": (r"A > B,\ \ B > C", r"A > C"),
         "contraposition": (r"A > C", r"\lnot C > \lnot A"), "excluded middle": (r"", r"(A > C) \lor (A > \lnot C)"),
         "disjunctive antecedents": (r"(A \lor B) > C", r"A > C")}
WHO = {"strengthening": r"Goodman's match", "transitivity": r"Stalnaker's Hoover", "contraposition": r"Goethe",
       "excluded middle": r"Bizet and Verdi \ (Quine)", "disjunctive antecedents": r"Spain in 1940 \ (McKay and "
                                                                                    r"van Inwagen)"}


def similarity(worlds, center, step=1.05, font_size=18) -> VGroup:
    """The actual world in the middle; the others on rings by distance."""
    c = np.asarray(center, float)
    g = VGroup()
    rings = VGroup()
    dists = sorted({w["dist"] for w in worlds})
    for k, dd in enumerate(dists):
        rings.add(Circle(radius=step * (k + 1), stroke_color=SPH, stroke_width=1.5).move_to(c))
    act = VGroup(Dot(c, radius=0.1, color=BEL), label(r"actual", font_size=font_size, color=BEL).next_to(
        c, DOWN, buff=0.08))
    pts, tags = {}, {}
    by = {}
    for w in worlds:
        by.setdefault(w["dist"], []).append(w)
    for dd, ws in by.items():
        k = dists.index(dd)
        r = step * (k + 1)
        base = [150, 80, -40, -110][min(k, 3)] * DEGREES
        for i, w in enumerate(ws):
            a = base + (i - (len(ws) - 1) / 2) * 75 * DEGREES
            u = np.array([np.cos(a), np.sin(a), 0])
            p = c + r * u
            pts[w["world"]] = p
            dot = Dot(p, radius=0.09, color=WHITE)
            t = label(w["world"], font_size=font_size)
            t.move_to(p + u * (0.34 + 0.5 * t.width * abs(np.cos(a)) + 0.5 * t.height * abs(np.sin(a))))
            tags[w["world"]] = VGroup(dot, t)
    g.add(rings, act, *tags.values())
    g.pts, g.tags = pts, tags
    return g


class Counter(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"Counterfactuals", r"What would have happened if?", lit=(1968, 1973), part=PART)
        with self.voiceover("Chapter seven. Counterfactuals."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.semantics()
        for k in ORDER:
            self.model(k)
        self.limits()
        self.critics()
        self.explanations()

    def semantics(self):
        hcs = VGroup(history_card(1968, r"Robert Stalnaker", r"`A Theory of Conditionals'", width=4.4, color=HIST),
                     history_card(1973, r"David Lewis", r"\textit{Counterfactuals}", width=3.8, color=HIST)).arrange(
            RIGHT, buff=0.4).to_edge(UP, buff=0.35)
        rule = MathTex(r"A > C \text{ is true at } w \iff C \text{ holds at all the } A\text{-worlds closest to } w",
                       font_size=32, color=NEW).next_to(hcs, DOWN, buff=0.5)
        rows = stack([
            (r"closeness: \ overall similarity to $w$; \ $w$ is closest to itself", WHITE),
            (r"Lewis: \ ties allowed; \ \ Stalnaker: \ always one closest $A$-world", GREY_A),
            (r"the same spheres as Grove's, \ now around a world instead of a belief set", BEL),
            (r"modus ponens holds: \ if $A$ is true here, \ the closest $A$-world is here", OK),
            (r"but five inferences valid for $\to$ \ fail for $>$", BAD),
        ], font_size=24, buff=0.3, width=12.4).next_to(rule, DOWN, buff=0.45)
        with self.voiceover(
            "Counterfactuals got their modern semantics from Robert Stalnaker in 1968 and David Lewis in 1973. "
            "<bookmark mark='a'/>If A had been the case, C would have been, is true at a world when C holds at all the "
            "A-worlds closest to it. <bookmark mark='b'/>Closeness is overall similarity, and each world is closest to "
            "itself. <bookmark mark='c'/>Lewis allows ties; Stalnaker insists there is always exactly one closest "
            "A-world. <bookmark mark='d'/>These are Grove's spheres again, now centred on a world rather than on a "
            "belief set. <bookmark mark='e'/>Modus ponens holds: if A is true here, then here is the closest A-world. "
            "<bookmark mark='f'/>But five inferences that are valid for the material conditional fail. The Reasoner "
            "builds a small model for each."
        ) as vo:
            self.play(FadeIn(hcs))
            vo.wait_until("a")
            self.play(Write(rule))
            for mk, r in zip("bcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def model(self, key):
        d = load("counter")["models"][key]
        head = label(TITLES[key], font_size=30, color=CONN).to_edge(UP, buff=0.3)
        who = label(WHO[key], font_size=21, color=GREY_B).next_to(head, DOWN, buff=0.12)
        prem, conc = FORMS[key]
        form = MathTex((prem + r"\ \ \vDash_{\to}\ \ " if prem else r"\vDash_{\to}\ \ ") + conc, font_size=30,
                       color=GREY_A).next_to(who, DOWN, buff=0.25)
        sim = similarity(d["worlds"], [-3.6, -1.3, 0], step=1.0 if len(d["worlds"]) > 2 else 1.25)
        lines = VGroup()
        for p, ok in zip(d["gloss"][:len(d["premises"])], d["premises_hold"]):
            lines.add(VGroup(label(rf"`{p}'", font_size=20), mark(ok, 24)).arrange(RIGHT, buff=0.25))
        concl_gloss = d["gloss"][-1] if key != "excluded middle" else d["gloss"][0] + r" \ \dots"
        if key == "excluded middle":
            lines.add(VGroup(label(rf"`{d['gloss'][0]}'", font_size=20), mark(False, 24)).arrange(RIGHT, buff=0.25))
            lines.add(VGroup(label(r"`\dots \ he would not have been Italian'", font_size=20), mark(False, 24)).arrange(
                RIGHT, buff=0.25))
        else:
            lines.add(VGroup(label(rf"`{concl_gloss}'", font_size=20, color=BAD),
                             mark(d["conclusion_holds"], 24)).arrange(RIGHT, buff=0.25))
        for ln in lines:
            if ln.width > 6.6:
                ln.width = 6.6
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.3, -0.6, 0])
        why = {
            "strengthening": r"the nearest struck world is dry; \ the nearest struck-and-wet world doesn't light",
            "transitivity": r"the nearest communist Hoover is American, \ and a traitor; \ the nearest Russian one is "
                            r"neither traitor nor American",
            "contraposition": r"the nearest world where he lived on still has him dead now",
            "excluded middle": r"two compatriot worlds tie: \ Lewis says neither conditional is true; \ Stalnaker "
                               r"must pick one",
            "disjunctive antecedents": r"the nearest Axis-or-Allies world is an Axis world; \ the nearest Allies "
                                       r"world is not",
        }[key]
        foot = label(why, font_size=20, color=GOAL).to_edge(DOWN, buff=0.3)
        if foot.width > 12.8:
            foot.width = 12.8
        closest = {"strengthening": ["struck, dry, lights", "struck, wet, no light"],
                   "transitivity": ["American communist", "Russian communist"],
                   "contraposition": ["lived on, now dead", "lived on, alive now"],
                   "excluded middle": ["both Italian", "both French"],
                   "disjunctive antecedents": ["joined the Axis", "joined the Allies"]}[key]
        if key == "strengthening":
            with self.voiceover(
                "Strengthening the antecedent, Nelson Goodman's match. <bookmark mark='a'/>If I had struck this "
                "match, it would have lit. True: the nearest world where it is struck is one where it is dry, and "
                "lights. <bookmark mark='b'/>If I had struck it and it had been wet, it would have lit. False: "
                "the nearest such world has a wet match that doesn't light. <bookmark mark='c'/>Adding to the "
                "antecedent can carry you to farther worlds."
            ) as vo:
                self._body(vo, head, who, form, sim, lines, closest, foot)
        elif key == "transitivity":
            with self.voiceover(
                "Transitivity, from Stalnaker. <bookmark mark='a'/>If J. Edgar Hoover had been born in Russia, he "
                "would have been a communist. If he had been a communist, he would have been a traitor. <bookmark "
                "mark='b'/>But not: if he had been born in Russia, he would have been a traitor. <bookmark "
                "mark='c'/>The nearest communist Hoover is an American traitor; the nearest Russian Hoover is a "
                "loyal Soviet citizen."
            ) as vo:
                self._body(vo, head, who, form, sim, lines, closest, foot)
        elif key == "contraposition":
            with self.voiceover(
                "Contraposition. <bookmark mark='a'/>If Goethe had lived past 1832, he would still be dead now. "
                "True. <bookmark mark='b'/>Contrapose: if Goethe were alive now, he would not have lived past "
                "1832. Absurd. <bookmark mark='c'/>The nearest world where he lived on is still one where he died "
                "long ago."
            ) as vo:
                self._body(vo, head, who, form, sim, lines, closest, foot)
        elif key == "excluded middle":
            with self.voiceover(
                "Conditional excluded middle, with Quine's Bizet and Verdi. <bookmark mark='a'/>If they had been "
                "compatriots, would Bizet have been Italian? Or Verdi French? <bookmark mark='b'/>The two "
                "compatriot worlds are equally close. Lewis: neither conditional is true, and the disjunction of "
                "the two fails. <bookmark mark='c'/>Stalnaker keeps the law of conditional excluded middle by "
                "insisting on one closest world; the Reasoner confirms it holds once the tie is broken, and says "
                "the choice between them is indeterminate."
            ) as vo:
                self._body(vo, head, who, form, sim, lines, closest, foot)
        elif key == "disjunctive antecedents":
            with self.voiceover(
                "Simplifying disjunctive antecedents. <bookmark mark='a'/>If Spain had fought in the war, on "
                "either side, it would have joined the Axis: plausible, given Franco. <bookmark "
                "mark='b'/>Simplify: if Spain had joined the Allies, it would have joined the Axis. Absurd. "
                "<bookmark mark='c'/>Yet the simplification seems valid in ordinary talk; many semanticists now "
                "treat disjunctive antecedents as a special case."
            ) as vo:
                self._body(vo, head, who, form, sim, lines, closest, foot)
        self.clear_scene()

    def _body(self, vo, head, who, form, sim, lines, closest, foot):
        self.play(FadeIn(head), FadeIn(who), FadeIn(form), FadeIn(sim))
        vo.wait_until("a")
        self.play(Create(Circle(radius=0.26, color=NEW, stroke_width=4).move_to(sim.pts[closest[0]])),
                  FadeIn(lines[0]))
        if len(lines) > 2:
            self.play(FadeIn(lines[1]))
        vo.wait_until("b")
        self.play(Create(Circle(radius=0.26, color=BAD, stroke_width=4).move_to(sim.pts[closest[1]])),
                  FadeIn(lines[-1]))
        vo.wait_until("c")
        self.play(FadeIn(foot))

    def limits(self):
        d = load("counter")["cem_stalnaker"]
        head = label(r"Stalnaker or Lewis?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        line = NumberLine(x_range=[1.0, 1.5, 0.1], length=8.0, include_numbers=True, font_size=20,
                          color=GREY_C).move_to([0, 0.9, 0])
        pts = VGroup(*[Dot(line.n2p(1 + 1 / n), radius=0.06, color=NEW) for n in range(2, 40)])
        ll = label(r"`if this line were longer than 1 inch': \ 1.5, \ 1.33, \ 1.25, \ \dots \ no closest world",
                   font_size=22).next_to(line, DOWN, buff=0.45)
        rows = stack([
            (r"Stalnaker: \ a unique closest world \ \ $\Rightarrow$ \ conditional excluded middle", BEL),
            (r"Lewis: \ ties, \ and no limit assumption: \ true iff some sphere makes $A \to C$ hold throughout", BEL),
            (rf"the Reasoner: \ with the Bizet--Verdi tie broken, \ excluded middle holds"
             + (r" \ $\checkmark$" if d["cem"] else ""), OK),
            (r"similarity itself: \ Lewis \ (1979): \ avoid big miracles, \ then keep the most matching facts \ "
             r"(Part 17)", GREY_A),
        ], font_size=22, buff=0.3, width=12.4).next_to(ll, DOWN, buff=0.45)
        with self.voiceover(
            "Which semantics is right? <bookmark mark='a'/>Lewis's line: if this line were longer than one inch. "
            "There are worlds where it is one and a half inches, one and a third, one and a quarter, and so on: no "
            "closest one. <bookmark mark='b'/>Stalnaker assumes there always is a closest antecedent world, which buys "
            "him conditional excluded middle. <bookmark mark='c'/>Lewis allows ties and drops the limit assumption: "
            "the counterfactual is true when some sphere around the world makes the material conditional hold "
            "throughout. <bookmark mark='d'/>The Reasoner confirms that once the Bizet and Verdi tie is broken, "
            "excluded middle holds, as Stalnaker says. <bookmark mark='e'/>And what makes worlds similar? Lewis's 1979 "
            "answer, which matters for causation in Part 17: first avoid big violations of law, then keep as many "
            "particular facts as possible."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(line), LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.05), FadeIn(ll))
            for mk, r in zip("bcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def critics(self):
        hc = history_card(1975, r"Kit Fine", r"review of Lewis's \textit{Counterfactuals}", width=5.4,
                          color=HIST).to_corner(UL, buff=0.35)
        nixon = stack([
            (r"`If Nixon had pressed the button, \ there would have been a nuclear holocaust.'", WHITE),
            (r"true, \ surely", OK),
            (r"but a world where a small fault stops the missiles \ looks far \textit{more} like ours", BAD),
        ], font_size=23).next_to(hc, DOWN, buff=0.4).set_x(0)
        prio = VGroup(label(r"Lewis \ (1979): \ similarity, \ in order of importance", font_size=24, color=BEL),
                      *[label(t, font_size=21) for t in (
                          r"1. \ avoid big, \ widespread violations of law",
                          r"2. \ maximize the region of perfect match of particular fact",
                          r"3. \ avoid small, \ local violations of law",
                          r"4. \ approximate similarity of particular fact: \ hardly matters")]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).next_to(nixon, DOWN, buff=0.45)
        foot = label(r"a small miracle at the button, \ then the laws take over: \ the holocaust world wins",
                     font_size=22, color=GOAL).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Kit Fine raised the strongest objection to similarity. <bookmark mark='a'/>If Nixon had pressed the "
            "button, there would have been a nuclear holocaust. <bookmark mark='b'/>Surely true. "
            "<bookmark mark='c'/>But a world where he presses it and a small electrical fault stops the missiles is "
            "far more like ours than one with a nuclear war. So similarity seems to make the counterfactual false. "
            "<bookmark mark='d'/>Lewis answered in 1979 by saying which similarities count, in order: first, avoid "
            "big, widespread violations of law; second, keep as large a region of exact match as possible; third, "
            "avoid even small violations; and approximate match of particular fact hardly matters. "
            "<bookmark mark='e'/>Then the closest world has one small miracle that gets the button pressed, and after "
            "that the laws run their course. The holocaust world wins. Lewis built his theory of causation, and the "
            "direction of time, on this ordering; Part 17 tests it."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abc", nixon):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(m) for m in prio], lag_ratio=0.3), run_time=4)
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def explanations(self):
        d = load("explain")
        head = label(r"Counterfactual explanations", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        sub = label(r"Wachter, \ Mittelstadt \ and Russell \ (2017): \ explain a decision by the closest world "
                    r"where it differs", font_size=21, color=GREY_A).next_to(head, DOWN, buff=0.2)
        ax = Axes(x_range=[30, 80, 10], y_range=[0, 6, 1], x_length=6.0, y_length=4.0, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 18}).move_to([-3.2, -1.0, 0])
        xl = label(r"income (\$k)", font_size=19, color=GREY_B).next_to(ax.x_axis, DOWN, buff=0.35)
        yl = label(r"years employed", font_size=19, color=GREY_B).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.35)
        line = ax.plot(lambda inc: (45 - 0.6 * inc) / 3, x_range=[55, 75], color=BEL, stroke_width=3)
        ll = label(r"approve above", font_size=18, color=BEL).next_to(ax.c2p(70, 1.6), UR, buff=0.05)
        x0 = ax.c2p(d["applicant"]["income_k"], d["applicant"]["years"])
        me = Dot(x0, color=BAD, radius=0.09)
        mel = label(r"refused", font_size=18, color=BAD).next_to(me, DOWN, buff=0.1)
        p1 = ax.c2p(d["applicant"]["income_k"] + d["l1"]["income_k"], d["applicant"]["years"] + d["l1"]["years"])
        p2 = ax.c2p(d["applicant"]["income_k"] + d["l2"]["income_k"], d["applicant"]["years"] + d["l2"]["years"])
        a1 = Arrow(x0, p1, buff=0.05, color=OK, stroke_width=4)
        a2 = Arrow(x0, p2, buff=0.05, color=NEW, stroke_width=4)
        rows = stack([
            (r"approve if \ $0.6 \cdot \text{income} + 3 \cdot \text{years} \geq 45$", WHITE),
            (rf"applicant: \ \${d['applicant']['income_k']}k, \ {d['applicant']['years']} years: \ refused", BAD),
            (rf"closest by $L_1$: \ `with \${d['l1']['income_k']:.0f}k more income, \ you'd be approved'", OK),
            (rf"closest by $L_2$: \ \${d['l2']['income_k']:.0f}k more \textit{{and}} {12 * d['l2']['years']:.0f} more "
             r"months", NEW),
            (r"which world is `closest' is a choice: \ Lewis's problem, \ in a credit office", GOAL),
        ], font_size=21, aligned_edge=LEFT, width=6.2).move_to([3.5, -0.9, 0])
        with self.voiceover(
            "Counterfactuals now explain the decisions of machines. <bookmark mark='a'/>Sandra Wachter, Brent "
            "Mittelstadt and Chris Russell proposed explaining an automated decision by the closest world in which it "
            "would have gone the other way. <bookmark mark='b'/>Take a simple loan rule. <bookmark mark='c'/>An "
            "applicant with fifty thousand dollars of income and two years in her job is refused. "
            "<bookmark mark='d'/>The closest approval, counting each change separately, is: with fifteen thousand "
            "more income, you would have been approved. <bookmark mark='e'/>Measured by straight-line distance, it is "
            "twelve thousand more income and seven more months in the job. <bookmark mark='f'/>Which world counts as "
            "closest is a choice, and it changes the explanation the applicant receives. Lewis's problem of "
            "similarity, in a credit office."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(sub))
            vo.wait_until("b")
            self.play(FadeIn(ax), FadeIn(xl), FadeIn(yl), Create(line), FadeIn(ll), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(me), FadeIn(mel), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(GrowArrow(a1), FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(GrowArrow(a2), FadeIn(rows[3]))
            vo.wait_until("f")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
