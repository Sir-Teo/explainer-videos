from __future__ import annotations

from videos.economics.econ9.common import *  # noqa: F403

CRUSOE = island.CAST["crusoe"].color
PPF = "#7BD88F"


class Production(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Production: \ Crusoe decentralized", r"Can prices coordinate production too, even inside one "
             r"person?", "Chapter ten. Production: Crusoe decentralized.", lit={1776: r"Smith's invisible hand"},
             scale=("person", "firm", "market"), horizon=("a day",))
        self.plan()
        self.market()
        self.limits()

    def axes(self, c):
        return plane([0, 12], [0, 8], center=LEFT * 3.0 + DOWN * 0.3, x_length=6.4, y_length=5.2,
                     xticks=[0, 3, 6, 9, 12], yticks=[0, 2, 4, 6, 8], xlabel=r"hours of leisure a day",
                     ylabel=r"coconuts a day", font_size=17)

    def plan(self):
        c = load("crusoe")
        ax = self.axes(c)
        ppf = path(ax, c["ppf_leisure"], c["ppf_c"], color=PPF, width=4)
        ind = path(ax, c["ind_leisure"], c["ind_c"], color=CRUSOE, width=3, yr=(0, 8))
        m = c["market"]
        P = Dot(ax.ax.c2p(m["leisure"], m["c"]), radius=0.1, color=WHITE)
        side = VGroup(
            label(r"Crusoe alone: \ 12 hours a day", font_size=24, color=CRUSOE),
            label(r"coconuts from work: \ $c = 2\sqrt{L}$, \\ each hour adds less than the last", font_size=22,
                  color=PPF),
            label(r"he likes coconuts and leisure: \\ $0.6 \log c + 0.4 \log(\text{leisure})$", font_size=22,
                  color=CRUSOE),
            label(rf"his best plan: \ work {c['plan']['L']:.2f} hours, \\ eat {c['plan']['c']:.2f} coconuts",
                  font_size=23),
            label(r"where his indifference curve \\ touches the frontier", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        tag = island_tag(corner=DR, font_size=15)
        with self.voiceover(
            "So far nothing has been produced. Bring back Robinson Crusoe, alone on the island, in the textbooks' "
            "favourite economy, the one Radford offered his camp as an alternative to. <bookmark mark='a'/> He has "
            "twelve waking hours a day. <bookmark mark='b'/> Hours of work turn into coconuts, two times the "
            "square root of the hours: each hour adds less than the one before. <bookmark mark='c'/> And he values "
            "both coconuts and rest. <bookmark mark='d'/> His best plan is to work five point one four hours and "
            "eat four point five four coconuts a day: <bookmark mark='e'/> the point where his indifference curve "
            "just touches what he can produce."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Indicate(side[0]))
            vo.wait_until("b")
            self.play(Create(ppf), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(ind), FadeIn(P, scale=0.5), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def market(self):
        c = load("crusoe")
        m = c["market"]
        ax = self.axes(c)
        a = ax.ax
        ppf = path(ax, c["ppf_leisure"], c["ppf_c"], color=PPF, width=4)
        ind = path(ax, c["ind_leisure"], c["ind_c"], color=CRUSOE, width=3, yr=(0, 8))
        w = m["w"]
        line = Line(a.c2p(12, m["profit"]), a.c2p(max(12 - (8 - m["profit"]) / w, 0), m["profit"] + w * min(
            12, (8 - m["profit"]) / w)), color=WHITE, stroke_width=3)
        P = Dot(a.c2p(m["leisure"], m["c"]), radius=0.1, color=WHITE)
        prof = Dot(a.c2p(12, m["profit"]), radius=0.08, color=E.ACCENT)
        pl = label(r"profit", font_size=18, color=E.ACCENT).next_to(prof, RIGHT, buff=0.1)
        side = VGroup(
            label(r"split him in two, \ and add a price: \ a wage", font_size=23),
            label(rf"Crusoe the firm hires hours \\ until the last one adds the wage: \ $w = {w:.3f}$ coconuts",
                  font_size=21, color=PPF),
            label(rf"and pays his profit, \ {m['profit']:.2f} coconuts, \ to Crusoe the owner", font_size=21,
                  color=E.ACCENT),
            label(r"Crusoe the worker chooses his hours \\ on a budget line of slope $-w$", font_size=21,
                  color=CRUSOE),
            label(rf"at this wage, \ hours offered = hours wanted = {m['L']:.2f}: \\ the planner's choice",
                  font_size=22, color=CC),
            label(r"the wage line touches both curves: \\ a separating line again", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Now split Crusoe in two, a firm and a household, and let them deal only through a price. "
            "<bookmark mark='a'/> Crusoe the manager hires hours at a wage, paid in coconuts, and keeps hiring "
            "until the last hour adds just the wage. <bookmark mark='b'/> Whatever is left over is profit, and he "
            "pays it to Crusoe the owner: two point two seven coconuts. <bookmark mark='c'/> Crusoe the worker "
            "takes that profit, and the wage for every hour he sells, and chooses his hours like any consumer, "
            "on a budget line whose slope is the wage. <bookmark mark='d'/> At a wage of nought point four four "
            "one coconuts an hour, the hours he offers equal the hours he wants to hire: five point one four, "
            "exactly the planner's choice. <bookmark mark='e'/> The wage line touches both the frontier and the "
            "indifference curve at the same point, and the welfare theorems carry over to production."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(ppf), FadeIn(ind), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(prof), FadeIn(pl), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(Create(line), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(P, scale=0.5), FadeIn(side[4]))
            vo.wait_until("e")
            self.play(FadeIn(side[5]))
        self.clear_scene()

    def limits(self):
        head = label(r"what production adds", font_size=32, color=E.ACCENT).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"firms maximize profit at the prices; \ households own the firms", font_size=26),
            label(r"both theorems still hold, \ if technology is convex", font_size=26, color=CC),
            label(r"convex means no increasing returns: \ Part 8's pipeline breaks it", font_size=26, color=HOLD),
            label(r"with increasing returns a price line can't support the best plan: \\ big firms, \ market "
                  r"power, \ Part 10", font_size=24, color=HOLD),
            label(r"and Arrow and Debreu's proof covers all of this: \ firms, \ households, \ many goods",
                  font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.4).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "So production adds firms that maximize profit at the going prices, and households that own them. "
            "<bookmark mark='a'/> Both welfare theorems still hold, with one more condition: the technology must be "
            "convex. <bookmark mark='b'/> That rules out increasing returns, like the pipeline of Part eight, where "
            "twice the steel carries four times the oil. <bookmark mark='c'/> With increasing returns, no straight "
            "price line can touch the frontier at the best plan without cutting through it, and a firm that took "
            "prices as given would want to grow without limit. That's where market power begins, in Part ten. "
            "<bookmark mark='d'/> Arrow and Debreu's existence theorem covers all of this, firms, households and "
            "any number of goods, as long as the convexity holds."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2), FadeIn(rows[0]))
            for mk, r in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
