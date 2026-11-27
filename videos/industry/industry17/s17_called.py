from __future__ import annotations

from videos.industry.industry17.common import *  # noqa: F403


class Called(VoiceoverScene):
    def construct(self):
        card(self, 15, "Called it?", "What did people forecast about the electric car, and what happened?",
             "Chapter fifteen. Called it? What did people forecast about the electric car, and what happened?",
             lit=("change",))
        self.tesla()
        self.eia()
        self.china()
        self.ours()

    def tesla(self):
        C = R["called"]["tesla"]
        pa = viz.plot_axes([2015.5, 2021], [0, 600_000], x_length=7.4, y_length=4.2, xticks=[2016, 2018, 2020],
                           yticks=[0, 200_000, 400_000, 600_000], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v / 1000:.0f}k",
                           ylabel="Tesla: vehicles produced", size=13).move_to([-2.2, -0.5, 0])
        plan = DashedLine(pa.ax.c2p(2017.6, C["plan"]), pa.ax.c2p(2018.4, C["plan"]), stroke_color=PRICE, stroke_width=4, dash_length=0.1)
        pl = tx("the plan: 500,000 in 2018", 15, PRICE, bold=True).next_to(plan, UP, buff=0.1)
        bars_ = viz.year_bars(pa, [2018, 2020], [C["p2018"], C["p2020"]], EV, width=0.6)
        labs = VGroup(tx(f"{C['p2018']:,.0f}", 15, EV, bold=True).next_to(bars_[0], UP, buff=0.08),
                      tx(f"{C['p2020']:,.0f}", 15, EV, bold=True).next_to(bars_[1], UP, buff=0.08))
        quote = VGroup(tx("Tesla, 4 May 2016:", 15, GREY_B),
                       tx("'we have decided to advance our 500,000", 15, WHITE), tx("total unit build plan ... to 2018,", 15, WHITE),
                       tx("two years earlier than previously planned'", 15, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([4.2, 1.2, 0])
        verdict = tx("Reached in 2020: the original date", 20, GOOD, bold=True).move_to([4.2, -1.2, 0])
        src = source("Tesla Motors, First Quarter 2016 Update (Form 8-K, 4 May 2016); Tesla, Forms 10-K 2018 and 2020", size=12)
        with self.voiceover(
            "This film's forecasts, starting with a carmaker's own. <bookmark mark='a'/> In May 2016 Tesla told its "
            "investors it would bring forward its plan to build half a million cars a year to 2018, two years earlier than "
            "planned. <bookmark mark='b'/> In 2018 it built "
            f"{C['p2018']:,.0f}: about half. <bookmark mark='c'/> In 2020 it built {C['p2020']:,.0f}. The target was met on "
            "its original date, two years after the accelerated one: right about the destination, wrong about the time. "
            "New plants take years to reach their rate."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src), FadeIn(quote[0]), FadeIn(ghost(bars_, quote[1:], plan, opacity=0.4)))
            vo.wait_until("a")
            self.play(FadeIn(quote[1:]), Create(plan), FadeIn(pl))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars_[0], DOWN), FadeIn(labs[0]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars_[1], DOWN), FadeIn(labs[1]), FadeIn(verdict))
        self.clear_scene()

    def eia(self):
        C = R["called"]
        aeo, us = C["aeo"], C["us"]
        pa = viz.plot_axes([2015, 2026], [0, 12], x_length=8.6, y_length=4.4, xticks=[2015, 2017, 2019, 2021, 2023, 2025],
                           yticks=[0, 3, 6, 9, 12], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:.0f}%",
                           ylabel="electric share of new US light vehicles (battery and plug-in hybrid)", size=13).move_to([-1.2, -0.5, 0])
        lf = poly(pa, [(y, aeo[y]) for y in range(2015, 2026)], PRICE, 3)
        lf.set_stroke(opacity=0.9)
        dash = DashedVMobject(lf, num_dashes=40)
        la = poly(pa, [(y, us[y]) for y in range(2015, 2026) if y in us], EV, 4)
        l1 = tx("EIA's forecast, January 2017", 15, PRICE, bold=True).next_to(pa.ax.c2p(2021, aeo[2021]), UP, buff=0.25).shift(LEFT * 0.6)
        l2 = tx("what happened (IEA)", 15, EV, bold=True).next_to(pa.ax.c2p(2023, us[2023]), RIGHT, buff=0.2).shift(DOWN * 0.35)
        pts = VGroup()
        for y in (2020, 2025):
            pts.add(VGroup(Dot(pa.ax.c2p(y, aeo[y]), radius=0.08, color=PRICE), Dot(pa.ax.c2p(y, us[y]), radius=0.08, color=EV),
                           tx(f"{y}: forecast {aeo[y]:.1f}%, actual {us[y]:.1f}%", 14, WHITE, bold=True).next_to(pa.ax.c2p(y, max(aeo[y], us[y])), UP, buff=0.35)))
        pts[1][2].shift(LEFT * 1.4)
        src = source("EIA, Annual Energy Outlook 2017, Reference case, supplement table 39; IEA, Global EV Outlook 2026 via Our "
                     "World in Data", size=12)
        with self.voiceover(
            "Next, America's Energy Information Administration, whose Annual Energy Outlook of January 2017 projected "
            "sales of every kind of light vehicle. <bookmark mark='a'/> Add up its battery and plug-in hybrid vehicles and "
            f"it expected them to be {aeo[2020]:.1f} per cent of new vehicles in 2020 and {aeo[2025]:.1f} per cent in "
            f"2025. <bookmark mark='b'/> What happened: {us[2020]:.1f} per cent in 2020, {us[2025]:.0f} per cent in 2025. "
            "<bookmark mark='c'/> Too high early, too low late, and in the end not far off: a good forecast, as long-range "
            "forecasts go."
        ) as vo:
            hd = tx("The EIA's 2017 outlook for America, against what happened", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
            self.play(FadeIn(pa), FadeIn(src), FadeIn(hd), FadeIn(l1), FadeIn(ghost(dash, la, opacity=0.45)))
            vo.wait_until("a")
            self.play(Create(dash), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(la), FadeIn(l2), run_time=2.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in pts], lag_ratio=0.4))
        self.clear_scene()

    def china(self):
        C = R["called"]["cn_plan"]
        rows = [("2017 plan: new energy vehicle sales by 2020", f"{C['nev2020']:.0f} million a year", f"{C['nev2020_actual']:.2f} million",
                 BAD, "short"),
                ("2017 plan: their share of sales by 2025", f"above {C['share2025']:.0f}%", f"{C['share2025_actual']:.1f}%", GOOD, "more than double"),
                ("2020 plan, restated: share by 2025", f"about {C['share2025_2020plan']:.0f}%", f"{C['share2025_actual']:.1f}%", GOOD, "more than double")]
        hdr = VGroup(tx("the target", 16, GREY_A, bold=True).move_to([1.4, 2.2, 0]), tx("what happened", 16, GREY_A, bold=True).move_to([4.6, 2.2, 0]))
        g = VGroup()
        for i, (what, tgt, act, col, v) in enumerate(rows):
            y = 1.3 - 1.25 * i
            g.add(VGroup(tx(what, 16, WHITE).move_to([-3.0, y, 0]), tx(tgt, 20, PRICE, bold=True).move_to([1.4, y, 0]),
                         tx(act, 22, col, bold=True).move_to([4.6, y, 0]), tx(v, 13, col).move_to([4.6, y - 0.35, 0])))
        src = source("MIIT, NDRC and MOST, Medium- and Long-Term Development Plan for the Automobile Industry (6 April 2017); "
                     "State Council General Office, New Energy Vehicle Industry Development Plan 2021-2035 (20 October 2020); "
                     "CAAM via the China Securities Journal and Xinhua", size=12)
        with self.voiceover(
            "Now a government's plans. <bookmark mark='a'/> In April 2017 three Chinese ministries set targets for the car "
            "industry: two million new energy vehicles a year by 2020. China sold "
            f"{C['nev2020_actual']:.2f} million. Short. <bookmark mark='b'/> And by 2025, new energy vehicles above twenty "
            f"per cent of sales. In 2025 they were {C['share2025_actual']:.0f} per cent. <bookmark mark='c'/> In 2020 the "
            "State Council restated the goal for 2025 as about twenty per cent. Five years out, the outcome was more than "
            "twice the plan."
        ) as vo:
            hd = tx("China's plans for new energy vehicles, against what happened", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
            self.play(FadeIn(src), FadeIn(hd), FadeIn(hdr), *[FadeIn(r_[0]) for r_ in g], FadeIn(ghost(*[r_[1] for r_ in g], opacity=0.4)))
            for mk, r_ in zip("abc", g):
                vo.wait_until(mk)
                self.play(FadeIn(r_[1]))
                self.play(FadeIn(r_[2], shift=LEFT * 0.2), FadeIn(r_[3]))
        self.clear_scene()

    def ours(self):
        C = R["called"]
        w = C["world"]
        proj = C["proj"]
        pa = viz.plot_axes([2015, 2027.5], [0, 45], x_length=8.4, y_length=4.4, xticks=[2015, 2018, 2021, 2024, 2026],
                           yticks=[0, 10, 20, 30, 40], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:.0f}%",
                           ylabel="electric share of new cars sold worldwide (IEA)", size=13).move_to([-1.6, -0.5, 0])
        dots = VGroup(*[Dot(pa.ax.c2p(y, w[y]), radius=0.08, color=EV) for y in range(2015, 2026)])
        fit = DashedVMobject(poly(pa, [(y, proj[y]) for y in range(2021, 2028)], PRICE, 3), num_dashes=30)
        p26 = Dot(pa.ax.c2p(2026, proj[2026]), radius=0.1, color=PRICE)
        l26 = tx(f"the S-curve through 2021-25 says {proj[2026]:.1f}% in 2026", 15, PRICE, bold=True).next_to(p26, LEFT, buff=0.15).shift(UP * 0.3)
        call = VGroup(tx("Industry, Built calls (27 November 2026):", 16, GREY_A),
                      tx(f"the IEA's world share for 2026", 18, WHITE, bold=True),
                      tx(f"will be below {C['threshold']:.0f}%", 24, PRICE, bold=True),
                      tx(f"probability {100 * C['prob']:.0f}%; scored mid-2027", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([4.6, 0.6, 0])
        why = VGroup(tx("why: China is already above half;", 14, GREY_A), tx("America repealed its credits in 2025;", 14, GREY_A),
                     tx("the fitted curve overshot 2025", 14, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([4.6, -1.5, 0])
        src = source("IEA, Global EV Outlook 2026 via Our World in Data; the logistic fit: this film's estimate", size=12)
        tag = estimate_tag("estimate: a logistic curve fitted to 2021-2025", size=13)
        with self.voiceover(
            "And our own call. <bookmark mark='a'/> These are the IEA's figures for the electric share of new cars sold "
            "worldwide, 2015 to 2025. <bookmark mark='b'/> Fit the S-shaped curve that new technologies usually follow "
            f"through the last five years, and it says {proj[2026]:.0f} per cent in 2026. <bookmark mark='c'/> We think "
            f"the real figure will come in below that: below {C['threshold']:.0f} per cent, with a probability of "
            f"{100 * C['prob']:.0f} per cent. China, the biggest market, is already past half and has less room to grow; "
            "America repealed its tax credits in 2025; and the same curve already ran ahead of the actual figure for "
            "2025. The IEA will publish the number in the middle of 2027, and we will score it here."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src), FadeIn(tag), FadeIn(ghost(dots, opacity=0.3)))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.1), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(fit), run_time=2.0)
            self.play(GrowFromCenter(p26), FadeIn(l26))
            vo.wait_until("c")
            self.play(FadeIn(call, shift=LEFT * 0.2))
            self.play(FadeIn(why))
        self.clear_scene()
