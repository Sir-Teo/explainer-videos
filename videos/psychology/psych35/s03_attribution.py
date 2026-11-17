from __future__ import annotations

from videos.psychology.psych35.common import *  # noqa: F403


def cube(pattern: str, size: float = 0.36) -> VGroup:
    """Kelley's cube as three 5x5 slices (occasions), persons down and entities across; filled where the behaviour
    happened."""
    g = VGroup()
    for o in range(3):
        sl = VGroup()
        for p in range(5):
            for e in range(5):
                on = (pattern == "person" and p == 0) or (pattern == "entity" and e == 0) or \
                     (pattern == "circumstance" and p == 0 and e == 0 and o == 0)
                sq = Square(side_length=size, stroke_width=1, stroke_color=GREY_C,
                            fill_color=PERSON if on else "#14181F", fill_opacity=1)
                sq.move_to([e * size, -p * size, 0])
                sl.add(sq)
        sl.shift(RIGHT * o * 0.35 + UP * o * 0.35)
        g.add(sl)
    return VGroup(*reversed(list(g)))


class Attribution(VoiceoverScene):
    def construct(self):
        self.card()
        self.kelley()
        self.essays()
        self.rational()
        self.biases()

    def card(self):
        card = chapter_card(2, r"Explaining behaviour", r"Was it the person, \ or the situation?",
                            lit={1958: r"Heider", 1967: r"Kelley; \ Jones \& Harris", 1995: r"Gilbert \& Malone"},
                            part=PART, scale=("person",), marr=("what", "how"))
        with self.voiceover("Chapter two. Explaining behaviour."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def kelley(self):
        d = load("kelley")
        head = heading(r"Kelley's cube: \ attribution as analysis of variance")
        sub = label(r"Kelley, \ 1967: \ explain a behaviour by what it varies with: \ persons, \ entities, \ occasions",
                    font_size=21, color=GREY_A).next_to(head, DOWN, buff=0.22)
        xs = [-5.3, -3.2, -1.05, 1.15, 3.3, 5.45]  # cube, points to, consensus, distinctiveness, consistency, Psyche
        ys = [1.0, -0.75, -2.5]
        hy = 2.3
        hdr = VGroup(*[VGroup(label(t, font_size=22, color=c), label(q, font_size=17, color=GREY_B)).arrange(
            DOWN, buff=0.08).move_to([x, hy, 0]) for x, t, q, c in (
            (xs[2], r"consensus", r"do others do it too?", CROWD),
            (xs[3], r"distinctiveness", r"only with this entity?", CROWD),
            (xs[4], r"consistency", r"every time?", CROWD))])
        cause_h = label(r"points to", font_size=22, color=GREY_A).move_to([xs[1], hy, 0])
        psy_h = VGroup(label(r"Psyche:", font_size=20, color=MODEL), label(r"share of variance", font_size=17,
                                                                         color=MODEL)).arrange(DOWN, buff=0.08)
        psy_h.move_to([xs[5], hy, 0])
        rules = VGroup(*[Line([-6.75, y - 0.88, 0], [6.75, y - 0.88, 0], color=GREY_D, stroke_width=1)
                         for y in ys[:2]])
        rules.add(Line([-6.75, hy - 0.45, 0], [6.75, hy - 0.45, 0], color=GREY_C, stroke_width=1.5))
        cubes, causes, cells, shares = VGroup(), VGroup(), VGroup(), VGroup()
        part_name = {"person": r"person", "entity": r"entity", "occasion": r"occasion",
                     "rest": r"one-off"}
        for k, (pat, nm, c) in enumerate((("person", r"the person", PERSON), ("entity", r"the entity", CROWD),
                                          ("circumstance", r"the occasion", MODEL))):
            cb = cube(pat).scale(0.62).move_to([xs[0], ys[k], 0])
            cubes.add(cb)
            causes.add(word_chip(nm, color=c, font_size=22, width=2.1).move_to([xs[1], ys[k], 0]))
            row = VGroup()
            for j, cue in enumerate(("consensus", "distinctiveness", "consistency")):
                hi = d[pat][cue] >= 0.5
                row.add(word_chip(r"high" if hi else r"low", color=GOOD if hi else GREY_B, font_size=21,
                                  width=1.3).move_to([xs[2 + j], ys[k], 0]))
            cells.add(row)
            sh = d[pat]["shares"]
            top = max(sh, key=lambda key: sh[key])
            shares.add(VGroup(label(pct(sh[top]), font_size=24, color=c),
                              label(part_name[top], font_size=18, color=GREY_A)).arrange(DOWN, buff=0.06)
                       .move_to([xs[5], ys[k], 0]))
        tag = psyche_tag(r"\texttt{social.kelley}")
        with self.voiceover(
            "In 1958 Heider described people as naive scientists, explaining behaviour by hidden causes. "
            "<bookmark mark='a'/> Kelley made the science explicit in 1967. Explain a behaviour the way a "
            "scientist explains an effect, by what it varies with: persons, entities and occasions. "
            "<bookmark mark='b'/> Three cues. Consensus: do other people do it too? Distinctiveness: does it happen "
            "only with this entity? Consistency: does it happen every time? <bookmark mark='c'/> Low consensus, "
            "low distinctiveness, high consistency points to the person. All three high points to the entity. Low "
            "consistency points to the occasion. <bookmark mark='d'/> Psyche reads each pattern as an analysis of "
            "variance. The main effect that carries the variance is the cause."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), LaggedStart(*[FadeIn(c_) for c_ in cubes], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(FadeIn(sub, shift=DOWN * 0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(h_, shift=DOWN * 0.1) for h_ in hdr], lag_ratio=0.4), Create(rules))
            vo.wait_until("c")
            for k in range(3):
                extra = [FadeIn(cause_h)] if k == 0 else []
                self.play(LaggedStart(*[FadeIn(c_) for c_ in cells[k]], lag_ratio=0.15),
                          FadeIn(causes[k], shift=LEFT * 0.1), *extra, run_time=0.9)
            vo.wait_until("d")
            self.play(FadeIn(psy_h), LaggedStart(*[FadeIn(s_, shift=LEFT * 0.1) for s_ in shares], lag_ratio=0.3))
        self.clear_scene()

    def essays(self):
        head = heading(r"The essay about Castro")
        A = axes([-0.6, 1.6], [10, 70], x_length=5.0, y_length=3.8, xticks=None, yticks=[10, 30, 50, 70],
                 yfmt=lambda v: f"{v:.0f}", ylabel=r"the writer's inferred attitude to Castro",
                 center=[-3.6, -0.3, 0], font_size=15)
        vals = [(0, 59.6, 17.4), (1, 44.1, 22.9)]
        b = VGroup()
        for x, pro, anti in vals:
            b.add(bars(A.ax, [x - 0.17, x + 0.17], [pro, anti], [GOOD, AUTH], width=0.3))
        names = VGroup(label(r"writer chose", font_size=16, color=GREY_A).next_to(A.ax.c2p(0, 10), DOWN, buff=0.2),
                       label(r"position assigned", font_size=16, color=GREY_A).next_to(A.ax.c2p(1, 10), DOWN,
                                                                                    buff=0.2))
        key = legend([(GOOD, r"pro-Castro essay"), (AUTH, r"anti-Castro essay")], font_size=15).next_to(A, UP, buff=0.1)
        rows = rows_of([
            (r"Jones and Harris, \ 1967: \ students read an essay for or against Fidel Castro and judged the "
             r"writer's true attitude", WHITE),
            (r"told the writer chose the side, \ they inferred matching attitudes: \ 59.6 against 17.4, \ on a scale "
             r"from 10 to 70", CROWD),
            (r"told the side was assigned, \ they still did: \ 44.1 against 22.9", AUTH),
            (r"the correspondence bias: \ inferring a disposition from behaviour the situation explains; \ Gilbert "
             r"and Malone's 1995 review gave it four causes", YOU),
        ], 5.8, 19, 0.32).move_to([3.4, -0.3, 0])
        tag = historical_tag(r"Jones \& Harris (1967); \ Gilbert \& Malone (1995)")
        with self.voiceover(
            "People don't always use the cube well. <bookmark mark='a'/> In 1967 Jones and Harris had "
            "students read an essay for or against Fidel Castro, and judge the writer's true attitude. "
            "<bookmark mark='b'/> When they were told the writer had chosen the side, they inferred a matching "
            "attitude, as anyone would. <bookmark mark='c'/> When they were told the side had been assigned, they "
            "still did, less strongly, but clearly. <bookmark mark='d'/> Inferring a disposition from behaviour "
            "that the situation explains is called the correspondence bias. In 1995 Daniel Gilbert and Patrick "
            "Malone's review traced it to four causes, from not seeing the situation to correcting for it too "
            "little."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(*[GrowFromEdge(r_, DOWN) for r_ in b[0]], FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(*[GrowFromEdge(r_, DOWN) for r_ in b[1]], FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def rational(self):
        d = load("essays")
        head = heading(r"A bias, \ or a reasonable inference?")
        A = axes([-0.6, 2.6], [-0.8, 0.8], x_length=5.4, y_length=3.6, xticks=None, yticks=[-0.6, 0, 0.6],
                 yfmt=lambda v: f"{v:g}", ylabel=r"inferred attitude \ (prior mean 0)", center=[-3.4, -0.4, 0],
                 font_size=15)
        b = VGroup()
        for k, key in enumerate(("pi100", "pi30", "pi0")):
            pro, anti = d[key]
            b.add(bars(A.ax, [k - 0.17, k + 0.17], [pro, anti], [GOOD, AUTH], width=0.3))
        zero = DashedLine(A.ax.c2p(-0.6, 0), A.ax.c2p(2.6, 0), color=GREY_C, stroke_width=1.5)
        names = VGroup(*[label(t, font_size=14, color=GREY_A).next_to(A.ax.c2p(k, -0.8), DOWN, buff=0.15)
                         for k, t in enumerate((r"chose", r"assigned, \ 30\% doubt", r"assigned, \ no doubt"))])
        rows = rows_of([
            (r"Psyche's observer: \ a writer who chooses argues for the side they hold; \ an assigned writer's "
             r"essay may still show their view, \ if the assignment did not fully bind them", WHITE),
            (rf"no doubt that the assignment bound the writer: \ nothing is inferred; \ a 30\% doubt: \ the essay "
             rf"still moves the estimate, \ {d['pi30'][0]:.2f} against {d['pi0'][0]:.2f}", MODEL),
            (r"so part of the correspondence bias is reasonable inference under uncertainty about the situation, "
             r"\ as Walker, \ Smith and Vul argued in 2022", PERSON),
            (r"the bias lies in how much people trust the behaviour over the situation, \ not in using it at all", YOU),
        ], 5.6, 19, 0.32).move_to([3.6, -0.3, 0])
        tag = psyche_tag(r"simulated; \ Walker, \ Smith \& Vul (2022)")
        with self.voiceover(
            "But is that a bias at all? <bookmark mark='a'/> Here's Psyche's observer. A writer who chooses argues "
            "for the side they hold. An assigned writer's essay might still show their view, if the assignment "
            "didn't fully bind them. <bookmark mark='b'/> With no doubt that the assignment bound the writer, "
            "nothing is inferred. With some doubt, thirty percent here, the essay still moves the estimate. "
            "<bookmark mark='c'/> So part of the correspondence bias is reasonable inference under uncertainty "
            "about the situation, as Walker, Smith and Vul argued in 2022. <bookmark mark='d'/> The bias lies in "
            "how much people trust the behaviour over the situation, not in using it at all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(zero), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), *[GrowFromEdge(r_, DOWN) for r_ in b[0]])
            vo.wait_until("b")
            self.play(*[FadeIn(r_) for r_ in b[1]], *[FadeIn(r_) for r_ in b[2]], FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def biases(self):
        head = heading(r"Four attribution biases, \ and their records")
        sub = label(r"as the textbooks list them", font_size=21, color=GREY_A).next_to(head, DOWN, buff=0.2)
        checks = verdict_row([
            (r"the fundamental attribution error \ (Ross, \ 1977): \ the essays reproduce, \ but the bias is weaker "
             r"when the situation is made plain, \ and in several East Asian samples", "replicated, smaller"),
            (r"the actor--observer asymmetry \ (Jones and Nisbett, \ 1971): \ I blame the situation, \ you blame "
             r"my character; \ Malle, \ 2006: \ 173 studies, \ close to zero overall", "failed"),
            (r"the self-serving bias: \ credit for success, \ circumstances for failure; \ Mezulis and colleagues, "
             r"\ 2004: \ large and robust, \ smaller in East Asian samples", "replicated"),
            (r"belief in a just world \ (Lerner and Simmons, \ 1966): \ observers who could not help a suffering "
             r"victim thought less of her; \ the theory's tests are uneven \ (Hafer and B\`egue, \ 2005)",
             "contested"),
        ], width=12.6, font_size=23)
        checks.move_to([0, -0.45, 0])
        tag = published_tag(r"Lerner \& Simmons (1966); \ Jones \& Nisbett (1971); \ Ross (1977); \ Mezulis et al.\ "
                            r"(2004); \ Hafer \& B\`egue (2005); \ Malle (2006)")
        with self.voiceover(
            "Textbooks file the correspondence bias in a list of attribution biases, and the list has fared "
            "unevenly. <bookmark mark='a'/> In 1977 Lee Ross named it the fundamental attribution error. The Castro "
            "essays reproduce, but the word fundamental hasn't held: the bias is weaker when the situation is made "
            "plain, and in several studies of East Asian participants. <bookmark mark='b'/> In 1971 Edward Jones "
            "and Richard Nisbett added a twist. Actors, they proposed, explain their own behaviour by the "
            "situation, while observers explain the same behaviour by the actor's character. "
            "<bookmark mark='c'/> It was taught for thirty years. Then in 2006 Bertram Malle pooled a hundred and "
            "seventy-three studies, and taken overall the asymmetry was close to zero. <bookmark mark='d'/> The "
            "self-serving bias, taking credit for success and blaming circumstances for failure, is the opposite "
            "case. In 2004 Amy Mezulis and colleagues pooled the studies and found it large and robust, though "
            "smaller in East Asian samples: a cousin of chapter five's better-than-average effect. "
            "<bookmark mark='e'/> And in 1966 Melvin Lerner and Carolyn Simmons had students watch a young woman "
            "apparently receive painful shocks for her mistakes. When they could do nothing to help her, they "
            "thought less of her. Lerner traced it to a belief in a just world: if the world is fair, victims must "
            "deserve what happens to them. <bookmark mark='f'/> Blaming innocent victims has reappeared in many "
            "experiments, but a 2005 review by Carolyn Hafer and Laurent Bègue found many of the theory's tests "
            "loose. <bookmark mark='g'/> Four entries in one list, and four different records. A list of biases is "
            "a list of claims, each to be checked on its own."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(checks.rows[0].claim, shift=RIGHT * 0.15))
            self.play(FadeIn(checks.rows[0].chip, scale=1.2))
            vo.wait_until("b")
            self.play(FadeIn(checks.rows[1].claim, shift=RIGHT * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(checks.rows[1].chip, scale=1.2))
            vo.wait_until("d")
            self.play(FadeIn(checks.rows[2].claim, shift=RIGHT * 0.15))
            self.play(FadeIn(checks.rows[2].chip, scale=1.2))
            vo.wait_until("e")
            self.play(FadeIn(checks.rows[3].claim, shift=RIGHT * 0.15))
            vo.wait_until("f")
            self.play(FadeIn(checks.rows[3].chip, scale=1.2))
            vo.wait_until("g")
            self.play(LaggedStart(*[Indicate(r_.chip, scale_factor=1.08) for r_ in checks.rows], lag_ratio=0.25))
        self.clear_scene()
