from __future__ import annotations

from videos.economics.econ64.common import *  # noqa: F403


def net_diagram(hidden=6):
    inp = Circle(radius=0.28, stroke_color=TEXT, stroke_width=2).move_to(LEFT * 2.2)
    il = label(r"$k$", font_size=24, color=TEXT).move_to(inp)
    hs = VGroup(*[Circle(radius=0.2, stroke_color=NET, stroke_width=2, fill_color=NET, fill_opacity=0.2).move_to(
        [0, (h - (hidden - 1) / 2) * 0.55, 0]) for h in range(hidden)])
    out = Circle(radius=0.28, stroke_color=GDP, stroke_width=2).move_to(RIGHT * 2.2)
    ol = label(r"$s$", font_size=24, color=GDP).move_to(out)
    edges = VGroup(*[Line(inp.get_right(), h.get_left(), stroke_width=1, color=GREY_C) for h in hs],
                   *[Line(h.get_right(), out.get_left(), stroke_width=1, color=GREY_C) for h in hs])
    cap = VGroup(label(r"capital", font_size=16, color=GREY_B).next_to(inp, DOWN, buff=0.15),
                 label(r"12 tanh units", font_size=16, color=GREY_B).next_to(hs, DOWN, buff=0.15),
                 label(r"saving rate", font_size=16, color=GREY_B).next_to(out, DOWN, buff=0.15))
    return VGroup(edges, inp, il, hs, out, ol, cap)


