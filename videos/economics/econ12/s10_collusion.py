from __future__ import annotations

from videos.economics.econ12.common import *  # noqa: F403

BERT = "#F2C14E"


class Collusion(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Collusion as a repeated game", r"When can a few firms keep prices high, \ and what makes it "
             r"harder?", "Chapter eight. Collusion as a repeated game.", lit={1964: r"Stigler's theory"},
             scale=("firm", "market"), horizon=("a season", "a decade"))
        self.trigger()
        self.numbers()
        self.stigler()
        self.called()

    def trigger(self):
        c = load("collusion")["duo"]
        rows = VGroup(
            label(r"the yards agree: \ 22.5 boats each, \ the monopoly's price, \ every season", font_size=24),
            label(r"if either ever builds more, \ both return to Cournot for good \ (Part 11's grim trigger)",
                  font_size=24, color=GREY_A),
            label(rf"keep the deal: \ \${c['collude']:,.1f} a season, \ for ever".replace(",", "{,}"), font_size=25,
                  color=CARTEL),
            label(rf"cheat: \ \${c['deviate']:,.2f} once, \ then \${c['nash']:.0f} a season".replace(",", "{,}"),
                  font_size=25, color=E.MISS),
            MathTex(r"\delta \ \ge\ \frac{\pi_{\text{cheat}} - \pi_{\text{cartel}}}{\pi_{\text{cheat}} - "
                    r"\pi_{\text{Cournot}}} = " + f"{c['delta']:.3f}", font_size=40, color=EQ),
            label(r"$\delta$: \ what next season's dollar is worth today, \ patience times the chance the market "
                  r"lasts", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.28).move_to(UP * 0.1)
        tag = published_tag(r"Friedman, Review of Economic Studies 38(1) (1971); \ the numbers: \ Agora", corner=DR,
                            font_size=13)
        with self.voiceover(
            "Part eleven showed that repetition can sustain cooperation. Here it is with boats. "
            "<bookmark mark='a'/> Suppose Crusoe and Dara agree to build twenty-two and a half boats each, every "
            "season, so that together they act as a monopoly. <bookmark mark='b'/> And suppose each believes that "
            "if either ever builds more, both will return to Cournot's thirty for good. James Friedman showed in "
            "1971 that such threats can hold a cartel together. <bookmark mark='c'/> Keeping the deal earns each "
            "yard a thousand and twelve dollars fifty a season, for ever. <bookmark mark='d'/> Cheating earns more "
            "once: the best reply to the other's twenty-two and a half is about thirty-four boats, for eleven "
            "hundred and thirty-nine dollars. Then nine hundred a season, for ever. <bookmark mark='e'/> Cheating "
            "doesn't pay if delta, the value today of next season's dollar, is at least nought point five two nine. "
            "<bookmark mark='f'/> Delta combines patience with the chance that the market will still be there next "
            "season; firms that meet often, in a stable market, have a delta close to one."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def numbers(self):
        c = load("collusion")
        ns = np.array(c["ns"])
        ax = plane([1, 11], [0.4, 1.0], center=LEFT * 2.9 + DOWN * 0.3, x_length=6.2, y_length=4.6,
                   xticks=[2, 4, 6, 8, 10], yticks=[0.5, 0.6, 0.7, 0.8, 0.9, 1.0], xlabel=r"number of firms",
                   ylabel=r"patience needed to collude, \ $\delta$", font_size=16, xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.1f}")
        a = ax.ax
        cc = path(ax, ns, c["cournot"], color=LEADER, width=3.5)
        bc = path(ax, ns, c["bertrand"], color=BERT, width=3.5)
        cd = VGroup(*[Dot(a.c2p(n, d), radius=0.06, color=LEADER) for n, d in zip(ns, c["cournot"])])
        bd = VGroup(*[Dot(a.c2p(n, d), radius=0.06, color=BERT) for n, d in zip(ns, c["bertrand"])])
        cl = label(r"quantities (Cournot)", font_size=16, color=LEADER).next_to(a.c2p(10, c["cournot"][-1]), DOWN,
                                                                            buff=0.35).shift(LEFT * 0.9)
        bl = label(r"prices (Bertrand)", font_size=16, color=BERT).next_to(a.c2p(10, c["bertrand"][-1]), UP,
                                                                       buff=0.1).shift(LEFT * 0.6)
        side = VGroup(
            label(r"with $N$ firms each gets a smaller share of the cartel's profit, \\ but a cheater still takes "
                  r"a big bite", font_size=20),
            MathTex(r"\text{prices: } \ \delta \ge 1 - \tfrac{1}{N}", font_size=34, color=BERT),
            label(rf"quantities: \ {c['cournot'][0]:.3f} with two, \\ {c['cournot'][-1]:.3f} with ten", font_size=21,
                  color=LEADER),
            label(r"more firms, \ more patience needed: \\ cartels of a few are easier to hold", font_size=21,
                  color=EQ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Now count the firms. <bookmark mark='a'/> With more members, each one's share of the cartel's profit "
            "shrinks, but a cheater still takes a large bite of the whole market. <bookmark mark='b'/> When firms "
            "set prices, a cheater undercutting by a cent takes everything, and the cartel holds only if delta is at "
            "least one minus one over N: a half with two firms, nine tenths with ten. <bookmark mark='c'/> When "
            "they set quantities, the threshold climbs from nought point five three with two firms to nought point "
            "seven five with ten. <bookmark mark='d'/> Either way, more firms need more patience, which is one reason "
            "cartels of a few hold better than cartels of many."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(bc), FadeIn(bd), FadeIn(bl), Write(side[1]))
            vo.wait_until("c")
            self.play(Create(cc), FadeIn(cd), FadeIn(cl), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def stigler(self):
        hc = history_card(1964, r"George Stigler, \ ``A Theory of Oligopoly''", r"collusion is a problem of policing: "
                          r"\ a cartel lasts only if it can detect the cheaters", color=CARTEL, width=11.4,
                          font_size=24).to_edge(UP, buff=0.45)
        rows = point_cards([
            (r"few firms", r"each one's cheating \\ is noticed", CARTEL),
            (r"prices in public", r"a secret discount \\ is hard to give", LEADER),
            (r"frequent meetings", r"punishment comes \\ quickly", EQ),
            (r"similar firms", r"one deal suits \\ everyone", COMPETE),
            (r"steady demand", r"a drop in sales means \\ someone cheated", PUMP),
            (r"many markets shared", r"cheat in one, \\ be punished in all", ENTRANT),
        ], width=12.6, cols=3, font_size=21).next_to(hc, DOWN, buff=0.45)
        tag = published_tag(r"Stigler, JPE 72(1) (1964); \ Bernheim and Whinston, RAND J. 21(1) (1990)", corner=DR,
                            font_size=13)
        with self.voiceover(
            "In 1964 George Stigler put the problem differently: collusion is a problem of policing. A cartel lasts "
            "only if its members can detect who is cheating, because a cut nobody notices is never punished. "
            "<bookmark mark='a'/> From that idea, and from the repeated game, comes a list of what helps. Few "
            "firms, so each one's cheating shows. Prices in public, so a secret discount is hard to give. Frequent "
            "meetings, so punishment comes quickly. Similar firms, so that one deal suits them all. Steady demand, "
            "so that a fall in your sales means someone cheated, not that the market shrank. And contact in many "
            "markets, which Douglas Bernheim and Michael Whinston showed lets firms that cheat in one be punished "
            "in all."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.1) for c_ in rows.cards], lag_ratio=0.6), run_time=14)
        self.clear_scene()

    def called(self):
        c = calls.CALLS["stigler_cheating"]
        cc = call_card(r"George Stigler", c.when,
                       r"cartels are undone by secret price cuts: \ cheating that goes undetected is what breaks them",
                       r"Levenstein and Suslow's survey (2006): \ cheating or weak monitoring breaks cartels "
                       r"occasionally; \ entry and quarrels among members, \ most often; \ many cartels last for "
                       r"years", c.verdict, width=12.4, font_size=23).move_to(UP * 0.6)
        q = label(r"newcomers and quarrels ended more cartels than secret cuts; \ then there is the law", font_size=24,
                  color=E.ACCENT).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"Levenstein and Suslow, JEL 44(1) (2006)", corner=DR, font_size=13)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> Stigler's theory predicts that secret price cuts are what undo cartels. "
            "<bookmark mark='b'/> In 2006 Margaret Levenstein and Valerie Suslow surveyed the empirical studies of "
            "cartels. Cheating, or monitoring too weak to catch it, broke cartels only occasionally. The most common "
            "causes of collapse were entry by new rivals and bargaining problems among the members, and many cartels "
            "lasted for years. <bookmark mark='c'/> Partly right: cartels do worry about cheating, and organize "
            "themselves to catch it: the lysine association kept tables of each member's sales against its "
            "target. But "
            "newcomers and quarrels ended more cartels than secret price cuts did. And then there is the law, the "
            "subject of the next chapter."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(Indicate(cc.right, color=WHITE, scale_factor=1.01))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3), FadeIn(q))
        self.clear_scene()
