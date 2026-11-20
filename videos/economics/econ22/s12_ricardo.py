from __future__ import annotations

from videos.economics.econ22.common import *  # noqa: F403


class Ricardo(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Ricardian equivalence", r"If the government cuts taxes today and borrows, \ are households "
             r"any richer?", "Chapter ten. Ricardian equivalence.", lit={1820: r"Ricardo", 1974: r"Barro"},
             scale=("household", "nation"), horizon=("a lifetime", "generations"))
        self.barro()
        self.fails()
        self.island()

    def barro(self):
        rc = load("ricardo")
        ax = plane([-1, 22], [-0.18, 0.12], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.6, y_length=4.4,
                   xticks=[0, 5, 10, 15, 20], yticks=[-0.15, -0.1, -0.05, 0, 0.05, 0.1], xlabel=r"years from now",
                   ylabel=r"taxes cut ($+$) or raised ($-$), \ years of income", xfmt=lambda v: f"{v:g}",
                   yfmt=lambda v: f"{v:g}", font_size=16)
        zero = seg(ax, -1, 0, 22, 0, color=GREY_B, width=2)

        def bar(x, v, col):
            top, base = ax.ax.c2p(x, v)[1], ax.ax.c2p(x, 0)[1]
            r_ = Rectangle(width=ax.ax.c2p(x + 0.6, 0)[0] - ax.ax.c2p(x - 0.6, 0)[0], height=abs(top - base),
                           stroke_width=0, fill_color=col, fill_opacity=0.85)
            return r_.move_to([ax.ax.c2p(x, 0)[0], (top + base) / 2, 0])
        b0 = bar(0, rc["cut"], SPEND)
        b1 = bar(rc["years"], -rc["later"], HOLD)
        l0 = label(r"a tax cut today: \ a month's income", font_size=18, color=SPEND).next_to(b0, UR, buff=0.1)
        l1 = label(rf"repaid with interest: \\ $\frac{{1}}{{12}} \times 1.03^{{20}} = {rc['later']:.3f}$",
                   font_size=18, color=HOLD).next_to(b1, LEFT, buff=0.15)
        side = VGroup(
            label(r"present value of the later tax:", font_size=20, color=GREY_A),
            MathTex(r"\frac{" + f"{rc['later']:.3f}" + r"}{1.03^{20}} = \frac{1}{12}", font_size=36, color=WHITE),
            label(r"the household is no richer", font_size=22, color=E.ACCENT),
            label(r"so it saves the whole cut, \\ to pay the tax", font_size=20, color=SAVE),
            label(r"private saving rises \\ one for one with the deficit", font_size=20, color=SAVE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        hc = history_card(1974, r"Robert Barro", r"\emph{Are Government Bonds Net Wealth?}", color=SAVE, width=6.2,
                          font_size=19).to_corner(UR, buff=0.25)
        tag = published_tag(r"Barro, JPE 82(6) (1974): \ 1095--1117", corner=DR, font_size=12)
        with self.voiceover(
            "The 2001 rebate was a tax cut paid for by borrowing. Does that make households richer? "
            "<bookmark mark='a'/> Suppose the government cuts taxes today by a month's income and borrows to pay "
            "for it. <bookmark mark='b'/> Twenty years later it must repay the debt with interest: at three "
            f"percent, a tax of {rc['later']:.3f} of a year's income. <bookmark mark='c'/> Discount that later tax "
            "back to today and it is exactly the cut. The household that will pay the later tax is no richer. "
            "<bookmark mark='d'/> A permanent-income household therefore saves the whole cut, ready for the tax. "
            "Private saving rises one for one with public borrowing, and national saving does not change. "
            "<bookmark mark='e'/> Robert Barro made the argument rigorous in 1974, and David Ricardo had stated it, "
            "and doubted it, in 1820. Hence the name: Ricardian equivalence. Borrowing and taxing are equivalent."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(hc), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowFromEdge(b0, DOWN), FadeIn(l0))
            vo.wait_until("b")
            self.play(GrowFromEdge(b1, UP), FadeIn(l1))
            vo.wait_until("c")
            self.play(FadeIn(side[0]), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
        self.clear_scene()

    def fails(self):
        rows = VGroup(
            label(r"why it fails, \ and when", font_size=28, color=E.ACCENT),
            label(r"1. \ liquidity: \ a household short of cash spends the cut, \ whatever it owes later", font_size=23,
                  color=CASH),
            label(r"2. \ finite lives: \ if the tax falls on the next generation, \ this one is richer", font_size=23,
                  color=OLD),
            label(r"\quad Barro's reply: \ parents who care about their children save for them, \ through bequests",
                  font_size=21, color=GREY_A),
            label(r"3. \ distorting taxes, \ uncertainty about who will pay, \ and inattention", font_size=23,
                  color=GREY_A),
            label(r"the test is the rebate itself: \ a debt-financed cut, \ 20--40\% spent in a quarter", font_size=23,
                  color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(UP * 0.1)
        with self.voiceover(
            "It is a benchmark, and its value is in showing exactly what has to fail for deficits to matter. "
            "<bookmark mark='a'/> First, liquidity. A household short of cash spends the cut now, whatever it will "
            "owe later, because it would have liked to borrow anyway. <bookmark mark='b'/> Second, lives end. If the "
            "tax will fall on the next generation, this one is richer, and spends. <bookmark mark='c'/> Barro's "
            "reply: parents who care about their children will save the cut and leave it to them, to pay the tax. "
            "That needs bequests to be operative, which is a question about real families. "
            "<bookmark mark='d'/> Third, real taxes distort, no one knows who will pay them, and people may simply "
            "not be paying attention. <bookmark mark='e'/> And the cleanest test is the 2001 rebate itself, a cut "
            "financed by borrowing. Households spent twenty to forty percent of it in a single quarter."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def island(self):
        rc = load("ricardo")
        items = list(rc["spent"].items())
        cols = (INCOME, CASH, SPEND, HOLD)
        ax = plane([0.4, len(items) + 0.6], [0, 0.6], center=LEFT * 1.4 + DOWN * 0.4, x_length=8.8, y_length=4.6,
                   xticks=[], yticks=[0, 0.2, 0.4, 0.6], ylabel=r"share of the tax cut spent within the year",
                   yfmt=lambda v: f"{v:g}", font_size=16)
        bars = VGroup()
        for k, ((name, v), col) in enumerate(zip(items, cols)):
            x = k + 1
            h_ = max(ax.ax.c2p(0, v)[1] - ax.ax.c2p(0, 0)[1], 0.02)
            b = Rectangle(width=ax.ax.c2p(x + 0.3, 0)[0] - ax.ax.c2p(x - 0.3, 0)[0], height=h_, stroke_width=0,
                          fill_color=col, fill_opacity=0.85).move_to(ax.ax.c2p(x, 0), aligned_edge=DOWN)
            nm = label(name.replace(", ", r", \\ "), font_size=17, color=col).next_to(ax.ax.c2p(x, 0), DOWN, buff=0.15)
            val = label(f"{v:.2f}", font_size=20, color=col).next_to(b, UP, buff=0.08)
            bars.add(VGroup(b, nm, val))
        side = VGroup(
            label(r"the same cut, \\ four kinds of household", font_size=21, color=GREY_A),
            label(r"national saving falls \\ by what is spent", font_size=20, color=WHITE),
            label(r"so whether deficits \\ crowd out saving \\ depends on who \\ gets the cut", font_size=20,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "On the Island, the same debt-financed cut lands on four kinds of household. <bookmark mark='a'/> The "
            "Ricardian household spends none of it. <bookmark mark='b'/> A buffer-stock renter spends "
            f"{rc['spent']['buffer-stock renters']:.2f} of it within the year. <bookmark mark='c'/> The Island as a "
            f"whole, owners and renters together, {rc['spent']['the Island, all']:.2f}. <bookmark mark='d'/> And "
            f"households short of cash, {rc['spent']['short of cash']:.2f}. <bookmark mark='e'/> What is spent is "
            "what national saving loses. So whether government borrowing crowds out saving, and whether a tax cut "
            "stimulates, depends on who gets the cut. Part thirty-two, on the Treasury, comes back to it."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            for mk, b in zip("abcd", bars):
                vo.wait_until(mk)
                self.play(GrowFromEdge(b[0], DOWN), FadeIn(b[1]), FadeIn(b[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.clear_scene()
