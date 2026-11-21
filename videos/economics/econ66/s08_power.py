from __future__ import annotations

from videos.economics.econ66.common import *  # noqa: F403


def hub_network(cut: bool = False, n: int = 10, r: float = 2.3):
    """A hub-and-spoke network: a hub (the dollar's clearing banks, a messaging system) in the middle and countries
    around it, with a few direct links between neighbours.  With ``cut``, one country's links to the hub are red and
    dashed."""
    hub = VGroup(Circle(radius=0.45, stroke_color=US, stroke_width=3, fill_color=US, fill_opacity=0.35),
                 label(r"hub", font_size=18, color=WHITE))
    nodes = VGroup()
    links = VGroup()
    for k in range(n):
        ang = 2 * np.pi * k / n + 0.2
        p = np.array([r * np.cos(ang), r * np.sin(ang), 0])
        c = TARIFF if (cut and k == 3) else ROW
        nodes.add(Circle(radius=0.2, stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=0.4).move_to(p))
        if cut and k == 3:
            links.add(DashedLine(p * 0.82, p / np.linalg.norm(p) * 0.5, color=TARIFF, stroke_width=2.5))
        else:
            links.add(Line(p * 0.88, p / np.linalg.norm(p) * 0.48, color=GREY_B, stroke_width=2))
    side = VGroup(*[Line(nodes[k].get_center(), nodes[(k + 1) % n].get_center(), color=GREY_D, stroke_width=1)
                    for k in range(0, n, 3)])
    return VGroup(side, links, nodes, hub)


