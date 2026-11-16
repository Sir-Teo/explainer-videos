from __future__ import annotations

from videos.psychology.psych38.common import *  # noqa: F403


class Trolley(VoiceoverScene):
    def construct(self):
        self.card()
        self.machine()
        self.countries()
        self.consortium()

    def card(self):
        card = chapter_card(8, r"One trolley, \ forty-two countries", r"What is universal in moral judgment?",
                            lit={2018: r"Awad et al.", 2020: r"Awad et al.", 2022: r"Bago et al."}, part=PART,
                            scale=("person", "culture"), marr=("what",))
        with self.voiceover("Chapter eight. One trolley, forty-two countries."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def machine(self):
        head = heading(r"The Moral Machine")
        car = VGroup(RoundedRectangle(corner_radius=0.12, width=1.6, height=0.6, color=WEST, fill_opacity=0.8,
                                      stroke_width=0),
                     Circle(radius=0.16, color=GREY_B, fill_opacity=1).move_to([-0.5, -0.32, 0]),
                     Circle(radius=0.16, color=GREY_B, fill_opacity=1).move_to([0.5, -0.32, 0])).move_to([-5.0, 0.6, 0])
        road = VGroup(Line([-6.2, 0.2, 0], [-1.0, 0.2, 0], color=GREY_D, stroke_width=3),
                      Line([-3.4, 0.2, 0], [-1.0, -1.1, 0], color=GREY_D, stroke_width=3))
        ahead = VGroup(*[little_person(0.45, color=PERSON) for _ in range(3)]).arrange(RIGHT, buff=0.1)
        ahead.move_to([-1.6, 0.55, 0])
        side = VGroup(*[little_person(0.45, color=WORLD) for _ in range(2)]).arrange(RIGHT, buff=0.1)
        side.move_to([-1.4, -0.75, 0])
        rows = rows_of([
            (r"Awad and colleagues, \ 2018: \ an online game asked what a self-driving car with failed brakes "
             r"should do", WHITE),
            (r"40 million decisions in ten languages, \ from over 2.3 million people in 233 countries and "
             r"territories", WEST),
            (r"near-universal preferences: \ spare humans over animals, \ more lives over fewer, \ the young over "
             r"the old; \ their strength varied by region", GOOD),
            (r"a self-selected sample of website visitors: \ huge, \ but not a census of humanity", AUTH),
        ], 6.4, 19, 0.36).move_to([3.2, -0.2, 0])
        tag = published_tag(r"Awad et al.\ (2018)")
        with self.voiceover(
            "Moral psychology's most famous dilemma went global on the internet. <bookmark mark='a'/> In 2018 Edmond "
            "Awad and colleagues reported an online game that asked what a self-driving car with failed brakes "
            "should do: stay its course, or swerve and kill someone else. <bookmark mark='b'/> They collected forty "
            "million decisions in ten languages, from over two point three million people in two hundred and thirty-"
            "three countries and territories. <bookmark mark='c'/> Some preferences were nearly universal: spare "
            "humans over animals, more lives over fewer, the young over the old. How strongly varied by region. "
            "<bookmark mark='d'/> It's a self-selected sample of website visitors. Huge, but not a census of "
            "humanity."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(road), FadeIn(car), FadeIn(ahead), FadeIn(side))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), car.animate.shift(RIGHT * 1.0))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def countries(self):
        d = load("trolley")
        head = heading(r"Same order, \ different levels")
        share = np.asarray(d["share"], float)
        n = len(share)
        A = axes([-1, n], [0.2, 1.0], x_length=6.2, y_length=3.6, xticks=None, yticks=[0.25, 0.5, 0.75, 1.0],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"share who accept", xlabel=r"42 countries, \ "
                 r"ordered by Switch", center=[-3.0, -0.1, 0], font_size=14)
        cols = (WEST, MODEL, WORLD)
        dots = VGroup(*[scatter(A.ax, np.arange(n), share[:, k], c, radius=0.05) for k, c in enumerate(cols)])
        links = VGroup(*[Line(A.ax.c2p(i, share[i, 0]), A.ax.c2p(i, share[i, 2]), color=GREY_D, stroke_width=1.5)
                         for i in range(n)])
        key = legend([(WEST, r"Switch"), (MODEL, r"Loop"), (WORLD, r"Footbridge")], font_size=14).move_to(
            A.ax.c2p(33, 0.32))
        rows = rows_of([
            (r"Awad and colleagues, \ 2020: \ the classic cases from 70{,}000 people in 42 countries", WHITE),
            (r"on average 81\% accepted Switch, \ 72\% Loop and 51\% Footbridge; \ the order held in every one of "
             r"the 42 countries", WEST),
            (r"the levels varied: \ fewer accepted the sacrifices in Eastern countries", WORLD),
            (rf"Psyche's model: \ a case effect shared by all countries plus a country level, \ on the log-odds "
             rf"scale; \ simulated with these averages, \ the order holds in "
             rf"{100 * d['order_same']:.0f}\% of countries while the levels spread", MODEL),
        ], 5.8, 19, 0.34).move_to([3.6, -0.2, 0])
        tag = psyche_tag(r"\texttt{culture.trolley}; \ Awad et al.\ (2020)")
        with self.voiceover(
            "The same site also offered the classic cases. <bookmark mark='a'/> In 2020 Awad and colleagues "
            "analysed answers from seventy thousand people in forty-two countries. <bookmark mark='b'/> On average, "
            "eighty-one percent accepted Switch, seventy-two percent Loop, and fifty-one percent Footbridge. And the "
            "order held in every one of the forty-two countries. <bookmark mark='c'/> The levels varied. Fewer "
            "people accepted the sacrifices in Eastern countries. <bookmark mark='d'/> Psyche's model writes it "
            "down: a case effect shared by every country, plus a country level, on the log-odds scale. Simulated "
            "with these averages, the order holds everywhere while the levels spread. Universal structure, local "
            "settings."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(links), FadeIn(dots[0]), FadeIn(dots[1]), FadeIn(dots[2]),
                      FadeIn(key))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Indicate(dots[2], color=WORLD, scale_factor=1.05))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def consortium(self):
        head = heading(r"Personal force, \ in 45 countries")
        A = axes([-0.6, 1.6], [0, 1.0], x_length=4.0, y_length=3.0, xticks=None, yticks=None,
                 ylabel=r"acceptability", center=[-3.8, -0.2, 0], font_size=15)
        b = bars(A.ax, [0, 1], [0.72, 0.42], [WEST, WORLD], width=0.6)
        names = VGroup(wrapped_label(r"no personal force", 1.8, 15, WEST).next_to(A.ax.c2p(0, 0), DOWN, buff=0.15),
                       wrapped_label(r"personal force", 1.8, 15, WORLD).next_to(A.ax.c2p(1, 0), DOWN, buff=0.15))
        note = label(r"the direction reported, \ drawn schematically", font_size=13, color=GREY_B).next_to(
            A, DOWN, buff=0.55)
        rows = rows_of([
            (r"Bago and colleagues, \ 2022: \ Greene's experiments on personal force and intention, \ repeated in "
             r"45 countries on every inhabited continent", WHITE),
            (r"harm done by personal force, \ a push rather than a switch, \ was judged less acceptable in every "
             r"cultural cluster", WORLD),
            (r"its interaction with intention replicated in Western countries, \ and was inconclusive in "
             r"Eastern and Southern ones", MODEL),
            (r"and individualism or collectivism did not predict the judgments", YOU),
        ], 6.2, 19, 0.36).move_to([3.3, -0.2, 0])
        tag = published_tag(r"Bago et al.\ (2022)")
        with self.voiceover(
            "A planned test followed. <bookmark mark='a'/> In 2022 Bence Bago and a large team repeated Greene's "
            "experiments on personal force and intention in forty-five countries, on every inhabited continent. "
            "<bookmark mark='b'/> Harm done by personal force, a push rather than a switch, was judged less "
            "acceptable in every cultural cluster. <bookmark mark='c'/> Its interaction with intention replicated "
            "in Western countries, and was inconclusive in Eastern and Southern ones. <bookmark mark='d'/> And "
            "individualism or collectivism didn't predict the judgments. The Ledger marks the difference between "
            "switching and pushing as replicated across countries."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(note))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), *[GrowFromEdge(x, DOWN) for x in b])
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
