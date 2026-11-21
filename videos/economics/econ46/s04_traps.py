from __future__ import annotations

from videos.economics.econ46.common import *  # noqa: F403


class Traps(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Poverty traps", r"Can a household be too poor to stop being poor?",
             "Chapter three. Poverty traps.", lit={2014: r"Kraay and McKenzie", 2022: r"Balboni et al."},
             scale=("household", "village"), horizon=("a decade",))
        self.technology()
        self.curve()
        self.paths()
        self.evidence()

    def technology(self):
        T = load("trap")
        k = np.array(T["k"])
        sel = k <= 70
        ax = plane([0, 70], [0, 25], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.2, y_length=4.8,
                   xticks=[0, 10, 20, 30, 40, 50, 60, 70], yticks=[0, 5, 10, 15, 20, 25],
                   xlabel=r"a household's capital, \ $k$", ylabel=r"output", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        lo = path(ax, k[sel], np.array(T["f_low"])[sel], FARM, 3.0)
        hi = path(ax, k[sel], np.array(T["f_high"])[sel], ESCAPE, 3.0, yr=(0, 25))
        sw = vline(ax, T["switch"], 0, 25, GREY_B)
        side = VGroup(
            label(r"a hoe and a plot: \\ $f = \sqrt{k}$", font_size=19, color=FARM),
            label(r"a cow, \ a cart, \ a shop: \\ $f = 4\sqrt{k} - 11$", font_size=19, color=ESCAPE),
            label(r"the 11 is a fixed cost: \\ worth paying only \\ with enough capital", font_size=19, color=GREY_A),
            label(rf"they cross at \\ $k$ = {T['switch']:.1f}", font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "A trap needs a reason why a little more capital does little, but a lot more does a lot. On the Island "
            "the reason is a choice of technology. <bookmark mark='a'/> A household with little can farm a plot "
            "with a hoe: output is the square root of its capital. <bookmark mark='b'/> Or it can buy into "
            "something better, a cow, a cart, a small shop, which produces four times the square root, <bookmark "
            "mark='c'/> less a fixed cost of eleven: the cow must be bought whole. <bookmark mark='d'/> The better "
            f"technology pays only above a capital of {T['switch']:.1f}. Below that, the household is better off "
            "with the hoe."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(lo), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(hi), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(sw), FadeIn(side[3]))
        self.clear_scene()

    def curve(self):
        T = load("trap")
        k = np.array(T["k"])
        sel = k <= 70
        dk = (np.array(T["next"]) - k)[sel]
        ax = plane([0, 70], [-0.35, 0.35], center=LEFT * 2.0 + DOWN * 0.3, x_length=7.2, y_length=4.8,
                   xticks=[0, 10, 20, 30, 40, 50, 60, 70], yticks=[-0.3, -0.15, 0, 0.15, 0.3],
                   xlabel=r"capital this year, \ $k_t$", ylabel=r"change over the year, \ $k_{t+1} - k_t$",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.2f}".replace("-", "{-}") if v else "0",
                   font_size=14)
        zero = DashedLine(ax.ax.c2p(0, 0), ax.ax.c2p(70, 0), color=GREY_B, stroke_width=1.6)
        mp = path(ax, k[sel], dk, POOR, 3.4)
        pts = VGroup(dot(ax, T["low"], 0, TRAP, 0.1), dot(ax, T["threshold"], 0, WHITE, 0.1),
                     dot(ax, T["high"], 0, ESCAPE, 0.1))

        def flow(x0, x1, col):
            y = ax.ax.c2p(0, -0.3)[1]
            return Arrow(np.array([ax.ax.c2p(x0, 0)[0], y, 0]), np.array([ax.ax.c2p(x1, 0)[0], y, 0]), buff=0,
                         color=col, stroke_width=4, max_tip_length_to_length_ratio=0.25)
        arrows = VGroup(flow(1, 8, TRAP), flow(17, 10, TRAP), flow(19.5, 57, ESCAPE), flow(69, 61.5, ESCAPE))
        eq = MathTex(r"k_{t+1} = s\,f(k_t) + (1-\delta)\,k_t", font_size=32, color=THEORY)
        side = VGroup(
            eq,
            label(rf"save {100 * T['s']:.0f}\%, \ lose {100 * T['delta']:.0f}\% a year", font_size=18, color=GREY_A),
            label(rf"a low steady state: \ $k$ = {T['low']:.0f}", font_size=18, color=TRAP),
            label(rf"a threshold: \ $k$ = {T['threshold']:.1f}", font_size=18, color=WHITE),
            label(rf"a high steady state: \ $k$ = {T['high']:.1f}", font_size=18, color=ESCAPE),
            label(r"arrows: \ where capital drifts", font_size=18, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Now let households save. <bookmark mark='a'/> Each year a household saves "
            f"{100 * T['s']:.0f} percent of its output, and loses {100 * T['delta']:.0f} percent of its capital to "
            "wear and death. Here is how much its capital changes over a year, at each level of capital. <bookmark "
            "mark='b'/> Above the dashed line capital grows; below it, capital shrinks. <bookmark mark='c'/> The "
            f"curve crosses the line three times. At {T['low']:.0f}, a low steady state: the hoe, forever. "
            f"<bookmark mark='d'/> At {T['high']:.0f}, a high one. <bookmark mark='e'/> And between them, at "
            f"{T['threshold']:.1f}, a threshold. Start below it and capital drifts down to the low state; start "
            "above it and it climbs to the high one. Two households with the same skills and the same patience "
            "end up in different worlds, because of where they started. That is a poverty trap."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), Create(zero), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(side[1]), Create(mp), run_time=2.0)
            vo.wait_until("b")
            self.play(Indicate(zero, color=WHITE))
            vo.wait_until("c")
            self.play(FadeIn(pts[0], scale=1.5), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(pts[2], scale=1.5), FadeIn(side[4]))
            vo.wait_until("e")
            self.play(FadeIn(pts[1], scale=1.5), FadeIn(side[3]), FadeIn(side[5]),
                      LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.3), run_time=2.0)
        self.clear_scene()

    def paths(self):
        T = load("trap")
        yrs = T["years"]
        axes, groups, labs = VGroup(), [], VGroup()
        for j, (key, col, nm) in enumerate((("0", TRAP, r"no transfer"), ("10", POOR, r"a transfer of 10"),
                                            ("20", ESCAPE, r"a transfer of 20"))):
            ax = plane([0, yrs], [0, 60], center=np.array([-4.5 + 4.5 * j, -0.4, 0]), x_length=3.6, y_length=3.8,
                       xticks=[0, 6, 12], yticks=[0, 20, 40, 60] if j == 0 else [],
                       xlabel=r"years", ylabel=r"capital" if j == 0 else "", xfmt=lambda v: f"{v:.0f}",
                       yfmt=lambda v: f"{v:.0f}", font_size=13)
            th = DashedLine(ax.ax.c2p(0, T["threshold"]), ax.ax.c2p(yrs, T["threshold"]), color=WHITE,
                            stroke_width=1.6)
            g = VGroup(*[path(ax, list(range(yrs + 1)), p, col, 1.4, yr=(0, 60), smooth=False)
                         for p in T["runs"][key]["paths"]])
            R = T["runs"][key]
            lab = VGroup(label(nm, font_size=19, color=col),
                         label(rf"{100 * R['share_above_end']:.0f}\% above the \\ threshold after {yrs} years",
                               font_size=16, color=WHITE)).arrange(DOWN, buff=0.08).next_to(ax, UP, buff=0.2)
            axes.add(VGroup(ax, th))
            groups.append(g)
            labs.add(lab)
        R0, R1, R2 = (T["runs"][k] for k in ("0", "10", "20"))
        foot = label(rf"white: \ the threshold, \ {T['threshold']:.1f}; \ forty households drawn from each "
                     r"3,000", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Here are the Island's households, three thousand of them, with capital around ten and good and bad "
            "years along the way. Forty of each are drawn. <bookmark mark='a'/> With no help, "
            f"{100 * R0['start_above']:.0f} percent start above the threshold, and after {yrs} years "
            f"{100 * R0['share_above_end']:.0f} percent are above it. The rest stay where they began. "
            "<bookmark mark='b'/> Now give each household a one-off transfer of ten, about what it already owns. "
            f"{100 * R1['crossed']:.0f} percent are pushed across the threshold, and after {yrs} years "
            f"{100 * R1['share_above_end']:.0f} percent are above it, climbing. Those it did not push across slide "
            "back, as if it had never happened. <bookmark mark='c'/> A transfer of twenty pushes everyone across, "
            f"and {100 * R2['share_above_end']:.0f} percent are above it twelve years later. In a trap, the size of "
            "a transfer matters in a way it does not in Part twenty's Solow model: a small one is spent, a large "
            "one changes a life."
        ) as vo:
            self.play(FadeIn(axes), FadeIn(foot), FadeIn(tag), run_time=1.0)
            for mk, j in zip("abc", range(3)):
                vo.wait_until(mk)
                self.play(LaggedStart(*[Create(p) for p in groups[j]], lag_ratio=0.03), FadeIn(labs[j]),
                          run_time=2.5)
        self.clear_scene()

    def evidence(self):
        Tk = tables.TRAPS_46.data
        cards = point_cards([
            (r"the sceptics", r"Kraay and McKenzie, \\ 2014: \ little evidence \\ for most traps; \ the \\ strongest "
                              r"are \\ geographic", HOLD),
            (r"the test", r"give a large asset \\ at random, \ and \\ watch who climbs", TRIAL),
            (r"Bangladesh", rf"{Tk['households']:,} households, \\ {Tk['years']} years: \ a cow \\ from BRAC, \ given "
                            r"\\ at random", POOR),
            (r"the finding", rf"a threshold in assets; \\ the trap costs {Tk['misallocation']} \\ times what it "
                             r"would \\ cost to push across", ESCAPE),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.2)
        head = label(r"do traps exist?", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.TRAPS_46.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Do real households face traps like this? <bookmark mark='a'/> For years the answer was: rarely. In "
            "2014 Aart Kraay and David McKenzie reviewed the evidence for each kind of trap in the models, and "
            "found little for most of them; the strongest case was for places, remote or unhealthy regions, more "
            "than for households. <bookmark mark='b'/> The test is the one the Island just ran: give households a "
            "large asset at random, and see who keeps climbing. <bookmark mark='c'/> Clare Balboni, Oriana "
            "Bandiera, Robin Burgess, Maitreesh Ghatak and Anton Heil followed six thousand households in rural "
            "Bangladesh for eleven years, half of them given cows by the charity BRAC at random. <bookmark "
            "mark='d'/> They found a threshold. Households that ended up above a certain level of assets kept "
            "accumulating and moved into better work; those below slid back. And they estimate that the trap "
            f"wastes {Tk['misallocation']} times what it would cost, once, to push households across it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(Circumscribe(cards.cards[0], color=WHITE, buff=0.05))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
