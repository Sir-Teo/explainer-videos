from __future__ import annotations

from videos.economics.econ12.common import *  # noqa: F403

HHI = "#F2C14E"


class Concentration(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Concentration: \ the Herfindahl index", r"Can one number say how much market power an "
             r"industry has?", "Chapter eleven. Concentration: the Herfindahl index.",
             lit={1950: r"Herfindahl's index"}, scale=("firm", "market", "nation"), horizon=("a year",))
        self.index()
        self.lerner()
        self.guidelines()

    def index(self):
        examples = [
            (r"one firm", [100]),
            (r"two equal", [50, 50]),
            (r"four equal", [25, 25, 25, 25]),
            (r"one big, \ three small", [70, 10, 10, 10]),
            (r"ten equal", [10] * 10),
        ]
        rows = VGroup()
        for k_, (name, sh) in enumerate(examples):
            h = ol.hhi(sh)
            y = 1.3 - 0.75 * k_
            bar = VGroup(*[Rectangle(width=0.058 * s_, height=0.42, stroke_color=BACKGROUND, stroke_width=1.5,
                                     fill_color=HHI if k == 0 else LEADER, fill_opacity=0.85 - 0.06 * k)
                           for k, s_ in enumerate(sh)]).arrange(RIGHT, buff=0)
            nm = label(name, font_size=22)
            nm.move_to(LEFT * 6.2 + UP * y, aligned_edge=LEFT)
            bar.move_to(LEFT * 2.6 + UP * y, aligned_edge=LEFT)
            val = label(rf"{h:,.0f}".replace(",", "{,}"), font_size=24, color=HHI).move_to(RIGHT * 3.6 + UP * y,
                                                                                         aligned_edge=LEFT)
            rows.add(VGroup(nm, bar, val))
        eq = MathTex(r"H = \sum_i s_i^2 \quad (\text{shares in percent: } 0 \text{ to } 10{,}000)", font_size=36,
                     color=HHI).to_edge(UP, buff=0.55)
        foot = label(r"Orris Herfindahl (1950) \ and Albert Hirschman (1945): \ it weighs big firms more", font_size=21,
                     color=GREY_A).to_edge(DOWN, buff=0.8)
        tag = published_tag(r"Herfindahl, Columbia dissertation (1950); \ Hirschman, \emph{National Power and the "
                            r"Structure of Foreign Trade} (1945)", corner=DR, font_size=12)
        with self.voiceover(
            "How concentrated is an industry? The standard number squares each firm's market share, in percent, and "
            "adds them up. It is named for Orris Herfindahl and Albert Hirschman, who proposed it independently. "
            "<bookmark mark='a'/> A monopoly scores ten thousand. <bookmark mark='b'/> Two equal firms score five "
            "thousand; four equal firms, two thousand five hundred. <bookmark mark='c'/> One firm with seventy "
            "percent and three with ten scores five thousand two hundred, more than two equal firms, because "
            "squaring weighs big firms more. <bookmark mark='d'/> Ten equal firms score a thousand."
        ) as vo:
            self.play(Write(eq), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]), FadeIn(foot))
        self.clear_scene()

    def lerner(self):
        c = load("concentration")
        rows = c["rows"]
        ax = plane([0.55, 0.78], [0.55, 0.78], center=LEFT * 3.1 + DOWN * 0.3, x_length=5.0, y_length=5.0,
                   xticks=[0.6, 0.65, 0.7, 0.75], yticks=[0.6, 0.65, 0.7, 0.75], xlabel=r"$H / \varepsilon$",
                   ylabel=r"the industry's Lerner index", font_size=16, xfmt=lambda v: f"{v:.2f}",
                   yfmt=lambda v: f"{v:.2f}")
        a = ax.ax
        diag = DashedLine(a.c2p(0.55, 0.55), a.c2p(0.78, 0.78), color=GREY_B, stroke_width=1.5)
        dots = VGroup(*[Dot(a.c2p(r["hhi_over_eps"], r["lerner"]), radius=0.09, color=HHI) for r in rows])
        names = [r"two equal", r"three equal", r"costs 10 and 20", r"10, 15, 25", r"five equal", r"8, 10, 12, 14"]
        tags = VGroup(*[label(n, font_size=14, color=GREY_A).next_to(d, RIGHT if k % 2 else LEFT, buff=0.08)
                        for k, (n, d) in enumerate(zip(names, dots))])
        side = VGroup(
            label(r"Keith Cowling and Michael Waterson (1976): \\ in Cournot's model, \ exactly", font_size=21),
            MathTex(r"\sum_i s_i \frac{P - c_i}{P} = \frac{H}{\varepsilon}", font_size=38, color=HHI),
            label(r"the share-weighted markup \ equals \\ concentration \ over the demand elasticity", font_size=21),
            label(r"six Island markets, \ equal and unequal costs: \\ every point on the line", font_size=21,
                  color=EQ),
            label(r"but it holds only if firms play Cournot: \\ under Bertrand two firms give a markup of zero",
                  font_size=21, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Cowling and Waterson, Economica 43(171) (1976); \ the markets: \ Agora", corner=DR,
                            font_size=13)
        with self.voiceover(
            "Why that index? <bookmark mark='a'/> In 1976 Keith Cowling and Michael Waterson showed that in "
            "Cournot's model it is exactly the right one. <bookmark mark='b'/> The industry's markup, each firm's "
            "Lerner index weighted by its share, equals the Herfindahl index divided by the elasticity of market "
            "demand. <bookmark mark='c'/> A concentrated industry facing inelastic demand marks up most. "
            "<bookmark mark='d'/> Agora solves six Island markets, some with equal costs and some unequal, and every "
            "one lands on the line. <bookmark mark='e'/> But the formula holds only if firms compete as Cournot "
            "assumed. Under Bertrand, two firms with a Herfindahl index of five thousand mark up by nothing at all. "
            "Concentration is a clue to market power, not a measurement of it, which is why Part forty-three "
            "measures markups directly."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), Create(diag))
            vo.wait_until("b")
            self.play(Write(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in dots], lag_ratio=0.3), FadeIn(tags),
                      FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def guidelines(self):
        c = load("concentration")
        g23, g10 = c["g2023"], c["g2010"]
        line = NumberLine(x_range=[0, 10000, 1000], length=11.4, include_numbers=False, color=GREY_B).move_to(UP * 0.6)
        nums = VGroup(*[label(f"{v:,}".replace(",", "{,}"), font_size=16, color=GREY_B).next_to(line.n2p(v), DOWN,
                                                                                               buff=0.15)
                        for v in (0, 5000, 10000)])
        m23 = VGroup(Triangle(color=LEADER, fill_opacity=1).scale(0.12).rotate(PI).next_to(
            line.n2p(g23["highly_concentrated"]), UP, buff=0.05),
            label(rf"2023: \ above {g23['highly_concentrated']:,}, \ highly concentrated".replace(",", "{,}"),
                  font_size=18, color=LEADER).next_to(line.n2p(g23["highly_concentrated"]), UP, buff=0.4))
        m10 = VGroup(Triangle(color=GREY_A, fill_opacity=1).scale(0.12).next_to(
            line.n2p(g10["highly_concentrated"]), DOWN, buff=0.05),
            label(rf"2010: \ above {g10['highly_concentrated']:,}".replace(",", "{,}"), font_size=18,
                  color=GREY_A).next_to(line.n2p(g10["highly_concentrated"]), DOWN, buff=0.75))
        rows = VGroup(
            label(rf"the American agencies presume a merger harmful \ if it leaves the index above "
                  rf"{g23['highly_concentrated']:,} \ and raises it by more than {g23['presumption_delta']}"
                  .replace(",", "{,}"), font_size=22, color=LEADER),
            label(rf"or creates a firm with more than {g23['share_test'][0]}\% of the market, \ with a rise above "
                  rf"{g23['share_test'][1]}", font_size=22, color=LEADER),
            label(rf"from 2010 to 2023 the thresholds were {g10['highly_concentrated']:,} and "
                  rf"{g10['presumption_delta']}: \ the new guidelines returned to the older, \ stricter line"
                  .replace(",", "{,}"), font_size=22, color=GREY_A),
            label(r"a merger of two of five equal firms: \ from 2{,}000 to 2{,}800, \ a rise of 800", font_size=22,
                  color=HHI),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"DOJ and FTC, Merger Guidelines (2023); \ Horizontal Merger Guidelines (2010)",
                            corner=UR, font_size=12)
        pre, post = Dot(line.n2p(2000), radius=0.09, color=HHI), Dot(line.n2p(2800), radius=0.09, color=CARTEL)
        jump = CurvedArrow(line.n2p(2000) + UP * 0.15, line.n2p(2800) + UP * 0.15, angle=-PI / 2, color=CARTEL,
                           stroke_width=2.5, tip_length=0.15)
        jl = label(r"two of five merge: \ 2{,}000 to 2{,}800", font_size=17, color=CARTEL).next_to(
            line.n2p(5600), UP, buff=0.35)
        with self.voiceover(
            "Competition authorities use the index as a first screen. <bookmark mark='a'/> Under the American "
            "merger guidelines of December 2023, a merger is presumed to lessen competition substantially if it "
            "leaves the market's index above eighteen hundred and raises it by more than a hundred, "
            "<bookmark mark='b'/> or if it creates a firm with more than thirty percent of the market, with a rise "
            "above a hundred. <bookmark mark='c'/> From 2010 to 2023 the line was two thousand five hundred, with a "
            "rise of two hundred; the new guidelines returned to the stricter number used before 2010. "
            "<bookmark mark='d'/> Merging two of five equal firms takes the index from two thousand to two "
            "thousand eight hundred, a rise of eight hundred: past both lines."
        ) as vo:
            self.play(Create(line), FadeIn(nums), FadeIn(tag), FadeIn(m23), FadeIn(m10))
            for mk, r in zip("abc", rows[:3]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1), FadeIn(pre), FadeIn(post), Create(jump), FadeIn(jl))
        self.clear_scene()
