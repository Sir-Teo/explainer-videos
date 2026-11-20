from __future__ import annotations

from videos.economics.econ44.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.ledger()
        self.question_of_rust()
        self.question()
        self.title()
        self.objectives()

    def ledger(self):
        L = load("ledger")
        R = load("rust")
        ax = plane([1975.5, 1985.5], [0, 400], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.4, y_length=4.8,
                   xticks=[1976, 1978, 1980, 1982, 1984], yticks=[0, 100, 200, 300, 400],
                   ylabel=r"miles since the engine was last rebuilt, \ thousands", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        lines, marks = VGroup(), VGroup()
        for k, b in enumerate(L["buses"]):
            col = interpolate_color(ManimColor(KEEP), ManimColor(BUS), k / max(len(L["buses"]) - 1, 1))
            lines.add(path(ax, b["t"], b["since"], col, 2.0, smooth=False, xr=(1975.5, 1985.5), yr=(0, 400)))
            for t in b["rebuilds"]:
                y = float(np.interp(t, b["t"], b["since"]))
                marks.add(dot(ax, t, y, REBUILD, 0.07))
        side = VGroup(
            label(r"Madison, \ Wisconsin: \\ ten of the city's 1975 \\ GMC buses", font_size=19, color=WHITE),
            label(r"each line: \ one bus's \\ engine mileage", font_size=18, color=BUS),
            label(r"red: \ Zurcher orders \\ the engine rebuilt", font_size=18, color=REBUILD),
            label(rf"{R['buses_all']} buses, \ 1974--1985; \\ on average rebuilt at \\ about "
                  rf"{round(R['mean_at'] / 1000, -1):.0f},000 miles", font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"Rust's data \ (Madison Metropolitan bus company), \ group 4", corner=DR, font_size=11)
        with self.voiceover(
            "In the 1970s and 1980s Harold Zurcher was the superintendent of maintenance at the bus company of "
            "Madison, Wisconsin. Every month, for every bus, Zurcher made the same decision. <bookmark mark='a'/> Each "
            "line here is one of the city's 1975 GMC buses, and it shows the miles on its engine since the engine "
            "was last rebuilt. The miles climb, month after month. <bookmark mark='b'/> At some point Zurcher "
            "ordered the engine taken out and rebuilt, at a large cost, and the count started again from zero. "
            f"<bookmark mark='c'/> Zurcher's records cover {R['buses_all']} buses from 1974 to 1985. On average an "
            f"engine was rebuilt at about {round(R['mean_at'] / 1000, -1):.0f} thousand miles, but not always: some "
            "engines went far longer, some much less."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(ln) for ln in lines], lag_ratio=0.1), FadeIn(side[1]), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m, scale=1.6) for m in marks], lag_ratio=0.1), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def question_of_rust(self):
        cards = point_cards([
            (r"the trade", r"rebuild early: \\ pay often; \\ rebuild late: \\ breakdowns, \ upkeep", BUS),
            (r"looking ahead", r"today's choice \\ changes every \\ future month", PATIENT),
            (r"what we see", r"the choices, \\ not the costs \\ or the reasons", HOLD),
            (r"John Rust, \ 1987", r"from the choices, \\ the costs Zurcher \\ must have believed", GAIN),
        ], width=12.8, cols=4, font_size=19).move_to(DOWN * 0.1)
        head = label(r"what was Zurcher thinking?", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.RUST_1987.tag, corner=DR, font_size=11)
        with self.voiceover(
            "The decision is a trade-off over time. <bookmark mark='a'/> Rebuild early and you pay for rebuilds "
            "often; rebuild late and you pay in breakdowns and rising upkeep. <bookmark mark='b'/> Today's choice "
            "changes every month that follows. <bookmark mark='c'/> We see Zurcher's choices, but not the costs "
            "or the reasons behind them. <bookmark mark='d'/> In 1987 the economist John Rust took the records and "
            "recovered, from the choices alone, what Zurcher must have believed a rebuild and an ageing engine cost. "
            "The method became the foundation of how economists estimate dynamic decisions, including how firms "
            "compete over time, the first theme of this part."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 36, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"how do you estimate decisions that look ahead?", font_size=26, color=BUS),
            label(r"how do firms compete when today's investment shapes tomorrow's market?", font_size=26,
                  color=PATIENT),
            label(r"what changes when the product is a platform or a network?", font_size=26, color=FIRM2),
            label(r"innovation, \ algorithms and the law: \ what should antitrust do?", font_size=26, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "So this part asks how firms compete over time, and what is different when the product is a network. "
            "<bookmark mark='a'/> How do you estimate decisions that look ahead? <bookmark mark='b'/> How do firms "
            "compete when today's investment shapes tomorrow's market? <bookmark mark='c'/> What changes when the "
            "product is a platform that brings two groups together, or a network whose value grows with its users? "
            "<bookmark mark='d'/> And what should antitrust do about innovation, acquisitions and pricing "
            "algorithms?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        F = load("film")
        mini = plane([1974.9, 1985.4], [0, 1], x_length=4.2, y_length=1.4)
        v = np.array(F["v"])
        v = (v - v.min()) / (v.max() - v.min())
        logo = path(mini, F["t"], v, BUS, 2.6, smooth=False)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 44 \ $\cdot$ \ Dynamics, \ Platforms and Antitrust", font_size=34, color=E.ACCENT)
        VGroup(logo, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part forty-four: dynamics, platforms and antitrust."):
            self.play(Create(logo), run_time=1.6)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act IX \ $\cdot$ \ The Fields", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"a game; \ Rust's model estimated on Zurcher's buses; \ conditional choice probabilities",
            r"dynamic oligopoly; \ vertical relations; \ two-sided platforms; \ networks and lock-in",
            r"competition and innovation; \ killer acquisitions; \ algorithms that learn to collude",
            r"antitrust's standards; \ regulating a firm that knows more",
            r"two dials; \ platform strategy and the agencies; \ the frontier",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "Here is the plan. <bookmark mark='a'/> A game about rebuilding engines, then Rust's model estimated on "
            "Zurcher's own buses, and a faster way to estimate it. <bookmark mark='b'/> Firms that compete over "
            "time, firms that sell to one another, platforms with two sides, and networks that lock in. "
            "<bookmark mark='c'/> Whether competition helps innovation, acquisitions that kill rivals' projects, and "
            "pricing algorithms that learn to collude. <bookmark mark='d'/> What antitrust law aims at, and how to "
            "regulate a firm that knows more than its regulator. <bookmark mark='e'/> Two dials, the people who do "
            "this work, and the frontier."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
