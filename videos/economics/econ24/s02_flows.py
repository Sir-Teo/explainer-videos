from __future__ import annotations

from videos.economics.econ24.common import *  # noqa: F403


class Flows(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Stocks and flows", r"How many jobs begin and end in a quiet month?",
             "Chapter one. Stocks and flows.", lit={1992: r"Davis and Haltiwanger", 2000: r"JOLTS begins"},
             scale=("market",), horizon=("a month",))
        self.jolts()
        self.tub()
        self.steady()

    def jolts(self):
        j = load("jolts")
        ax = plane([2000.9, 2026.8], [0, 17000], center=LEFT * 1.7 + DOWN * 0.3, x_length=8.6, y_length=5.0,
                   xticks=[2005, 2010, 2015, 2020, 2025], yticks=[0, 4000, 8000, 12000, 16000],
                   ylabel=r"thousands a month, \ United States", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v / 1000:.0f}m", font_size=16)
        hires = path(ax, j["t"], j["hires"], color=MATCH, width=3, smooth=False)
        seps = path(ax, j["t"], j["seps"], color=SEP, width=3, smooth=False)
        net = path(ax, j["t"], np.clip(j["net"], 0, None), color=WHITE, width=2, smooth=False)
        side = VGroup(
            label(rf"hires: \ {j['mean_hires'] / 1000:.2f} million \\ a month \ (2001--2019)", font_size=20,
                  color=MATCH),
            label(rf"separations: \ {j['mean_seps'] / 1000:.2f} million", font_size=20, color=SEP),
            label(rf"of which quits: \ {j['mean_quits'] / 1000:.2f} million", font_size=19, color=SEP),
            label(rf"net change: \ {j['mean_net']:.0f} thousand", font_size=21, color=WHITE),
            label(rf"April 2020: \\ {j['apr2020_seps'] / 1000:.1f} million separations", font_size=19, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"BLS, \ Job Openings and Labor Turnover Survey, \ via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "Every month, the American Bureau of Labor Statistics asks a large sample of employers how many people "
            "they hired, and how many left. The survey began at the end of 2000. <bookmark mark='a'/> In an "
            f"ordinary month before the pandemic, employers hired about {j['mean_hires'] / 1000:.1f} million "
            f"people. <bookmark mark='b'/> And about {j['mean_seps'] / 1000:.1f} million left their jobs: "
            f"<bookmark mark='c'/> more than half of them, about {j['mean_quits'] / 1000:.1f} million, because they "
            "quit; the rest were laid off, or left for other reasons, such as retirement. <bookmark mark='d'/> The "
            f"difference, close to the change in payroll jobs that the news reports each month, was only about {j['mean_net']:.0f} thousand. "
            "<bookmark mark='e'/> In April 2020, separations jumped to "
            f"{j['apr2020_seps'] / 1000:.1f} million in a single month."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(hires), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), Indicate(hires, color=WHITE))
            vo.wait_until("b")
            self.play(Create(seps), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(net), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def tub(self):
        tub = VGroup(
            Line(LEFT * 2.2 + UP * 1.2, LEFT * 2.2 + DOWN * 1.4, color=GREY_B, stroke_width=5),
            Line(LEFT * 2.2 + DOWN * 1.4, RIGHT * 2.2 + DOWN * 1.4, color=GREY_B, stroke_width=5),
            Line(RIGHT * 2.2 + DOWN * 1.4, RIGHT * 2.2 + UP * 1.2, color=GREY_B, stroke_width=5),
        ).move_to(DOWN * 0.3)
        water = Rectangle(width=4.3, height=0.9, fill_color=WORKER, fill_opacity=0.55, stroke_width=0)
        water.align_to(tub[1], DOWN).shift(UP * 0.05)
        water_lbl = label(r"the unemployed: \ a stock", font_size=22, color=WORKER).move_to(water)
        inflow = Arrow(tub.get_top() + LEFT * 3.4 + UP * 1.0, tub.get_top() + LEFT * 1.1 + DOWN * 0.3, color=SEP,
                       stroke_width=6, buff=0)
        outflow = Arrow(tub.get_bottom() + RIGHT * 1.1 + UP * 0.3, tub.get_bottom() + RIGHT * 3.6 + DOWN * 0.6,
                        color=MATCH, stroke_width=6, buff=0)
        in_l = label(r"in: \ the employed who lose \\ or leave their jobs, \ $s(1-u)$", font_size=20,
                     color=SEP).next_to(inflow.get_start(), UP, buff=0.15)
        out_l = label(r"out: \ the unemployed \\ who find jobs, \ $f u$", font_size=20,
                      color=MATCH).next_to(outflow.get_end(), RIGHT, buff=0.15).shift(UP * 0.4)
        eq = MathTex(r"u_{t+1} - u_t \;=\; s\,(1 - u_t) \;-\; f\,u_t", font_size=40).to_edge(UP, buff=0.6)
        with self.voiceover(
            "So think of unemployment as water in a tub. <bookmark mark='a'/> The level is a stock: the share of "
            "the labour force that is out of work and looking. <bookmark mark='b'/> Water flows in when people who "
            "have jobs lose or leave them: a fraction s of the employed, each month. <bookmark mark='c'/> And it "
            "drains out when the unemployed find work: a fraction f of them. <bookmark mark='d'/> The level rises "
            "if the inflow exceeds the outflow, and falls if not. Every model in this part is a theory of s and f."
        ) as vo:
            self.play(Create(tub), run_time=1.2)
            vo.wait_until("a")
            self.play(FadeIn(water), FadeIn(water_lbl))
            vo.wait_until("b")
            self.play(GrowArrow(inflow), FadeIn(in_l))
            vo.wait_until("c")
            self.play(GrowArrow(outflow), FadeIn(out_l))
            vo.wait_until("d")
            self.play(Write(eq))
        self.clear_scene()

    def steady(self):
        f = load("flows")
        u = f["mean_s"] / (f["mean_s"] + f["mean_f"])
        rows = VGroup(
            MathTex(r"\text{steady state:}\quad s(1-u) = f u \quad\Longrightarrow\quad u^* = \frac{s}{s+f}",
                    font_size=44, color=WHITE),
            label(rf"American averages since 1948 \ (chapter 10 measures them): \ $f \approx {f['mean_f']:.2f}$ a "
                  rf"month, \ $s \approx {f['mean_s']:.3f}$", font_size=23, color=GREY_A),
            MathTex(rf"u^* \approx \frac{{{f['mean_s']:.3f}}}{{{f['mean_s']:.3f} + {f['mean_f']:.2f}}} \approx "
                    rf"{100 * u:.1f}\%", font_size=44, color=WORKER),
            label(r"the flows are fast: \ more than half the unemployed find work each month, \ so the level "
                  r"tracks the steady state closely", font_size=22, color=TIGHT),
            label(r"Davis and Haltiwanger, \ with plant records: \ gross job creation and destruction dwarf the net "
                  r"change, \ in every industry and every year", font_size=21, color=JOB),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Davis and Haltiwanger, QJE 107(3) (1992); \ Davis, Haltiwanger and Schuh, \emph{Job "
                            r"Creation and Destruction} (1996)", corner=DR, font_size=12)
        with self.voiceover(
            "When the tub settles, inflow equals outflow. <bookmark mark='a'/> s times one minus u equals f times "
            "u, so the steady-state rate is s over s plus f. <bookmark mark='b'/> Chapter ten measures these flows "
            f"for America since 1948. On average, about {100 * f['mean_f']:.0f} percent of the unemployed found work "
            f"each month, and about {100 * f['mean_s']:.0f} percent of the employed lost or left their jobs into "
            f"unemployment. <bookmark mark='c'/> That gives about {100 * u:.1f} percent, close to the average "
            "unemployment rate. <bookmark mark='d'/> The flows are so fast that the level never strays far from "
            "its steady state for long. <bookmark mark='e'/> Steven Davis and John Haltiwanger found the same churn "
            "among employers, using the records of manufacturing plants: in every industry and every year, the "
            "jobs created and destroyed dwarf the net change. A market where so much is always moving needs a "
            "theory of how workers and jobs meet."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
