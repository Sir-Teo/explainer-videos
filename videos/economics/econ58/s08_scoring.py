from __future__ import annotations

from videos.economics.econ58.common import *  # noqa: F403


class Scoring(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Scoring a bill", r"What will a law cost over ten years, \ and how good are the scores?",
             "Chapter seven. Scoring a bill.", lit={1975: r"the CBO opens", 2010: r"the OBR", 2017: r"a dynamic "
                                                    r"score"},
             scale=("nation",), horizon=("a decade",))
        self.kinds()
        self.budget_window()
        self.dynamic()
        self.track_record()

    def kinds(self):
        chain = flow_chain([(r"the baseline: \ current law, \ projected ten years ahead", GREY_B),
                            (r"static: \ the bill's arithmetic, \ nobody changes anything", STATIC),
                            (r"conventional: \ people respond, \ the economy's size held fixed", BEHAV),
                            (r"dynamic: \ output, \ prices and interest rates change too", DYN)],
                           direction=DOWN, box_w=6.4, box_h=0.75, buff=0.3, font_size=21,
                           notes=[r"what would happen anyway", r"rarely published", r"the official score in the "
                                  r"United States, \ from the Play it", r"for big bills, \ alongside"],
                           note_size=19)
        chain.move_to(DOWN * 0.1)
        head = label(r"the scorekeepers: \ CBO and the Joint Committee on Taxation; \ the OBR; \ the CPB",
                     font_size=24, color=E.ACCENT).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A law is scored, not appraised. In America the Congressional Budget Office, since 1975, and the Joint "
            "Committee on Taxation estimate what each bill does to the budget; in Britain the Office for Budget "
            "Responsibility, since 2010; in the Netherlands the Central Planning Bureau, which even scores the "
            "parties' election programmes. <bookmark mark='a'/> Everything starts from a baseline: the budget under "
            "current law, projected ten years ahead. <bookmark mark='b'/> A static score is the bill's arithmetic "
            "with no one changing anything. <bookmark mark='c'/> The conventional score, the official one in "
            "Washington, lets people respond, as the Play it did, while holding the size of the economy fixed. "
            "<bookmark mark='d'/> A dynamic score lets output, prices and interest rates move too, and is published "
            "alongside for the biggest bills."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                anims = [FadeIn(chain.boxes[k], shift=DOWN * 0.1), FadeIn(chain.notes[k], shift=RIGHT * 0.1)]
                if k:
                    anims.append(GrowArrow(chain.arrows[k - 1]))
                self.play(*anims)
        self.clear_scene()

    def budget_window(self):
        S = load("scoring")
        W = S["window"]
        ax = plane([0, 15.5], [0, 130], center=LEFT * 2.4 + DOWN * 0.6, x_length=7.6, y_length=4.2,
                   xticks=[1, 5, 10, 15], yticks=[0, 50, 100], xlabel=r"year", ylabel=r"cost, \ millions a year",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=15)
        win = shade(ax, [(0.5, 10.5)], 0, 130, "#2C3E50", 0.6)
        wl = label(r"the ten-year window", font_size=18, color=CBO).next_to(ax.ax.c2p(5.5, 130), DOWN, buff=0.1)

        def bar(k, h, col, op=0.85):
            p0, p1 = ax.ax.c2p(k - 0.35, 0), ax.ax.c2p(k + 0.35, h)
            return Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=col, fill_opacity=op,
                             stroke_width=0).move_to((p0 + p1) / 2)

        scored = VGroup(*[bar(k, 100, BEHAV) for k in range(1, 9)])
        gap = VGroup(*[bar(k, 100, COST, 0.35) for k in range(9, 11)])
        after = VGroup(*[bar(k, 100, COST, 0.35) for k in range(11, 16)])
        side = VGroup(
            label(rf"written to expire after year 8: \ scored at {W['window']:.0f}", font_size=21, color=BEHAV),
            label(rf"if extended, \ as most are: \ {W['permanent']:.0f} in the window", font_size=21, color=COST),
            label(r"the 2017 tax cuts: \ individual rates set to expire after 2025; \ made permanent in 2025",
                  font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(UP, buff=0.5).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "The ten-year window is a rule, and rules are gamed. <bookmark mark='a'/> A tax cut costing a hundred "
            "million a year, written to expire after eight years, is scored at "
            f"{W['window']:.0f} million. <bookmark mark='b'/> Nobody expects it to expire; if it is extended, as most "
            f"such cuts are, it costs {W['permanent']:.0f} in the window and keeps costing after. <bookmark mark='c'/> "
            "The individual tax cuts of 2017 were written to expire after 2025, which lowered their score and kept "
            "the bill within the Senate's rules; in 2025 Congress made them permanent, and the cost of doing so was "
            "scored then."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(win), FadeIn(wl))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in scored], lag_ratio=0.15), FadeIn(side[0]),
                      run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in (*gap, *after)], lag_ratio=0.15),
                      FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def dynamic(self):
        S = load("scoring")
        D = S["dynamic"]
        TC = tables.TCJA_2017.data
        t = np.array(D["t"])
        ax = plane([0.4, 10.6], [-0.3, 1.4], center=LEFT * 2.6 + DOWN * 0.5, x_length=7.0, y_length=4.4,
                   xticks=list(range(1, 11)), yticks=[0, 0.5, 1.0], xlabel=r"year",
                   ylabel=r"cost, \ \% of GDP", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", font_size=15)
        z = Line(ax.ax.c2p(0.4, 0), ax.ax.c2p(10.6, 0), color=GREY_C, stroke_width=1.2)

        def rect(k, y0, y1, col):
            p0, p1 = ax.ax.c2p(k - 0.32, y0), ax.ax.c2p(k + 0.32, y1)
            return Rectangle(width=p1[0] - p0[0], height=abs(p1[1] - p0[1]), fill_color=col, fill_opacity=0.85,
                             stroke_width=0).move_to((p0 + p1) / 2)

        conv = VGroup(*[rect(k, 0, c, BEHAV) for k, c in zip(t, D["conventional"])])
        grow = VGroup(*[rect(k, c + g, c, BEN) for k, c, g in zip(t, D["conventional"], D["growth"])])
        rate = VGroup(*[rect(k, c, c + r, DYN) for k, c, r in zip(t, D["conventional"], D["rates"])])
        side = VGroup(
            label(rf"a tax cut of 1\% of GDP a year: \ {D['sum_conventional']:.1f}\% over ten years", font_size=19,
                  color=BEHAV),
            label(rf"growth: \ output up to 0.4\%, \ taxed at 30\%: \ ${D['sum_growth']:+.2f}$".replace("-", "{-}"),
                  font_size=19, color=BEN),
            label(rf"interest rates: \ each point of debt adds 0.025 to the rate on all debt: \ "
                  rf"${D['sum_rates']:+.2f}$", font_size=19, color=DYN),
            label(rf"dynamic: \ {D['sum_dynamic']:.2f}\% \ (and {D['sum_service']:.2f} of interest on the new debt)",
                  font_size=20, color=WHITE),
            label(rf"CBO on the 2017 act: \ \${TC['cbo_total']} trillion, \ after growth ${{-}}${TC['feedback']} and "
                  rf"added interest $+${TC['interest']}", font_size=18, color=CBO),
            label(r"CBO on the House's 2025 bill: \ the dynamic score \$0.4 trillion higher", font_size=18,
                  color=CBO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).to_edge(RIGHT, buff=0.25)
        if side.width > 6.6:
            side.width = 6.6
            side.to_edge(RIGHT, buff=0.25)
        tag = published_tag(r"Island toy; \ CBO (April 2018); \ CBO's dynamic estimate of H.R. 1 (2025)", corner=DL,
                            font_size=12)
        with self.voiceover(
            "What does a dynamic score add? An Island toy makes the two forces visible. <bookmark mark='a'/> A tax "
            "cut costs one percent of GDP a year, ten percent over the window. <bookmark mark='b'/> Lower taxes "
            "raise output a little, up to four tenths of a percent here, and the government taxes some of that: the "
            f"growth pays back {abs(D['sum_growth']):.2f} points. <bookmark mark='c'/> But the cut is borrowed, and "
            "more debt raises interest rates, on all of the government's debt, not just the new: that adds "
            f"{D['sum_rates']:.2f} points. <bookmark mark='d'/> The dynamic score, {D['sum_dynamic']:.2f}, is higher "
            "than the conventional one. <bookmark mark='e'/> Real scores show both forces. In April 2018 CBO put the "
            f"2017 tax act at about {TC['cbo_total']} trillion dollars over its window, with growth paying back "
            f"about {TC['feedback']} trillion and higher interest costing about as much again. <bookmark mark='f'/> "
            "And in 2025 its dynamic estimate of the House's tax bill was about four hundred billion dollars more "
            "costly than its conventional one. Tax cuts can pay for part of themselves; at today's debt, the "
            "interest can take it back."
        ) as vo:
            self.play(FadeIn(ax), Create(z), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in conv], lag_ratio=0.1), FadeIn(side[0]),
                      run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in grow], lag_ratio=0.1), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in rate], lag_ratio=0.1), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.clear_scene()

    def track_record(self):
        S = load("scoring")
        H = S["horizon"]
        ax = plane([0.4, 11.6], [0, 3.2], center=LEFT * 3.6 + DOWN * 0.3, x_length=5.6, y_length=4.4,
                   xticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], yticks=[0, 1, 2, 3], xlabel=r"year of the projection",
                   ylabel=r"error, \ \% of GDP", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=13)
        bars = VGroup()
        for h in H:
            p0, p1 = ax.ax.c2p(h["year"] - 0.32, 0), ax.ax.c2p(h["year"] + 0.32, h["mae"])
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=CBO, fill_opacity=0.8,
                               stroke_width=0).move_to((p0 + p1) / 2))
        rm = VGroup(*[dot(ax, h["year"], h["rmse"], WHITE, 0.06) for h in H])
        k1, k6, k11 = H[0], H[5], H[10]
        b01 = S["dec2001"]
        yrs = [d["year"] for d in b01]
        bx = plane([2000.5, 2011.5], [-10, 7], center=RIGHT * 3.6 + DOWN * 0.3, x_length=5.4, y_length=4.4,
                   xticks=[2001, 2004, 2007, 2010], yticks=[-10, -5, 0, 5], xlabel=r"fiscal year",
                   ylabel=r"surplus or deficit, \ \% of GDP", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0", font_size=13)
        zz = DashedLine(bx.ax.c2p(2000.5, 0), bx.ax.c2p(2011.5, 0), color=GREY_C, stroke_width=1.2)
        lp = path(bx, yrs, [d["projected"] for d in b01], CBO, 3.0, smooth=False)
        la = path(bx, yrs, [d["adjusted"] for d in b01], BEHAV, 2.6, smooth=False)
        lo = path(bx, yrs, [d["actual"] for d in b01], WHITE, 3.0, smooth=False)
        keys = VGroup(label(r"May 2001's projection", font_size=15, color=CBO),
                      label(r"with the laws passed later", font_size=15, color=BEHAV),
                      label(r"what happened", font_size=15, color=WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        keys.next_to(bx.ax.c2p(2001, -6), RIGHT, buff=0.1)
        last = b01[-1]
        tag = data_tag(r"CBO, \ eval-projections: \ every baseline, \ 1984--2025", corner=DL, font_size=12)
        with self.voiceover(
            "How good are the scores? CBO publishes its own record, and the Data Room has every baseline since "
            f"1984. <bookmark mark='a'/> Once the effects of laws passed later are taken out, its projection of the "
            f"deficit for the year it is in misses by {k1['mae']:.1f} percent of GDP on average; <bookmark mark='b'/> "
            f"six years out, by {k6['mae']:.1f} points; eleven years out, by {k11['mae']:.1f}. The white dots are "
            "the root mean squared errors, a little larger. <bookmark mark='c'/> The biggest misses are not CBO's "
            f"economics but the laws. In May 2001 it projected a surplus of {last['projected']:.1f} percent of GDP "
            f"for 2011. <bookmark mark='d'/> Two rounds of tax cuts, two wars, a drug benefit and a stimulus later, "
            "the same "
            f"projection with the new laws would have been a deficit of {abs(last['adjusted']):.1f} percent. "
            f"<bookmark mark='e'/> The actual deficit, after the financial crisis, was {abs(last['actual']):.1f}. "
            "A baseline is a projection of current law, and current law changes."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0], DOWN))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars[1:]], lag_ratio=0.12), FadeIn(rm),
                      run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(bx), Create(zz), Create(lp), FadeIn(keys[0]), run_time=1.5)
            vo.wait_until("d")
            self.play(Create(la), FadeIn(keys[1]), run_time=1.5)
            vo.wait_until("e")
            self.play(Create(lo), FadeIn(keys[2]), run_time=1.5)
        self.clear_scene()
