from __future__ import annotations

from videos.economics.econ14.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 14, r"In practice: \ pay, \ franchises and procurement", r"Where do real contracts sit between a "
             r"wage and a rent, \ and why?", "Chapter fourteen. In practice: pay, franchises and procurement.",
             lit={1987: r"Brickley and Dark", 1990: r"Jensen and Murphy", 1993: r"Laffont and Tirole",
                  1998: r"Hall and Liebman"},
             scale=("person", "firm", "government"), horizon=("a year",))
        self.spectrum()
        self.executives()
        self.procurement()

    def spectrum(self):
        x0, x1, y = -5.6, 5.6, 0.2
        line = Line([x0, y, 0], [x1, y, 0], color=GREY_B, stroke_width=3)
        ends = VGroup(label(r"a wage: \ the agent keeps none \\ of what extra effort adds", font_size=18, color=GREY_A
                            ).next_to([x0, y, 0], DOWN, buff=1.25),
                      label(r"a rent: \ the agent keeps \\ all of it", font_size=18, color=PAY
                            ).next_to([x1, y, 0], DOWN, buff=1.25))

        def X(v):
            return x0 + (x1 - x0) * v

        items = [
            (0.0, r"civil servant, \\ cost-plus contract", GREY_A, UP),
            (0.08, r"salesperson's \\ commission", SIGNAL, DOWN),
            (0.5, r"sharecropper, \\ half the crop", EFFORT, UP),
            (0.9, r"franchisee: \ the profit, \\ less royalties", TEAM, DOWN),
            (1.0, r"fixed rent, \ fixed-price \\ contract, \ Xiaogang", PAY, UP),
        ]
        marks = VGroup()
        for v, t, col, side in items:
            d = Dot([X(v), y, 0], radius=0.09, color=col)
            lab = label(t, font_size=17, color=col).next_to(d, side, buff=0.3)
            marks.add(VGroup(d, lab))
        head = label(r"the agent's share of what their extra effort adds", font_size=26, color=E.ACCENT).to_edge(
            UP, buff=0.6)
        foot = label(r"positions roughly illustrative: \ the formula of chapter four says where each should sit",
                     font_size=19, color=GREY_B).to_edge(DOWN, buff=0.5)
        rows = label(r"franchising: \ outlets far from head office, \ hard to watch, \ are likelier to be franchised",
                     font_size=21, color=TEAM).next_to(foot, UP, buff=0.3)
        tag = published_tag(r"Brickley and Dark, JFE 18(2) (1987)", corner=DR, font_size=13)
        with self.voiceover(
            "Every contract in this part sits somewhere on one line: the share of what extra effort adds that the "
            "agent keeps. <bookmark mark='a'/> At one end, a wage: a civil servant, or a firm on a cost-plus "
            "contract, which is paid its costs whatever they are. <bookmark mark='b'/> A salesperson's commission is "
            "a small share of each sale. A sharecropper keeps half. <bookmark mark='c'/> A franchisee keeps the "
            "outlet's profit, less the royalties and fees paid to the brand. And at the far end, a fixed rent, a "
            "fixed-price contract, or Xiaogang's quota. <bookmark mark='d'/> Where each should sit is what chapter "
            "four's formula says: more toward the rent where effort responds and results are clean, more toward the "
            "wage where luck dominates or the measure misses much of the job. Franchising fits: in James Brickley and "
            "Frederick Dark's data, outlets far from head office, which are costly to watch, were likelier to be "
            "franchised, and those near it to be owned."
        ) as vo:
            self.play(FadeIn(head), Create(line), FadeIn(ends), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(marks[0]))
            vo.wait_until("b")
            self.play(FadeIn(marks[1]), FadeIn(marks[2]))
            vo.wait_until("c")
            self.play(FadeIn(marks[3]), FadeIn(marks[4]))
            vo.wait_until("d")
            self.play(FadeIn(foot), FadeIn(rows))
        self.clear_scene()

    def executives(self):
        rows = VGroup(
            label(r"Michael Jensen and Kevin Murphy, \ 1990: \ for each \$1,000 of shareholders' wealth, \ chief "
                  r"executives' wealth moved about \$3.25", font_size=22),
            label(r"in this part's terms: \ a share of about $0.003$", font_size=24, color=PAY),
            label(r"their reading: \ paid like bureaucrats", font_size=23, color=RISK),
            label(r"Brian Hall and Jeffrey Liebman, \ 1998: \ count stock and options, \ and the link was far stronger, "
                  r"\ and growing", font_size=22, color=SIGNAL),
            label(r"a small share of a very large firm \ is still a great deal of money", font_size=23,
                  color=E.ACCENT),
            label(r"and few firms filter out the market, \ as chapter five's principle says they should", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.34).move_to(UP * 0.1)
        tag = published_tag(r"Jensen and Murphy, JPE 98(2) (1990); \ Hall and Liebman, QJE 113(3) (1998)", corner=DR,
                            font_size=13)
        with self.voiceover(
            "Where do chief executives sit? <bookmark mark='a'/> In 1990 Michael Jensen and Kevin Murphy estimated "
            "that for each thousand dollars of shareholders' wealth, a chief executive's own wealth moved by about "
            "three dollars and twenty-five cents. <bookmark mark='b'/> In this part's terms, a share of about three "
            "thousandths. <bookmark mark='c'/> They concluded that executives were paid like bureaucrats. "
            "<bookmark mark='d'/> Eight years later Brian Hall and Jeffrey Liebman counted the stock and options "
            "executives held, which had grown enormously, and found the link far stronger, and rising. "
            "<bookmark mark='e'/> The two are less at odds than they sound: a small share of a very large firm is "
            "still a great deal of money, and what matters for effort is the dollars at stake, not the share. "
            "<bookmark mark='f'/> What remains a puzzle is how rarely pay filters out the market as a whole, as "
            "Bertrand and Mullainathan's oil executives showed."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def procurement(self):
        heads = [r"contract", r"the firm keeps \\ cost savings", r"who bears \\ cost overruns", r"used where"]
        xs = [-4.6, -1.5, 1.4, 4.5]
        head = VGroup(*[label(h, font_size=19, color=GREY_B).move_to(RIGHT * x + UP * 2.3) for h, x in zip(heads, xs)])
        rule = Line(LEFT * 6.3 + UP * 1.75, RIGHT * 6.3 + UP * 1.75, color=GREY_C, stroke_width=1.5)
        data = [
            (r"cost-plus", r"none", r"the buyer", r"new weapons, \\ research", GREY_A),
            (r"incentive", r"a share", r"split", r"large projects \\ with some risk", SIGNAL),
            (r"fixed price", r"all", r"the firm", r"routine goods \\ and services", PAY),
        ]
        rows = VGroup()
        for i, (a_, b_, c_, d_, col) in enumerate(data):
            y = 1.05 - 1.05 * i
            rows.add(VGroup(*[label(t, font_size=21, color=col if k == 0 else WHITE).move_to(RIGHT * x + UP * y)
                              for k, (t, x) in enumerate(zip((a_, b_, c_, d_), xs))]))
        foot = VGroup(
            label(r"Laffont and Tirole: \ a regulator should offer a menu, \ from cost-plus to fixed price", font_size=22,
                  color=E.ACCENT),
            label(r"efficient firms choose fixed price and work hard; \ the others, \ cost-plus; \ the efficient are "
                  r"left less of a windfall", font_size=21, color=GREY_A),
            label(r"and when even the result can't be written down, \ ownership does the work \ (part eight)",
                  font_size=21, color=TEAM),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"Laffont and Tirole, \ A Theory of Incentives in Procurement and Regulation (1993)",
                            corner=DR, font_size=13)
        with self.voiceover(
            "Governments face the same line when they buy. <bookmark mark='a'/> A cost-plus contract pays the "
            "firm's costs plus a fee: the firm keeps none of what it saves, and the buyer bears every overrun. It "
            "is used where costs are too uncertain for any firm to promise a price, like a new weapon. "
            "<bookmark mark='b'/> A fixed-price contract is the rent: the firm keeps every saving and bears every "
            "overrun. <bookmark mark='c'/> Incentive contracts split the difference by an agreed share. "
            "<bookmark mark='d'/> Jean-Jacques Laffont and Jean Tirole showed that a buyer who can't tell an "
            "efficient firm from an inefficient one should offer a menu. <bookmark mark='e'/> Efficient firms choose "
            "something close to a fixed price and work hard to cut costs; the others choose something close to "
            "cost-plus. The menu leaves the efficient firms less of a windfall than one fixed price for all would. "
            "<bookmark mark='f'/> And when even the result can't be written into a contract, part eight's answer "
            "applies: who owns the asset decides who invests in it."
        ) as vo:
            self.play(FadeIn(head), Create(rule), FadeIn(rows[0]), FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            for mk, r in zip("def", foot):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
