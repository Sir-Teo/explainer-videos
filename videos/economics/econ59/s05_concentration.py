from __future__ import annotations

from videos.economics.econ59.common import *  # noqa: F403


class Concentration(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Shares and concentration", r"How concentrated is too concentrated?",
             "Chapter four. Shares and concentration.", lit={1982: r"the HHI enters", 2010: r"thresholds raised",
                                                             2023: r"lowered again"},
             scale=("market",), horizon=("a decade",))
        self.hhi()
        self.guidelines()

    def hhi(self):
        C = load("concentration")
        town = next(r for r in C["towns"] if r["cedar"])
        T = load("towns")
        k = town["town"]
        pres = np.array([True, True, True, True])
        eq = merger.equilibrium(pres, cost_shift=float(T["cost"][k]))
        s = np.array(eq["s"][:3])
        s = 100 * s / s.sum()
        cols = (ALDER, BIRCH, CEDAR)
        names = ("Alder", "Birch", "Cedar")
        bar0 = VGroup()
        x0 = -6.2
        w = 6.0
        for v, col in zip(s, cols):
            bw = w * v / 100
            bar0.add(Rectangle(width=bw, height=0.7, fill_color=col, fill_opacity=0.85, stroke_width=0).move_to(
                [x0 + bw / 2, 1.6, 0]))
            x0 += bw
        lab0 = VGroup(*[label(rf"{n} {v:.0f}\%", font_size=18, color=BLACK).move_to(b) for n, v, b in
                        zip(names, s, bar0)])
        bar1 = VGroup(Rectangle(width=w * (s[0] + s[1]) / 100, height=0.7, fill_color=ALDER, fill_opacity=0.85,
                                stroke_width=0).move_to([-6.2 + w * (s[0] + s[1]) / 200, 0.2, 0]),
                      Rectangle(width=w * s[2] / 100, height=0.7, fill_color=CEDAR, fill_opacity=0.85,
                                stroke_width=0).move_to([-6.2 + w * (s[0] + s[1]) / 100 + w * s[2] / 200, 0.2, 0]))
        lab1 = VGroup(label(rf"Alder--Birch {s[0] + s[1]:.0f}\%", font_size=18, color=BLACK).move_to(bar1[0]),
                      label(rf"Cedar {s[2]:.0f}\%", font_size=18, color=BLACK).move_to(bar1[1]))
        tb = label(r"before", font_size=18, color=GREY_A).next_to(bar0, LEFT, buff=0.2)
        ta = label(r"after", font_size=18, color=GREY_A).next_to(bar1, LEFT, buff=0.2)
        VGroup(tb, ta).align_to(tb, RIGHT)
        eqs = VGroup(
            MathTex(r"\text{HHI} = \sum_i s_i^2", font_size=36, color=WHITE),
            MathTex(rf"{s[0]:.0f}^2 + {s[1]:.0f}^2 + {s[2]:.0f}^2 \approx {town['pre']:,.0f}".replace(",", "{,}"),
                    font_size=30, color=GREY_A),
            MathTex(r"\Delta\text{HHI} = (s_A + s_B)^2 - s_A^2 - s_B^2 = 2\,s_A s_B", font_size=32,
                    color=E.ACCENT),
            MathTex(rf"2 \times {s[0]:.0f} \times {s[1]:.0f} \approx {town['delta']:,.0f}".replace(",", "{,}"),
                    font_size=30, color=GREY_A),
            label(r"a monopoly scores 10,000; \ ten equal firms, \ 1,000".replace(",", "{,}"), font_size=20,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4).shift(UP * 0.3)
        if eqs.width > 6.0:
            eqs.width = 6.0
            eqs.to_edge(RIGHT, buff=0.4)
        note_ = label(r"shares of superstore sales in one Island town \ (the market of chapter three)", font_size=18,
                      color=GREY_B).next_to(bar1, DOWN, buff=0.6).align_to(bar1, LEFT)
        tag = island_tag(r"the Island: \ one town with all three chains", corner=DL, font_size=12)
        with self.voiceover(
            "Once a market is drawn, shares can be counted, and the agencies summarize them with the "
            "Herfindahl-Hirschman index: the sum of the squared shares, in percent. <bookmark mark='a'/> In this "
            f"Island town Alder has {s[0]:.0f} percent of superstore sales, Birch {s[1]:.0f}, Cedar {s[2]:.0f}. "
            f"<bookmark mark='b'/> The index is about {town['pre']:,.0f}. A monopoly scores ten thousand; ten equal "
            "firms, a thousand. <bookmark mark='c'/> When Alder and Birch merge, their shares add, <bookmark "
            "mark='d'/> and the index rises by twice the product of the two shares: here by about "
            f"{town['delta']:,.0f} points. The index is crude: it knows nothing of who competes with whom inside "
            "the market. But it is cheap, and the guidelines turn it into presumptions."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(note_))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in bar0], lag_ratio=0.3), FadeIn(lab0),
                      FadeIn(tb))
            vo.wait_until("b")
            self.play(FadeIn(eqs[0]), FadeIn(eqs[1]), FadeIn(eqs[4]))
            vo.wait_until("c")
            self.play(TransformFromCopy(VGroup(bar0[0], bar0[1]), bar1[0]), TransformFromCopy(bar0[2], bar1[1]),
                      FadeIn(lab1), FadeIn(ta))
            vo.wait_until("d")
            self.play(FadeIn(eqs[2]), FadeIn(eqs[3]))
        self.clear_scene()

    def guidelines(self):
        C = load("concentration")
        ax = plane([1000, 4000], [0, 1400], center=LEFT * 2.6 + DOWN * 0.45, x_length=6.6, y_length=4.8,
                   xticks=[1000, 1800, 2500, 3200, 4000], yticks=[0, 100, 200, 500, 1000, 1400],
                   xlabel=r"HHI after the merger", ylabel=r"rise in the HHI",
                   xfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"), yfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"),
                   font_size=14)

        def region(x0, y0, col, op=0.16):
            p0, p1 = ax.ax.c2p(x0, y0), ax.ax.c2p(4000, 1400)
            return Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=col, fill_opacity=op,
                             stroke_color=col, stroke_width=2).move_to((p0 + p1) / 2)
        r82 = region(1800, 100, GREY_B)
        r10 = region(2500, 200, CARTEL)
        r23 = region(1800, 100, GOV, 0.22)
        inds = C["industries"]
        cols = {"cement kilns": CARTEL, "banks": ALDER, "grocers": BIRCH, "bakeries": CEDAR, "hospitals": WORK}
        dots = VGroup()
        for r in inds:
            x = min(r["post"], 3950)
            d = Dot(ax.ax.c2p(x, min(r["delta"], 1380)), radius=0.09, color=cols[r["name"]])
            dl = label(r["name"] + (r" (off the chart)" if r["post"] > 4000 else ""), font_size=15,
                       color=cols[r["name"]]).next_to(d, UP, buff=0.06)
            dots.add(VGroup(d, dl))
        tab = VGroup()
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"\ ", r"1982", r"2010", r"2023")])
        tab.add(head)
        for r in inds:
            tab.add(VGroup(label(r["name"], font_size=16, color=cols[r["name"]]),
                           *[label(r"presumed" if r["verdict"][y] else r"--", font_size=15,
                                   color=CARTEL if r["verdict"][y] else GREY_C) for y in ("1982", "2010", "2023")]))
        for i, row in enumerate(tab):
            for j, m in enumerate(row):
                if j == 0:
                    m.move_to([-m.width / 2, -0.42 * i, 0])
                else:
                    m.move_to([0.25 + 1.2 * (j - 0.5), -0.42 * i, 0])
        tab.to_edge(RIGHT, buff=0.5).shift(UP * 1.6)
        notes = VGroup(
            label(r"1982 \ (grey): \ above 1,800, \ rise above 100".replace(",", "{,}"), font_size=16,
                  color=GREY_B),
            label(r"2010 \ (red): \ above 2,500, \ rise above 200".replace(",", "{,}"), font_size=16, color=CARTEL),
            label(r"2023 \ (pink): \ back to 1,800 and 100, \ or a 30\% share with a rise above 100"
                  .replace(",", "{,}"), font_size=16, color=GOV),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(tab, DOWN, buff=0.45).align_to(tab, LEFT)
        if notes.width > 5.6:
            notes.width = 5.6
            notes.align_to(tab, LEFT)
        tag = island_tag(r"the Island: \ five industries, \ a proposed merger in each", corner=DL, font_size=12)
        tw = C["towns"]
        with self.voiceover(
            "The guidelines draw lines on two numbers: the index after the merger, and its rise. <bookmark mark='a'/> "
            "In 1982 a merger was presumed likely to harm competition when the index ended above eighteen hundred "
            "and rose by more than a hundred. <bookmark mark='b'/> The 2010 guidelines raised the lines to "
            "twenty-five hundred and two hundred, closer to what the agencies were actually challenging. "
            "<bookmark mark='c'/> The 2023 guidelines brought them back to eighteen hundred and a hundred, and "
            "added the Philadelphia National Bank rule: a merged share above thirty percent, with a rise above a "
            "hundred. <bookmark mark='d'/> Here are five proposed Island mergers. Two cement kilns of four, the "
            "banks, the hospitals: presumed harmful under every version. The bakeries: under none. <bookmark "
            "mark='e'/> And the grocers: presumed in 1982, not in 2010, presumed again in 2023. The economics did "
            "not change; the line did. As for the superstores, in every Island town where Alder and Birch meet the "
            f"index rises by at least {min(r['delta'] for r in tw):,.0f} points, far past any line, because the "
            "market of chapter three is so narrow. Draw the market as everyone who sells a pen, and the same "
            "merger barely moves the index. That is why the market was the first fight."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(FadeIn(r82), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(r10), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeOut(r82), FadeIn(r23), FadeIn(notes[2]))
            vo.wait_until("d")
            for k in (0, 1, 4, 3):
                self.play(FadeIn(dots[k], scale=1.3), FadeIn(tab[k + 1]), run_time=0.6)
            vo.wait_until("e")
            self.play(FadeIn(dots[2], scale=1.3), FadeIn(tab[3]))
            self.play(Indicate(tab[3], color=WHITE, scale_factor=1.05))
        self.clear_scene()
