from __future__ import annotations

from videos.economics.econ36.common import *  # noqa: F403


def web_point(lat: float, lon: float) -> np.ndarray:
    """A simple equirectangular map, scaled to the frame."""
    return np.array([lon / 180 * 6.2, lat / 90 * 3.0 - 0.3, 0])


class Hook(VoiceoverScene):
    def construct(self):
        self.box()
        self.web()
        self.question()
        self.title()
        self.objectives()

    def box(self):
        I_ = tables.IDEAL_X.data
        cards = point_cards([
            (r"26 April 1956", r"a converted tanker, \\ the \emph{Ideal X}, \\ leaves Newark for Houston", ARCH),
            (rf"{I_['trailers']} boxes", r"truck trailers \\ lifted on deck \\ by crane", WHITE),
            (r"loading by hand", rf"about \${I_['hand']:.2f} a ton, \\ by McLean's reckoning", TARIFF),
            (r"loading boxes", rf"under {100 * I_['box']:.0f} cents a ton", GAIN),
        ], width=12.8, cols=4, font_size=20).move_to(DOWN * 0.2)
        head = label(r"Malcom McLean's box", font_size=32, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.IDEAL_X.tag, corner=DR, font_size=12)
        with self.voiceover(
            "On the twenty-sixth of April 1956 a converted wartime tanker, the Ideal X, left Port Newark for Houston. "
            "<bookmark mark='a'/> On its deck were fifty-eight truck trailers, lifted aboard by crane, with the "
            "goods still inside. Its owner, Malcom McLean, ran a trucking company. <bookmark mark='b'/> Loading a "
            "ship by hand, sack by sack and crate by crate, cost by his reckoning about five dollars and eighty-three "
            "cents a ton. <bookmark mark='c'/> Loading his boxes cost under sixteen cents. <bookmark mark='d'/> "
            "Today most manufactured goods that cross an ocean travel in such boxes, and trade has grown into "
            "something the theories of the last part could not explain."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            for mk, c in zip("abc", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(Indicate(cards.cards[3], color=WHITE, scale_factor=1.03))
        self.clear_scene()

    def web(self):
        W = load("web")
        frame = Rectangle(width=12.6, height=6.0, stroke_color=GREY_D, stroke_width=1).move_to(DOWN * 0.3)
        nodes = VGroup()
        pos = {}
        for c, (lat, lon) in W["nodes"].items():
            pos[c] = web_point(lat, lon)
            node = VGroup(Dot(pos[c], radius=0.06, color=WHITE))
            if c not in ("GBR", "FRA", "ITA", "ESP", "NLD", "CHE"):
                node.add(label(c, font_size=13, color=GREY_A).next_to(pos[c], UP, buff=0.05))
            nodes.add(node)
        vmax = max(v for _, _, v in W["links"])
        links = VGroup(*[Line(pos[a], pos[b], stroke_width=0.6 + 7 * v / vmax,
                              color=CHINA if "CHN" in (a, b) else (USA if "USA" in (a, b) else ARCH),
                              stroke_opacity=0.75) for a, b, v in W["links"]])
        a, b, v = W["largest"]
        side = label(rf"the forty largest flows among twenty economies, \ 2019 \ (Europe's six unlabelled); \ the "
                     rf"largest: \ {a}--{b}, \ \${v:.0f} billion", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.3)
        tag = data_tag(r"CEPII Gravity database (BACI), \ 2019", corner=DR, font_size=12)
        with self.voiceover(
            "Here is the result in 2019: the forty largest trade flows among twenty large economies, each line as "
            "thick as the trade along it. <bookmark mark='a'/> Two things stand out. The biggest flows run between "
            f"neighbours: the largest of all is between Mexico and the United States, about {v:.0f} billion dollars "
            "a year. <bookmark mark='b'/> And the rich economies trade enormous amounts with each other, Germany "
            "with France, Japan with America, often in the same kinds of goods. Neither fits the theories of Part "
            f"thirty-five, which predict trade between countries that differ. In all, the world traded about "
            f"{W['world_bn'] / 1000:.0f} trillion dollars of goods that year."
        ) as vo:
            self.play(FadeIn(frame), FadeIn(nodes), FadeIn(tag))
            self.play(LaggedStart(*[Create(ln) for ln in links], lag_ratio=0.05), run_time=3.0)
            vo.wait_until("a")
            self.play(FadeIn(side), Indicate(links[0], color=WHITE, scale_factor=1.0))
            vo.wait_until("b")
            self.play(*[Indicate(ln, color=WHITE, scale_factor=1.0) for ln, (x, y, _) in zip(links, W["links"])
                        if {x, y} <= {"DEU", "FRA", "NLD", "ITA", "GBR", "ESP", "CHE"}])
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 38, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"why do similar countries trade similar goods?", font_size=26, color=ARCH),
            label(r"why does trade fall so fast with distance, \ and stop at borders?", font_size=26, color=FISH),
            label(r"why do so few firms export, \ and what happens to the rest?", font_size=26, color=FIRM),
            label(r"what did imports from China do to American towns?", font_size=26, color=CHINA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "This part's question: why is most trade between similar countries, and what did a generation of "
            "imports from China do? <bookmark mark='a'/> Why do similar countries trade similar goods? "
            "<bookmark mark='b'/> Why does trade fall so fast with distance, and stop at borders? "
            "<bookmark mark='c'/> Why do so few firms export, and what happens to the rest? <bookmark mark='d'/> "
            "And what did the surge of imports from China do to the American towns that made the same things?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        F = load("film")
        mini = plane([1985, 2025], [0, 560], x_length=4.2, y_length=1.4)
        logo = path(mini, F["t"], F["v"], CHINA, 2.6, smooth=False)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 36 \ $\cdot$ \ Trade II: \ Scale, \ Firms and Gravity", font_size=34, color=E.ACCENT)
        VGroup(logo, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part thirty-six: scale, firms and gravity."):
            self.play(Create(logo), run_time=1.6)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act VII \ $\cdot$ \ The World Economy", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"cars for cars; \ variety and scale; \ the home-market effect",
            r"a game of guessing trade; \ gravity, \ distance and borders",
            r"firms: \ exporters are rare; \ Melitz's selection; \ Eaton and Kortum",
            r"one formula for the gains; \ a counterfactual on real data",
            r"the China shock; \ the tariffs of 2018 and 2025; \ value chains; \ three dials",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "Here is the plan. <bookmark mark='a'/> Trade in cars for cars, and the theory of variety and scale "
            "that explains it. <bookmark mark='b'/> A game of guessing trade flows, and the most successful equation "
            "in economics, gravity. <bookmark mark='c'/> Firms: why exporters are rare, and what trade does to the "
            "rest, with two models that put firms and countries together. <bookmark mark='d'/> One formula for the "
            "gains from trade, and a counterfactual computed on real trade data. <bookmark mark='e'/> And the "
            "evidence: the China shock, the tariffs of 2018 and 2025, value chains, and three dials."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