class Deep(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Deep learning as a solution method", r"Can a neural network solve an economic model?",
             "Chapter eight. Deep learning as a solution method.", lit={1972: r"Brock and Mirman",
                                                                        2021: r"Maliar, Maliar and Winant"},
             scale=("household", "nation"), horizon=("a decade",))
        self.setup_net()
        self.train()
        self.why()

    def setup_net(self):
        E_ = load("euler")
        eqs = VGroup(label(r"$k' = s(k)\, k^{\alpha}, \qquad c = (1 - s(k))\, k^{\alpha}$", font_size=30),
                     label(r"Euler: \ $\dfrac{1}{c} = \beta\,\alpha\, k'^{\,\alpha - 1}\,\dfrac{1}{c'}$", font_size=30),
                     label(r"loss: \ the squared Euler error on 64 capital stocks", font_size=22, color=GREY_A)
                     ).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.5)
        net = net_diagram().scale(0.9).next_to(eqs, DOWN, buff=0.6)
        tag = published_tag(r"Maliar, \ Maliar and Winant, \ JME 122 (2021); \ Brock and Mirman, \ JET 4(3) (1972)",
                            corner=DL, font_size=12)
        with self.voiceover(
            "Machine learning can also solve models. Take Part twenty's growth model in its simplest form: log "
            "utility, capital that wears out in a year. <bookmark mark='a'/> Each year output, k to the alpha, is "
            "split between consumption and next year's capital, by a saving rate s that may depend on k. <bookmark "
            "mark='b'/> The optimal rule satisfies the Euler equation at every k. <bookmark mark='c'/> So "
            "represent s by a small neural network, capital in, a saving rate out, and train it to make the Euler "
            f"equation hold on sixty-four capital stocks, with the series' own automatic differentiation computing "
            f"the gradients. William Brock and Leonard Mirman found the answer by hand in 1972: save alpha times "
            f"beta, {E_['exact']:.4f}, whatever k is. The network does not know that."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(eqs[0]))
            vo.wait_until("b")
            self.play(FadeIn(eqs[1]))
            vo.wait_until("c")
            self.play(FadeIn(eqs[2]), FadeIn(net))
        self.clear_scene()

    def train(self):
        E_ = load("euler")
        k = np.array(E_["k"]) / E_["kss"]
        axl = plane([0, 3000], [-9, 0], center=LEFT * 3.6 + DOWN * 0.3, x_length=5.0, y_length=4.4,
                    xticks=[0, 1000, 2000, 3000], yticks=[-8, -6, -4, -2, 0], xlabel=r"training step",
                    ylabel=r"squared Euler error \ (log$_{10}$)", xfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"),
                    yfmt=lambda v: f"{v:.0f}".replace("-", "{-}"), font_size=13)
        lo = np.log10(np.maximum(np.array(E_["loss"]), 1e-12))
        steps = np.arange(len(lo)) * 10
        lc = path(axl, steps, lo, NET, 3.0, smooth=False)
        axr = plane([0.2, 2.5], [0.15, 0.45], center=RIGHT * 3.2 + DOWN * 0.3, x_length=5.0, y_length=4.4,
                    xticks=[0.5, 1.0, 1.5, 2.0, 2.5], yticks=[0.2, 0.3, 0.4], xlabel=r"capital, \ steady state = 1",
                    ylabel=r"saving rate $s(k)$", xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}",
                    font_size=13)
        ex = seg(axr, 0.2, E_["exact"], 2.5, E_["exact"], TRUTHC, 2.4, dashed=True)
        snaps = VGroup(*[path(axr, k, sn["s"], NET, 2.6, yr=(0.15, 0.45)) for sn in E_["snaps"]])
        orders = {6: "six", 7: "seven", 8: "eight", 9: "nine"}.get(int(lo[0] - lo[-1]), "many")
        for j, s_ in enumerate(snaps):
            s_.set_fill(opacity=0).set_stroke(opacity=0.35 + 0.65 * j / max(len(snaps) - 1, 1))
        cap = label(rf"after training: \ largest gap {E_['max_err']:.5f}", font_size=19, color=E.ACCENT).to_edge(
            DOWN, buff=0.35)
        tag = island_tag(r"computed: \ agora.learn.euler\_net, \ explainer.ai.autodiff", corner=DL, font_size=12)
        with self.voiceover(
            f"Train it. <bookmark mark='a'/> On the left, the squared Euler error, falling by {orders} orders "
            "of magnitude. <bookmark mark='b'/> On the right, the rule the network has learned, at the start, after "
            "fifty steps, after two hundred, and at the end, against Brock and Mirman's answer in gold. <bookmark "
            f"mark='c'/> The learned rule is flat at alpha times beta, within {E_['max_err']:.5f} everywhere on "
            "the grid. The network found the closed form without being told it."
        ) as vo:
            self.play(FadeIn(axl), FadeIn(axr), FadeIn(ex), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(lc), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(s_) for s_ in snaps], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(cap))
        self.clear_scene()

    def why(self):
        cards = point_cards([
            (r"why bother", r"a grid has a point for every combination of states: \ ten states with ten points each "
             r"is ten billion points; \ a network's cost grows far more slowly", NET),
            (r"what it reaches", r"Part 52's economies with many households, \ portfolios, \ several shocks: \ "
             r"deep equilibrium nets \ (Azinovic, \ Gaegauf and Scheidegger, \ 2022)", ALGO),
            (r"the checks", r"Euler errors off the training points, \ simulated paths, \ and a known case like this "
             r"one", TRUTHC),
            (r"the risks", r"no guarantee of a global optimum, \ and errors can hide where the economy rarely goes",
             HOLD),
        ], cols=2, width=12.8, font_size=20).move_to(DOWN * 0.2)
        head = label(r"why economists train networks", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Azinovic, \ Gaegauf and Scheidegger, \ IER 63(4) (2022)", corner=DL, font_size=12)
        with self.voiceover(
            "Why do this when a grid would do? <bookmark mark='a'/> Because a grid needs a point for every "
            "combination of states, and the count explodes: ten state variables with ten points each is ten "
            "billion points. A network's cost grows far more slowly. <bookmark mark='b'/> That reaches the "
            "economies of Part fifty-two, with many kinds of household, portfolios and several shocks: Marlon "
            "Azinovic, Luca Gaegauf and Simon Scheidegger's deep equilibrium nets, and the methods of Lilia and "
            "Serguei Maliar and Pablo Winant. <bookmark mark='c'/> The checks are the old ones: Euler errors off the "
            "training points, simulated paths, and a case with a known answer, like this one. <bookmark mark='d'/> "
            "The risks are new: no guarantee of the global optimum, and errors that hide where the economy rarely "
            "goes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()