class Power(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Weaponized interdependence", r"How does depending on a supplier, \ or a network, \ become "
             r"power over you?", "Chapter six. Weaponized interdependence.",
             lit={2019: "Farrell and Newman", 2023: "Clayton, Maggiori and Schreger"}, scale=("world",),
             horizon=("a year",))
        self.networks()
        self.dependence()
        self.hegemon()

    def networks(self):
        g = hub_network().move_to(LEFT * 3.2 + DOWN * 0.3)
        g2 = hub_network(cut=True).move_to(LEFT * 3.2 + DOWN * 0.3)
        rows = VGroup(
            label(r"the panopticon: \ the hub sees every transaction", font_size=20, color=US),
            label(r"the chokepoint: \ the hub can cut a country off", font_size=20, color=TARIFF),
            label(r"2012: \ Iranian banks cut off from SWIFT's messages", font_size=19, color=GREY_A),
            label(r"2022: \ about \$300 billion of Russia's reserves frozen", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 3.2 + UP * 0.2)
        tag = published_tag(r"Farrell and Newman, \ \emph{International Security} 44(1) (2019)", corner=DL,
                            font_size=12)
        with self.voiceover(
            "Henry Farrell and Abraham Newman argued in 2019 that globalization did not produce a flat network of "
            "equals. <bookmark mark='a'/> It produced hubs: the dollar's clearing banks, the messaging system "
            "SWIFT, a few cloud providers, a few chip foundries. Countries connect to each other through them. "
            "<bookmark mark='b'/> A state that controls a hub gains two powers. The panopticon: it sees every "
            "transaction that passes through. <bookmark mark='c'/> And the chokepoint: it can cut a country off. "
            "<bookmark mark='d'/> In 2012 Iranian banks were disconnected from SWIFT's messages. In 2022, after "
            "the invasion of Ukraine, about three hundred billion dollars of the Russian central bank's reserves "
            "held abroad were frozen. Interdependence, which economists had seen as a source of peace, had become "
            "a weapon."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(g), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), Indicate(g[3], color=US))
            vo.wait_until("c")
            self.play(Transform(g, g2), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2:]))
        self.clear_scene()

    def dependence(self):
        Pw = load("power")
        s = np.array(Pw["share"])
        ax = plane([0, 0.5], [0, 0.32], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.2, y_length=4.8,
                   xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5], yticks=[0, 0.1, 0.2, 0.3],
                   xlabel=r"share of spending on the supplier's goods",
                   ylabel=r"loss of real income if it cuts you off", xfmt=lambda v: f"{100 * v:.0f}\\%",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        ls = {k: path(ax, s, Pw[f"loss{k}"], THETA[f"{k}.0"], 3.0) for k in (2, 4, 8)}
        key = legend_rows([(THETA["2.0"], "hard to replace (theta = 2)"), (THETA["4.0"], "theta = 4"),
                           (THETA["8.0"], "easy to replace (theta = 8)")], font_size=15).next_to(
            ax.ax, RIGHT, buff=0.3).shift(UP * 1.4)
        eq = MathTex(r"\text{loss} = 1 - (1 - s)^{1/\theta}", font_size=34, color=GREY_A).next_to(key, DOWN,
                                                                                               buff=0.5)
        ex = Pw["examples"]
        side = label(rf"$s = 20\%$, \ $\theta = 4$: \ {100 * ex['0.20']:.1f}\%", font_size=19,
                     color=THETA["4.0"]).next_to(eq, DOWN, buff=0.4)
        tag = published_tag(r"Arkolakis, \ Costinot and Rodr\'iguez-Clare, \ AER 102(1) (2012); \ "
                            r"agora.tradewar.cutoff\_loss", corner=DL, font_size=12)
        with self.voiceover(
            "How much power does dependence give? Part thirty-six's formula for the gains from trade answers it. "
            "<bookmark mark='a'/> If a share s of your spending goes to one supplier's goods, and it cuts you off, "
            "your real income falls by one minus one minus s to the power one over theta. <bookmark mark='b'/> At "
            f"a fifth of spending and theta of four, that is {100 * ex['0.20']:.1f} percent of income, every year "
            "the cutoff lasts. <bookmark mark='c'/> It is much larger when the goods are hard to replace, low theta, "
            "and small when other suppliers can step in. <bookmark mark='d'/> That loss is the most a supplier can "
            "demand from you by threatening a cutoff: a concession worth more than the loss, and you would rather "
            "be cut off. Which is why the goods that matter for power are the ones with few suppliers and no "
            "substitutes: rare earths, advanced chips, some medicines."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(Create(ls[4]), FadeIn(key[1]), FadeIn(side), run_time=1.8)
            vo.wait_until("c")
            self.play(Create(ls[2]), Create(ls[8]), FadeIn(key[0]), FadeIn(key[2]), run_time=1.8)
            vo.wait_until("d")
            self.play(Indicate(ls[2], color=THETA["2.0"], scale_factor=1.0))
        self.clear_scene()

    def hegemon(self):
        cards = point_cards([
            (r"the hegemon", r"a country at the centre of many networks can tie them together: \ a threat in "
             r"one, \ to win in another", US),
            (r"the target", r"complies when the threatened loss exceeds what is asked, \ and hedges by "
             r"diversifying, \ at a cost", ROW),
            (r"the price of power", r"hedging is waste from the world's point of view: \ the fear of "
             r"cutoffs makes everyone poorer, \ even if no cutoff happens", TARIFF),
            (r"the counter-move", r"targets build their own hubs: \ payment systems, \ reserve assets, \ "
             r"suppliers \ (chapter eleven)", STATE),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"a framework for geoeconomics", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Clayton, \ Maggiori and Schreger, \ \emph{A Framework for Geoeconomics}, \ NBER "
                            r"working paper (2023)", corner=DL, font_size=12)
        with self.voiceover(
            "Christopher Clayton, Matteo Maggiori and Jesse Schreger built this into a framework. <bookmark "
            "mark='a'/> A hegemon at the centre of many networks, finance, technology, trade, can tie them "
            "together: a threat in one to win something in another. <bookmark mark='b'/> A target complies when "
            "the loss it is threatened with exceeds what it is asked to give, and it hedges, diversifying away from "
            "the hegemon, at a cost. <bookmark mark='c'/> From the world's point of view the hedging is waste: the "
            "fear of cutoffs makes everyone poorer even when no cutoff happens. <bookmark mark='d'/> And targets "
            "answer by building their own hubs: payment systems, reserve assets, suppliers. Chapter eleven returns "
            "to the most important of them, the dollar."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
