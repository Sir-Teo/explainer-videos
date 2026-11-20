from __future__ import annotations

from videos.economics.econ44.common import *  # noqa: F403


class Vertical(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Vertical relations", r"When firms sell to firms, what changes?",
             "Chapter five. Vertical relations.", lit={1950: r"Spengler", 1978: r"Bork", 2007: r"\emph{Leegin}"},
             scale=("firm", "market"), horizon=("a year",))
        self.double()
        self.fixes()
        self.foreclosure()

    def double(self):
        V = load("vertical")
        a, c = TRUTH["vertical"]["a"], TRUTH["vertical"]["c"]
        ax = plane([0, a], [0, a], center=LEFT * 1.8 + DOWN * 0.4, x_length=7.6, y_length=4.8,
                   xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 2, 4, 6, 8, 10], xlabel=r"quantity", ylabel=r"price",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        dem = seg(ax, 0, a, a, 0, KEEP, 3.0)
        cost = seg(ax, 0, c, a, c, GREY_B, 2.0, dashed=True)
        w = seg(ax, 0, V["w"], a, V["w"], FIRM1, 2.0, dashed=True)
        p_int = VGroup(dot(ax, V["q_int"], V["p_int"], GAIN, 0.1),
                       label(rf"integrated: \ {V['p_int']:.0f}", font_size=17, color=GAIN).next_to(
                           ax.ax.c2p(V["q_int"], V["p_int"]), RIGHT, buff=0.15))
        p_sep = VGroup(dot(ax, V["q_sep"], V["p_sep"], LOSS, 0.1),
                       label(rf"two markups: \ {V['p_sep']:.0f}", font_size=17, color=LOSS).next_to(
                           ax.ax.c2p(V["q_sep"], V["p_sep"]), RIGHT, buff=0.15))
        side = VGroup(
            label(rf"demand: \ $P$ = {a:.0f} $-$ $Q$; \\ the maker's cost {c:.0f}", font_size=18, color=KEEP),
            label(rf"the maker charges the \\ retailer {V['w']:.0f}, \ its own \\ monopoly price", font_size=18,
                  color=FIRM1),
            label(rf"the retailer adds a \\ second markup: \ {V['p_sep']:.0f}", font_size=18, color=LOSS),
            label(rf"profits: \ {V['profit_int']:.0f} integrated \\ against {V['profit_m'] + V['profit_r']:.0f} "
                  rf"together; \\ buyers' surplus {V['cs_int']:.0f} against {V['cs_sep']:.0f}", font_size=18,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = published_tag(tables.VERTICAL.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Most firms sell to other firms. A maker sells to a retailer, who sells to you. <bookmark mark='a'/> "
            f"Take demand that falls from {a:.0f} dollars, and a maker whose cost is {c:.0f}. A single integrated "
            f"firm would charge {V['p_int']:.0f}. <bookmark mark='b'/> But a separate maker charges the retailer "
            f"its own best price, {V['w']:.0f}. <bookmark mark='c'/> The retailer, treating {V['w']:.0f} as its "
            f"cost, adds a markup of its own and charges {V['p_sep']:.0f}. <bookmark mark='d'/> Two markups stacked "
            "on each other: double marginalization, as Joseph Spengler called it in 1950. The two firms together "
            f"earn {V['profit_m'] + V['profit_r']:.0f} instead of {V['profit_int']:.0f}, and buyers' surplus falls "
            f"from {V['cs_int']:.0f} to {V['cs_sep']:.0f}. Everyone loses: integration here helps consumers."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(dem), Create(cost), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(p_int, scale=1.3))
            vo.wait_until("b")
            self.play(Create(w), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(p_sep, scale=1.3), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def fixes(self):
        cards = point_cards([
            (r"merge", r"one firm, \\ one markup", GAIN),
            (r"two-part tariff", r"sell at cost, \\ charge a fixed fee \\ for the right", PATIENT),
            (r"resale price \\ maintenance", r"the maker sets \\ the retail price; \\ judged case by case \\ since "
                                              r"\emph{Leegin} (2007)", FIRM1),
            (r"but", r"the same contracts \\ can soften \\ competition among \\ retailers or makers", LOSS),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.1)
        head = label(r"three fixes, \ and a warning", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.VERTICAL.tag, corner=DR, font_size=11)
        with self.voiceover(
            "There are fixes. <bookmark mark='a'/> Merge, so there is one markup. <bookmark mark='b'/> Sell to the "
            "retailer at cost and charge a fixed fee for the right to sell, a two-part tariff, so the retailer prices "
            "as an integrated firm would. <bookmark mark='c'/> Or let the maker set a minimum retail price, resale "
            "price maintenance, illegal in itself in the United States from 1911 until the Supreme Court's Leegin "
            "decision in 2007, and judged case by case since. <bookmark mark='d'/> The warning: the same contracts can "
            "also "
            "dampen competition, among retailers who would otherwise undercut each other, or among makers who use "
            "them to keep a cartel's prices visible."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def foreclosure(self):
        steps = flow_chain([(r"the worry", LOSS), (r"Chicago's reply", GAIN), (r"the modern view", PATIENT)],
                           notes=[r"a firm that owns a \\ bottleneck shuts \\ rivals out of the \\ market downstream",
                                  r"there is only one \\ monopoly profit: \\ owning both stages \\ adds nothing",
                                  r"foreclosure can pay \\ when it raises rivals' \\ costs or commits \\ the firm"],
                           box_w=3.1, font_size=21, note_size=17).move_to(UP * 0.5)
        foot = label(r"which story holds is a question about the facts of each market", font_size=21,
                     color=E.ACCENT).to_edge(DOWN, buff=0.9)
        tag = published_tag(tables.VERTICAL.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Vertical mergers raise a second worry. <bookmark mark='a'/> A firm that owns a bottleneck, say the only "
            "pipeline, might buy a firm downstream and shut that firm's rivals out. <bookmark mark='b'/> The Chicago "
            "school, Robert Bork among them, replied that there is only one monopoly profit to be had: the "
            "pipeline's owner can take it all in the price of transport, so buying downstream adds no power. "
            "<bookmark mark='c'/> Later theory found exceptions. Foreclosure can pay when it raises rivals' costs, "
            "or when owning the downstream firm lets the bottleneck commit to a high price it could not otherwise "
            "keep. <bookmark mark='d'/> Which story holds is a question about each market's facts, which is why "
            "vertical cases are fought over evidence."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(steps.boxes[0]))
            vo.wait_until("a")
            self.play(FadeIn(steps.notes[0]))
            for k, mk in zip(range(2), "bc"):
                vo.wait_until(mk)
                self.play(GrowArrow(steps.arrows[k]), FadeIn(steps.boxes[k + 1]), FadeIn(steps.notes[k + 1]))
            vo.wait_until("d")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()
