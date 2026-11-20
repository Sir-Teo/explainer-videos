from __future__ import annotations

from videos.economics.econ31.common import *  # noqa: F403


class QE(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Quantitative easing", r"What does buying bonds do, \ and how would anyone know?",
             "Chapter nine. Quantitative easing.",
             lit={1981: r"Wallace", 2011: r"Gagnon, \ Raskin, \ Remache and Sack"}, scale=("market", "nation"),
             horizon=("a day", "years"))
        self.accounts()
        self.size()
        self.events()

    def accounts(self):
        cbk = tacct(r"the central bank", CB, [(r"$+100$ \ bonds", BOND)], [(r"$+100$ \ reserves", RES)], width=4.0,
                    height=1.4)
        bank = tacct(r"the seller's bank", OUTPUT, [(r"$+100$ \ reserves", RES)], [(r"$+100$ \ deposits", OUTPUT)],
                     width=4.0, height=1.4)
        fund = tacct(r"a pension fund", PRICE, [(r"$-100$ \ bonds", BOND), (r"$+100$ \ deposits", OUTPUT)], [],
                     width=4.0, height=1.4)
        VGroup(cbk, bank, fund).arrange(RIGHT, buff=0.6).move_to(UP * 1.0)
        rows = VGroup(
            label(r"the central bank pays with reserves it creates", font_size=22, color=RES),
            label(r"the private sector holds fewer long bonds and more short-term money", font_size=22, color=BOND),
            label(r"in a frictionless world this changes nothing \ (Wallace, \ 1981): \ swapping one government "
                  r"liability for another", font_size=20, color=HOLD),
            label(r"in this one, \ investors who need long bonds pay more for the fewer left: \ long yields fall",
                  font_size=20, color=E.ACCENT),
        ).arrange(DOWN, buff=0.28).to_edge(DOWN, buff=0.5)
        tag = published_tag(r"Wallace, \ \emph{AER} 71(3) (1981); \ Vayanos and Vila, \ \emph{Econometrica} 89(1) "
                            r"(2021)", corner=DR, font_size=12)
        with self.voiceover(
            "Quantitative easing in T-accounts. <bookmark mark='a'/> The central bank buys a hundred of long-term "
            "government bonds from a pension fund, and pays by crediting a hundred of new reserves to the fund's "
            "bank, <bookmark mark='b'/> which credits the fund's deposit. <bookmark mark='c'/> The fund now holds "
            "a deposit instead of a bond. <bookmark mark='d'/> Nothing has been given away: the private sector "
            "holds less long-term debt and more short-term money. <bookmark mark='e'/> In a world without "
            "frictions, Neil Wallace showed in 1981, such a swap changes nothing at all, since both are liabilities "
            "of the government in the end. <bookmark mark='f'/> In this world, some investors, like pension funds, "
            "need long bonds to match long promises, and when the central bank removes some, the rest become "
            "dearer: long yields fall. Dimitri Vayanos and Jean-Luc Vila wrote that mechanism down as a model of "
            "preferred habitats."
        ) as vo:
            self.play(FadeIn(cbk), FadeIn(tag))
            vo.wait_until("a")
            self.play(Indicate(cbk.left, color=WHITE), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(bank))
            vo.wait_until("c")
            self.play(FadeIn(fund))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
            vo.wait_until("f")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def size(self):
        Q = load("qe")
        t = np.array(Q["t"])
        ax = plane([2007, 2027], [0, 10], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.8, y_length=4.8,
                   xticks=[2008, 2012, 2016, 2020, 2024], yticks=[0, 2, 4, 6, 8, 10],
                   ylabel=r"the Federal Reserve's assets, \ trillions of dollars", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=15)
        line = path(ax, t, Q["assets"], CB, 3.2, smooth=False)
        marks = VGroup()
        for x, name in ((2008.9, r"QE1"), (2010.84, r"QE2"), (2012.7, r"QE3"), (2017.75, r"runoff"),
                        (2020.2, r"2020"), (2022.45, r"runoff")):
            y = float(np.interp(x, t, Q["assets"]))
            marks.add(VGroup(Dot(ax.ax.c2p(x, y), radius=0.06, color=PRICE),
                             label(name, font_size=15, color=PRICE).next_to(ax.ax.c2p(x, y), UL, buff=0.06)))
        side = VGroup(
            label(rf"August 2008: \ \${Q['pre']:.1f} trillion", font_size=18, color=CB),
            label(r"three rounds of purchases, \\ 2008--14; \ a pause; \ runoff", font_size=18, color=PRICE),
            label(rf"2020: \ the largest round; \\ peak \${Q['peak']:.1f} trillion, \ {Q['peak_date'][:4]}",
                  font_size=18, color=PRICE),
            label(rf"now \${Q['last']:.1f} trillion", font_size=18, color=CB),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Federal Reserve Board: \ H.4.1, \ total assets (WALCL), \ via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "This is what the Federal Reserve did. <bookmark mark='a'/> Its assets were "
            f"{Q['pre']:.1f} trillion dollars in August 2008. <bookmark mark='b'/> Three rounds of purchases "
            "between late 2008 and 2014 took them past four trillion; from 2017 they were allowed to run off. "
            "<bookmark mark='c'/> In 2020 came the largest round of all, and a peak of "
            f"{Q['peak']:.1f} trillion dollars in {Q['peak_date'][:4]}. <bookmark mark='d'/> Since then the Fed "
            f"has let them shrink again, to {Q['last']:.1f} trillion. Did any of it work?"
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(line), run_time=3)
            self.play(LaggedStart(*[FadeIn(m) for m in marks[:4]], lag_ratio=0.3), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(marks[4]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(marks[5]), FadeIn(side[3]))
        self.clear_scene()

    def events(self):
        Q = load("qe")
        ev = Q["events"]
        bp = Q["event_bp"]
        ax = plane([0, 9], [-60, 20], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.4, y_length=4.6,
                   xticks=[], yticks=[-60, -40, -20, 0, 20], ylabel=r"change in the 10-year Treasury yield, \ "
                   r"basis points", yfmt=lambda v: f"{v:+.0f}" if v else "0", font_size=15)
        zero = seg(ax, 0, 0, 9, 0, GREY_C, 1.5)
        bars, names = VGroup(), VGroup()
        for k, (e, b) in enumerate(zip(ev, bp)):
            p0, p1 = ax.ax.c2p(k + 0.65, 0), ax.ax.c2p(k + 1.35, b)
            r = Rectangle(width=p1[0] - p0[0], height=abs(p1[1] - p0[1]), fill_color=BOND if b < 0 else INFL,
                          fill_opacity=0.85, stroke_width=0).move_to((p0 + p1) / 2)
            bars.add(r)
            d = e["date"]
            mon = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")[int(d[5:7]) - 1]
            names.add(label(rf"{int(d[8:])} {mon} \\ {d[:4]}", font_size=13, color=GREY_B).next_to(
                ax.ax.c2p(k + 1, 0), UP if b < 0 else DOWN, buff=0.1))
        side = VGroup(
            label(r"the eight days Gagnon, \ Raskin, \\ Remache and Sack chose: \\ news about purchases", font_size=17,
                  color=GREY_A),
            label(rf"together: \ {Q['total_bp']:+.0f} basis points \\ (their figure: \ $-91$)", font_size=18,
                  color=BOND),
            label(rf"every other day, \ November 2008 \\ to March 2010: \ {Q['nonevent_bp']:+.0f}", font_size=18,
                  color=INFL),
            label(r"``QE works in practice, \\ but it doesn't work in theory'' \\ --- Bernanke, \ January 2014",
                  font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Gagnon, \ Raskin, \ Remache and Sack, \ \emph{IJCB} 7(1) (2011); \ Bernanke at "
                            r"Brookings, \ 16 January 2014; \ DGS10 via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "The first test was an event study. <bookmark mark='a'/> Joseph Gagnon, Matthew Raskin, Julie Remache "
            "and Brian Sack picked the eight days between November 2008 and November 2009 that brought news about "
            "the first purchases, and measured what long yields did on each. <bookmark mark='b'/> Here is the "
            "ten-year Treasury yield on those days, from close to close. The announcement of the twenty-fifth of "
            f"November: {bp[0]:+.0f} basis points. The eighteenth of March 2009, when the Fed said it would buy "
            f"Treasuries: {bp[4]:+.0f}. <bookmark mark='c'/> Together, {abs(Q['total_bp']):.0f} basis points; their "
            "own figure was ninety-one. Their models of the term premium gave a similar range. "
            f"<bookmark mark='d'/> The sceptics' reply: on all the other days of the period, the same yield rose by "
            f"{Q['nonevent_bp']:.0f} basis points, as the economy recovered and deficits grew, and the result "
            "depends on which days you pick. <bookmark mark='e'/> Ben Bernanke's verdict, at the Brookings "
            "Institution in January 2014, as he left office: the problem with QE is that it works in practice, but "
            "it doesn't work in theory."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, UP if v < 0 else DOWN) for b, v in zip(bars, bp)],
                                  lag_ratio=0.25), FadeIn(names), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()
