from __future__ import annotations

from videos.economics.econ30.common import *  # noqa: F403


class Taylor(VoiceoverScene):
    def construct(self):
        card(self, 7, r"A rule for the central bank", r"Can a simple formula describe what a central bank does?",
             "Chapter seven. A rule for the central bank.", lit={1993: r"Taylor"}, scale=("nation",),
             horizon=("a quarter", "a decade"))
        self.rule()
        self.chart()
        self.since()

    def rule(self):
        rows = VGroup(
            label(r"John Taylor, \ 1993: \ a rule that described the Federal Reserve", font_size=26, color=E.ACCENT),
            MathTex(r"i = 2 + \pi + 0.5\,(\pi - 2) + 0.5\, x", font_size=46, color=CB),
            label(r"2: \ a neutral real rate; \ $\pi$: \ inflation over the past year; \ $x$: \ the output gap",
                  font_size=22, color=GREY_A),
            label(r"each point of inflation raises the rate by 1.5 points: \ the real rate rises too", font_size=22,
                  color=INFL),
            label(r"each point of output gap, \ by half a point", font_size=22, color=OUTPUT),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Taylor, \ \emph{Carnegie-Rochester Conference Series} 39 (1993): \ 195--214",
                            corner=DR, font_size=12)
        with self.voiceover(
            "In 1993 John Taylor proposed a rule simple enough to fit on an index card. <bookmark mark='a'/> The "
            "federal funds rate equals two, plus inflation, plus half the gap between inflation and two percent, "
            "plus half the output gap. <bookmark mark='b'/> Two is the neutral real rate; inflation is over the "
            "past year; the gap is output against its potential. <bookmark mark='c'/> So each extra point of "
            "inflation raises the policy rate by a point and a half, which means the real rate rises too: the "
            "central bank leans against inflation. <bookmark mark='d'/> And each point of output gap adds half a "
            "point."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                if isinstance(r_, MathTex):
                    self.play(Write(r_), run_time=1.3)
                else:
                    self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def chart(self):
        T = load("taylor")
        t = np.array(T["t"])
        k = (t >= 1985) & (t < 2008)
        ax = plane([1985, 2008], [-2, 12], center=LEFT * 1.7 + DOWN * 0.3, x_length=8.6, y_length=4.8,
                   xticks=[1985, 1990, 1995, 2000, 2005], yticks=[0, 4, 8, 12], ylabel=r"percent",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=15)
        band = Rectangle(width=ax.ax.c2p(2006.0, 0)[0] - ax.ax.c2p(1987.6, 0)[0], height=4.8, fill_color=CB,
                         fill_opacity=0.08, stroke_width=0).move_to(ax.ax.c2p((1987.6 + 2006.0) / 2, 5))
        ff = path(ax, t[k], np.array(T["ff"])[k], RATE, 3, smooth=False)
        rl = path(ax, t[k], np.clip(np.array(T["rule"])[k], -2, 12), CB, 3, smooth=False)
        F = T["fit"]
        side = VGroup(
            label(r"pink: \ the federal funds rate", font_size=19, color=RATE),
            label(r"green: \ Taylor's rule, \\ with the GDP deflator and \\ the CBO's output gap", font_size=19,
                  color=CB),
            label(r"shaded: \ Greenspan, \ 1987--2006", font_size=19, color=GREY_A),
            label(rf"fitted over those years: \\ {F['pi']:.2f} on inflation, \\ {F['gap']:.2f} on the gap",
                  font_size=19, color=E.ACCENT),
            label(r"more than one for one \\ on inflation", font_size=20, color=INFL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Federal Reserve; \ BEA: \ GDP deflator; \ CBO: \ potential GDP; \ via FRED", corner=DR,
                       font_size=12)
        with self.voiceover(
            "How well does it fit? <bookmark mark='a'/> In pink, the federal funds rate from 1985 to 2007. "
            "<bookmark mark='b'/> In green, Taylor's rule, computed from the GDP deflator and the Budget Office's "
            "output gap as they stand today. <bookmark mark='c'/> Through Alan Greenspan's years as chair, the two "
            "move together, with a correlation of "
            f"{T['corr']:.2f} and a typical gap of {T['rmse']:.1f} points. <bookmark mark='d'/> A regression over "
            f"those years puts {F['pi']:.2f} on inflation and {F['gap']:.2f} on the output gap. "
            "<bookmark mark='e'/> The number that matters is the first one: more than one for one. The next chapter "
            "shows why."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(Create(ff), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(rl), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(band), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def since(self):
        T = load("taylor")
        t = np.array(T["t"])
        k = t >= 2005
        ax = plane([2005, 2027], [-4, 12], center=LEFT * 1.7 + DOWN * 0.3, x_length=8.6, y_length=4.8,
                   xticks=[2005, 2010, 2015, 2020, 2025], yticks=[-4, 0, 4, 8, 12], ylabel=r"percent",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=15)
        zero = seg(ax, 2005, 0, 2027, 0, GREY_C, 2)
        ff = path(ax, t[k], np.array(T["ff"])[k], RATE, 3, smooth=False)
        rl = path(ax, t[k], np.clip(np.array(T["rule"])[k], -4, 12), CB, 3, smooth=False)
        side = VGroup(
            label(rf"2009--2015: \ the rule fell to {T['rule_2009']:.1f}\%; \\ the funds rate stopped at "
                  rf"{T['ff_2009']:.2f}\%", font_size=19, color=CB),
            label(r"the zero lower bound: \\ chapter twelve", font_size=19, color=HOLD),
            label(r"2021--22: \ the rule called for \\ far higher rates, \ sooner", font_size=19, color=INFL),
            label(r"a rule describes a central bank; \\ it does not bind one", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Federal Reserve; \ BEA; \ CBO; \ via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "And since then? <bookmark mark='a'/> From 2009 to 2015 the rule called for a negative interest rate, "
            f"as low as {say_num(T['rule_2009'], 1)} percent, but the federal funds rate stopped just above zero. "
            "<bookmark mark='b'/> That is the zero lower bound, chapter twelve's subject. <bookmark mark='c'/> In "
            "2021 and 2022 the rule called for much higher rates, much sooner, than the Federal Reserve set. "
            "<bookmark mark='d'/> A rule describes a central bank; it does not bind one. But as a description, "
            "it is what the model needs."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag), Create(ff), Create(rl), run_time=1.5)
            for mk, r_ in zip("abcd", side):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
