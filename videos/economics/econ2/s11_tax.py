from __future__ import annotations

from videos.economics.econ2.common import *  # noqa: F403


class Tax(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Who pays a tax?", r"Does it matter who hands the money to the government?",
             "Chapter nine. Who pays a tax?", scale=("market", "nation"), horizon=("a year",))
        self.on_sellers()
        self.on_buyers()
        self.split()
        self.evidence()

    # ------------------------------------------------------------------
    def _pit_axes(self):
        ax = price_axes(10, (1, 3.5), x_length=6.6, y_length=4.6, qticks=list(range(0, 11, 2)),
                        pticks=[1, 1.5, 2, 2.5, 3, 3.5], qlabel=r"units", plabel=r"price", center=LEFT * 3.0 + DOWN * 0.4)
        return ax, ax.ax

    def on_sellers(self):
        d = load("tax")
        sup = load("supply")
        t = d["t"]
        v, c = sup["values"], sup["costs"]
        ax, a = self._pit_axes()
        st = market_steps(a, Market(tuple(v), tuple(c)).steps())
        shifted = step_curve(a, [(k, k + 1, x + t) for k, x in enumerate(sorted(c))], TAX, 4)
        wedge = Arrow(a.c2p(8.5, c[8]), a.c2p(8.5, c[8] + t), buff=0, color=TAX, stroke_width=4,
                      max_tip_length_to_length_ratio=0.3)
        wl = label(rf"+{dollars(t)}", font_size=22, color=TAX).next_to(wedge, RIGHT, buff=0.1)
        on = d["on_sellers"]
        paid = DashedLine(a.c2p(0, on["paid"]), a.c2p(10, on["paid"]), color=E.DEMAND, stroke_width=2.5)
        kept = DashedLine(a.c2p(0, on["received"]), a.c2p(10, on["received"]), color=E.SUPPLY, stroke_width=2.5)
        q0, q1 = d["q0"], d["q_taxed"]
        lost = Rectangle(width=a.c2p(1, 0)[0] - a.c2p(0, 0)[0], height=a.c2p(0, v[q0 - 1])[1] - a.c2p(0, c[q0 - 1])[1],
                         stroke_width=0, fill_color=E.MISS, fill_opacity=0.65).move_to(
            (a.c2p(q0 - 1, c[q0 - 1]) + a.c2p(q0, v[q0 - 1])) / 2)
        rows = VGroup(
            label(rf"a tax of {dollars(t)} a unit, \ paid by the sellers", font_size=26, color=TAX),
            label(rf"before: \ {q0} units at about {dollars(d['p0'])}", font_size=24, color=GREY_A),
            label(rf"buyers now pay {dollars(on['paid'])}", font_size=26, color=E.DEMAND),
            label(rf"sellers now keep {dollars(on['received'])}", font_size=26, color=E.SUPPLY),
            label(rf"{q1:.0f} units trade: \ the lost unit was worth {dollars(d['lost'])}", font_size=24, color=E.MISS),
            label(rf"the market still makes {pct(on['efficiency'], 1)} of the most it could", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).to_edge(RIGHT, buff=0.4).shift(UP * 0.2)
        tag = agora_tag(r"computed: Agora, learning traders; medians of 41 runs, sixth period", corner=DR, font_size=16)
        with self.voiceover(
            f"Put a tax of {money_words(t)} on every unit sold in the pit, and make the sellers pay it. "
            "<bookmark mark='a'/> To a seller, the tax is like a higher cost: a seller whose card says two dollars "
            f"now needs two dollars {int(round(t * 100))} to break even. The whole supply staircase rises by "
            f"{money_words(t)}. <bookmark mark='b'/> Run the market with Agora's learning traders. Before the tax, "
            f"{q0} units traded at about {money_words(d['p0'])}. <bookmark mark='c'/> Now the buyers pay about "
            f"{money_words(on['paid'])}, and the sellers, after handing over the tax, keep about "
            f"{money_words(on['received'])}. Each side has lost about twenty cents. <bookmark mark='d'/> And one unit "
            f"fewer is traded. That unit was worth {money_words(d['lost'])} more to its buyer than it cost its seller, "
            "and that's the deadweight loss of the tax: the gain from a trade the tax prevented, which nobody gets, "
            "not even the government."
        ) as vo:
            self.play(FadeIn(ax), Create(st.demand), Create(st.supply), FadeIn(tag), FadeIn(rows[0]), run_time=1.5)
            vo.wait_until("a")
            self.play(TransformFromCopy(st.supply, shifted), GrowArrow(wedge), FadeIn(wl), run_time=1.5)
            self.play(st.supply.animate.set_stroke(opacity=0.3))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(paid), FadeIn(rows[2]))
            self.play(Create(kept), FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(lost), FadeIn(rows[4]))
            self.play(FadeIn(rows[5]))
        self.clear_scene()

    def on_buyers(self):
        d = load("tax")
        s_, b_ = d["on_sellers"], d["on_buyers"]
        t = d["t"]
        table = VGroup()
        head = VGroup(VectorizedPoint(), label(r"sellers pay the tax", font_size=26, color=TAX),
                      label(r"buyers pay the tax", font_size=26, color=TAX))
        r1 = VGroup(label(r"price called in the pit", font_size=24, color=GREY_A),
                    label(dollars(s_["paid"]), font_size=30), label(dollars(b_["received"]), font_size=30))
        r2 = VGroup(label(r"what buyers give up", font_size=24, color=E.DEMAND),
                    label(dollars(s_["paid"]), font_size=30, color=E.DEMAND),
                    label(dollars(b_["paid"]), font_size=30, color=E.DEMAND))
        r3 = VGroup(label(r"what sellers keep", font_size=24, color=E.SUPPLY),
                    label(dollars(s_["received"]), font_size=30, color=E.SUPPLY),
                    label(dollars(b_["received"]), font_size=30, color=E.SUPPLY))
        r4 = VGroup(label(r"units traded", font_size=24, color=GREY_A), label(f"{s_['n']:.0f}", font_size=30),
                    label(f"{b_['n']:.0f}", font_size=30))
        for r in (head, r1, r2, r3, r4):
            r[0].move_to([-4.2, 0, 0])
            r[1].move_to([0.3, 0, 0])
            r[2].move_to([4.3, 0, 0])
            table.add(r)
        table.arrange(DOWN, buff=0.42).move_to(UP * 0.3)
        for r in table:
            for k, x in enumerate((-4.2, 0.3, 4.3)):
                r[k].set_x(x)
        foot = label(r"who hands over the money does not decide who bears the tax", font_size=28, color=E.ACCENT)
        foot.to_edge(DOWN, buff=0.6)
        tag = agora_tag(r"computed: Agora, learning traders; medians of 41 runs", corner=DR, font_size=16)
        with self.voiceover(
            "Now take the same tax off the sellers and put it on the buyers: at the till, every buyer pays the "
            f"price plus {money_words(t)} to the government. <bookmark mark='a'/> The price called out in the pit "
            f"falls, to about {money_words(b_['received'])}. <bookmark mark='b'/> But add the tax, and the buyers give up "
            f"{money_words(b_['paid'])}, within a few cents of before. The sellers keep "
            f"{money_words(b_['received'])}, also within a few cents. And the same number of units trade. "
            "<bookmark mark='c'/> This is one of the most useful results in economics, and one of the least "
            "believed. Who hands the money to the government doesn't decide who bears the tax. The market moves the "
            "price until the burden falls where it falls, whichever side the law names."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            self.play(FadeIn(r1[0]), FadeIn(r1[1]), FadeIn(r2[0]), FadeIn(r2[1]), FadeIn(r3[0]), FadeIn(r3[1]),
                      FadeIn(r4[0]), FadeIn(r4[1]))
            vo.wait_until("a")
            self.play(FadeIn(r1[2], shift=LEFT * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(r2[2], shift=LEFT * 0.1), FadeIn(r3[2], shift=LEFT * 0.1), FadeIn(r4[2], shift=LEFT * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()

    def split(self):
        d = load("tax")
        fish = d["fish"]
        el = fish["elasticity"]
        ax = price_axes(4, (0, 1), x_length=6.4, y_length=4.2, qticks=[0, 1, 2, 3, 4], pticks=[0, 0.25, 0.5, 0.75, 1],
                        qlabel=r"how much buyers respond, \ relative to sellers", plabel=r"share of the tax buyers bear",
                        money=False, center=LEFT * 2.8 + DOWN * 0.35)
        a = ax.ax
        curve = VMobject(stroke_color=TAX, stroke_width=4).set_points_smoothly(
            [a.c2p(x, y) for x, y in zip(d["ratio"], d["share"])])
        r_fish = abs(el["demand"]) / el["supply"]
        dot = Dot(a.c2p(r_fish, fish["sell"]["buyers_share"]), radius=0.09, color=E.FISH)
        dl = label(rf"the Island's fish: \ buyers bear {100 * fish['sell']['buyers_share']:.0f}\%", font_size=22,
                   color=E.FISH).next_to(dot, UR, buff=0.12)
        formula = MathTex(r"\text{buyers' share} = \frac{\varepsilon_S}{\varepsilon_S + |\varepsilon_D|}", font_size=40)
        formula.to_corner(UR, buff=0.6)
        ex = VGroup(
            label(r"demand hardly responds: \ buyers pay", font_size=24, color=E.DEMAND),
            label(r"cigarettes, \ petrol in the short run", font_size=21, color=GREY_B),
            label(r"supply cannot respond: \ sellers pay", font_size=24, color=E.SUPPLY),
            label(r"land: \ there is only so much of it", font_size=21, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).next_to(formula, DOWN, buff=0.5).align_to(formula, LEFT)
        tag = agora_tag(r"computed: Agora, the straight-line formula", corner=DR, font_size=16)
        with self.voiceover(
            "So where does the burden fall? <bookmark mark='a'/> On whichever side can get out of the way less. "
            "The share buyers bear is the sellers' elasticity over the sum of the two. <bookmark mark='b'/> On the "
            f"Island's fish market, buyers respond a little less than fishers do, so buyers bear about "
            f"{100 * fish['sell']['buyers_share']:.0f} percent of a tax on fish. <bookmark mark='c'/> When demand "
            "hardly responds, as with cigarettes, or petrol this month, the buyers pay nearly all of it. "
            "<bookmark mark='d'/> When supply can't respond at all, the sellers pay. Land is the classic case: "
            "there's only so much of it, so a tax on land falls on its owners, which is why Henry George wanted to "
            "tax nothing else."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(formula), Create(curve), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(dot, scale=0.5), FadeIn(dl))
            vo.wait_until("c")
            self.play(FadeIn(ex[0]), FadeIn(ex[1]))
            vo.wait_until("d")
            self.play(FadeIn(ex[2]), FadeIn(ex[3]))
        self.clear_scene()

    def evidence(self):
        head = heading(r"When who pays does matter")
        a = study_card(r"Salience", r"Chetty, Looney and Kroft (2009)",
                       [(r"what", r"a grocery store tags about 750 products with prices that include the sales tax, "
                                  r"for three weeks"),
                        (r"found", r"sales of the tagged products fall about 8\%"),
                        (r"and", r"taxes built into the shelf price cut drinking more than taxes added at the till")],
                       design="DiD", width=6.3, font_size=21)
        b = study_card(r"Evasion", r"Kopczuk, Marion, Muehlegger and Slemrod (2016)",
                       [(r"what", r"US states collect diesel tax from retailers, or further up the chain"),
                        (r"found", r"more of the tax reaches the pump price when suppliers remit it"),
                        (r"why", r"retailers evade more; \ the tax that is paid is the tax that counts")],
                       design="DiD", width=6.3, font_size=21)
        VGroup(a, b).arrange(RIGHT, buff=0.35, aligned_edge=UP).next_to(head, DOWN, buff=0.4)
        foot = label(r"the textbook result assumes everyone sees the tax, \ and everyone pays it", font_size=26,
                     color=E.ACCENT).to_edge(DOWN, buff=0.5)
        src = published_tag(r"\emph{AER} 99(4), 2009; \ \emph{AEJ: Economic Policy} 8(2), 2016", corner=DR, font_size=16)
        with self.voiceover(
            "The theory has two quiet assumptions, and the evidence finds both of them failing. "
            "<bookmark mark='a'/> The first is that people see the tax. In 2009 Raj Chetty, Adam Looney and Kory "
            "Kroft tagged about seven hundred and fifty products in a grocery store with prices that included the "
            "sales tax, for three weeks. Sales of those products fell by about eight percent, though the price at "
            "the till hadn't changed at all. Taxes that are hidden until the checkout are partly invisible. "
            "<bookmark mark='b'/> The second is that the tax is paid. American states collect their diesel taxes "
            "at different points: some from the retailer, some from the supplier further up the chain. Wojciech "
            "Kopczuk and his co-authors found that more of the tax reaches the pump price when suppliers remit it, "
            "because retailers evade more. <bookmark mark='c'/> So who writes the cheque matters exactly when it "
            "changes who notices the tax, or who manages not to pay it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(b, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()
