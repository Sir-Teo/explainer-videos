from __future__ import annotations

from videos.economics.econ44.common import *  # noqa: F403


class Algorithms(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Algorithms that learn to collude", r"Can pricing software collude without being told to?",
             "Chapter ten. Algorithms that learn to collude.", lit={2020: r"Calvano et al.", 2024: r"Assad et al."},
             scale=("firm", "market"), horizon=("a day", "a year"))
        self.rules()
        self.learned()
        self.punish()
        self.evidence()

    def rules(self):
        Q = load("qlearn")
        eq = MathTex(r"Q(s, p) \;\leftarrow\; Q(s, p) + \alpha\,\big[\pi + \delta \max_{p'} Q(s', p') - Q(s, p)\big]",
                     font_size=36, color=E.ACCENT).to_edge(UP, buff=0.7)
        rows = VGroup(
            label(r"two sellers, \ the same product range, \ logit demand \ (Calvano et al.'s game)", font_size=21,
                  color=WHITE),
            label(rf"15 prices, \ from below the competitive {Q['nash']:.2f} to above the monopoly {Q['monopoly']:.2f}",
                  font_size=21, color=GREY_A),
            label(r"each algorithm sees only last period's two prices, \ and its own profit", font_size=21,
                  color=FIRM1),
            label(r"it tries prices, \ at first at random, \ and keeps score of what paid: \ $Q$", font_size=21,
                  color=PATIENT),
            label(r"no communication, \ no instruction to collude", font_size=22, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).next_to(eq, DOWN, buff=0.55)
        tag = published_tag(tables.ALGORITHMS.tag, corner=DR, font_size=11)
        with self.voiceover(
            "More and more prices are set by software that learns. Could such software learn to collude? "
            "Emilio Calvano and his coauthors set up a test, which the Island runs here. <bookmark mark='a'/> Two "
            "sellers with similar products and logit demand. <bookmark mark='b'/> Fifteen possible prices, from "
            f"below the competitive price of {Q['nash']:.2f} to above the price a monopolist would charge, "
            f"{Q['monopoly']:.2f}. <bookmark mark='c'/> Each algorithm sees only last period's two prices and its "
            "own profit. <bookmark mark='d'/> It is a Q-learner: it tries prices, at first mostly at random, and "
            "keeps a running score of how well each price did in each situation, counting the future at a discount, "
            "updated by the formula at the top. <bookmark mark='e'/> The two never communicate, and nobody tells "
            "them to collude."
        ) as vo:
            self.play(FadeIn(tag), Write(eq), run_time=1.5)
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def learned(self):
        Q = load("qlearn")
        gains = np.array(Q["gains"])
        ax = plane([-0.1, 1.1], [0, 1.0], center=LEFT * 1.8 + DOWN * 0.6, x_length=8.2, y_length=3.0,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[], xlabel=r"profit gain: \ 0 at competition, \ 1 at "
                   r"monopoly", xfmt=lambda v: f"{v:.2f}", font_size=14)
        rng = np.random.default_rng(3)
        dts = VGroup(*[dot(ax, g, 0.5 + rng.uniform(-0.25, 0.25), FIRM1, 0.09) for g in gains])
        n0 = VGroup(vline(ax, 0, 0, 1.0, NASH, 2.4), label(r"competition", font_size=16, color=NASH).next_to(
            ax.ax.c2p(0, 1.0), UP, buff=0.05))
        n1 = VGroup(vline(ax, 1, 0, 1.0, MONO, 2.4), label(r"monopoly", font_size=16, color=MONO).next_to(
            ax.ax.c2p(1, 1.0), UP, buff=0.05))
        mean = VGroup(vline(ax, Q["mean_gain"], 0, 1.0, E.ACCENT, 2.0),
                      label(rf"mean {Q['mean_gain']:.2f}", font_size=17, color=E.ACCENT).next_to(
                          ax.ax.c2p(Q["mean_gain"], 0.0), DOWN, buff=0.45))
        side = VGroup(
            label(rf"{len(gains)} sessions, \\ about {Q['iterations'] / 1e6:.1f} million \\ periods each", font_size=18,
                  color=WHITE),
            label(rf"average price \\ {Q['mean_price']:.2f}", font_size=18, color=FIRM1),
            label(r"every session \\ above competition", font_size=19, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            f"Let them play. <bookmark mark='a'/> Each session runs about {Q['iterations'] / 1e6:.1f} million "
            f"periods, until both algorithms have stopped changing their minds; here are {len(gains)} sessions. "
            "<bookmark mark='b'/> On a scale where zero is the competitive profit and one the monopoly profit, "
            f"every session ends well above competition, at {Q['mean_gain']:.2f} on average. "
            f"<bookmark mark='c'/> The average price is {Q['mean_price']:.2f}, against {Q['nash']:.2f} under "
            f"competition and {Q['monopoly']:.2f} under monopoly. Calvano and his coauthors found the same: "
            "algorithms that learn on their own consistently charge supracompetitive prices."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(n0), FadeIn(n1), FadeIn(side[0]), run_time=1.2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in dts], lag_ratio=0.15), FadeIn(mean),
                      run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.clear_scene()

    def punish(self):
        Q = load("qlearn")
        dv = Q["median"]["dev"]
        n = len(dv["p1"])
        ax = plane([0, n - 1], [1.4, 2.0], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=list(range(0, n, 2)), yticks=[1.4, 1.6, 1.8, 2.0], xlabel=r"period",
                   ylabel=r"price", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", font_size=14)
        nash = seg(ax, 0, Q["nash"], n - 1, Q["nash"], NASH, 1.6, dashed=True)
        mono = seg(ax, 0, Q["monopoly"], n - 1, Q["monopoly"], MONO, 1.6, dashed=True)
        l1 = path(ax, np.arange(n), dv["p1"], FIRM1, 3.0, smooth=False)
        l2 = path(ax, np.arange(n), np.array(dv["p2"]) + 0.005, FIRM2, 3.0, smooth=False)
        dev = VGroup(dot(ax, 1, dv["p1"][1], FIRM1, 0.1),
                     label(r"firm 1 \\ undercuts", font_size=16, color=FIRM1).next_to(ax.ax.c2p(1, dv["p1"][1]), DOWN,
                                                                                    buff=0.15))
        side = VGroup(
            label(r"gold: \ firm 1; \ blue: \ firm 2", font_size=18, color=WHITE),
            label(r"period 1: \ firm 1 cuts \\ its price once", font_size=18, color=FIRM1),
            label(r"firm 2 answers \\ with a price war", font_size=18, color=FIRM2),
            label(r"then both drift back up", font_size=18, color=E.ACCENT),
            label(rf"punished in {100 * Q['share_punished']:.0f}\% \\ of the sessions", font_size=18, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Is this collusion, or merely slow learning? The test is what happens after a deviation. "
            "<bookmark mark='a'/> Take the median session. In period one, force firm one to cut its price to the "
            "most profitable undercut, just once. <bookmark mark='b'/> In the next periods firm two answers with a "
            "lower price of its own: a price war, which costs firm one the profit it grabbed. "
            "<bookmark mark='c'/> Then both drift back up to where they were. <bookmark mark='d'/> That is the "
            "pattern of a cartel that enforces itself, a punishment followed by a return to cooperation, as in "
            f"Part twelve, here learned by trial and error. On the Island {say_pct(Q['share_punished'], 0)} of the "
            "sessions punish a deviation this way."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(nash), Create(mono), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(l1), Create(l2), FadeIn(dev), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def evidence(self):
        cards = point_cards([
            (r"Germany's petrol", r"stations that adopted \\ pricing algorithms \\ raised margins only \\ where they "
                                  r"had rivals", BUS),
            (r"duopolies", r"margins rose only \\ when both stations \\ adopted", LOSS),
            (r"the law", r"collusion is illegal \\ when firms agree; \\ algorithms need \\ no agreement", HOLD),
            (r"the options", r"audit the software, \\ limit what it sees, \\ or treat the result \\ as the offence",
             PATIENT),
        ], width=12.8, cols=4, font_size=17).move_to(DOWN * 0.1)
        head = label(r"in markets, \ and in the law", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.ALGORITHMS.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Does it happen in real markets? <bookmark mark='a'/> Stephanie Assad, Robert Clark, Daniel Ershov and "
            "Lei Xu studied German petrol stations, many of which adopted pricing algorithms around 2017. Margins "
            "rose only for stations that had rivals nearby, <bookmark mark='b'/> and in markets with two stations, "
            "only when both adopted. <bookmark mark='c'/> The law has a gap: collusion is illegal when firms agree, "
            "and algorithms that learn need no agreement. <bookmark mark='d'/> Proposals range from auditing the "
            "software, to limiting the information it may use, to treating the outcome itself as the offence."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
