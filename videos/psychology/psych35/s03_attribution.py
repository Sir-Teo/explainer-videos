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
        cubes = VGroup()
        for k, (pat, nm, c) in enumerate((("person", r"the person", PERSON), ("entity", r"the entity", CROWD),
                                          ("circumstance", r"the occasion", MODEL))):
            cb = cube(pat).scale(0.8).move_to([-4.6 + 3.0 * k, 1.1, 0])
            sh = d[pat]["shares"]
            cap = VGroup(label(nm, font_size=20, color=c),
                         label(rf"person {sh['person']:.0%}, \ entity {sh['entity']:.0%}".replace("%", r"\%"),
                               font_size=14, color=GREY_A)).arrange(DOWN, buff=0.08).next_to(cb, DOWN, buff=0.2)
            cubes.add(VGroup(cb, cap))
        rows = rows_of([
            (r"Kelley, \ 1967: \ explain a behaviour the way a scientist explains an effect, \ by what it varies "
             r"with: \ persons, \ entities, \ occasions", WHITE),
            (r"consensus: \ do others do it too? \ distinctiveness: \ only with this entity? \ consistency: \ every "
             r"time?", CROWD),
            (r"low consensus, \ low distinctiveness, \ high consistency: \ the person; \ all three high: \ the "
             r"entity; \ low consistency: \ the occasion", PERSON),
            (r"Psyche reads each pattern as an analysis of variance: \ the main effect that carries the variance "
             r"is the cause", MODEL),
        ], 12.4, 20, 0.26).move_to([0, -2.3, 0])
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
            self.play(FadeIn(head), FadeIn(tag), LaggedStart(*[FadeIn(c_[0]) for c_ in cubes], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(*[FadeIn(c_[1]) for c_ in cubes], FadeIn(rows[3]))
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
