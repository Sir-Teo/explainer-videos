from __future__ import annotations

from videos.economics.econ29.common import *  # noqa: F403


class Cycle(VoiceoverScene):
    def construct(self):
        card(self, 1, r"What a cycle is", r"Booms and slumps measured against what?", "Chapter one. What a cycle "
             "is.", lit={1946: r"Burns and Mitchell", 1997: r"Hodrick and Prescott", 2018: r"Hamilton"},
             scale=("nation",), horizon=("a quarter", "a decade"))
        self.burns()
        self.trend()
        self.hamilton()
        self.endpoint()
        self.table()

    def burns(self):
        C = load("cycle")
        t, ly = np.array(C["t"]), np.array(C["ly"])
        ax = plane([1946, 2027], [7.4, 10.4], center=DOWN * 0.55 + LEFT * 0.2, x_length=11.6, y_length=4.4,
                   xticks=[1950, 1970, 1990, 2010], yticks=[np.log(x) for x in (2000, 5000, 10000, 25000)],
                   ylabel=r"real GDP, \ billions of 2017 dollars \ (log scale)", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{np.exp(v):,.0f}".replace(",", "{,}"), font_size=15)
        rec = shade(ax, C["recessions"], 7.4, 10.4)
        line = path(ax, t, ly, OUTPUT, 3, smooth=False)
        quote = VGroup(
            label(r"Burns and Mitchell, \ \emph{Measuring Business Cycles}, \ 1946:", font_size=19, color=E.ACCENT),
            label(r"expansions at about the same time in many activities, \ then similarly general contractions; "
                  r"\ recurrent but not periodic; \ from more than a year to ten or twelve years", font_size=18,
                  color=GREY_A)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        key = label(rf"grey: \ the NBER's {len(C['recessions'])} recessions since 1947", font_size=18,
                    color=GREY_B).next_to(ax.ax.c2p(1990, 7.6), UP, buff=0.05)
        tag = data_tag(r"BEA: \ real GDP; \ NBER: \ recession dates; \ via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "First, what is a business cycle? <bookmark mark='a'/> In 1946, Arthur Burns and Wesley Mitchell "
            "defined it as expansions that happen at about the same time in many economic activities, followed by "
            "similarly general contractions: recurrent, but not periodic, and lasting from more than a year to ten "
            "or twelve years. <bookmark mark='b'/> Here is America's real output since 1947, on a log scale, so "
            "that a straight line is steady growth. <bookmark mark='c'/> The grey bands are the recessions dated by "
            f"the committee of the National Bureau of Economic Research that Burns and Mitchell built: "
            f"{len(C['recessions'])} of them. <bookmark mark='d'/> Look how small they are against the growth. The "
            "cycle is a wobble around a trend, and to measure the wobble you first need the trend."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(quote, shift=DOWN * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(ax), Create(line), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(rec), FadeIn(key))
            self.bring_to_front(line)
            vo.wait_until("d")
            self.play(Indicate(line, color=WHITE, scale_factor=1.0))
        self.clear_scene()

    def trend(self):
        C = load("cycle")
        t, ly, tr = np.array(C["t"]), np.array(C["ly"]), np.array(C["trend"])
        top = plane([1946, 2027], [7.4, 10.4], center=UP * 1.5 + LEFT * 2.0, x_length=8.6, y_length=2.6,
                    xticks=[1950, 1970, 1990, 2010], yticks=[8, 9, 10], ylabel=r"log real GDP",
                    xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        bot = plane([1946, 2027], [-10, 6], center=DOWN * 2.0 + LEFT * 2.0, x_length=8.6, y_length=2.6,
                    xticks=[1950, 1970, 1990, 2010], yticks=[-10, -5, 0, 5], ylabel=r"cycle: \ \% from trend",
                    xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        y_l = path(top, t, ly, OUTPUT, 2.5, smooth=False)
        tr_l = path(top, t, tr, E.ACCENT, 3, smooth=False)
        rec = shade(bot, C["recessions"], -10, 6)
        zero = seg(bot, 1946, 0, 2027, 0, GREY_D, 1.5)
        cyc = path(bot, t, C["hp"], OUTPUT, 2.5, smooth=False, yr=(-10, 6))
        eq = MathTex(r"\min_{\tau}\ \sum_t (y_t-\tau_t)^2 + \lambda \sum_t \big(\Delta^2 \tau_t\big)^2",
                     font_size=30).to_edge(RIGHT, buff=0.3).shift(UP * 2.2)
        side = VGroup(
            label(r"fit the data closely...", font_size=19, color=OUTPUT),
            label(r"...but keep the trend smooth: \\ penalize changes in its slope", font_size=19, color=E.ACCENT),
            label(r"$\lambda = 1600$ for quarterly data: \\ a convention, \ not an estimate", font_size=19,
                  color=HOLD),
            label(rf"the cycle's standard deviation: \\ {C['sd_hp']:.1f}\% of output", font_size=19, color=OUTPUT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(eq, DOWN, buff=0.4)
        if side.get_right()[0] > 7.0:
            side.shift(LEFT * (side.get_right()[0] - 6.95))
        tag = published_tag(r"Hodrick and Prescott, \ \emph{JMCB} 29(1) (1997), \ circulated from 1980; \ BEA via "
                            r"FRED", corner=DR, font_size=12)
        with self.voiceover(
            "The most used trend in macroeconomics was proposed by Robert Hodrick and Edward Prescott, in a paper "
            "circulated from 1980 and published in 1997. <bookmark mark='a'/> Choose a trend tau to make two things "
            "small at once: the gaps between the data and the trend, and the changes in the trend's slope. "
            "<bookmark mark='b'/> The first term keeps the trend close to the data. <bookmark mark='c'/> The second "
            "keeps it smooth. Lambda sets the balance, and for quarterly data everyone uses sixteen hundred, a "
            "convention rather than an estimate. <bookmark mark='d'/> Here is the trend through log output, in "
            "gold. <bookmark mark='e'/> Subtract it and what is left is the cycle: output's percentage gap from "
            f"trend. Its standard deviation is {C['sd_hp']:.1f} percent, and every recession shows as a dip."
        ) as vo:
            self.play(FadeIn(top), Create(y_l), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(tr_l), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(bot), FadeIn(rec), FadeIn(zero), run_time=0.6)
            self.play(Create(cyc), FadeIn(side[3]), run_time=2)
        self.clear_scene()

    def hamilton(self):
        C = load("cycle")
        ax = plane([1946, 2027], [-12, 10], center=LEFT * 2.0 + DOWN * 0.3, x_length=8.6, y_length=4.8,
                   xticks=[1950, 1970, 1990, 2010], yticks=[-10, -5, 0, 5, 10], ylabel=r"\% from trend",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=15)
        rec = shade(ax, C["recessions"], -12, 10)
        zero = seg(ax, 1946, 0, 2027, 0, GREY_D, 1.5)
        hp = path(ax, C["t"], C["hp"], OUTPUT, 2.5, smooth=False, yr=(-12, 10))
        hm = path(ax, C["ham_t"], C["ham"], TECH, 2.5, smooth=False, yr=(-12, 10))
        side = VGroup(
            label(r"Hamilton, \ 2018: \\ ``Why you should never \\ use the HP filter''", font_size=20,
                  color=TECH),
            label(r"it can invent cycles \\ the data do not have, \\ and it rewrites the end", font_size=19,
                  color=HOLD),
            label(r"his cycle: \ the error in \\ forecasting output two years \\ ahead from its last four "
                  r"quarters", font_size=19, color=TECH),
            label(rf"the two agree on timing \\ (correlation {C['corr_hp_ham']:.2f}), \\ not on size: \ "
                  rf"{C['sd_ham']:.1f}\% against {C['sd_hp']:.1f}\%", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Hamilton, \ \emph{Review of Economics and Statistics} 100(5) (2018); \ BEA via FRED",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Not everyone accepts the convention. <bookmark mark='a'/> In 2018 James Hamilton published a paper "
            "called Why You Should Never Use the Hodrick-Prescott Filter. <bookmark mark='b'/> He showed it can "
            "create cyclical patterns that are not in the data, and that its estimate near the end of the sample "
            "keeps changing as new data arrive. <bookmark mark='c'/> His alternative: define the cycle as the error "
            "you make when you forecast output two years ahead by a regression on its last four quarters. Whatever "
            "you could not have seen coming is the cycle. <bookmark mark='d'/> In red, Hamilton's cycle; in green, "
            f"Hodrick and Prescott's. They agree about timing, with a correlation of {C['corr_hp_ham']:.2f}, but "
            f"Hamilton's swings are twice the size: {C['sd_ham']:.1f} percent against {C['sd_hp']:.1f}. How big the "
            "cycle is depends on how you define the trend, and so does every number a model is asked to match."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(rec), FadeIn(zero), Create(hp), FadeIn(tag), run_time=1.2)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(hm), FadeIn(side[3]), run_time=2)
        self.clear_scene()

    def endpoint(self):
        C = load("cycle")["endpoint"]
        t = np.array(C["t"])
        k = t >= 2000
        ax = plane([2000, 2008.75], [-3, 3], center=LEFT * 2.0 + DOWN * 0.3, x_length=8.4, y_length=4.6,
                   xticks=[2000, 2002, 2004, 2006, 2008], yticks=[-3, -2, -1, 0, 1, 2, 3], ylabel=r"\% from trend",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.0f}" if v else "0", font_size=15)
        zero = seg(ax, 2000, 0, 2008.75, 0, GREY_D, 1.5)
        early = path(ax, t[k], np.array(C["early"])[k], E.ACCENT, 3, smooth=False)
        late = path(ax, t[k], np.array(C["late"])[k], OUTPUT, 3, smooth=False)
        e_end, l_end = C["early"][-1], C["late"][-1]
        side = VGroup(
            label(r"gold: \ the HP cycle as it looked \\ with data to the autumn of 2008", font_size=19,
                  color=E.ACCENT),
            label(rf"2008, \ third quarter: \ {e_end:+.1f}\% \\ (below trend)", font_size=19, color=E.ACCENT),
            label(r"green: \ the same quarters, \\ filtered with today's data", font_size=19, color=OUTPUT),
            label(rf"the same quarter: \ {l_end:+.1f}\% \\ (above trend)", font_size=19, color=OUTPUT),
            label(r"near the end the trend is a guess \\ about data that have not arrived", font_size=20,
                  color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"BEA: \ real GDP, \ via FRED; \ this film's filtering", corner=DR, font_size=12)
        with self.voiceover(
            "Here is the end-point problem at work. <bookmark mark='a'/> In gold, the Hodrick-Prescott cycle for "
            "2000 to 2008, computed with only the data available up to the third quarter of 2008. "
            f"<bookmark mark='b'/> It puts that quarter {say_num(abs(e_end), 1)} percent below trend: the trend "
            "carries on at the pace of the boom years, and output has fallen short of it. <bookmark mark='c'/> In "
            "green, the same quarters filtered with all the data we have today, including the recession and the "
            f"slow recovery that followed. <bookmark mark='d'/> Now the same quarter is {say_num(l_end, 1)} percent "
            "above trend, because the trend has bent down to meet the years after. <bookmark mark='e'/> Near the "
            "end of a sample, the trend is a guess about data that have not arrived. So the most recent cycle, the "
            "one a policymaker cares about, is the one any filter measures worst; here even its sign flipped."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(Create(early), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(late), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def table(self):
        F = load("facts")
        d = F["data"]
        names = [("y", r"output \ (real GDP)", OUTPUT), ("c", r"consumer spending", CONS),
                 ("i", r"investment", INVEST), ("n", r"hours worked$^*$", HOURS),
                 ("w", r"output per hour$^*$", PROD)]
        head = VGroup(label(r"series", font_size=21, color=GREY_B), label(r"s.d., \ \%", font_size=21, color=GREY_B),
                      label(r"relative to output", font_size=21, color=GREY_B),
                      label(r"correlation with output", font_size=21, color=GREY_B))
        xs = [-4.4, -0.9, 1.8, 4.9]
        for h, x in zip(head, xs):
            h.move_to(RIGHT * x + UP * 2.2)
        rows = VGroup()
        for n, (k, nm, col) in enumerate(names):
            y = 1.3 - 0.75 * n
            r = VGroup(label(nm, font_size=22, color=col).move_to(RIGHT * xs[0] + UP * y),
                       label(rf"{d[k]['sd']:.2f}", font_size=22).move_to(RIGHT * xs[1] + UP * y),
                       label(rf"{d[k]['rel']:.2f}", font_size=22).move_to(RIGHT * xs[2] + UP * y),
                       label(rf"{d[k]['corr']:.2f}", font_size=22).move_to(RIGHT * xs[3] + UP * y))
            rows.add(r)
        rule = Line(LEFT * 6.3, RIGHT * 6.3, stroke_color=GREY_D, stroke_width=1.5).move_to(UP * 1.8)
        foot = label(r"$^*$nonfarm business sector, \ relative to and correlated with its output", font_size=16,
                     color=GREY_B).move_to(DOWN * 2.45)
        title = label(rf"the American business cycle, \ {F['first'][:4]}--{F['last'][:4]}, \ HP-filtered, "
                      r"quarterly", font_size=25, color=E.ACCENT).to_edge(UP, buff=0.35)
        tag = data_tag(r"BEA and BLS, \ via FRED; \ this film's filtering", corner=DR, font_size=12)
        with self.voiceover(
            "With a filter in hand, the cycle becomes a table of numbers, and this table is what any model of the "
            "cycle is asked to explain. America, 1948 to 2019, before the pandemic. <bookmark mark='a'/> Output's "
            f"cycle has a standard deviation of {d['y']['sd']:.1f} percent. <bookmark mark='b'/> Consumer spending "
            f"moves less, {d['c']['rel']:.2f} times as much, and that includes cars and other durables. "
            f"<bookmark mark='c'/> Investment moves {d['i']['rel']:.1f} times as much as output: it is where the "
            "cycle lives. <bookmark mark='d'/> Hours worked move almost as much as output, and with it. "
            f"<bookmark mark='e'/> Output per hour moves about half as much, with a correlation of only "
            f"{d['w']['corr']:.2f}. Hold on to these numbers: in chapter nine the model gets its own column."
        ) as vo:
            self.play(FadeIn(title), FadeIn(head), FadeIn(rule), FadeIn(foot), FadeIn(tag))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
        self.clear_scene()
