from __future__ import annotations

from videos.economics.econ20.common import *  # noqa: F403


class Accounting(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Growth accounting: \ Solow's residual", r"How much of a country's growth comes from more "
             r"capital, \ more and better labour, \ and how much from neither?",
             "Chapter seven. Growth accounting: Solow's residual.",
             lit={1956: r"Abramovitz", 1957: r"Solow's residual", 1967: r"Jorgenson and Griliches"},
             scale=("nation",), horizon=("decades",))
        self.equation()
        self.solow57()
        self.redo()
        self.countries()
        self.inside()

    def equation(self):
        rows = VGroup(
            MathTex(r"Y = A\,K^{\alpha}\,(hL)^{1-\alpha}", font_size=50),
            MathTex(r"\underbrace{g_Y}_{\text{output}} = \underbrace{\alpha\, g_K}_{\text{capital}} + "
                    r"\underbrace{(1-\alpha)(g_L + g_h)}_{\text{hours and skills}} + "
                    r"\underbrace{g_A}_{\text{the residual}}", font_size=40),
            MathTex(r"g_A = g_Y - \alpha\, g_K - (1-\alpha)(g_L + g_h)", font_size=46, color=TFP),
        ).arrange(DOWN, buff=0.6).move_to(UP * 0.7)
        notes = label(r"$\alpha$ from the national accounts: \ one minus labour's share of income", font_size=22,
                      color=GREY_A).next_to(rows, DOWN, buff=0.5)
        with self.voiceover(
            "The model also gives a way to take growth apart. <bookmark mark='a'/> Write output as technology, A, "
            "times capital to the alpha, times hours worked, made more skilled by human capital h, to the one minus "
            "alpha. <bookmark mark='b'/> Take logs and differentiate with time, and output's growth rate is the sum "
            "of capital's growth weighted by alpha, the growth of hours and skills weighted by one minus alpha, and "
            "the growth of A. <bookmark mark='c'/> Everything except A can be measured. So A's growth is what is left "
            "over: the residual, also called total factor productivity. <bookmark mark='d'/> The weight alpha comes "
            "from the national accounts: under competition, it is capital's share of income."
        ) as vo:
            self.play(Write(rows[0]), run_time=1.6)
            for mk, r in zip("bc", rows[1:]):
                vo.wait_until(mk)
                self.play(Write(r), run_time=1.6)
            vo.wait_until("d")
            self.play(FadeIn(notes))
        self.clear_scene()

    def solow57(self):
        a = load("accounting")["solow57"]
        hc = history_card(1957, r"Robert Solow", r"\emph{Technical Change and the Aggregate Production Function}, "
                          r"\ Review of Economics and Statistics", color=TFP, width=11.4, font_size=23).to_edge(
            UP, buff=0.45)
        bar_w = 10.0
        base = hc.get_bottom() + DOWN * 1.6
        cap = Rectangle(width=bar_w * a["capital"], height=0.8, stroke_width=0, fill_color=CAPITAL,
                        fill_opacity=0.9)
        tech = Rectangle(width=bar_w * a["technical"], height=0.8, stroke_width=0, fill_color=TFP, fill_opacity=0.9)
        bar = VGroup(cap, tech).arrange(RIGHT, buff=0).move_to(base)
        lc = label(rf"capital: \ {100 * a['capital']:.1f}\%", font_size=21, color=CAPITAL).next_to(cap, DOWN,
                                                                                                 buff=0.2)
        lt = label(rf"technical change: \ {100 * a['technical']:.1f}\%", font_size=24, color=TFP).next_to(tech, DOWN,
                                                                                                        buff=0.2)
        head = label(r"output per man-hour, \ US private non-farm economy, \ 1909--1949: \ doubled", font_size=22,
                     color=GREY_A).next_to(bar, UP, buff=0.3)
        rows = VGroup(
            label(r"Moses Abramovitz, \ a year earlier: \ the residual is ``some sort of measure of our ignorance''",
                  font_size=21, color=GREY_A),
            label(r"a correction to Solow's arithmetic \ (Hogan, \ 1958) \ raised it to 90\%", font_size=20,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(lt, DOWN, buff=0.6).set_x(0)
        tag = published_tag(r"Solow, REStat 39(3) (1957): \ 312--320; \ Abramovitz, AER 46(2) (1956)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Solow did exactly this in 1957, for the United States. <bookmark mark='a'/> Between 1909 and 1949, "
            "output per man-hour in the private non-farm economy doubled. <bookmark mark='b'/> More capital per "
            "worker accounted for an eighth of the increase. <bookmark mark='c'/> The other seven eighths, "
            f"{100 * a['technical']:.1f} percent, he attributed to technical change in the broadest sense: anything "
            "that shifts the production function. <bookmark mark='d'/> Moses Abramovitz, who had found much the "
            "same a year earlier, called the residual some sort of measure of our ignorance about the causes of "
            "growth. <bookmark mark='e'/> A critic who checked Solow's arithmetic found a slip; corrected, the share "
            "came to ninety percent."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(head))
            vo.wait_until("b")
            self.play(GrowFromEdge(cap, LEFT), FadeIn(lc))
            vo.wait_until("c")
            self.play(GrowFromEdge(tech, LEFT), FadeIn(lt))
            vo.wait_until("d")
            self.play(FadeIn(rows[0]))
            vo.wait_until("e")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def redo(self):
        a = load("accounting")
        us = a["countries"]["USA"]
        per = a["us_periods"]
        parts = [(r"capital deepening", us["deepening"], CAPITAL), (r"schooling", us["human_capital"], HUMAN),
                 (r"the residual", us["tfp"], TFP)]
        scale_ = 3.0 / 0.01          # screen units per percentage point... per unit of growth
        x0 = -5.6
        y = 1.6
        bars = VGroup()
        x = x0
        for name, v, c in parts:
            r = Rectangle(width=v * scale_, height=0.75, stroke_width=0, fill_color=c, fill_opacity=0.9)
            r.move_to([x + v * scale_ / 2, y, 0])
            t = label(rf"{name} \\ {pc(v, 2)}", font_size=18, color=c).next_to(r, DOWN, buff=0.15)
            bars.add(VGroup(r, t))
            x += v * scale_
        tot = label(rf"output per hour: \ {pc(us['per_hour'], 2)} a year, \ 1950--2019 \ $\cdot$ \ the residual "
                    rf"{100 * us['tfp_share_per_hour']:.0f}\%", font_size=22, color=OUTPUT).next_to(bars, UP,
                                                                                               buff=0.35)
        tot.set_x(0)
        ax = plane([0, 4], [0, 0.018], center=DOWN * 2.0, x_length=9.2, y_length=2.6, xticks=[], yticks=[0, 0.01],
                   ylabel=r"residual, \ a year", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        cols = VGroup()
        for i, (k, v) in enumerate(per.items()):
            h_ = v["tfp"]
            r = Rectangle(width=1.2, height=max(0.01, ax.ax.c2p(0, h_)[1] - ax.ax.c2p(0, 0)[1]), stroke_width=0,
                          fill_color=TFP, fill_opacity=0.85)
            r.move_to(ax.ax.c2p(i + 0.5, 0), aligned_edge=DOWN)
            lab = VGroup(label(k.replace("-", "--"), font_size=15, color=GREY_A),
                         label(pc(h_, 2), font_size=15, color=TFP))
            lab[0].next_to(r, DOWN, buff=0.1)
            lab[1].next_to(r, UP, buff=0.06)
            cols.add(VGroup(r, lab))
        src = data_tag(r"Penn World Table 11.0; \ hours $=$ emp $\times$ avh; \ $\alpha$ $=$ 1 $-$ labsh", corner=UR,
                       font_size=11)
        with self.voiceover(
            "Here is the same accounting on the Penn World Table, for the United States from 1950 to 2019, per hour "
            f"worked. <bookmark mark='a'/> Output per hour grew by {100 * us['per_hour']:.2f} percent a year. "
            f"<bookmark mark='b'/> More capital per hour contributed {100 * us['deepening']:.2f} points, and "
            f"more schooling {100 * us['human_capital']:.2f}. <bookmark mark='c'/> The residual: "
            f"{100 * us['tfp']:.2f} points, about {100 * us['tfp_share_per_hour']:.0f} percent. Measured "
            "schooling has eaten into Solow's seven eighths, but half of growth is still unexplained by the inputs. "
            "<bookmark mark='d'/> And the residual is not steady. It grew by "
            f"{100 * per['1950-1973']['tfp']:.1f} percent a year until 1973, by half a percent from 1973 to 1995, by "
            f"{100 * per['1995-2005']['tfp']:.1f} percent in the decade of the internet's spread, and by half a "
            "percent again since 2005."
        ) as vo:
            self.play(FadeIn(src), FadeIn(tot))
            vo.wait_until("a")
            self.play(Indicate(tot))
            vo.wait_until("b")
            self.play(FadeIn(bars[0]), FadeIn(bars[1]))
            vo.wait_until("c")
            self.play(FadeIn(bars[2]))
            vo.wait_until("d")
            self.play(FadeIn(ax), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cols], lag_ratio=0.3),
                      run_time=3)
        self.clear_scene()

    def countries(self):
        a = load("accounting")
        order = a["order"]
        unit = 0.62 / 0.01            # screen units per unit of growth: 0.62 per percentage point
        x_zero = -1.2
        rows = VGroup()
        for i, c in enumerate(order):
            r = a["countries"][c]
            y = 2.35 - i * 0.62
            name = label(rf"{COUNTRY[c][0]}, \ {r['first']}--{r['last']}", font_size=17,
                         color=COUNTRY[c][1]).move_to([x_zero - 0.8, y, 0], aligned_edge=RIGHT)
            segs = VGroup()
            x = x_zero
            for v, col in ((r["deepening"], CAPITAL), (r["human_capital"], HUMAN)):
                w = max(v, 0) * unit
                segs.add(Rectangle(width=max(w, 0.001), height=0.4, stroke_width=0, fill_color=col,
                                   fill_opacity=0.9).move_to([x + w / 2, y, 0]))
                x += w
            t = r["tfp"] * unit
            if t >= 0:
                segs.add(Rectangle(width=max(t, 0.001), height=0.4, stroke_width=0, fill_color=TFP,
                                   fill_opacity=0.9).move_to([x + t / 2, y, 0]))
            else:
                segs.add(Rectangle(width=-t, height=0.4, stroke_width=1.5, stroke_color=TFP, fill_color=TFP,
                                   fill_opacity=0.25).move_to([x_zero + t / 2, y, 0]))
            total = label(rf"{pc(r['per_hour'])} \ (residual {pc(r['tfp'])})".replace("-", "{-}"), font_size=15,
                          color=GREY_A).move_to([x_zero + max(r['per_hour'], 0) * unit + 0.15, y, 0],
                                                aligned_edge=LEFT)
            rows.add(VGroup(name, segs, total))
        zero = Line([x_zero, 2.7, 0], [x_zero, 2.35 - 7 * 0.62 - 0.3, 0], color=GREY_C, stroke_width=1.5)
        key = VGroup(*[VGroup(Square(0.22, stroke_width=0, fill_color=col, fill_opacity=0.9),
                              label(t, font_size=16, color=col)).arrange(RIGHT, buff=0.1)
                       for t, col in ((r"capital per hour", CAPITAL), (r"schooling", HUMAN),
                                      (r"residual", TFP))]).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.3)
        head = label(r"growth of output per hour, \ a year, \ taken apart", font_size=24,
                     color=GREY_A).to_edge(UP, buff=0.25)
        k, c = a["countries"]["KOR"], a["countries"]["CHN"]
        rich = [a["countries"][x]["tfp_share_per_hour"] for x in ("USA", "GBR", "JPN")]
        with self.voiceover(
            "Now eight countries, each over the longest span the table covers well. <bookmark mark='a'/> In the rich "
            f"countries the residual is between about {100 * min(rich):.0f} and {100 * max(rich):.0f} percent of the "
            "growth of output per hour. <bookmark mark='b'/> South "
            f"Korea's output per hour grew {100 * k['per_hour']:.1f} percent a year from 1966; more than half of "
            "that was more capital. <bookmark mark='c'/> China's grew by "
            f"{100 * c['per_hour']:.1f} percent from 1980, with a residual of {100 * c['tfp']:.1f} percent, the "
            "largest here. <bookmark mark='d'/> And in Brazil and Nigeria the residual is about zero or below: all "
            "their growth came from accumulating, and output per hour grew slowly for countries so far behind. A "
            "country can pile up capital and "
            "still fail to use it better."
        ) as vo:
            self.play(FadeIn(head), FadeIn(key), Create(zero),
                      LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in rows[:3]], lag_ratio=0.3), run_time=2)
            vo.wait_until("a")
            self.play(*[Indicate(r_[1]) for r_ in rows[:3]])
            vo.wait_until("b")
            self.play(FadeIn(rows[3], shift=RIGHT * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(rows[4], shift=RIGHT * 0.1), FadeIn(rows[5], shift=RIGHT * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(rows[6], shift=RIGHT * 0.1), FadeIn(rows[7], shift=RIGHT * 0.1))
        self.clear_scene()

    def inside(self):
        cards = point_cards([
            (r"technology", r"new ideas, \\ new machines", TFP),
            (r"organization", r"management, \\ better use of the same inputs", OUTPUT),
            (r"reallocation", r"workers moving \\ from farms to factories", LABOUR),
            (r"mismeasurement", r"better machines \\ counted as more machines?", HOLD),
        ], width=12.6, cols=2, font_size=23).move_to(DOWN * 0.2)
        head = label(r"what is in the residual?", font_size=36, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Jorgenson and Griliches, REStud 34(3) (1967)", corner=DR, font_size=12)
        with self.voiceover(
            "What is in the residual? <bookmark mark='a'/> Technology, in the sense of new ideas and new machines. "
            "<bookmark mark='b'/> Organization: better management of the same inputs. <bookmark mark='c'/> "
            "Reallocation: a worker who moves from a farm to a factory produces more without any new capital. "
            "<bookmark mark='d'/> And mismeasurement. In 1967 Dale Jorgenson and Zvi Griliches argued that if the "
            "quality of capital and labour were measured properly, most of the residual would disappear. Better "
            "measurement has since shrunk it, but not to zero. The next part builds a model of the biggest item, "
            "ideas."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
