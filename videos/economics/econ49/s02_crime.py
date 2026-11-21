from __future__ import annotations

from videos.economics.econ49.common import *  # noqa: F403


class Crime(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Crime as a choice", r"Who offends, and what would deter them?",
             "Chapter one. Crime as a choice.", lit={1968: r"Becker", 1970: r"Stigler"}, scale=("person", "city"),
             horizon=("a day", "a year"))
        self.supply()
        self.trade()
        self.planner()

    def supply(self):
        O = load("offenders")
        edges = np.array(O["edges"])
        share = np.array(O["hist"], float)
        ax = plane([0, 6], [0, 0.15], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.8, y_length=4.4,
                   xticks=[0, 1, 2, 3, 4, 5, 6], yticks=[0, 0.05, 0.1, 0.15], xlabel=r"gain from the offence, "
                   r"\ in years of prison it is worth", ylabel=r"share of potential offenders, \ per fifth of a year",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        bars = VGroup()
        for x0, x1, h in zip(edges[:-1], edges[1:], share):
            p0, p1 = ax.ax.c2p(x0, 0), ax.ax.c2p(x1, h)
            bars.add(Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 0.005), stroke_width=0.6,
                               stroke_color=BLACK, fill_color=GREY_B, fill_opacity=0.8).move_to((p0 + p1) / 2))
        cut = O["expected"]
        line = vline(ax, cut, 0, 0.15, FINE, 2.6)
        line_l = label(rf"$p \times S = {O['p']:.1f} \times {O['sentence']:.0f} = {cut:.1f}$", font_size=18,
                       color=FINE).next_to(ax.ax.c2p(cut, 0.145), RIGHT, buff=0.1)
        offend = VGroup(*[b for b, x0 in zip(bars, edges[:-1]) if x0 >= cut])
        side = VGroup(
            label(rf"{20000:,} of the Island's \\ potential offenders".replace(",", "{,}"), font_size=18, color=WHITE),
            label(rf"caught one time \\ in {1 / O['p']:.0f}; \ {O['sentence']:.0f} years if so", font_size=18,
                  color=CHANCE),
            label(rf"offend if the gain \\ beats {cut:.1f} years: \\ "
                  rf"{100 * O['play']['risk-neutral']['start']:.0f}\% do",
                  font_size=18, color=CRIME),
            label(r"raise $p$ or $S$: \\ the line moves right, \\ and fewer offend", font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Here is Becker's model on the Island. <bookmark mark='a'/> Twenty thousand potential offenders, each "
            "with a gain from some offence, measured in the years of prison it would be worth to them. Most gains "
            "are small; a few are large. <bookmark mark='b'/> The police catch one offender in five, and the "
            f"sentence is {O['sentence']:.0f} years. <bookmark mark='c'/> Someone who does not mind risk offends when "
            f"the gain beats the expected punishment, the chance times the sentence: {cut:.1f} years. Here, "
            f"{100 * O['play']['risk-neutral']['start']:.0f} percent of them would. <bookmark mark='d'/> Raise "
            "either the chance or the sentence and the line moves right: fewer offend. The supply of offences, like "
            "any supply, slopes."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.06), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(line), FadeIn(line_l), FadeIn(side[2]))
            self.play(offend.animate.set_fill(CRIME, opacity=0.85), run_time=1.5)
            vo.wait_until("d")
            new_cut = 2 * cut
            line2 = vline(ax, new_cut, 0, 0.15, FINE, 2.6)
            still = VGroup(*[b for b, x0 in zip(bars, edges[:-1]) if cut <= x0 < new_cut])
            self.play(Transform(line, line2), line_l.animate.next_to(ax.ax.c2p(new_cut, 0.145), RIGHT, buff=0.1),
                      still.animate.set_fill(GREY_B, opacity=0.8), FadeIn(side[3]), run_time=2.0)
        self.clear_scene()

    def trade(self):
        P = load("planner")
        f = np.array(P["curve_f"])
        ax = plane([0, 42], [0, 0.45], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.8, y_length=4.4,
                   xticks=[0, 10, 20, 30, 40], yticks=[0, 0.1, 0.2, 0.3, 0.4], xlabel=r"the fine, \ $F$",
                   ylabel=r"the chance of being caught, \ $p$", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        fg = np.linspace(0.5, 40, 400)
        curves = VGroup(*[path(ax, fg, k / fg, c, 2.4 if k != P["k"] else 3.4, yr=(0, 0.45)) for k, c in
                          ((0.3, GREY_B), (P["k"], FINE), (1.2, GREY_B))])
        k_l = label(rf"gold: \ $p \times F = {P['k']:.1f}$, \\ the same deterrence \\ all along; \ grey: \ 0.3 "
                    r"and 1.2", font_size=17, color=FINE)
        wall = vline(ax, P["f_max"], 0, 0.45, LOSS, 2.4)
        wall_l = label(r"the largest fine \\ anyone can pay", font_size=15, color=LOSS).next_to(
            ax.ax.c2p(P["f_max"], 0.42), LEFT, buff=0.1)
        tr = ValueTracker(float(f[0]))
        d = always_redraw(lambda: Dot(ax.ax.c2p(tr.get_value(), P["k"] / tr.get_value()), radius=0.09, color=WHITE))
        read = always_redraw(lambda: label(rf"fine {tr.get_value():.0f}, \ chance {100 * P['k'] / tr.get_value():.0f}"
                                           rf"\%: \ catching costs {P['cost_p'] * P['k'] / tr.get_value():.2f}",
                                           font_size=19, color=WHITE).to_edge(UP, buff=0.5))
        side = VGroup(
            k_l,
            label(r"catching is costly: \\ police, \ courts", font_size=18, color=POLICE),
            label(r"a fine is nearly free \\ to impose: \ money \\ moves, \ nothing is lost", font_size=18, color=FINE),
            label(rf"Becker: \ the largest \\ fine, \ the smallest \\ chance; \ here \\ {P['f_star']:.0f} and "
                  rf"{100 * P['p_star']:.0f}\%, \\ and {100 * P['offences_star']:.1f}\% offend", font_size=18,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Becker's second question was the city's: what is the cheapest way to deter? <bookmark mark='a'/> For "
            "an offender who does not mind risk, only the product of the chance and the fine matters. Every point "
            "on this curve deters exactly as much. <bookmark mark='b'/> But the points do not cost the same. "
            "Catching people takes police, courts and time; <bookmark mark='c'/> a fine, once someone is caught, "
            "costs almost nothing: money moves from one pocket to another. <bookmark mark='d'/> So slide along the "
            "curve: a bigger fine, a smaller chance, the same deterrence, less spent on catching. <bookmark "
            "mark='e'/> The slide stops only at the largest fine anyone can pay. Becker's answer: fines as large "
            "as possible, enforcement as thin as possible. On the Island, with each offence doing harm worth two "
            f"years, the best plan is a fine of {P['f_star']:.0f} and a chance of {100 * P['p_star']:.0f} percent, "
            f"and only {100 * P['offences_star']:.1f} percent offend."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(curves[1]), FadeIn(k_l), run_time=2.0)
            self.play(Create(curves[0]), Create(curves[2]), run_time=1.0)
            vo.wait_until("b")
            self.add(d, read)
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(tr.animate.set_value(float(f[-1])), run_time=6.0, rate_func=smooth)
            vo.wait_until("e")
            self.play(Create(wall), FadeIn(wall_l), FadeIn(side[3]))
        self.clear_scene()

    def planner(self):
        cards = point_cards([
            (r"no one can pay \\ that much", r"fines are capped by \\ wealth; \ beyond it, \\ prison, \ which is \\ "
                                               r"costly to impose", FINE),
            (r"marginal \\ deterrence", r"if theft and murder \\ cost the same, \\ why leave a \\ witness? "
                                        r"\ (Stigler)", LOSS),
            (r"mistakes", r"the innocent are \\ sometimes convicted: \\ huge, \ rare \\ penalties punish \\ them "
                          r"too", CHANCE),
            (r"who offends?", r"risk, \ impatience, \\ the next chapter's \\ question", E.ACCENT),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.2)
        head = label(r"why real penalties are not like that", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.BECKER_1968.tag + r"; \ Stigler, \ JPE (1970)", corner=DR, font_size=11)
        with self.voiceover(
            "No country hangs parking offenders, and the model says why not, once it is filled in. <bookmark "
            "mark='a'/> Fines are capped by what people have; beyond that the penalty must be prison, which costs "
            "the state money and the prisoner years, and is no longer a mere transfer. <bookmark mark='b'/> George "
            "Stigler added marginal deterrence: if robbery and murder carried the same penalty, a robber would lose "
            "nothing by killing the witness, so penalties must rise with the harm. <bookmark mark='c'/> Courts make "
            "mistakes, and a huge penalty applied rarely is also applied, sometimes, to the innocent. <bookmark "
            "mark='d'/> And the model so far assumed offenders who do not mind risk and count every future year "
            "of prison fully. Change that, and the answer to the simplest question changes. Which is the next "
            "chapter's game."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(Indicate(cards.cards[0], color=WHITE, scale_factor=1.04))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
