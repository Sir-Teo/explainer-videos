from __future__ import annotations

from videos.economics.econ37.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.checkerboard()
        self.lumpy()
        self.question()
        self.title()
        self.objectives()

    def checkerboard(self):
        S = load("schelling")
        frames = S["frames"]
        sq = board(frames[0], size=5.6).move_to(LEFT * 2.9 + DOWN * 0.2)
        like = DecimalNumber(100 * S["like"][0], num_decimal_places=0, font_size=56, color=E.ACCENT)
        pc = label(r"\%", font_size=40, color=E.ACCENT)
        meter = VGroup(like, pc).arrange(RIGHT, buff=0.08)
        rnd = Integer(0, font_size=34, color=GREY_A)
        side = VGroup(
            label(r"a coin's neighbours \\ who are its own kind", font_size=20, color=GREY_A),
            meter,
            VGroup(label(r"round", font_size=24, color=GREY_A), rnd).arrange(RIGHT, buff=0.2),
            label(r"the rule: \ content if at least \\ a third of the neighbours \\ are its own kind", font_size=20,
                  color=WHITE),
        ).arrange(DOWN, buff=0.4).move_to(RIGHT * 3.9 + UP * 0.3)
        head = label(r"Thomas Schelling's checkerboard", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.35)
        tag = published_tag(tables.SCHELLING_1971.tag + r"; \ played by Agora", corner=DR, font_size=12)
        with self.voiceover(
            "Around 1969 the economist Thomas Schelling began a game with coins on a checkerboard. "
            "<bookmark mark='a'/> Two kinds of coin, scattered at random, with a tenth of the squares left empty. "
            "Each coin looks at its eight neighbours. <bookmark mark='b'/> The rule: a coin is content if at least "
            "a third of its neighbours are its own kind. Otherwise it moves to an empty square where it would be "
            "content. No coin minds being in the minority, and no coin wants a neighbourhood of its own kind. "
            "<bookmark mark='c'/> Here is the board, played round by round."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(sq, lag_ratio=0.002), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(FadeIn(side[3]))
            vo.wait_until("c")
        with self.voiceover(
            f"In the first round {S['unhappy'][0]} coins are discontented, and move. Each move makes some "
            "neighbours less content, and they move in turn. <bookmark mark='a'/> "
            f"After {S['rounds']} rounds nobody wants to move, and the "
            f"average coin's neighbours are {100 * S['final']:.0f} percent its own kind, up from half. "
            "<bookmark mark='b'/> Mild preferences, an extreme result: a pattern that nobody chose. Schelling "
            "published the model in 1971, and it became a classic of how choices about where to live add up to a "
            "map."
        ) as vo:
            for k in range(1, len(frames)):
                anims = recolour(sq, frames[k - 1], frames[k])
                self.play(*anims, like.animate.set_value(100 * S["like"][k]), rnd.animate.set_value(k),
                          run_time=1.6)
            vo.wait_until("a")
            self.play(Indicate(meter, color=WHITE, scale_factor=1.15))
            vo.wait_until("b")
        self.clear_scene()

    def lumpy(self):
        Z = load("zipf")
        pops = np.array(Z["pops"])
        top10 = pops[:10].sum() / pops.sum()
        ax = plane([0.4, 10.6], [0, 21], center=LEFT * 1.6 + DOWN * 0.45, x_length=8.8, y_length=4.6, xticks=[],
                   yticks=[0, 5, 10, 15, 20], ylabel=r"people, \ millions, \ 2024", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        bars, nms = VGroup(), VGroup()
        for k in range(10):
            v = pops[k] / 1e6
            p0, p1 = ax.ax.c2p(k + 0.62, 0), ax.ax.c2p(k + 1.38, v)
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=CITY, fill_opacity=0.85,
                               stroke_width=0).move_to((p0 + p1) / 2))
            nms.add(label(Z["names"][k], font_size=13, color=GREY_A).rotate(PI / 5).next_to(
                ax.ax.c2p(k + 1, 0), DOWN, buff=0.25))
        side = VGroup(
            label(rf"{Z['n']} metropolitan areas \\ hold {pops.sum() / 1e6:.0f} million people", font_size=19,
                  color=WHITE),
            label(rf"the ten largest: \\ {100 * top10:.0f}\% of them", font_size=19, color=CITY),
            label(rf"New York alone: \\ {pops[0] / 1e6:.1f} million", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.4)
        tag = data_tag(r"US Census Bureau, \ Vintage 2024 estimates", corner=DR, font_size=12)
        with self.voiceover(
            "People sort themselves at every scale, and so does economic activity. Here are America's ten largest "
            f"metropolitan areas in 2024. <bookmark mark='a'/> The country's {Z['n']} metropolitan areas hold "
            f"{pops.sum() / 1e6:.0f} million people; <bookmark mark='b'/> the ten largest hold "
            f"{100 * top10:.0f} percent of them, <bookmark mark='c'/> and New York alone "
            f"{pops[0] / 1e6:.1f} million, more than most countries. Land is cheap almost everywhere, yet people "
            "pay enormous rents to crowd into a few places."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1),
                      FadeIn(nms), run_time=2.5)
            for mk, r_ in zip("abc", side):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.15))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 38, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"why do people and firms crowd together, \ and pay so much to do it?", font_size=26, color=CITY),
            label(r"why are cities' sizes so regular, \ and their rents so high?", font_size=26, color=RENT),
            label(r"what does a place do to the people who grow up in it?", font_size=26, color=AMENITY),
            label(r"can policy move activity, \ and should it?", font_size=26, color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "This part's question: why is economic activity piled up in a few places, and what does that do to the "
            "people in them? <bookmark mark='a'/> Why do people and firms crowd together, and pay so much to do it? "
            "<bookmark mark='b'/> Why are the sizes of cities so regular, and their rents so high? "
            "<bookmark mark='c'/> What does a place do to the children who grow up in it? <bookmark mark='d'/> And "
            "can policy move economic activity, and should it?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        S = load("schelling")
        logo = board(S["frames"][-1], size=1.7)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 37 \ $\cdot$ \ Cities and Regions", font_size=34, color=E.ACCENT)
        VGroup(logo, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part thirty-seven: cities and regions."):
            self.play(FadeIn(logo, lag_ratio=0.002), run_time=1.6)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act VII \ $\cdot$ \ The World Economy", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"Schelling's board, \ played; \ von Th\"unen's rings; \ the monocentric city",
            r"why cities exist: \ sharing, \ matching, \ learning; \ Zipf's law; \ core and periphery",
            r"spatial equilibrium: \ wages, \ rents and amenities; \ housing supply; \ rent control",
            r"neighbourhoods and children; \ the Berlin Wall; \ railways and highways",
            r"place-based policy; \ two dials; \ remote work and the climate",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "Here is the plan. <bookmark mark='a'/> Schelling's board, played; the rings of land use around a "
            "market town; and the model of a city with one centre. <bookmark mark='b'/> Why cities exist at all, "
            "the strange regularity of their sizes, and how a country splits into a core and a periphery. "
            "<bookmark mark='c'/> Spatial equilibrium, where wages, rents and the pleasures of a place move "
            "together; the supply of housing; and rent control. <bookmark mark='d'/> What neighbourhoods do to "
            "children; the Berlin Wall as an experiment; railways and highways. <bookmark mark='e'/> And policies "
            "aimed at places, two dials, and the frontier: working from home, and the climate."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
