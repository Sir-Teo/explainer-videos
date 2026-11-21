from __future__ import annotations

from videos.economics.econ57.common import *  # noqa: F403


def bars(ax, vals, cols, width=0.6):
    g = VGroup()
    for k, (v, c) in enumerate(zip(vals, cols)):
        p0, p1 = ax.ax.c2p(k - width / 2, 0), ax.ax.c2p(k + width / 2, v)
        g.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=c,
                        fill_opacity=0.85).move_to((p0 + p1) / 2))
    return g


class Nowcast(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Nowcasting", r"How can anyone see this quarter before its statistics are out?",
             "Chapter four. Nowcasting.", lit={2002: r"Stock and Watson", 2008: r"Giannone, \ Reichlin and Small",
                                              2014: r"GDPNow"},
             scale=("nation",), horizon=("a day", "a year"))
        self.bridge()
        self.factor()

    def bridge(self):
        B = load("bridge")
        eq = MathTex(r"\underbrace{y_q}_{\text{GDP growth}} = a + b_1\, \underbrace{\overline{\text{payrolls}}_q}"
                     r"_{\text{average of 3 months}} + b_2\, \underbrace{\overline{\text{production}}_q}"
                     r"_{\text{average of 3 months}} + e_q", font_size=34, color=WHITE).to_edge(UP, buff=0.5)
        note_ = label(r"months not yet out: \ filled by each indicator's own forecast \ (the `ragged edge')",
                      font_size=20, color=GREY_A).next_to(eq, DOWN, buff=0.3)
        vals = [B["rmse_ar"], B["rmse_m1"], B["rmse_m2"], B["rmse_m3"]]
        names = (r"before \\ the quarter", r"after \\ month 1", r"after \\ month 2", r"after \\ month 3")
        ax = plane([-0.6, 3.6], [0, 2.6], center=LEFT * 1.6 + DOWN * 1.1, x_length=7.0, y_length=3.6,
                   xticks=[], yticks=[0, 1, 2], xlabel=r"", ylabel=r"error, \ points of growth \ (root mean square)",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        bb = bars(ax, vals, [BENCH, NOW, NOW, NOW])
        labs = VGroup(*[label(n_, font_size=16, color=GREY_A).next_to(ax.ax.c2p(k, 0), DOWN, buff=0.2)
                        for k, n_ in enumerate(names)])
        vl = VGroup(*[label(f"{v:.2f}", font_size=18, color=WHITE).next_to(b_, UP, buff=0.08)
                      for v, b_ in zip(vals, bb)])
        side = VGroup(
            label(rf"American GDP, \ {B['quarters'][0][:4]}--{B['quarters'][-1][:4]}: \\ {B['n']} quarters, \ "
                  r"the two \\ pandemic quarters left out", font_size=17, color=GREY_A),
            label(r"pseudo real time: \ today's data, \\ the release calendar imposed", font_size=17,
                  color=E.SOURCE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35).shift(DOWN * 0.9)
        tag = data_tag(r"FRED: \ GDPC1, \ PAYEMS, \ INDPRO", corner=DR, font_size=12)
        with self.voiceover(
            "The oldest nowcasting tool is the bridge equation. <bookmark mark='a'/> Regress GDP growth on the "
            "quarterly averages of a few monthly indicators, here payrolls and industrial production, which come "
            "out within weeks. <bookmark mark='b'/> In the middle of a quarter some months are missing; fill them "
            "with each indicator's own forecast. Nowcasters call this the ragged edge. <bookmark mark='c'/> Run it "
            f"on American data since {B['quarters'][0][:4]}, refitting each quarter on the past only. Before the "
            "quarter, a simple autoregression in GDP misses by "
            f"{B['rmse_ar']:.2f} points on average; <bookmark mark='d'/> after one month of indicators, by "
            f"{B['rmse_m1']:.2f}; after two, {B['rmse_m2']:.2f}; after all three, {B['rmse_m3']:.2f}. These use "
            "today's revised data with the release calendar imposed, pseudo real time, so a nowcaster at the time "
            "would have done somewhat worse."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(eq), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(note_))
            vo.wait_until("c")
            self.play(FadeIn(ax), FadeIn(labs), GrowFromEdge(bb[0], DOWN), FadeIn(vl[0]), FadeIn(side))
            vo.wait_until("d")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b_, DOWN), FadeIn(v_)) for b_, v_ in
                                    zip(bb[1:], vl[1:])], lag_ratio=0.5), run_time=2.5)
        self.clear_scene()

    def factor(self):
        Isl = load("island")
        eqs = VGroup(
            MathTex(r"f_t = \phi f_{t-1} + \eta_t", font_size=32, color=NOW),
            MathTex(r"x_{it} = \lambda_i f_t + e_{it} \qquad i = \text{payrolls, production, retail, survey}",
                    font_size=30, color=SPF),
            MathTex(r"y_q = \mu + \beta\, \tfrac13\,(f_{3q} + f_{3q-1} + f_{3q-2}) + \varepsilon_q", font_size=30,
                    color=GB),
        ).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.4)
        why = label(r"the Kalman filter skips whatever has not been released: \ the ragged edge for free",
                    font_size=19, color=GREY_A).next_to(eqs, DOWN, buff=0.25)
        rm = Isl["rmse"]
        ax = plane([-0.6, 4.6], [0, 3.6], center=LEFT * 1.8 + DOWN * 1.6, x_length=7.6, y_length=3.0,
                   xticks=[], yticks=[0, 1, 2, 3], xlabel=r"", ylabel=r"error \ (root mean square)",
                   yfmt=lambda v: f"{v:.0f}", font_size=13)
        bb = bars(ax, rm, [BENCH] + [NOW] * 4, width=0.55)
        names = (r"before", r"survey", r"month 1", r"month 2", r"month 3")
        labs = VGroup(*[label(n_, font_size=15, color=GREY_A).next_to(ax.ax.c2p(k, 0), DOWN, buff=0.15)
                        for k, n_ in enumerate(names)])
        vl = VGroup(*[label(f"{v:.2f}", font_size=16, color=WHITE).next_to(b_, UP, buff=0.06) for v, b_ in
                      zip(rm, bb)])
        side = VGroup(
            label(rf"{Isl['n']} Island quarters, \\ growth's s.d. \ {Isl['sd_y']:.1f}", font_size=17, color=GREY_A),
            label(rf"one-s.d. bands cover \\ {100 * np.mean(Isl['coverage']):.0f}\% \ (should be 68\%)", font_size=17,
                  color=LATEST),
            label(r"news: \ each revision is \\ weights $\times$ (released $-$ expected)", font_size=17,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35).shift(DOWN * 1.4)
        tag = island_tag(r"simulated: \ the Island's factor model", corner=DR, font_size=12)
        with self.voiceover(
            "The method central banks use now is a dynamic factor model, after James Stock and Mark Watson, run "
            "through the Kalman filter, as Domenico Giannone, Lucrezia Reichlin and David Small showed in 2008. "
            "<bookmark mark='a'/> One unseen factor, the state of the economy, moves slowly from month to month. "
            "<bookmark mark='b'/> Each monthly indicator is that factor plus its own noise. <bookmark mark='c'/> "
            "And GDP growth is the quarter's average of the factor, plus noise. <bookmark mark='d'/> The Kalman "
            "filter, Part fifty-five's tool, simply skips whatever has not been released, so the ragged edge costs "
            "nothing. <bookmark mark='e'/> On the Island, where the model is true, the error falls from "
            f"{rm[0]:.2f} before the quarter to {rm[-1]:.2f} once all three months are in, and the bands are "
            "honest: one standard deviation covers about two thirds of outcomes. <bookmark mark='f'/> Every "
            "revision of the nowcast can be split into the news in each release, what came out minus what was "
            "expected, times a weight. That is how a nowcaster explains a revision: the news in the payroll "
            "number moved us by this much. The Atlanta Fed's GDPNow, since 2014, and the New York Fed's staff "
            "nowcast, first published in 2016, publish exactly such numbers."
        ) as vo:
            self.play(FadeIn(tag))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(eqs[k], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(why))
            vo.wait_until("e")
            self.play(FadeIn(ax), FadeIn(labs), LaggedStart(*[AnimationGroup(GrowFromEdge(b_, DOWN), FadeIn(v_))
                                                             for b_, v_ in zip(bb, vl)], lag_ratio=0.3),
                      FadeIn(side[0]), FadeIn(side[1]), run_time=3.0)
            vo.wait_until("f")
            self.play(FadeIn(side[2]))
        self.clear_scene()
