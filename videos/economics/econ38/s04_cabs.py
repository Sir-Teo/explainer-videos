from __future__ import annotations

from videos.economics.econ38.common import *  # noqa: F403


class Cabs(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Do people choose their hours?", r"What do cab drivers do on a busy day?",
             "Chapter three. Do people choose their hours?",
             lit={1997: r"Camerer et al.", 2015: r"Farber", 2021: r"Angrist, \ Caldwell and Hall"},
             scale=("person",), horizon=("a day",))
        self.two_theories()
        self.evidence()

    def two_theories(self):
        ax = plane([10, 50], [4, 14], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.4, y_length=4.6,
                   xticks=[10, 20, 30, 40, 50], yticks=[4, 6, 8, 10, 12, 14], xlabel=r"what a driver earns an hour "
                   r"today, \ \$", ylabel=r"hours driven today", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        ws = np.linspace(10, 50, 80)
        target = path(ax, ws, 300 / ws, LOSS, 3.4, yr=(4, 14))
        opt = path(ax, ws, 6 + 0.12 * (ws - 10), WAGE, 3.4, yr=(4, 14))
        side = VGroup(
            label(r"red: \ a daily target, \ \$300: \\ quit when you reach it, \\ so a busy day is short", font_size=18,
                  color=LOSS),
            label(r"green: \ the standard model: \\ work longer when \\ each hour pays more", font_size=18,
                  color=WAGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(RIGHT, buff=0.4)
        tag = published_tag(r"Camerer et al.\ (1997); \ the standard model", corner=DR, font_size=12)
        days = VGroup()
        for k, (nm, v) in enumerate((("Sun", 18), ("Tue", 21), ("Mon", 24), ("Thu", 26.5), ("Sat", 31),
                                     ("Wed: \\ rain", 36), ("Fri: \\ a convention", 42))):
            p = ax.ax.c2p(v, 4)
            days.add(VGroup(Dot(p, radius=0.07, color=E.ACCENT),
                            label(nm, font_size=15, color=E.ACCENT).move_to(p + UP * (0.35 + 0.3 * (k % 2)))))
        dhead = label(r"one driver's week: \ what an hour paid each day", font_size=18, color=E.ACCENT).to_edge(
            RIGHT, buff=0.4).shift(DOWN * 2.0)
        with self.voiceover(
            "Most people cannot choose their hours from day to day. Cab drivers can, and their days differ: rain, "
            "conventions and holidays make some days pay far more than others. <bookmark mark='a'/> If drivers aim for "
            "a fixed amount each day, say three hundred dollars, and stop when they reach it, a busy day is a short "
            "day: hours fall as hourly earnings rise, with an elasticity of minus one. <bookmark mark='b'/> The "
            "standard "
            "model says the opposite: when an hour pays more, work more of them, and rest on slow days."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            self.play(FadeIn(dhead), LaggedStart(*[FadeIn(d, shift=DOWN * 0.15) for d in days], lag_ratio=0.35),
                      run_time=3.0)
            vo.wait_until("a")
            self.play(Create(target), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(opt), FadeIn(side[1]), run_time=1.5)
        self.clear_scene()

    def evidence(self):
        Cb = tables.CABS.data
        cards = point_cards([
            (r"1997: \ Camerer et al.", r"New York cab drivers' \\ trip sheets: \ hours fall \\ on high-earning days",
             LOSS),
            (r"2015: \ Farber", rf"every New York taxi trip, \\ {Cb['farber_years'][0]}--{Cb['farber_years'][1]}: "
                               r"\\ drivers work more \\ when it pays more", WAGE),
            (r"2021: \ Uber in Boston", rf"drivers offered random \\ fee cuts: \ a Frisch \\ elasticity near "
                                         rf"{Cb['uber_frisch']:.1f}", E.ACCENT),
        ], width=12.4, cols=3, font_size=20).move_to(DOWN * 0.1)
        head = label(r"what drivers actually do", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        foot = label(r"with flexible hours, \ people respond to pay much as the standard model says", font_size=20,
                     color=GREY_A).to_edge(DOWN, buff=0.6)
        tag = published_tag(tables.CABS.tag, corner=DR, font_size=11)
        with self.voiceover(
            "What do drivers do? <bookmark mark='a'/> In 1997 Colin Camerer, Linda Babcock, George Loewenstein and "
            "Richard Thaler studied New York drivers' trip sheets and found hours falling on high-earning days, as if "
            "drivers had daily targets, a famous result for behavioural economics. <bookmark mark='b'/> In 2015 Henry "
            "Farber used every New York taxi trip over five years and found drivers working more when the pay was "
            "better, with the drivers who stayed in the business responding most. <bookmark mark='c'/> And in 2021 "
            "Joshua Angrist, Sydnee Caldwell and Jonathan Hall ran an experiment, offering Boston's Uber drivers "
            "random "
            f"cuts in the platform's fee: a Frisch elasticity of about {Cb['uber_frisch']:.1f}, more than twice the "
            "survey estimates. <bookmark mark='d'/> Where hours are flexible, people respond to pay much as the "
            "standard model says."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abc", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()
